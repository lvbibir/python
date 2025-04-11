import requests
import json

# 设置请求的 URL
url = "http://platform.ai.cnpc/kunlun/ingress/api/h3t-eeceff/6ede2fb11ceb481e8c51cffcc40d2517/ai-bad5c916c57346959d84e1b42bd41c5b/service-c0d63a93c4ba4ff5a494a286b99bbb71/v1/chat/completions"

# 设置请求头
headers = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3ODNmNTQ4ODY4Mzk0M2VkOWU1NDQ3NjQwY2Y3OTA5MyIsImlzcyI6ImFwaS1hdXRoLWtleSIsImV4cCI6NDg5NDY4MjU3NH0.ZU8uoKTUpdtUN2LZSiji9lypsdqnYk4VYkq6GO96HSxqcTNK-Y8cQpBuFurr5rhxK_7vZ9M6LB2auI5Jh7CynF-7Kwpl6XOkYAwIym-44UVNDpdJHMj1hOB403dBsaV8cJZsYsfsrHNxCNHMAiOl2Uv4Hr6M9yPgirmV31qt3UmKgz6IxaqKqnQZnd_4lHKN0t-vURNynTwyrHzWTNTtcT2Va5lNezDjs-8LUKcaBTtji-ciG7xpkEUUTjdrNcvuJKBcHD4zAlWJBMCZ6iblT1fLOW6uUH_P2IRIWDC98lQ4vVjh2HmH5i1l3PY3Dx8t9IGYpfsroX85engxBRXB9Q",
    "Content-Type": "application/json",
}

# 设置请求体
data = {
    "model": "DeepSeekV3quant",
    "max_tokens": 4096,
    "messages": [{"role": "user", "content": "1+1等于几"}],
    "stream": False,
}

# 发送 POST 请求并忽略 SSL 验证
response = requests.post(url, headers=headers, data=json.dumps(data))

# 打印响应
print(response.status_code)
print(response.json())
