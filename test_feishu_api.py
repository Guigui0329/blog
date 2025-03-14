import requests

# 配置信息
FEISHU_APP_ID = "cli_a758c1a95478100c"
FEISHU_APP_SECRET = "zKG6ERRByVnc4Wgm10GtDeqaH5Mpe6Fw"
BASE_ID = "HdmbbrqiGaTamQsGFF1czYsFn6c"
TABLE_ID = "tblp76kJ6faJ26hn"

# 获取访问令牌
def get_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        token = response.json().get("tenant_access_token")
        print(f"获取到的访问令牌: {token}")
        return token
    print(f"获取访问令牌失败，状态码: {response.status_code}, 响应内容: {response.text}")
    return None

# 获取飞书多维表格数据
def get_feishu_data():
    access_token = get_access_token()
    if not access_token:
        return None
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{BASE_ID}/tables/{TABLE_ID}/records"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"获取到的多维表格数据: {data}")
        return data
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None

if __name__ == "__main__":
    get_feishu_data()