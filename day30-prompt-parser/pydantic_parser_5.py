import os
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

# 导入环境变量
load_dotenv()

llm = ChatOpenAI(
    model = "deepseek-chat",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = os.getenv("DEEPSEEK_BASE_URL"),
)

# 定义 Pydantic 模型
class Resume(BaseModel):
    name:str = Field(...,description="姓名")
    age:int = Field(...,description="年龄")
    skills:List[str] = Field(default_factory=list,description="技能列表")
    school:str = Field(...,description="毕业院校")

#创建解析器
parser = PydanticOutputParser(pydantic_object= Resume)

prompt = ChatPromptTemplate.from_messages([
    ("system","从文本中抽取候选人信息。\n\n格式要求：\n{format_instructions}"),
    ("human","{text}"),
])

# 测试
chain = prompt |llm |parser
result = chain.invoke({
    "text": "张三，男，1998年生，浙大计算机本科，会 Python 和 SQL。",
    "format_instructions":parser.get_format_instructions(),
})

print(type(result))
print(result.name)
print(result.skills)
print(result.model_dump)

