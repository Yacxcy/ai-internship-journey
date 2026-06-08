import os
from dotenv import load_dotenv
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

# 导入环境变量
load_dotenv()

class ResumeInfo(BaseModel):
    name:str = Field(...,description="姓名")
    age:int = Field(...,description="年龄")
    school:Optional[str] = Field(None,description="毕业院校")
    degree:Optional[str] = Field(None,description="学历")
    company: Optional[str] = Field(None, description="当前公司")
    position: Optional[str] = Field(None, description="当前职位")
    years: Optional[int] = Field(None, description="工作年限")
    skills: List[str] = Field(default_factory=list, description="技能列表")
    phone: Optional[str] = None
    email: Optional[str] = None

class ResumeExtractor:
    def __init__(self):
        # 初始化 LLM 和解析器
        self.llm = ChatOpenAI(
            model = "deepseek-v4-pro",
            api_key = os.getenv("DEEPSEEK_API_KEY"),
            base_url = os.getenv("DEEPSEEK_BASE_URL"),
            temperature=0,
        )
        # 定义 Pydantic 模型和解析器
        self.parser = PydanticOutputParser(pydantic_object=ResumeInfo)
        # 定义提示模板
        self.prompt = ChatPromptTemplate.from_messages([
            ("system",
             "你是简历解析专家。从简历文本中抽取候选人信息。\n"
             "如果某字段无法确认，输出 null 或空数组。\n\n"
             "格式要求：\n{format_instructions}"),
             ("human","{text}")
        ])
        # 构建链
        self.chain = self.prompt | self.llm | self.parser
    # 定义抽取方法
    def extract(self,text:str)->ResumeInfo:
        return self.chain.invoke({
            "text":text,
            "format_instructions":self.parser.get_format_instructions(),
        })

    # 定义批量抽取方法
    def batch(self,texts:List[str])->List[ResumeInfo]:
        return self.chain.batch([
            {"text":t,"format_instructions":self.parser.get_format_instructions()} # 每条文本都要加上格式说明
            for t in texts
        ])

# 测试
if __name__ == "__main__":
    # 创建实例
    extractor = ResumeExtractor()

    samples =[
        "张三，男，1998年5月生，浙江杭州人。2020年浙大计算机本科。现就职阿里巴巴 Python 高级开发，4 年。13800138000",
        "Lily Chen, 28, Master of CS at Tsinghua. ByteDance frontend, 3 years. Skills: React, TypeScript. lily@bytedance.com",
        "王某，35，清华本科，前美团技术专家，分布式系统，8 年后端，熟悉 Java/Go/MySQL。",
    ]

    result = extractor.batch(samples)
    for r in result:
        print(r.model_dump_json(indent=2,ensure_ascii=False))
        print("----------------------") 
