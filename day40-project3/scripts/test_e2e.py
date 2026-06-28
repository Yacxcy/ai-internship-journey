import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.agent.graph import chat

tests = [
    ("我们公司报销流程是什么？", "knowledge_base"),
    ("2026 年最新 LLM 排行榜", "search"),
    ("年终奖按工资 1.5 个月算，月薪 18000 是多少", "calc + maybe kb"),
    ("你好", "no_tool"),
]

for q,expected in tests:
    print(f"\n{'=' * 60}")
    print(f"Q: {q}")
    print(f"Expected: {expected}")
    print(f"{'=' * 60}")
    answer = chat(q,thread_id = "test")
    print(f"A: {answer}\n")