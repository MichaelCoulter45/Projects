import time
from typing import Callable

class Rule:
    def __init__(self, name: str, matcher: Callable, action: Callable, cooldown: float = 1.0):
        self.name = name
        self.matcher = matcher
        self.action = action
        self.cooldown = cooldown
        self._last_triggered = 0.0

    def run(self, frame) -> bool:
        now = time.time()
        if now - self._last_triggered < self.cooldown:
            return False
        matches = self.matcher(frame)
        if matches:
            for (x, y) in matches:
                self.action(x, y)
            self._last_triggered = now
            return True
        return False


class RuleManager:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule: Rule):
        self.rules.append(rule)

    def run_rules(self, frame):
        for rule in self.rules:
            rule.run(frame)
