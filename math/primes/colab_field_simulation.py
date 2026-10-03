import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Optional


# ── Core Classes ──────────────────────────────────────────────────────────────

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.threshold = np.random.uniform(0.1, 0.5)
        self.direction = np.random.uniform(-1, 1, 2)
        self.direction /= np.linalg.norm(self.direction)
        self.speed = np.random.uniform(0.005, 0.02)
        self.signal = self.threshold
        self.pending: list = []
        self.active = True
        self.history = []

    def move(self, others, bounds=(0, 1)):
        pull = np.zeros(2)
        for other in others:
            if other is self:
                continue
            sig = other.signal_at(self.x, self.y)
            if sig > 0.01:
                d = np.array([other.x - self.x, other.y - self.y])
                dist = np.linalg.norm(d)
                if dist > 0:
                    pull += (d / dist) * sig

        if np.linalg.norm(pull) > 0:
            pull /= np.linalg.norm(pull)
            self.direction = 0.7 * self.direction + 0.3 * pull
            self.direction /= np.linalg.norm(self.direction)

        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

        if self.x <= bounds[0] or self.x >= bounds[1]:
            self.direction[0] *= -1
        if self.y <= bounds[0] or self.y >= bounds[1]:
            self.direction[1] *= -1
        self.x = np.clip(self.x, bounds[0], bounds[1])
        self.y = np.clip(self.y, bounds[0], bounds[1])

    def signal_at(self, tx, ty):
        dist = np.sqrt((self.x - tx)**2 + (self.y - ty)**2)
        return self.signal / (1 + dist**2)

    def update(self, value, from_pos=None, tick=None):
        if value > self.threshold:
            before = self.threshold
            self.threshold = value
            self.signal = self.threshold
            self.speed = min(0.03, self.speed + 0.002)
            self.history.append({
                "tick": tick,
                "event": "update",
                "pos": (self.x, self.y),
                "from_pos": from_pos,
                "before": before,
                "after": self.threshold,
                "gain": self.threshold - before,
            })
            return True
        return False

    def load(self, packet, stress):
        if stress >= packet.activation:
            self._apply(packet)
        else:
            self.pending.append(packet)

    def check_pending(self, stress):
        applied, waiting = [], []
        for p in self.pending:
            if stress >= p.activation:
                self._apply(p)
                applied.append(p)
            else:
                waiting.append(p)
        self.pending = waiting
        return applied

    def _apply(self, packet):
        if packet.value > self.threshold:
            before = self.threshold
            self.threshold = packet.value
            self.signal = self.threshold
            self.history.append({
                "tick": None,
                "event": "applied",
                "pos": (self.x, self.y),
                "before": before,
                "after": self.threshold,
                "gain": self.threshold - before,
                "pending_count": len(self.pending),
            })


@dataclass
class Packet:
    value: float
    activation: float
    origin: Optional[tuple] = None

    def send(self, node, stress):
        node.load(self, stress)


class Field:
    def __init__(self, n=12):
        self.nodes = [Node(np.random.uniform(0.1, 0.9),
                           np.random.uniform(0.1, 0.9)) for _ in range(n)]
        self.stress = 0.0
        self.tick = 0
        self.log = []
        self.history_mean = []
        self.history_stress = []

    def step(self):
        for node in self.nodes:
            node.move(self.nodes)

        transfers = 0
        for i, a in enumerate(self.nodes):
            for j, b in enumerate(self.nodes):
                if i >= j:
                    continue
                if a.signal_at(b.x, b.y) > 0.1 and b.signal_at(a.x, a.y) > 0.1:
                    before_a = a.threshold
                    before_b = b.threshold
                    t1 = a.update(b.threshold, from_pos=(b.x, b.y), tick=self.tick)
                    t2 = b.update(a.threshold, from_pos=(a.x, a.y), tick=self.tick)
                    if t1 or t2:
                        self.log.append({
                            "tick": self.tick,
                            "event": "transfer",
                            "nodes": (i, j),
                            "position": ((a.x, a.y), (b.x, b.y)),
                            "before": (before_a, before_b),
                            "after": (a.threshold, b.threshold),
                            "stress": self.stress,
                        })
                        transfers += t1 + t2

        self.history_mean.append(self.mean_threshold())
        self.history_stress.append(self.stress)
        self.tick += 1
        return transfers

    def inject(self, packet):
        for node in self.nodes:
            packet.send(node, self.stress)
        self.log.append({
            "tick": self.tick,
            "event": "inject",
            "value": packet.value,
            "activation": packet.activation,
            "stress": self.stress,
        })

    def degrade(self, amount=0.1):
        self.stress = min(1.0, self.stress + amount)
        applied = []
        for node in self.nodes:
            applied.extend(node.check_pending(self.stress))
        if applied:
            self.log.append({
                "tick": self.tick,
                "event": "applied",
                "count": len(applied),
                "stress": self.stress,
            })
        return applied

    def mean_threshold(self):
        return np.mean([n.threshold for n in self.nodes])

    def summary(self):
        transfers = [e for e in self.log if e["event"] == "transfer"]
        applications = [e for e in self.log if e["event"] == "applied"]
        if not transfers:
            return {"total_transfers": 0, "first_tick": None,
                    "peak_gain": 0, "total_applied": 0}
        gains = []
        for e in transfers:
            for idx in range(2):
                g = e["after"][idx] - e["before"][idx]
                if g > 0:
                    gains.append(g)
        return {
            "total_transfers": len(transfers),
            "first_tick": transfers[0]["tick"],
            "last_tick": transfers[-1]["tick"],
            "peak_gain": max(gains),
            "mean_gain": np.mean(gains),
            "total_applied": sum(e["count"] for e in applications),
        }


# ── Visualization ─────────────────────────────────────────────────────────────

def plot_field(field, title="Field State"):
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Node positions colored by threshold
    ax = axes[0]
    xs = [n.x for n in field.nodes]
    ys = [n.y for n in field.nodes]
    thresholds = [n.threshold for n in field.nodes]
    sc = ax.scatter(xs, ys, c=thresholds, cmap="plasma", s=100,
                    vmin=0, vmax=1, zorder=3)
    plt.colorbar(sc, ax=ax, label="threshold")
    for i, node in enumerate(field.nodes):
        ax.annotate(str(i), (node.x, node.y), fontsize=7,
                    ha='center', va='center', color='white', zorder=4)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Node positions / thresholds")
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    # Mean threshold over time
    ax = axes[1]
    ax.plot(field.history_mean, color="steelblue", linewidth=1.5)
    ax.set_title("Mean threshold over ticks")
    ax.set_xlabel("tick")
    ax.set_ylabel("mean threshold")
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)

    # Transfer events by tick
    ax = axes[2]
    transfer_ticks = [e["tick"] for e in field.log if e["event"] == "transfer"]
    if transfer_ticks:
        ax.hist(transfer_ticks, bins=max(10, len(set(transfer_ticks))),
                color="coral", edgecolor="black", linewidth=0.5)
    ax.set_title("Transfers per tick")
    ax.set_xlabel("tick")
    ax.set_ylabel("count")
    ax.grid(True, alpha=0.3)

    fig.suptitle(title, fontsize=13)
    plt.tight_layout()
    plt.show()


def plot_node_history(field):
    fig, ax = plt.subplots(figsize=(10, 5))
    for i, node in enumerate(field.nodes):
        if node.history:
            ticks = [e["tick"] if e["tick"] is not None else field.tick
                     for e in node.history]
            values = [e["after"] for e in node.history]
            ax.step(ticks, values, where="post", label=f"node {i}", linewidth=1)
    ax.set_title("Node threshold over time")
    ax.set_xlabel("tick")
    ax.set_ylabel("threshold")
    ax.set_ylim(0, 1)
    ax.legend(loc="upper left", fontsize=7, ncol=3)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


# ── Run ───────────────────────────────────────────────────────────────────────

np.random.seed(7)
field = Field(n=12)

# Run ticks
for t in range(100):
    field.step()

# Inject a packet with a delayed activation threshold
p = Packet(value=0.95, activation=0.4)
field.inject(p)

# Degrade stress in steps
for _ in range(10):
    field.degrade(0.05)
    field.step()

# Results
print("SUMMARY:")
for k, v in field.summary().items():
    print(f"  {k}: {v}")

print()
print("FINAL THRESHOLDS:")
for i, node in enumerate(field.nodes):
    print(f"  node {i}: {node.threshold:.4f}  events: {len(node.history)}")

# Plots
plot_field(field, title="Field after 100 ticks + stress degradation")
plot_node_history(field)
