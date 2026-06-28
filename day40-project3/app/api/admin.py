import json
import time
from pathlib import Path
from app.api.chat import LOG_FILE
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()  # 创建路由对象

# 日志查看接口
@router.get("/admin/logs/recent")
def recennt_logs(n :int = 50):
    if not LOG_FILE.exists():
        return []
    lines = LOG_FILE.read_text(encoding = "utf-8").strip().split("\n")
    return [json.loads(l) for l in lines[-n:]]

@router.get("/admin/status")
def status():
    if not LOG_FILE.exists():
        return {"total":0}
    records =[json.loads(l) for l in LOG_FILE.read_text(encoding = "utf-8").strip().split("\n")]
    return {
        "total" :len(records),
        "avg_duration":sum(r["duration_sec"] for r in records)/len(records),
        "tool_distribution":{
            t:sum(1 for r in records if t in r["tool_used"])
            for t in ["search_kb", "web_search", "calculator"]
        }
    }