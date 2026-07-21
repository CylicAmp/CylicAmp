"""
Security ML Framework — MSW Ethical Hacking / Intrusion Detection
© 2026 Michael Warren Song. All Rights Reserved.

CNN-based network traffic classifier built on the DR/spine theorem feature layer.
Designed for: intrusion detection, anomaly classification, bot-network forensics.

Architecture:
  Raw traffic features
      ↓
  DR feature engineering (spine theorem, FLUX states, mod-9 residues)
      ↓
  StandardScaler + OneHotEncoder
      ↓
  SMOTE (class balance)
      ↓
  CNN classifier (Conv2D → MaxPool → Flatten → Dense)
      ↓
  Accuracy / F1 / ROC-AUC output

The DR feature layer is the mathematical spine — the same structure that
underlies the twin prime lattice, ABBC manifold, and zeta-zero alignment.
All domains. One framework.
"""

import numpy as np
import pandas as pd
import warnings
import time

warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

try:
    from imblearn.over_sampling import SMOTE
    SMOTE_AVAILABLE = True
except ImportError:
    SMOTE_AVAILABLE = False

try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential, Model
    from tensorflow.keras.layers import (
        Conv1D, MaxPooling1D, Conv2D, MaxPooling2D,
        Flatten, Dense, Dropout, BatchNormalization, Input
    )
    from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False


# ── DR spine theorem (core feature engine) ────────────────────────────────

FLUX_STATES = {3, 6, 9}          # Tesla FLUX states — natural engagement avoids suppression
NATURAL_FLUX_RATIO = 1 / 3       # Expected FLUX ratio in organic data


def digital_root(n: int) -> int:
    n = abs(int(n))
    if n == 0:
        return 0
    return 1 + (n - 1) % 9


def flux_ratio(values) -> float:
    """Fraction of values whose DR lands in {3,6,9}."""
    if len(values) == 0:
        return 0.0
    drs = [digital_root(v) for v in values]
    return sum(1 for d in drs if d in FLUX_STATES) / len(drs)


def spine_rigidity(values) -> float:
    """
    Mod-9 rigidity score: fraction of consecutive differences that share
    the same mod-9 residue.  Artificial sequences score high (>0.7).
    """
    if len(values) < 3:
        return 0.0
    diffs = [(values[i + 1] - values[i]) % 9 for i in range(len(values) - 1)]
    most_common = max(set(diffs), key=diffs.count)
    return diffs.count(most_common) / len(diffs)


def dr_entropy(values) -> float:
    """Shannon entropy of the DR distribution (max = log2(9) ≈ 3.17)."""
    if len(values) == 0:
        return 0.0
    counts = np.zeros(10)
    for v in values:
        counts[digital_root(v)] += 1
    probs = counts[1:] / len(values)          # DR 1–9
    probs = probs[probs > 0]
    return -np.sum(probs * np.log2(probs))


def extract_dr_features(window: list) -> dict:
    """
    Extract all DR-based features from a window of numeric values.
    Used as the spine theorem feature layer for the ML pipeline.
    """
    if not window:
        return {k: 0.0 for k in [
            'flux_ratio', 'flux_deviation', 'flux_suppressed',
            'spine_rigidity', 'dr_entropy', 'dr_uniformity',
            'mean_dr', 'std_dr', 'mod9_dominant_diff'
        ]}

    drs = [digital_root(v) for v in window]
    fr = flux_ratio(window)
    counts = np.array([drs.count(i) for i in range(1, 10)], dtype=float)
    expected = len(window) / 9
    chi2 = float(np.sum((counts - expected) ** 2 / expected)) if expected > 0 else 0.0

    diffs = [(window[i + 1] - window[i]) % 9 for i in range(len(window) - 1)]
    dominant_diff = max(set(diffs), key=diffs.count) if diffs else 0

    return {
        'flux_ratio':        fr,
        'flux_deviation':    abs(fr - NATURAL_FLUX_RATIO),
        'flux_suppressed':   float(fr < 0.2),
        'spine_rigidity':    spine_rigidity(window),
        'dr_entropy':        dr_entropy(window),
        'dr_uniformity':     1.0 / (1.0 + chi2),
        'mean_dr':           float(np.mean(drs)),
        'std_dr':            float(np.std(drs)),
        'mod9_dominant_diff': float(dominant_diff),
    }


# ── Data loading ──────────────────────────────────────────────────────────

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load CSV traffic/security dataset with basic cleaning.
    Compatible with NSL-KDD, CICIDS, and custom formats.
    """
    data = pd.read_csv(file_path)

    # Strip whitespace from column names
    data.columns = data.columns.str.strip()

    # Drop fully-null columns and duplicate rows
    data.dropna(axis=1, how='all', inplace=True)
    data.drop_duplicates(inplace=True)

    # Coerce numeric columns, fill missing with median
    for col in data.select_dtypes(include=[np.number]).columns:
        data[col].fillna(data[col].median(), inplace=True)

    # Fill categorical missing with mode
    for col in data.select_dtypes(include=['object']).columns:
        data[col].fillna(data[col].mode().iloc[0] if not data[col].mode().empty else 'unknown',
                         inplace=True)

    return data


# ── Preprocessing pipeline ────────────────────────────────────────────────

def preprocess_data(data: pd.DataFrame,
                    target_col: str = 'label',
                    categorical_cols: list = None,
                    window_col: str = None,
                    window_size: int = 10) -> tuple:
    """
    Full preprocessing:
      1. Separate features / target
      2. Encode categoricals
      3. Scale numerics
      4. Inject DR spine features (if window_col provided)
      5. SMOTE for class balance

    Returns: X_train, X_test, y_train, y_test, preprocessor
    """
    if target_col not in data.columns:
        raise ValueError(f"Target column '{target_col}' not found in data.")

    X = data.drop(columns=[target_col])
    y = data[target_col]

    # Encode target
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Inject DR spine features on a numeric window column
    if window_col and window_col in X.columns:
        values = X[window_col].tolist()
        dr_records = []
        for i in range(len(values)):
            start = max(0, i - window_size)
            window = values[start:i + 1]
            dr_records.append(extract_dr_features(window))
        dr_df = pd.DataFrame(dr_records, index=X.index)
        X = pd.concat([X, dr_df], axis=1)

    # Identify column types
    if categorical_cols is None:
        categorical_cols = X.select_dtypes(include=['object']).columns.tolist()

    numeric_cols = [c for c in X.columns if c not in categorical_cols]

    # Build sklearn preprocessor
    transformers = [('num', StandardScaler(), numeric_cols)]
    if categorical_cols:
        transformers.append(('cat', OneHotEncoder(handle_unknown='ignore',
                                                   sparse_output=False),
                             categorical_cols))

    preprocessor = ColumnTransformer(transformers=transformers)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    X_train_proc = preprocessor.fit_transform(X_train)
    X_test_proc  = preprocessor.transform(X_test)

    # SMOTE to balance attack vs normal class distribution
    if SMOTE_AVAILABLE:
        unique, counts = np.unique(y_train, return_counts=True)
        min_samples = counts.min()
        k_neighbors = min(5, min_samples - 1)
        if k_neighbors >= 1:
            sm = SMOTE(random_state=42, k_neighbors=k_neighbors)
            X_train_proc, y_train = sm.fit_resample(X_train_proc, y_train)

    return X_train_proc, X_test_proc, y_train, y_test, preprocessor, le


# ── CNN model ─────────────────────────────────────────────────────────────

def build_cnn_model(input_dim: int, num_classes: int) -> 'Sequential':
    """
    1D-CNN for tabular security feature vectors.

    Input is reshaped to (input_dim, 1) for Conv1D layers.
    Output: softmax over num_classes, or sigmoid for binary.
    """
    if not TF_AVAILABLE:
        raise ImportError("TensorFlow not available — install tensorflow to use CNN model.")

    model = Sequential([
        Input(shape=(input_dim, 1)),

        Conv1D(64, kernel_size=3, activation='relu', padding='same'),
        BatchNormalization(),
        MaxPooling1D(pool_size=2),
        Dropout(0.25),

        Conv1D(128, kernel_size=3, activation='relu', padding='same'),
        BatchNormalization(),
        MaxPooling1D(pool_size=2),
        Dropout(0.25),

        Conv1D(64, kernel_size=3, activation='relu', padding='same'),
        BatchNormalization(),
        Dropout(0.25),

        Flatten(),
        Dense(256, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),

        Dense(128, activation='relu'),
        Dropout(0.3),

        Dense(num_classes if num_classes > 2 else 1,
              activation='softmax' if num_classes > 2 else 'sigmoid'),
    ])

    loss = 'sparse_categorical_crossentropy' if num_classes > 2 else 'binary_crossentropy'
    model.compile(optimizer='adam', loss=loss, metrics=['accuracy'])
    return model


def train_model(model, X_train, y_train, X_val, y_val,
                epochs: int = 50, batch_size: int = 64):
    """Train CNN with early stopping and LR reduction."""
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6),
    ]

    # Reshape for Conv1D
    X_train_r = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_val_r   = X_val.reshape(X_val.shape[0], X_val.shape[1], 1)

    history = model.fit(
        X_train_r, y_train,
        validation_data=(X_val_r, y_val),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        verbose=1,
    )
    return history


# ── Evaluation ────────────────────────────────────────────────────────────

def evaluate_model(model, X_test, y_test, num_classes: int,
                   label_encoder=None) -> dict:
    """
    Compute accuracy, F1 (weighted), ROC-AUC, plus DR feature audit
    of the test predictions (spine theorem applied to model output).
    """
    X_test_r = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)
    y_pred_proba = model.predict(X_test_r, verbose=0)

    if num_classes > 2:
        y_pred = np.argmax(y_pred_proba, axis=1)
        try:
            auc = roc_auc_score(y_test, y_pred_proba, multi_class='ovr',
                                average='weighted')
        except Exception:
            auc = float('nan')
    else:
        y_pred = (y_pred_proba.flatten() > 0.5).astype(int)
        try:
            auc = roc_auc_score(y_test, y_pred_proba.flatten())
        except Exception:
            auc = float('nan')

    acc = accuracy_score(y_test, y_pred)
    f1  = f1_score(y_test, y_pred, average='weighted', zero_division=0)

    # DR audit on predictions — natural predictions should show FLUX ratio ≈ 1/3
    pred_flux = flux_ratio(y_pred.tolist())
    pred_rigidity = spine_rigidity(y_pred.tolist())

    results = {
        'accuracy':        acc,
        'f1_weighted':     f1,
        'roc_auc':         auc,
        'pred_flux_ratio': pred_flux,
        'pred_spine_rigidity': pred_rigidity,
        'pred_flux_natural': abs(pred_flux - NATURAL_FLUX_RATIO) < 0.1,
    }

    if label_encoder is not None:
        results['class_names'] = list(label_encoder.classes_)

    return results


def print_evaluation_report(results: dict):
    """Print formatted evaluation report."""
    print("\n" + "=" * 60)
    print("SECURITY ML FRAMEWORK — EVALUATION REPORT")
    print("=" * 60)
    print(f"  Accuracy     : {results['accuracy']:.4f}  ({results['accuracy']*100:.2f}%)")
    print(f"  F1 (weighted): {results['f1_weighted']:.4f}")
    print(f"  ROC-AUC      : {results['roc_auc']:.4f}")
    print()
    print("DR SPINE AUDIT ON PREDICTIONS:")
    print(f"  FLUX ratio      : {results['pred_flux_ratio']:.3f}  (natural ≈ {NATURAL_FLUX_RATIO:.3f})")
    print(f"  Spine rigidity  : {results['pred_spine_rigidity']:.3f}  (artificial > 0.7)")
    print(f"  FLUX natural    : {'YES — predictions look organic' if results['pred_flux_natural'] else 'NO — anomalous prediction distribution'}")
    if 'class_names' in results:
        print(f"\n  Classes: {results['class_names']}")
    print("=" * 60)


# ── Synthetic demo ────────────────────────────────────────────────────────

def generate_synthetic_traffic(n_normal: int = 800,
                               n_attack: int = 200,
                               n_features: int = 40) -> pd.DataFrame:
    """
    Generate synthetic network traffic for demo/testing.
    Normal traffic: organic DR distribution (FLUX ratio ≈ 1/3).
    Attack traffic: spine-rigid, FLUX-suppressed patterns.
    """
    rng = np.random.default_rng(42)

    # Normal: random poisson-like values, organic DR
    normal_data = rng.integers(1, 65535, size=(n_normal, n_features))
    normal_labels = ['normal'] * n_normal

    # Attack: arithmetic progressions with FLUX suppression
    attack_data = np.zeros((n_attack, n_features), dtype=int)
    for i in range(n_attack):
        start = rng.integers(10, 100)
        step  = rng.integers(1, 10)
        row = [(start + j * step) for j in range(n_features)]
        # Suppress FLUX states (replace any that land on 3,6,9 DR)
        row = [v + 1 if digital_root(v) in FLUX_STATES else v for v in row]
        attack_data[i] = row
    attack_labels = ['attack'] * n_attack

    data = np.vstack([normal_data, attack_data])
    labels = normal_labels + attack_labels

    # Shuffle
    idx = rng.permutation(len(labels))
    df = pd.DataFrame(data[idx], columns=[f'f{i}' for i in range(n_features)])
    df['label'] = np.array(labels)[idx]

    # Add a categorical feature (protocol type)
    protocols = rng.choice(['tcp', 'udp', 'icmp'], size=len(df))
    df['protocol'] = protocols

    return df


def run_demo():
    """End-to-end demo: synthetic traffic → CNN → evaluation."""
    print("SECURITY ML FRAMEWORK — DEMO")
    print("Spine theorem + CNN intrusion detection")
    print("=" * 60)

    if not TF_AVAILABLE:
        print("TensorFlow not installed. Running DR feature audit only.\n")
        df = generate_synthetic_traffic()
        normal = df[df['label'] == 'normal']['f0'].tolist()
        attack = df[df['label'] == 'attack']['f0'].tolist()
        print("Normal traffic DR features:")
        nf = extract_dr_features(normal[:100])
        for k, v in nf.items():
            print(f"  {k}: {v:.4f}")
        print("\nAttack traffic DR features:")
        af = extract_dr_features(attack[:100])
        for k, v in af.items():
            print(f"  {k}: {v:.4f}")
        print("\nKey signal: attack flux_ratio < 0.2, spine_rigidity > 0.7")
        return

    print("Generating synthetic traffic...")
    df = generate_synthetic_traffic(n_normal=800, n_attack=200)
    print(f"  {len(df)} samples | classes: {df['label'].value_counts().to_dict()}")

    print("\nPreprocessing (DR features + SMOTE)...")
    X_train, X_test, y_train, y_test, preprocessor, le = preprocess_data(
        df,
        target_col='label',
        categorical_cols=['protocol'],
        window_col='f0',
        window_size=10,
    )
    num_classes = len(le.classes_)
    print(f"  Train: {X_train.shape} | Test: {X_test.shape} | Classes: {num_classes}")

    print("\nBuilding CNN...")
    model = build_cnn_model(input_dim=X_train.shape[1], num_classes=num_classes)
    model.summary()

    print("\nTraining...")
    t0 = time.time()
    X_tr, X_val, y_tr, y_val = train_test_split(X_train, y_train,
                                                  test_size=0.15, random_state=42)
    train_model(model, X_tr, y_tr, X_val, y_val, epochs=30, batch_size=64)
    print(f"  Training time: {time.time() - t0:.1f}s")

    print("\nEvaluating...")
    results = evaluate_model(model, X_test, y_test, num_classes, le)
    print_evaluation_report(results)

    return model, results


if __name__ == "__main__":
    run_demo()
