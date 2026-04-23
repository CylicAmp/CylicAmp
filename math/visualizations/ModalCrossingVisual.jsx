import React, { useState, useEffect, useRef, useCallback } from 'react';

const MOD = 37;
const ORBIT_P = [0, 1, 4, 13, 3, 10, 31, 20, 24, 36, 35, 32, 23, 33, 26, 5, 16, 12];
const ORBIT_V = [2, 7, 22, 30, 17, 15, 9, 28, 11, 34, 29, 14, 6, 19, 21, 27, 8, 25];
const GATE = 18;

const promote = n => (2 * n + 19) % MOD;

// 37-slot narrative state registry
const STATE_MAP = {
  0: 'NULL_ELEMENT', 1: 'UNITY', 2: 'DUALITY', 3: 'TRINITY',
  4: 'FOUNDATION', 5: 'QUINTESSENCE', 6: 'HARMONY', 7: 'MYSTERY',
  8: 'INFINITY', 9: 'COMPLETION', 10: 'PERFECTION', 11: 'PORTAL',
  12: 'CYCLE', 13: 'TRANSFORMATION', 14: 'BALANCE', 15: 'RESONANCE',
  16: 'INTEGRATION', 17: 'BRIDGE', 18: 'GATE_SOVEREIGN', 19: 'THRESHOLD',
  20: 'EXPANSION', 21: 'PROMOTION', 22: 'ELEVATION', 23: 'SYNTHESIS',
  24: 'CONVERGENCE', 25: 'APEX', 26: 'ORBIT_LOCK', 27: 'VERIFIED',
  28: 'CRYSTALLIZED', 29: 'SEALED', 30: 'MANIFEST', 31: 'ANCHORED',
  32: 'RESOLVED', 33: 'ECHOED', 34: 'ARCHIVED', 35: 'MIRRORED',
  36: 'COMPLETE'
};

const getPos = (val, radius) => {
  const angle = (val / MOD) * 2 * Math.PI - Math.PI / 2;
  return {
    x: 100 + radius * Math.cos(angle),
    y: 100 + radius * Math.sin(angle)
  };
};

// Equal-temperament frequency mapping across mod 37
const getFreq = n => 440 * Math.pow(2, n / 37);

const ModalCrossingVisual = () => {
  const [step, setStep] = useState(0);           // animation frame in orbit
  const [hovered, setHovered] = useState(null);  // element under cursor
  const [running, setRunning] = useState(false);
  const [showLabels, setShowLabels] = useState(true);
  const audioCtxRef = useRef(null);

  // Enhancement I: Reality Engine Rotation
  useEffect(() => {
    if (!running) return;
    const interval = setInterval(() => setStep(s => (s + 1) % 18), 1000);
    return () => clearInterval(interval);
  }, [running]);

  // Enhancement III: Sound Mapping
  const playTone = useCallback((n) => {
    if (!audioCtxRef.current) {
      audioCtxRef.current = new (window.AudioContext || window.webkitAudioContext)();
    }
    const ctx = audioCtxRef.current;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.frequency.value = getFreq(n);
    osc.type = 'sine';
    gain.gain.setValueAtTime(0.15, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);
    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + 0.4);
  }, []);

  const activeP = ORBIT_P[step];
  const activeV = ORBIT_V[step];

  // Bezier promotion arc: outer ring → gate center → inner ring
  const PromotionArc = ({ from }) => {
    const to = promote(from);
    const start = getPos(from, 70);
    const end = getPos(to, 45);
    const ctrl = { x: 100, y: 100 }; // gate
    return (
      <path
        d={`M ${start.x} ${start.y} Q ${ctrl.x} ${ctrl.y} ${end.x} ${end.y}`}
        fill="none"
        stroke="#f97316"
        strokeWidth="0.8"
        strokeDasharray="2 2"
        opacity="0.7"
      />
    );
  };

  // Structural connection lines between paired elements
  const StructuralLines = () =>
    ORBIT_P.map((p, i) => {
      const v = ORBIT_V[i];
      const ps = getPos(p, 70);
      const vs = getPos(v, 45);
      return (
        <line
          key={`str-${i}`}
          x1={ps.x} y1={ps.y}
          x2={vs.x} y2={vs.y}
          stroke="white"
          strokeWidth="0.3"
          opacity="0.08"
        />
      );
    });

  const OrbitDot = ({ val, radius, color, label }) => {
    const pos = getPos(val, radius);
    const isHov = hovered === val;
    const isActiveStep = val === activeP || val === activeV;
    return (
      <g
        style={{ cursor: 'pointer' }}
        onMouseEnter={() => { setHovered(val); playTone(val); }}
        onMouseLeave={() => setHovered(null)}
      >
        <circle
          cx={pos.x} cy={pos.y}
          r={isHov ? 4 : isActiveStep && running ? 3.5 : 2.5}
          fill={color}
          opacity={isHov || isActiveStep ? 1 : 0.7}
          style={{ transition: 'r 0.2s' }}
        />
        {showLabels && (
          <text
            x={pos.x + (pos.x > 100 ? 4 : -4)}
            y={pos.y + 1}
            fontSize="3.5"
            fill={color}
            textAnchor={pos.x > 100 ? 'start' : 'end'}
            opacity="0.85"
          >
            {val}
          </text>
        )}
      </g>
    );
  };

  return (
    <div style={{ fontFamily: 'monospace', background: '#0a0a0f', color: '#e0e0ff', minHeight: '100vh', padding: '24px' }}>

      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: '24px' }}>
        <h1 style={{ color: '#a78bfa', fontSize: '1.3rem', letterSpacing: '0.12em', margin: 0 }}>
          MODAL CROSSING VISUALIZATION
        </h1>
        <p style={{ color: '#6b7280', fontSize: '0.75rem', margin: '4px 0 0' }}>
          LoB 20 — mod 37 orbit geometry — GEOMETRY LOCKED
        </p>
      </div>

      {/* Controls */}
      <div style={{ display: 'flex', gap: '8px', justifyContent: 'center', marginBottom: '20px', flexWrap: 'wrap' }}>
        <button
          onClick={() => setRunning(r => !r)}
          style={{
            padding: '6px 18px', borderRadius: '6px', cursor: 'pointer',
            background: running ? '#7c3aed' : '#1f2937',
            border: '1px solid #7c3aed', color: '#ddd6fe', fontSize: '0.8rem'
          }}
        >
          {running ? '⏸ Pause Orbit' : '▶ Run Orbit'}
        </button>
        <button
          onClick={() => setStep(s => (s + 1) % 18)}
          style={{
            padding: '6px 18px', borderRadius: '6px', cursor: 'pointer',
            background: '#1f2937', border: '1px solid #374151', color: '#9ca3af', fontSize: '0.8rem'
          }}
        >
          Step →
        </button>
        <button
          onClick={() => setShowLabels(l => !l)}
          style={{
            padding: '6px 18px', borderRadius: '6px', cursor: 'pointer',
            background: '#1f2937', border: '1px solid #374151', color: '#9ca3af', fontSize: '0.8rem'
          }}
        >
          {showLabels ? 'Hide' : 'Show'} Labels
        </button>
      </div>

      {/* SVG Visualization */}
      <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '24px' }}>
        <svg viewBox="0 0 200 200" width="420" height="420" style={{ background: '#0d1117', borderRadius: '12px', border: '1px solid #1f2937' }}>

          {/* Ring guides */}
          <circle cx="100" cy="100" r="70" fill="none" stroke="#22d3ee" strokeWidth="0.3" opacity="0.2" />
          <circle cx="100" cy="100" r="45" fill="none" stroke="#fbbf24" strokeWidth="0.3" opacity="0.2" />

          {/* Structural connection lines */}
          <StructuralLines />

          {/* Promotion arcs — hovered or active */}
          {hovered !== null && ORBIT_P.includes(hovered) && <PromotionArc from={hovered} />}
          {running && <PromotionArc from={activeP} />}

          {/* [P] outer ring — cyan */}
          {ORBIT_P.map(val => (
            <OrbitDot key={`p-${val}`} val={val} radius={70} color="#22d3ee" />
          ))}

          {/* [V] inner ring — gold */}
          {ORBIT_V.map(val => (
            <OrbitDot key={`v-${val}`} val={val} radius={45} color="#fbbf24" />
          ))}

          {/* Gate 18 — center, sovereign */}
          <circle cx="100" cy="100" r="5" fill="#ef4444" opacity="0.9" />
          <circle cx="100" cy="100" r="8" fill="none" stroke="#ef4444" strokeWidth="0.5" opacity="0.4" />
          <text x="100" y="103" fontSize="4" fill="white" textAnchor="middle">18</text>

          {/* Active step highlight ring */}
          {running && (() => {
            const ap = getPos(activeP, 70);
            const av = getPos(activeV, 45);
            return (
              <>
                <circle cx={ap.x} cy={ap.y} r="5" fill="none" stroke="#22d3ee" strokeWidth="0.8" opacity="0.9" />
                <circle cx={av.x} cy={av.y} r="5" fill="none" stroke="#fbbf24" strokeWidth="0.8" opacity="0.9" />
              </>
            );
          })()}
        </svg>
      </div>

      {/* Step & Hover Info panels */}
      <div style={{ display: 'flex', gap: '12px', marginBottom: '20px', flexWrap: 'wrap' }}>

        {/* Enhancement I: step state */}
        <div style={{ flex: '1 1 200px', background: '#111827', border: '1px solid #1f2937', borderRadius: '8px', padding: '14px' }}>
          <div style={{ color: '#6b7280', fontSize: '0.7rem', marginBottom: '6px' }}>ORBIT STEP {step + 1} / 18</div>
          <div style={{ fontSize: '0.82rem', lineHeight: '1.8' }}>
            <div><span style={{ color: '#22d3ee' }}>[P] active: </span><span style={{ color: '#e0e0ff' }}>{activeP}</span><span style={{ color: '#6b7280' }}> — {STATE_MAP[activeP]}</span></div>
            <div><span style={{ color: '#fbbf24' }}>[V] active: </span><span style={{ color: '#e0e0ff' }}>{activeV}</span><span style={{ color: '#6b7280' }}> — {STATE_MAP[activeV]}</span></div>
            <div><span style={{ color: '#f97316' }}>g({activeP}) = </span><span style={{ color: '#e0e0ff' }}>{promote(activeP)}</span></div>
          </div>
        </div>

        {/* Enhancement II: hover info */}
        <div style={{ flex: '1 1 200px', background: '#111827', border: '1px solid #1f2937', borderRadius: '8px', padding: '14px' }}>
          <div style={{ color: '#6b7280', fontSize: '0.7rem', marginBottom: '6px' }}>HOVER PROBE</div>
          {hovered !== null ? (
            <div style={{ fontSize: '0.82rem', lineHeight: '1.8' }}>
              <div><span style={{ color: '#a78bfa' }}>n = </span>{hovered}</div>
              <div><span style={{ color: '#a78bfa' }}>state: </span>{STATE_MAP[hovered]}</div>
              <div><span style={{ color: '#a78bfa' }}>ring: </span>
                {hovered === GATE ? 'CENTER / GATE' : ORBIT_P.includes(hovered) ? '[P] outer' : '[V] inner'}
              </div>
              {ORBIT_P.includes(hovered) && (
                <div><span style={{ color: '#f97316' }}>g(n) → </span>{promote(hovered)} ({STATE_MAP[promote(hovered)]})</div>
              )}
              <div><span style={{ color: '#a78bfa' }}>freq: </span>{getFreq(hovered).toFixed(2)} Hz</div>
            </div>
          ) : (
            <div style={{ color: '#4b5563', fontSize: '0.8rem' }}>Hover any element…</div>
          )}
        </div>

        {/* Enhancement IV: 37R Registry */}
        <div style={{ flex: '1 1 200px', background: '#111827', border: '1px solid #1f2937', borderRadius: '8px', padding: '14px' }}>
          <div style={{ color: '#6b7280', fontSize: '0.7rem', marginBottom: '6px' }}>37R STATE REGISTRY</div>
          <div style={{ fontSize: '0.7rem', lineHeight: '1.7', maxHeight: '100px', overflowY: 'auto' }}>
            {[GATE, activeP, activeV].map(n => (
              <div key={n}>
                <span style={{ color: n === GATE ? '#ef4444' : ORBIT_P.includes(n) ? '#22d3ee' : '#fbbf24' }}>
                  R-{String(n).padStart(2, '0')}:
                </span>{' '}
                <span style={{ color: '#9ca3af' }}>{STATE_MAP[n]}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Legend */}
      <div style={{ display: 'flex', gap: '20px', justifyContent: 'center', fontSize: '0.72rem', color: '#6b7280' }}>
        <span><span style={{ color: '#22d3ee' }}>●</span> [P] outer r=70 — potential</span>
        <span><span style={{ color: '#fbbf24' }}>●</span> [V] inner r=45 — verified</span>
        <span><span style={{ color: '#ef4444' }}>●</span> Gate 18 — sovereign</span>
        <span><span style={{ color: '#f97316' }}>--</span> g(n) promotion arc</span>
      </div>

    </div>
  );
};

export default ModalCrossingVisual;
