import os # 导入os模块，用于获取环境变量
from openai import OpenAI # 从openai模块导入OpenAI类
from dotenv import load_dotenv # 从dotenv模块导入load_dotenv函数，用于加载环境变量

load_dotenv() # 加载环境变量
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),base_url=os.getenv("DEEPSEEK_BASE_URL")) # 创建OpenAI客户端实例

RESUME_TEXT ="""张三，男，1998年5月生，浙江杭州人。2020年毕业于浙江大学计算机科学与技术专业，本科。
现就职于阿里巴巴，担任高级 Python 后端开发工程师，工作 4 年。
联系方式：13800138000，邮箱 zhangsan@example.com。
熟悉技术栈：Python、Django、FastAPI、MySQL、Redis、Kafka。""" # 定义一个字符串变量，包含个人简历信息

PROMPTS ={
    "1_zero_shot":"从下面简历中提取：姓名、年龄、毕业院校、当前职位、邮箱。\n\n" + RESUME_TEXT, # 定义一个字典，包含零样本任务所需的提示
    "2_few_shot": """按照例子格式提取信息：
    例子1：
    输入：李四，1995年生，北京大学硕士，目前在腾讯做产品经理。
    输出：姓名: 李四 | 年龄: 30 | 院校: 北京大学 | 职位: 产品经理

    例子2：
    输入：王五，1990年北京出生，2015年清华大学计算机毕业，在字节做架构师。
    输出：姓名: 王五 | 年龄: 35 | 院校: 清华大学 | 职位: 架构师

    输入：""" + RESUME_TEXT + "\n输出：", # 定义一个字典，包含少样本任务所需的提示，提供了两个例子来指导模型如何提取信息
    "3_cot": "请一步步分析下面简历，先列出原文里的关键信息，然后整理成结构化格式（姓名、年龄、院校、职位、邮箱）。\n\n" + RESUME_TEXT, # 定义一个字典，包含链式思维任务所需的提示，要求模型先分析关键信息，再整理成结构化格式
    "4_role": "你是顶级 HR 简历解析专家。请从下面简历中精准提取候选人的：姓名、年龄、毕业院校、当前职位、邮箱。\n\n" + RESUME_TEXT, # 定义一个字典，包含角色扮演任务所需的提示，要求模型以顶级HR专家的身份来提取信息
    
    "5_xml": """<task>从简历中提取候选人信息</task>

    <resume>
    """ + RESUME_TEXT + """
    </resume>

    <output_format>
    姓名: <name>
    年龄: <age>
    院校: <school>
    职位: <position>
    邮箱: <email>
    </output_format>

    请按 output_format 给出结果。""", # 定义一个字典，包含结构化输出任务所需的提示，要求模型按照指定的XML格式来提取信息
}

for name,prompt in PROMPTS.items(): # 遍历PROMPTS字典中的每个键值对，分别执行不同的提示任务
    print(f"\n========== {name} ==========")   # 输出当前任务的名称，使用格式化字符串
    resp = client.chat.completions.create(
        model = "deepseek-v4-pro", # 模型名称
        messages = [{"role":"user","content":prompt}], # 消息内容，包含用户的提示
        temperature = 0, # 温度参数，控制生成文本的随机程度，0表示最确定的输出
    )
    print(resp.choices[0].message.content) # 输出模型生成的内容，访问响应对象中的第一条选择的消息内容