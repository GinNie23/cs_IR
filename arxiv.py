import requests
import os

def fetch_new_papers(query, limits):
    url = f"http://export.arxiv.org/api/query?search_query={query}&start=0&max_results={limits}&sortBy=submittedDate&sortOrder=descending"
    response = requests.get(url)
    papers = []

    # 解析返回的内容
    entries = response.text.split('<entry>')[1:]
    for entry in entries:
        title = entry.split('<title>')[1].split('</title>')[0]
        link = entry.split('<id>')[1].split('</id>')[0]
        papers.append({"title": title, "link": link})

    return papers

def translate_text(text, caiyun_token):
    url = "https://api.caiyunapp.com/v2/translate"  # 彩云小译 API 地址
    headers = {
        "Content-Type": "application/json",
        "X-Caiyun-Token": caiyun_token  # 彩云小译 Token
    }

    payload = {
        "text": text,
        "source": "en",  # 源语言
        "target": "zh"   # 目标语言
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()["targetText"]  # 提取翻译后的文本

def send_message_to_feishu(message, feishu_url):
    payload = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }
    response = requests.post(feishu_url, json=payload)
    print("消息发送成功:", response.status_code)

if __name__ == "__main__":
    QUERY = os.environ.get("QUERY")
    LIMITS = os.environ.get("LIMITS")
    FEISHU_URL = os.environ.get("FEISHU_URL")
    CAIYUN_TOKEN = os.environ.get("CAIYUN_TOKEN")

    # 获取新论文
    papers = fetch_new_papers(QUERY, LIMITS)
    message = "今天的新论文:\n"
    for paper in papers:
        # 翻译标题
        translated_title = translate_text(paper['title'], CAIYUN_TOKEN)
        message += f"* [{translated_title}]({paper['link']})\n"

        # 发送到飞书
    send_message_to_feishu(message, FEISHU_URL)