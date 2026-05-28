from pydantic import BaseModel,Field, EmailStr
from typing import List,Optional

class Resume(BaseModel):
    name:str = Field(...,description = "姓名") 
    age:int = Field(...,ge=0,le=100,description = "年龄")
    school:Optional[str] = Field(None,description = "院校")
    skills:List[str] = Field(default_factory = list,description = "技能列表")
    email:Optional[str] = None

# 1. 从字典创建
data = {"name": "张三", "age": 25, "skills": ["python", "sql"]}
r = Resume(**data)
print(r)

# 2. 转字典 / JSON
print(r.model_dump()) # 转字典
print(r.model_dump_json()) # 转JSON字符串

# 3. 校验失败会报错
try:
    Resume(name="李四", age=-5) # 年龄为负数，校验失败
except Exception as e:
    print(f"校验失败: {e}")

# 4. 从 JSON 字符串解析
json_str = '{"name": "王五", "age": 30, "skills": ["go"]}'
r2 =Resume.model_validate_json(json_str)
print(r2)