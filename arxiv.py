import json
import requests
import xml.etree.ElementTree as ET

# 函数：获取 ArXiv 论文
def fetch_arxiv_papers(query, limits):
    base_url = "http://export.arxiv.org/api/query?"
    search_query = f"search_query={query}&max_results={limits}"
    response = requests.get(base_url + search_query)

    if response.status_code == 200:
        return response.text  # 返回获取的论文信息
    else:
        raise Exception(f"Error fetching papers from ArXiv: {response.status_code} - {response.text}")

    # 函数：进行翻译
def translate_text(source_texts, caiyun_token):
    url = "http://api.interpreter.caiyunai.com/v1/translator"

    payload = {
        "source": source_texts,
        "trans_type": "auto2zh",  # 自动检测源语言并翻译为中文
        "request_id": "demo",      # 可修改为唯一的 request_id
        "detect": True,
    }

    headers = {
        "content-type": "application/json",
        "x-authorization": f"token {caiyun_token}",  # 使用传入的 API Token
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return json.loads(response.text)["target"]
    else:
        print(f"Error from Caiyun API: {response.status_code} - {response.text}")
        return None  # 处理错误情况

# 函数：发送消息到飞书
def send_to_feishu(feishu_url, message):
    payload = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }
    response = requests.post(feishu_url, json=payload)