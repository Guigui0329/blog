from flask import Flask, render_template
from config import Config
import requests

app = Flask(__name__)
config = Config()

# 获取访问令牌
def get_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {
        "app_id": config.FEISHU_APP_ID,
        "app_secret": config.FEISHU_APP_SECRET
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("tenant_access_token")
    return None

# 获取飞书多维表格数据的函数
def get_feishu_data():
    access_token = get_access_token()
    if not access_token:
        return None
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{config.BASE_ID}/tables/{config.TABLE_ID}/records"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()
        # 处理金句输出中的换行符
        if 'data' in data and 'items' in data['data']:
            for record in data['data']['items']:
                if 'fields' in record and '金句输出' in record['fields']:
                    for item in record['fields']['金句输出']:
                        if 'text' in item:
                            item['text'] = item['text'].replace('\n', '<br>')
        return data
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None

@app.route('/')
def index():
    data = get_feishu_data()
    return render_template('index.html', data=data)

@app.route('/detail/<record_id>')
def detail(record_id):
    # 根据记录ID获取文章详情
    # 这里需要实现获取单条记录的逻辑
    return render_template('detail.html')

if __name__ == '__main__':
    app.run(debug=True)