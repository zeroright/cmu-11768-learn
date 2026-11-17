"""HW1 starter: minimal agent harness with tool dispatch + observation loop.

Implements the skeleton of an agent loop, matching CMU 11-768 L01-L05 scope.
Goal: fill in TODOs to make agent handle multi-step tasks.
"""
from dataclasses import dataclass, field
from typing import Callable, Any
import json

# ---------- Tools ----------

def calculator(expr: str) -> str:
    """Evaluate a math expression."""
    try:
        return str(eval(expr, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"error: {e}"

def file_search(query: str) -> str:
    """Stub: search files and return hits."""
    return f"[file_search:{query}] found 2 hits: README.md, app.py"

def todo_add(item: str) -> str:
    """Add an item to in-memory todo list."""
    _STATE['todos'].append(item)
    return f"added: {item}"

_STATE = {'todos': []}

TOOLS: dict[str, Callable] = {
    'calculator': calculator,
    'file_search': file_search,
    'todo_add': todo_add,
}

# ---------- Schemas (like OpenAI tool spec) ----------

TOOL_SCHEMAS = [
    {"name":"calculator","description":"Evaluate math","parameters":{"type":"object","properties":{"expr":{"type":"string"}},"required":["expr"]}},
    {"name":"file_search","description":"Search files","parameters":{"type":"object","properties":{"query":{"type":"string"}},"required":["query"]}},
    {"name":"todo_add","description":"Add todo","parameters":{"type":"object","properties":{"item":{"type":"string"}},"required":["item"]}},
]

# ---------- Model abstraction ----------

class MockLLM:
    """Replace with real LLM call. Mock returns scripted tool calls for demo."""
    def __init__(self):
        self.script = [
            # (thought, tool_call or None)
            ("I need to know the total.", {"name":"calculator","arguments":{"expr":"12*30+5"}}),
            ("Now I should save a note.", {"name":"todo_add","arguments":{"item":"send recap to user"}}),
            ("Done, summarize.", None),
        ]
        self.i = 0
    def step(self, prompt: str, history: list) -> tuple[str, dict | None]:
        if self.i >= len(self.script):
            return "I have nothing more to do.", None
        t, a = self.script[self.i]; self.i += 1
        return t, a

# ---------- Harness ----------

@dataclass
class Agent:
    llm: Any
    tools: dict
    schemas: list
    max_steps: int = 8
    history: list = field(default_factory=list)

    def dispatch(self, name: str, args: dict) -> str:
        if name not in self.tools:
            return f"error: tool '{name}' not registered"
        try:
            return str(self.tools[name](**args))
        except Exception as e:
            return f"error: {e}"

    def run(self, task: str) -> str:
        print(f"[task] {task}")
        for step in range(self.max_steps):
            # TODO 1: render prompt with history + tool schemas (you should use schemas!)
            prompt = self._render_prompt(task)
            # TODO 2: ask model for (thought, tool_call) — currently mocked
            thought, call = self.llm.step(prompt, self.history)
            print(f"[thought {step}] {thought}")
            self.history.append({"role":"assistant","content":thought,"tool_call":call})
            if call is None:
                return f"final: {thought}"
            # TODO 3: dispatch tool and append observation
            obs = self.dispatch(call['name'], call.get('arguments', {}))
            print(f"[action {step}] {call['name']}({call.get('arguments')})")
            print(f"[observation {step}] {obs}")
            self.history.append({"role":"tool","name":call['name'],"content":obs})
        return "final: max steps reached"

    def _render_prompt(self, task: str) -> str:
        # TODO 4: serialize schemas into the prompt so the model knows what tools exist
        tool_desc = "\n".join(f"- {s['name']}: {s['description']}" for s in self.schemas)
        return f"Task: {task}\nTools:\n{tool_desc}\n"

if __name__ == "__main__":
    agent = Agent(llm=MockLLM(), tools=TOOLS, schemas=TOOL_SCHEMAS)
    print(agent.run("Compute 12*30+5 and add a todo"))
    print("todos:", _STATE['todos'])
