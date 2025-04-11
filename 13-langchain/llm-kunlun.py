'''
简单使用 langchain 进行大模型 API 的对话
'''

import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

os.environ['REQUESTS_CA_BUNDLE'] = '/etc/ssl/certs/中国石油认证中心.pem'

llm = ChatOpenAI(
    api_key="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3ODNmNTQ4ODY4Mzk0M2VkOWU1NDQ3NjQwY2Y3OTA5MyIsImlzcyI6ImFwaS1hdXRoLWtleSIsImV4cCI6NDg5NDY4MjU3NH0.ZU8uoKTUpdtUN2LZSiji9lypsdqnYk4VYkq6GO96HSxqcTNK-Y8cQpBuFurr5rhxK_7vZ9M6LB2auI5Jh7CynF-7Kwpl6XOkYAwIym-44UVNDpdJHMj1hOB403dBsaV8cJZsYsfsrHNxCNHMAiOl2Uv4Hr6M9yPgirmV31qt3UmKgz6IxaqKqnQZnd_4lHKN0t-vURNynTwyrHzWTNTtcT2Va5lNezDjs-8LUKcaBTtji-ciG7xpkEUUTjdrNcvuJKBcHD4zAlWJBMCZ6iblT1fLOW6uUH_P2IRIWDC98lQ4vVjh2HmH5i1l3PY3Dx8t9IGYpfsroX85engxBRXB9Q",
    base_url="http://platform.ai.cnpc/kunlun/ingress/api/h3t-eeceff/6ede2fb11ceb481e8c51cffcc40d2517/ai-bad5c916c57346959d84e1b42bd41c5b/service-c0d63a93c4ba4ff5a494a286b99bbb71/v1",
    model="DeepSeekV3quant",  # 此处以qwen-plus为例，您可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    # other params...
)

prompt = ChatPromptTemplate.from_messages(
    [("system", "你是一个世界级的技术专家"), ("user", "{input}")]
)

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

result = chain.invoke({"input": "帮我写一篇关于AI的技术文章, 100个字"})

print(result)
