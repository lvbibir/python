import os
from openai import OpenAI
import chromadb
from chromadb.config import Settings

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # 从环境变量中获取 API Key
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 通义千问的 base_url
)

# 初始化 Chroma 客户端
chroma_client = chromadb.Client(
    Settings(
        persist_directory="/home/lvbibir/python/13-langchain/chroma_db",  # 向量数据库存储路径
    )
)

# 创建或加载集合（Collection）
collection = chroma_client.get_or_create_collection(name="text_embeddings")


# 生成文本的向量表示
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-v3", input=text, encoding_format="float"
    )
    return response.data[0].embedding


# 将文本和向量存储到 Chroma 数据库
def store_text_to_chroma(text):
    # 生成向量
    embedding = get_embedding(text)

    # 将文本和向量存储到 Chroma
    collection.add(
        documents=[text],  # 文本内容
        embeddings=[embedding],  # 向量表示
        ids=["unique_id_1"],  # 唯一标识符
    )
    print(f"文本已存储到 Chroma 数据库: {text}")


# 示例文本
text = "衣服的质量杠杠的，很漂亮，不枉我等了这么久啊，喜欢，以后还来这里买"

# 存储文本到 Chroma
store_text_to_chroma(text)


# 查询 Chroma 数据库
def query_chroma(query_text, top_k=1):
    # 生成查询文本的向量
    query_embedding = get_embedding(query_text)

    # 查询最相似的文本
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results


# 示例查询
query_text = "我是谁"
results = query_chroma(query_text)
print("查询结果:", results)
