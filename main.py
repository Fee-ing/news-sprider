# main.py

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
import os
from dotenv import load_dotenv
from datetime import datetime

URL = "https://tophub.today/"
CONFIG = [
  {"keyword": "微博", "title": "微博", "sort": 0},
  {"keyword": "百度", "title": "百度", "sort": 1},
  {"keyword": "哔哩哔哩", "title": "B站", "sort": 2},
  {"keyword": "抖音", "title": "抖音", "sort": 3},
  {"keyword": "快手", "title": "快手", "sort": 4},
  {"keyword": "腾讯新闻", "title": "腾讯", "sort": 5},
  {"keyword": "百度贴吧", "title": "贴吧", "sort": 6},
  {"keyword": "知乎", "title": "知乎", "sort": 7},
  {"keyword": "微信", "title": "微信", "sort": 8},
  {"keyword": "掘金", "title": "掘金", "sort": 9},
  {"keyword": "36氪", "title": "36氪", "sort": 10},
  {"keyword": "IT之家", "title": "IT之家", "sort": 11},
  {"keyword": "虎嗅网", "title": "虎嗅", "sort": 12},
  # {
  #   "keyword": "虎扑社区",
  #   "title": "虎扑社区",
  #   "sort": 5
  # }
]

load_dotenv()

EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.environ.get("EMAIL_RECEIVER")


def crawl_data():
  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
  }

  try:
    response = requests.get(URL, headers=headers)
    response.raise_for_status()  # 如果状态码不是200，会抛出异常

    soup = BeautifulSoup(response.text, "html.parser")

    # --- 重要：请在这里编写你具体的解析逻辑 ---
    # 示例：获取某个特定元素，如一个新闻列表的第一条新闻
    result = []
    config_copy = CONFIG.copy()
    for block in soup.select("div.bc-cc > div.cc-cd"):
      title = block.select_one("div.cc-cd-ih a div.cc-cd-lb > span").text.strip()
      for data in config_copy:
        if data["keyword"] == title:
          list = []
          for item in block.select("div.cc-cd-cb a"):
            list.append(
              {
                "url": item["href"],
                "content": item.find("span", class_="t").text.strip(),
                "views": item.find("span", class_="e").text.strip(),
              }
            )
          result.append({"title": data["title"], "list": list, "sort": data["sort"]})
          config_copy.remove(data)
          break
    return sorted(result, key=lambda x: x["sort"])

  except requests.exceptions.RequestException as e:
    print(f"网络请求失败: {e}")
    return None
  except Exception as e:
    print(f"解析页面时发生错误: {e}")
    return None


def send_email(data_list):
  if not all([EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER]):
    print(
      "错误：环境变量 EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER 未设置完整。"
    )
    return

  # 解析多个收件人
  EMAIL_RECEIVER_LIST = [
    email.strip() for email in EMAIL_RECEIVER.split(",") if email.strip()
  ]

  if not EMAIL_RECEIVER_LIST:
    print("错误：未设置有效的收件人地址。")
    return

  smtp_server = "smtp.qq.com"
  smtp_port = 465

  for receiver in EMAIL_RECEIVER_LIST:
    msg = MIMEMultipart("alternative")
    msg["From"] = formataddr(("今日新闻热榜", EMAIL_SENDER))
    msg["To"] = receiver
    msg["Subject"] = Header(f"快点来看看今天有哪些大事发生了吧", "utf-8")

    news_html = ""
    tag_html = ""
    if data_list:
      for idx, item in enumerate(data_list):
        list_html = ""
        tag_html += f"""
        <a class="header-tag">{item['title']}</a>
        """
        for i, list_item in enumerate(item["list"]):
          list_html += f"""
          <a class="news" href="{list_item['url']}" target="_blank">
            <div class="news-sort">{i+1}</div>
            <div class="news-title">{list_item['content']}</div>
            <div class="news-view">{list_item['views']}</div>
          </a>
          """

        news_html += f"""
        <div class="block" id="tag-{idx+1}">
          <input type="radio" name="tab" id="tab-{idx+1}"" {"checked" if idx == 0 else ""}>
          <label class="tab-button" for="tab-{idx+1}">
            <div class="button-text">🔥 {item['title']}</div>
            <span>共{len(item['list'])}条</span>
          </label>
          <div class="content">
            <div class="list">
              {list_html}
            </div>
          </div>
        </div>
        """

    page_html = f"""
    <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>今日热榜</title>
        <style type="text/css">
          * {{ margin: 0; padding: 0;box-sizing: border-box; }}
          a,
          a:link,
          a:visited,
          a:hover,
          a:active,
          a:focus {{
            outline: 0;
            background-color: transparent;
            text-decoration: none;
            -webkit-tap-highlight-color:rgba(0,0,0,0);
            -webkit-tap-highlight-color: transparent;
          }}
          ::-webkit-scrollbar {{ width: 6px; }}
          ::-webkit-scrollbar-track {{ background: #ffffff; border-radius: 3px; }}
          ::-webkit-scrollbar-thumb {{ background: #f1f5f9; border-radius: 3px; }}
          html, body {{ width: 100%; height: 100%; overflow: hidden; }}
          body {{ overflow-y: auto;scroll-behavior: smooth; }}
          .app {{ margin: 0 auto;max-width: 1000px; }}
          .header {{
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            border-radius: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 10px 0 15px;
          }}
          .footer {{
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            padding: 18px 0;
            margin-top: 20px;
            border-radius: 12px;
            background-color: #2d3748;
          }}
          .body {{
            margin-top: 20px;
            position: relative;
          }}
          .block input {{
            display: none;
          }}
          .news {{
            display: flex;
            align-items: center;
            line-height: 1;
            text-decoration: none;
            color: #2d3748;
            font-size: 13px;
            overflow: hidden;
          }}
          .news-sort {{
            width: 22px;
            height: 22px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #667eea;
            color: #ffffff;
            border-radius: 50%;
            font-size: 12px;
            font-weight: 600;
          }}
          .news-title {{
            flex: 1;
            font-weight: 500;
            line-height: 1.4;
            margin-left: 10px;
          }}
          .news-view {{
            margin-left: 10px;
            color: #94a3b8;
            font-size: 11px;
            text-align: right;
          }}
          .block {{
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            overflow: hidden;
            padding: 20px;
          }}
          .block:not(:first-child) {{
            margin-top: 20px;
          }}
          .tab-button {{
            display: flex;
            align-items: center;
            padding-bottom: 20px;
            font-size: 16px;
            font-weight: 600;
          }}
          .tab-button .button-text {{
            flex: 1;
          }}
          .tab-button span {{
            color: #94a3b8;
            font-size: 12px;
          }}
          .news {{
            border-top: 1px solid #f1f5f9;
            padding: 10px 0;
          }}
          .news:not(:last-child) {{
            margin: 0;
          }}
          .tag-list {{
            display: flex;
            align-items: center;
            font-size: 13px;
            margin-top: 8px;
          }}
          .header-tag {{
            padding: 0 10px;
            color: rgba(255, 255, 255, 0.9);
            text-decoration: none;
          }}
          .header-tag:not(:last-child) {{
            border-right: 1px solid rgba(255, 255, 255, 0.5);
          }}
          /* 移动端适配 */
          @media only screen and (max-width: 768px) {{
            .app {{
              width: calc(100% - 20px);
            }}
            .body {{
              margin-top: 10px;
            }}
            .footer {{
              margin-top: 10px;
            }}
            .block {{
              padding: 0 5px 10px;
              width: 100px;
              background-color: #f1f5f9;
              border-radius: 0;
              box-shadow: none;
              margin-top: 0 !important;
            }}
            .block:first-child {{
              padding-top: 10px;
              border-radius: 12px 12px 0 0;
            }}
            .block:last-child {{
              padding-bottom: 10px;
              border-radius: 0 0 12px 12px;
            }}
            .tab-button {{
              display: flex;
              align-items: center;
              padding: 10px 5px;
              font-size: 11px;
              font-weight: 500;
              color: #667eea;
              background-color: rgba(102, 126, 234, 0.15);
              border-radius: 8px;
              cursor: pointer;
              touch-action: manipulation;
              -webkit-tap-highlight-color:rgba(0,0,0,0);
              -webkit-tap-highlight-color: transparent;
              transition: background-color 0.3s, color 0.3s;
            }}
            .tab-button span {{
              display: none;
            }}
            .content {{
              position: absolute;
              display: none;
              width: calc(100% - 110px);
              height: 100%;
              background-color: #ffffff;
              border-radius: 12px;
              margin-left: 10px;
              box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
              overflow: hidden;
              top: 0;
              right: 0;
              padding: 10px 5px;
            }}
            .list {{
              height: 100%;
              overflow-y: auto;
              padding-right: 6px;
            }}
            [id^="tab"]:checked~label {{
              background-color: #667eea;
              color: #ffffff;
            }}
            [id^="tab"]:checked~.content {{
              display: block;
            }}
            .news {{
              border: none;
              padding: 0;
            }}
            .news:not(:last-child) {{
              margin-bottom: 15px;
            }}
            .news-sort {{
              width: 18px;
              height: 18px;
              font-size: 10px;
            }}
            .news-title {{
              font-size: 12px;
            }}
            .news-view {{
              font-size: 10px;
            }}
            .tag-list {{
              font-size: 9px;
            }}
            .header-tag {{
              padding: 0 5px;
            }}
          }}
        </style>
      </head>
      <body>
        <div class="app"> 
          <div class="header">
            <h1 style="color: #ffffff; font-size: 24px;">📰 今日新闻热榜</h1>
            <div class="tag-list">{tag_html}</div>
          </div>
          <div class="body">{news_html}</div>
          <div class="footer">
            <p style="color: #a0aec0; font-size: 11px; line-height: 1.6;">每天7:00 - 21:00期间定时推送</p>
            <p style="margin-top: 6px; color: #718096; font-size: 10px;">©Powered by Fee 以上内容仅供参考</p>
          </div>
        </div>
      </body>
      </html>
      """

    msg.attach(MIMEText(page_html, "html", "utf-8"))

    # 发送邮件
    try:
      server = smtplib.SMTP_SSL(smtp_server, smtp_port)
      server.login(EMAIL_SENDER, EMAIL_PASSWORD)
      server.sendmail(EMAIL_SENDER, [receiver], msg.as_string())
      print(f"✓ 邮件发送成功：{receiver}")
    except Exception as e:
      print(f"邮件发送失败: {e}")
    finally:
      server.quit()


if __name__ == "__main__":
  print("开始爬取数据...")
  data = crawl_data()

  if data:
    print("数据爬取成功，正在发送邮件...")
    send_email(data)
  else:
    print("数据爬取失败，跳过邮件发送。")
