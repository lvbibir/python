from langchain_community.embeddings import HuggingFaceBgeEmbeddings

# 定义模型名称和参数
model_name = "BAAI/bge-m3"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}

# 初始化嵌入模型
hf = HuggingFaceBgeEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)

# 嵌入示例文本
embedding = hf.embed_query("hi this is harrison")
print(len(embedding))  # 输出嵌入向量的长度
