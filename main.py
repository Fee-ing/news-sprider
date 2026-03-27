# main.py

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
import os
from datetime import datetime

url = "https://tophub.today/"
fliter_keywords = ['微博', '知乎', '百度', '微信', '虎扑社区']

EMAIL_SEMDER = '732843374@qq.com'
EMAIL_PASSWORD = 'aiunwzrdaekmbcih'
EMAIL_RECEIVER = '2809750987@qq.com'

def crawl_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # 如果状态码不是200，会抛出异常
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # --- 重要：请在这里编写你具体的解析逻辑 ---
        # 示例：获取某个特定元素，如一个新闻列表的第一条新闻
        # first_news = soup.find('div', class_='news-item').get_text(strip=True) if soup.find('div', class_='news-item') else "暂无新闻"
        result = []
        fliter_keywords_copy = fliter_keywords.copy()
        for block in soup.select('div.bc-cc > div.cc-cd'):
            title = block.select_one('div.cc-cd-ih a div.cc-cd-lb > span').text.strip()
            if any(keyword == title for keyword in fliter_keywords_copy):
                list = []
                for item in block.select('div.cc-cd-cb a'):
                    list.append({
                        "url": item['href'],
                        "content": item.find('span', class_='t').text.strip(),
                        "views": item.find('span', class_='e').text.strip(),
                    })
                result.append({
                    "title": title,
                    "list": list,
                })
                fliter_keywords_copy.remove(title)
            
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {e}")
        return None
    except Exception as e:
        print(f"解析页面时发生错误: {e}")
        return None

def send_email(data_list):
    if not all([EMAIL_SEMDER, EMAIL_PASSWORD, EMAIL_RECEIVER]):
        print("错误：环境变量 EMAIL_SEMDER, EMAIL_PASSWORD, EMAIL_RECEIVER 未设置完整。")
        return

    # 邮件服务器配置 (以QQ邮箱为例)
    smtp_server = "smtp.qq.com"  # 请根据你的发件邮箱修改
    smtp_port = 465

    crawl_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 构造邮件
    msg = MIMEMultipart('alternative')
    msg['From'] = formataddr(('今日热榜，请查收', EMAIL_SEMDER))
    msg['To'] = formataddr(('社会主义接班人', EMAIL_RECEIVER))
    msg['Subject'] = Header(f"今日热榜 - {crawl_time}", 'utf-8')

    
    python
# main.py

def send_email(data_list):
    if not all([EMAIL_SEMDER, EMAIL_PASSWORD, EMAIL_RECEIVER]):
        print("错误：环境变量 EMAIL_SEMDER, EMAIL_PASSWORD, EMAIL_RECEIVER 未设置完整。")
        return

    smtp_server = "smtp.qq.com"
    smtp_port = 465
    crawl_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    msg = MIMEMultipart('alternative')
    msg['From'] = formataddr(('今日热榜，请查收', EMAIL_SEMDER))
    msg['To'] = formataddr(('社会主义接班人', EMAIL_RECEIVER))
    msg['Subject'] = Header(f"今日热榜 - {crawl_time}", 'utf-8')

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="x-apple-disable-message-reformatting">
        <meta name="format-detection" content="telephone=no, address=no, email=no, date=no, url=no">
        <!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml><![endif]-->
        <style type="text/css">
            /* 客户端重置 */
            * {{ margin: 0; padding: 0; }}
            body, table, td, a {{ -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }}
            table, td {{ mso-table-lspace: 0pt; mso-table-rspace: 0pt; }}
            img {{ -ms-interpolation-mode: bicubic; border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; }}
            a {{ text-decoration: none; }}
            
            /* 主体宽度控制 */
            html, body {{ 
                width: 100% !important; 
                height: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
            }}
            
            /* 确保图片不溢出 */
            img {{ max-width: 100% !important; height: auto !important; }}
            
            /* 滚动容器样式 */
            .scroll-container {{ 
                max-height: 450px; 
                overflow-y: auto; 
                overflow-x: hidden;
                -webkit-overflow-scrolling: touch;
            }}
            
            /* 滚动条样式 - Webkit 浏览器 */
            .scroll-container::-webkit-scrollbar {{ width: 6px; }}
            .scroll-container::-webkit-scrollbar-track {{ background: #f1f1f1; border-radius: 3px; }}
            .scroll-container::-webkit-scrollbar-thumb {{ background: #c1c1c1; border-radius: 3px; }}
            
            /* 文本截断样式 - 关键修复 */
            .content-text {{ 
                display: block; 
                overflow: hidden; 
                text-overflow: ellipsis; 
                white-space: nowrap; 
                max-width: 100%;
            }}
            
            /* 固定表格布局 - 确保列宽生效 */
            .item-table {{ 
                table-layout: fixed !important; 
                width: 100% !important;
            }}
            
            /* ========== 移动端媒体查询 - 强制覆盖 ========== */
            @media only screen and (max-width: 600px) {{
                /* 容器强制全宽 */
                .container {{ 
                    width: 100% !important; 
                    max-width: 100% !important;
                    min-width: 100% !important;
                }}
                /* 内容区域 */
                .content-padding {{ padding: 15px 10px !important; }}
                .header-padding {{ padding: 20px 15px !important; }}
                .footer-padding {{ padding: 15px 12px !important; }}
                
                /* 字体大小调整 */
                .header-title {{ font-size: 18px !important; }}
                .header-time {{ font-size: 11px !important; }}
                .topic-title {{ font-size: 15px !important; }}
                .topic-count {{ font-size: 10px !important; }}
                .item-content {{ font-size: 13px !important; }}
                .item-views {{ font-size: 10px !important; }}
                
                /* 序号样式 */
                .item-number {{ 
                    font-size: 9px !important; 
                    width: 16px !important; 
                    height: 16px !important; 
                    line-height: 16px !important; 
                }}
                
                /* 滚动容器 */
                .scroll-container {{ max-height: 300px !important; }}
                
                /* 卡片样式 */
                .topic-card {{ 
                    padding: 10px !important; 
                    margin-bottom: 10px !important;
                    width: 100% !important;
                    box-sizing: border-box !important;
                }}
                
                /* 列宽调整 - 关键修复 */
                .col-number {{ width: 22px !important; min-width: 22px !important; }}
                .col-content {{ width: auto !important; }}
                .col-views {{ width: 60px !important; min-width: 60px !important; }}
                
                /* 内容文本强制截断 */
                .content-text {{ 
                    max-width: 100% !important; 
                    width: 100% !important;
                }}
            }}
            
            /* 小屏幕适配 (iPhone SE 等) */
            @media only screen and (max-width: 360px) {{
                .header-title {{ font-size: 16px !important; }}
                .topic-title {{ font-size: 14px !important; }}
                .item-content {{ font-size: 12px !important; }}
                .col-views {{ width: 55px !important; min-width: 55px !important; }}
                .content-padding {{ padding: 12px 8px !important; }}
                .col-number {{ width: 20px !important; min-width: 20px !important; }}
            }}
        </style>
    </head>
    <body style="margin: 0 !important; padding: 0 !important;overflow: hidden; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; width: 100% !important;">
        <!-- 外层表格 - 全宽背景 -->
        <table width="calc(100% - 21px)" cellpadding="0" cellspacing="0" style="width: calc(100% - 21px) !important;overflow: hidden; margin: 0 auto !important; padding: 0 !important;" role="presentation">
            <tr>
                <td class="outer-td" align="center" style="width: 100%;" valign="top">
                    <!-- 主容器 - 桌面端 600px，移动端 100% -->
                    <!--[if mso]>
                    <table width="100%" cellpadding="0" cellspacing="0" style="width: 100%;">
                    <tr>
                    <td>
                    <![endif]-->
                    <table class="container" width="100%" cellpadding="0" cellspacing="0" style="width: 100%; max-width: 800px; background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); overflow: hidden; margin: 0 auto;" role="presentation">
                    <![endif]-->
                        
                        <!-- 头部 -->
                        <tr>
                            <td class="header-padding" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px 20px; text-align: center;">
                                <h1 class="header-title" style="margin: 0; color: #ffffff; font-size: 22px; font-weight: 600; letter-spacing: 1px;">📰 今日热榜</h1>
                                <p class="header-time" style="margin: 8px 0 0 0; color: rgba(255, 255, 255, 0.9); font-size: 12px;">{crawl_time}</p>
                            </td>
                        </tr>
                        
                        <!-- 内容区域 -->
                        <tr>
                            <td class="content-padding" style="padding: 20px 15px;">
    """
    
    if data_list:
        for idx, topic in enumerate(data_list):
            card_bg = "#f8f9fa" if idx % 2 == 0 else "#ffffff"
            display_list = topic['list']
            total_count = len(topic['list'])
            has_more = total_count > 10
            
            html_content += f"""
                                <!-- 主题卡片 -->
                                <div class="topic-card" style="background-color: {card_bg}; border-radius: 8px; padding: 15px; margin-bottom: 15px; border-left: 4px solid #667eea; overflow: hidden; width: 100%; box-sizing: border-box;">
                                    <h2 class="topic-title" style="margin: 0 0 10px 0; color: #2d3748; font-size: 17px; font-weight: 600; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">
                                        🔥 {topic['title']}
                                        <span class="topic-count" style="float: right; font-size: 11px; color: #a0aec0; font-weight: 400;">
                                            共{total_count}条
                                        </span>
                                    </h2>
                                    
                                    <!-- 滚动容器 -->
                                    <div class="scroll-container" style="max-height: 450px; overflow-y: auto; overflow-x: hidden; -webkit-overflow-scrolling: touch; padding-right: 4px;">
                                        <table width="100%" cellpadding="0" cellspacing="0" style="width: 100%; table-layout: fixed;" role="presentation">
            """
            
            # 遍历列表项，添加序号（最多 10 条）
            for item_idx, item in enumerate(display_list, start=1):
                html_content += f"""
                                            <tr>
                                                <td style="padding: 6px 0; border-bottom: 1px solid #f0f0f0;">
                                                    <table class="item-table" width="100%" cellpadding="0" cellspacing="0" style="width: 100%; table-layout: fixed;" role="presentation">
                                                        <colgroup>
                                                            <col width="26" />
                                                            <col />
                                                            <col width="75" />
                                                        </colgroup>
                                                        <tr>
                                                            <!-- 第一列：序号（固定宽度） -->
                                                            <td class="col-number" style="vertical-align: middle; padding-right: 6px; width: 26px; min-width: 26px;">
                                                                <span class="item-number" style="display: inline-block; width: 20px; height: 20px; line-height: 20px; text-align: center; background-color: #667eea; color: #ffffff; border-radius: 50%; font-size: 11px; font-weight: 600;">
                                                                    {item_idx}
                                                                </span>
                                                            </td>
                                                            <!-- 第二列：content（占据剩余空间，强制截断） -->
                                                            <td class="col-content" style="vertical-align: middle; overflow: hidden; width: auto;">
                                                                <a href="{item['url']}" class="item-content" style="color: #2d3748; text-decoration: none; font-size: 13px; font-weight: 500; line-height: 1.4; display: block; overflow: hidden;">
                                                                    <span class="content-text" style="display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; width: 100%;">{item['content']}</span>
                                                                </a>
                                                            </td>
                                                            <!-- 第三列：views（固定宽度，右对齐） -->
                                                            <td class="col-views" style="vertical-align: middle; text-align: right; padding-left: 6px; width: 75px; min-width: 75px;">
                                                                <span class="item-views" style="color: #a0aec0; font-size: 10px; white-space: nowrap; display: block;">
                                                                    👁️ {item['views']}
                                                                </span>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                """
            
            html_content += """
                                        </table>
                                    </div>
            """
            
            # 如果有更多内容，添加提示
            if has_more:
                html_content += f"""
                                    <p style="margin: 8px 0 0 0; text-align: center; color: #a0aec0; font-size: 11px;">
                                        ⋯ 还有 {total_count - 10} 条内容，向上滑动查看 ⋯
                                    </p>
                """
            
            html_content += """
                                </div>
            """
    else:
        html_content += """
                                <div style="text-align: center; padding: 40px 15px; background-color: #f8f9fa; border-radius: 8px; width: 100%; box-sizing: border-box;">
                                    <p style="margin: 0; color: #718096; font-size: 15px;">😔 未获取到有效数据</p>
                                    <p style="margin: 8px 0 0 0; color: #a0aec0; font-size: 12px;">请稍后重试</p>
                                </div>
        """

    html_content += f"""
                            </td>
                        </tr>
                        
                        <!-- 底部 -->
                        <tr>
                            <td class="footer-padding" style="background-color: #2d3748; padding: 18px 20px; text-align: center;">
                                <p style="margin: 0; color: #a0aec0; font-size: 11px; line-height: 1.6;">
                                    此邮件由 Python 爬虫自动生成 · 数据来源：<a href="{url}" style="color: #667eea; text-decoration: none;">tophub.today</a>
                                </p>
                                <p style="margin: 6px 0 0 0; color: #718096; font-size: 10px;">
                                    © {datetime.now().strftime('%Y')} 今日热榜推送服务
                                </p>
                            </td>
                        </tr>
                    </table>
                    <!--[if mso]>
                    </td>
                    </tr>
                    </table>
                    <![endif]-->
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    # 发送邮件
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(EMAIL_SEMDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SEMDER, [EMAIL_RECEIVER], msg.as_string())
        print("邮件发送成功！")
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