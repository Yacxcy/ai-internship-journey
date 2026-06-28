import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.agent.graph import chat

with open("tests/test_set.json","r",encoding="utf-8") as f:
    cases = json.load(f)

results = {"total":len(cases),"pass":0,"fail":[]}

for case in cases:
    answer = chat(case["question"],thread_id = f"eval-{case['id']}")
    hits = sum(1 for kw in case["expected_keywords"] if kw in answer)
    needed = max(1,len(case["expected_keywords"]) // 2)
    if hits>= needed:
        results["pass"] += 1
        print(f"✅ Q{case['id']}")
    else:
        results["fail"].append({"id": case["id"], "q": case["question"], "a": answer[:200]})
        print(f"❌ Q{case['id']}: {case['question']}")

print(f"\n通过率: {results['pass']}/{results['total']} = {results['pass']/results['total']*100:.1f}%")