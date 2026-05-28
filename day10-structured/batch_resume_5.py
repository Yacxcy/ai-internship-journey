import os
import json
import pandas as pd
from openai import OpenAI
from typing import List, Optional
from pydantic import BaseModel, Field,EmailStr
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),base_url=os.getenv("DEEPSEEK_BASE_URL"))

# 定义 Pydantic 模型
class ResumeInfo(BaseModel):
    name:str = Field(...,description = "姓名") 
    age:Optional[int] =Field(None,description = "年龄")
    school:Optional[str] = None
    degree: Optional[str] = Field(None, description="学历，本科/硕士/博士")
    company: Optional[str] = None
    position: Optional[str] = None
    years: Optional[int] = Field(None, description="工作年限")
    skills: List[str] = Field(default_factory=list)
    phone: Optional[str] = None
    email: Optional[str] = None

# 从模型生成简历信息
def extract(text:str)->ResumeInfo:
    schema = json.dumps(ResumeInfo.model_json_schema(),ensure_ascii = False,indent = 2)
    prompt = f"""从简历中抽取候选人信息，按 JSON Schema 输出 JSON。
    Schema:{schema}
    简历:{text}
    只输出 JSON。
    """
    resp = client.chat.completions.create(
        model = "deepseek-v4-pro",
        messages= [{"role":"user","content":prompt}],
        response_format={"type":"json_object"}, # 指定返回的格式为 JSON 对象
        temperature = 0,
    )
    return ResumeInfo.model_validate_json(resp.choices[0].message.content) # 直接将返回的 JSON 字符串解析为 Pydantic 模型实例

RESUMES = [
    "张三，男，1998年5月生，浙江杭州人。2020年浙大计算机本科。现就职阿里巴巴 Python 高级开发，4 年。13800138000",
    "Lily Chen, 28, Master of CS at Tsinghua. Working at ByteDance as a frontend engineer for 3 years. Skills: React, TypeScript, Node.js. lily@bytedance.com",
    "王某某，35，清华本科，前美团技术专家，主攻分布式系统，做过 8 年后端，熟悉 Java/Go/MySQL。",
    "刘佳，26 岁，硕士在读，复旦计算机视觉方向，无工作经验，会 PyTorch。15000000000",
    "赵敏，41，本科上海交大，目前在百度任 AI 总监，团队 30 人，10 年经验。zhao@baidu.com",
]

results=[]
for i,text in enumerate(RESUMES):
    print(f"\n--- 处理第 {i+1} 份 ---")
    try:
        info = extract(text)
        results.append(info.model_dump())
        print(f"✓ {info.name}")
    except Exception as e:
        print(f"✗ 处理失败: {e}")
        results.append({"error": str(e)})

df =pd.DataFrame(results) # 将结果转换为 DataFrame
df.to_csv("resume_results.csv", index=False,encoding="utf-8-sig") # 保存为 CSV 文件
print("\n=== 抽取结果 ===")
print(df)



