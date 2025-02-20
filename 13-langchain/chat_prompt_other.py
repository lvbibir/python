from langchain.prompts import HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=("你是一个乐于助人的助手, 可以润色内容, 使其看起来更简单易读")
        ),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
)

# 使用 format_messages 方法格式化消息
messages = chat_template.format_messages(text="我不喜欢吃好吃的东西")
# 打印格式化后的消息
print(messages)