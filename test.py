import requests

# 您的 Mapbox Access Token
access_token = 'pk.eyJ1IjoicmF5dGFuIiwiYSI6ImNtNHRpaXFrMDBiZGcyanBvZ21xcXl5NnAifQ.sKCK5cCaw7Sns6uIkdIZvQ'

# 要转换的地址
address = '台北市信義區信義路五段7號'

# 构建请求 URL
url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json'

# 设置请求参数
params = {
    'access_token': access_token,
    'limit': 1,  # 返回的结果数量，设置为1表示只返回最匹配的结果
    'language': 'zh-TW'  # 返回结果的语言，设置为繁体中文
}

# 发送 GET 请求
response = requests.get(url, params=params)

# 检查请求是否成功
if response.status_code == 200:
    data = response.json()
    if data['features']:
        # 获取经纬度坐标
        longitude, latitude = data['features'][0]['center']
        print(f'地址: {address}')
        print(f'经度: {longitude}')
        print(f'纬度: {latitude}')
    else:
        print('未找到匹配的地址。')
else:
    print(f'请求失败，状态码: {response.status_code}')
