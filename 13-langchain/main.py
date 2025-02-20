from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import os

llm = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-max",  # 此处以qwen-plus为例，您可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    # other params...
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个世界级的技术专家"),
    ("user", "{input}")
]
)

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

result = chain.invoke({"input": "帮我写一篇关于AI的技术文章, 100个字"})

print(result)