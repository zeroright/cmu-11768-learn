"""HW2 starter: agent evaluation harness.

Build a small task set + scorer to evaluate an agent end-to-end.
Matches L06-L10: pick one domain (coding/gui/research) and measure success rate.
"""
from dataclasses import dataclass, field
from typing import Callable, Any
import json, time, statistics

# ---------- Task definition ----------

@dataclass
class Task:
    id: str
    prompt: str
    expected: str  # or callable validator
    domain: str = "generic"
    max_steps: int = 8
    validate: Callable[[str], bool] | None = None
    def check(self, answer: str) -> bool:
        if self.validate: return self.validate(answer)
        return self.expected.lower() in answer.lower()

# ---------- Mock agent ----------

class MockAgent:
    """Replace with real agent. Mock returns canned answers."""
    def run(self, task: str) -> dict:
        time.sleep(0.01)
        return {'answer': task + ' :: done', 'steps': 3, 'tokens': 1200, 'cost': 0.012, 'tool_calls': 2}

# ---------- Evaluation ----------

@dataclass
class Result:
    task_id: str
    ok: bool
    steps: int
    tokens: int
    cost: float
    latency_s: float
    answer: str

def evaluate(agent, tasks: list[Task]) -> dict:
    results: list[Result] = []
    for t in tasks:
        t0 = time.time()
        out = agent.run(t.prompt)
        lat = time.time() - t0
        ok = t.check(out['answer'])
        results.append(Result(task_id=t.id, ok=ok, steps=out['steps'], tokens=out['tokens'], cost=out['cost'], latency_s=lat, answer=out['answer']))
    n = len(results)
    return {
        'n': n,
        'success_rate': sum(r.ok for r in results)/n,
        'avg_steps': statistics.mean(r.steps for r in results),
        'avg_tokens': statistics.mean(r.tokens for r in results),
        'total_cost': sum(r.cost for r in results),
        'avg_latency': statistics.mean(r.latency_s for r in results),
        'results': [r.__dict__ for r in results],
    }

if __name__ == '__main__':
    tasks = [
        Task(id='t1', prompt='Compute 12*30+5', expected='365'),
        Task(id='t2', prompt='Search for the config file', expected='app.py'),
        Task(id='t3', prompt='Add a todo to send recap', expected='send recap'),
        Task(id='t4', prompt='Summarize yesterday meeting', expected='meeting'),
        Task(id='t5', prompt='List top 3 issues', expected='issue'),
    ]
    agent = MockAgent()
    report = evaluate(agent, tasks)
    print(json.dumps({k:v for k,v in report.items() if k!='results'}, indent=2, ensure_ascii=False))
    for r in report['results']:
        print(f"  {r['task_id']}: ok={r['ok']} steps={r['steps']} cost=${r['cost']:.3f}")
