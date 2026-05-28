import pydantic_extract_3
from pydantic import ValidationError


def extract_with_retry(text: str,max_retries: int=3) -> Order:
    last_error = None
    for i in range(max_retries):
        try:
            return pydantic_extract_3.extract_order(text)
        except ValidationError as e:
            last_error = e
            print(f"[第 {i+1} 次失败] {e}")
    raise RuntimeError(f"抽取失败: {last_error}")

if __name__ == "__main__":
    text =  """老板你好，我要 3 台 iPhone 15 Pro，每台 8999 元。
收件人是李小明，电话 13900139000，
地址：北京市朝阳区望京 SOHO T1 楼 2008 室。"""
    print(extract_with_retry(text))