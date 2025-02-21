import os
import sys
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 获取当前 python 所在的文件夹的绝对路径
# 如果是 python 解释器, PWD 为 py 文件的目录名
# 如果是二进制程序, PWD 为 二进制程序的目录名
if getattr(sys, "frozen", False):
    PWD = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    PWD = os.path.dirname(os.path.abspath(__file__))

docs = []
# 修改文件路径拼接，确保路径正确
file = os.path.join(PWD, "rule.txt")
with open(file, "wb") as f:
    f.write(file.getvalue())

loader = TextLoader(file, encoding="utf-8")
docs.extend(loader.load())

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
print(splits)
