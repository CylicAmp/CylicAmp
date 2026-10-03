import numpy as np
from dataclasses import dataclass
from typing import Optional


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.threshold = np.random.uniform(0.1, 0.5)
        self.direction = np.random.uniform(-1, 1, 2)
        self.direction /= np.linalg.norm(self.direction)
        self.speed = np.random.uniform(0.005, 0.02)
        self.signal = self.threshold
        self.pending: list["Packet"] = []
        self.active = True
        self.history = []

    def move(self, others: list, bounds=(0, 1)):
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

    def load(self, packet: "Packet", stress: float):
        if stress >= packet.activation:
            self._apply(packet)
        else:
            self.pending.append(packet)

    def check_pending(self, stress: float):
        applied, waiting = [], []
        for p in self.pending:
            if stress >= p.activation:
                self._apply(p)
                applied.append(p)
            else:
                waiting.append(p)
        self.pending = waiting
        return applied

    def _apply(self, packet: "Packet"):
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

    def send(self, node: Node, stress: float):
        node.load(self, stress)


class Field:
    def __init__(self, n=12):
        self.nodes = [Node(np.random.uniform(0.1, 0.9),
                           np.random.uniform(0.1, 0.9)) for _ in range(n)]
        self.stress = 0.0
        self.tick = 0
        self.log = []

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

        self.tick += 1
        return transfers

    def inject(self, packet: Packet):
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


if __name__ == "__main__":
    np.random.seed(7)
    field = Field(n=12)

    print(f"tick 0 | mean: {field.mean_threshold():.4f}")
    for t in range(1, 51):
        transfers = field.step()
        if t % 10 == 0:
            print(f"tick {t:>3} | mean: {field.mean_threshold():.4f} | transfers: {transfers}")

    p = Packet(value=0.95, activation=0.4)
    field.inject(p)
    pending = sum(len(n.pending) for n in field.nodes)
    print(f"\npending in {pending} nodes | stress: {field.stress:.1f}")

    for _ in range(5):
        field.degrade(0.1)
        print(f"stress {field.stress:.1f} | mean: {field.mean_threshold():.4f}")

    print()
    print("SUMMARY:")
    for k, v in field.summary().items():
        print(f"  {k}: {v}")

    print()
    print("NODE HISTORIES:")
    for i, node in enumerate(field.nodes):
        if node.history:
            print(f"  node {i}: {len(node.history)} events | threshold: {node.threshold:.4f}")
            for entry in node.history:
                print(f"    {entry}")
