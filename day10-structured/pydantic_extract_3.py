import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),base_url=os.getenv("DEEPSEEK_BASE_URL"))


# 定义 Pydantic 模型
class Order(BaseModel):
    """订单信息"""
    product_name:str = Field(..., description="商品名称")
    quantity:int = Field(...,gt=0,description="数量")
    unit_price:float = Field(...,gt=0,description="单价(元)")
    total: float = Field(..., description="总价（元）= 数量 * 单价")
    customer_name: str = Field(..., description="收件人姓名")
    address: str = Field(..., description="收货地址")
    phone: str = Field(..., description="联系电话")

# 从模型生成订单信息
def extract_order(text:str)->Order:
    schema = json.dumps(Order.model_json_schema(),ensure_ascii = False,indent=2) # 获取模型的 JSON Schema,并转换为 JSON 字符串
    prompt = f"""你是订单信息抽取助手。请从下面的文本中抽取订单信息，严格按 JSON Schema 输出 JSON。
    Schema:
    {schema}

    用户描述:
    {text}

    请只输出 JSON，不要其他文字。"""

    resp = client.chat.completions.create(
        model = "deepseek-v4-pro",
        messages=[{"role":"user","content":prompt}],
        response_format={"type":"json_object"}, # 指定返回的格式为 JSON 对象
        temperature = 0,
    )
    return Order.model_validate_json(resp.choices[0].message.content) # 直接将返回的 JSON 字符串解析为 Pydantic 模型实例

# 测试
if __name__ == "__main__":
    text = """老板你好，我要 3 台 iPhone 15 Pro，每台 8999 元。收件人是李小明，
    电话 13900139000，地址：北京市朝阳区望京 SOHO T1 楼 2008 室。"""

    order = extract_order(text)
    print(order)
    print(order.model_dump_json(indent=2, ensure_ascii=False))
