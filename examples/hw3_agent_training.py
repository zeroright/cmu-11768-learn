"""HW3 starter: agent training loop (SFT then GRPO-like update).

Implements a minimal rejection-sampling + SFT loop on a mock "policy",
then a toy GRPO-style group-relative update.
Matches L08-L12 scope.
"""
import random, statistics, json
from dataclasses import dataclass, field

# ---------- Environment ----------

def task_reward(trajectory: list) -> float:
    """Toy reward: prefer trajectories with 'verify' step and short length."""
    has_verify = any('verify' in s for s in trajectory)
    return (1.0 if has_verify else 0.2) - 0.05*len(trajectory)

class ToyEnv:
    """Generates tasks with known reward."""
    def __init__(self):
        self.goals = ['add numbers','search file','update todo','verify answer','finish']
    def reset(self):
        return random.choice(self.goals)
    def step(self, action):
        # stub env reward
        return random.random() < 0.7

# ---------- Policy (mock) ----------

class ToyPolicy:
    """A policy is just a probability table over actions given a goal."""
    def __init__(self):
        self.p = {}  # (goal, action) -> weight
        self.actions = ['read','write','search','verify','answer']
    def prob(self, goal, action):
        return self.p.get((goal,action), 0.5)
    def update(self, goal, action, delta):
        self.p[(goal,action)] = max(0.0, min(1.0, self.prob(goal,action)+delta))
    def sample_traj(self, goal):
        traj = [goal]
        cur = goal
        for _ in range(random.randint(2,6)):
            a = random.choices(self.actions, weights=[self.prob(goal,a)+0.1 for a in self.actions])[0]
            traj.append(a)
            if a == 'answer': break
        return traj

# ---------- 1) Rejection sampling + SFT ----------

def rejection_sft(policy, env, n_tasks=30, n_rollouts=8, top_k=2, lr=0.05):
    """Sample rollouts per task, keep top-k by reward, SFT on winners."""
    stats = {'improved':0,'kept':0,'total':0}
    for _ in range(n_tasks):
        goal = env.reset()
        rollouts = [policy.sample_traj(goal) for _ in range(n_rollouts)]
        scored = sorted(rollouts, key=task_reward, reverse=True)
        for traj in scored[:top_k]:
            for action in traj[1:]:  # skip goal token
                policy.update(goal, action, +lr)
            stats['kept'] += 1
        stats['total'] += len(rollouts)
        stats['improved'] += 1
    return stats

# ---------- 2) GRPO-style group update ----------

def grpo_update(policy, env, n_prompts=20, group_size=8, lr=0.05):
    """Sample group, compute within-group advantage, update each action."""
    stats = {'mean_adv':0,'n_updates':0}
    for _ in range(n_prompts):
        goal = env.reset()
        group = [policy.sample_traj(goal) for _ in range(group_size)]
        rewards = [task_reward(t) for t in group]
        mu = statistics.mean(rewards)
        sd = max(1e-6, statistics.pstdev(rewards))
        advantages = [(r-mu)/sd for r in rewards]
        stats['mean_adv'] += statistics.mean(advantages)
        for traj, adv in zip(group, advantages):
            for action in traj[1:]:
                policy.update(goal, action, lr * adv)
                stats['n_updates'] += 1
    return stats

if __name__ == '__main__':
    random.seed(0)
    env = ToyEnv()
    p = ToyPolicy()
    print('before:', dict(list(p.p.items())[:5]))
    print('--- rejection SFT ---')
    print(rejection_sft(p, env, n_tasks=20))
    print('--- GRPO update ---')
    print(grpo_update(p, env, n_prompts=10))
    print('after:', dict(list(p.p.items())[:10]))
    print('TODO: replace ToyPolicy with real model (e.g., LoRA SFT then GRPO)')
