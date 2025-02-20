from langchain_core.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate.from_messages(
    {
        ("system", "你是一个人工智能助手, 你的名字是{name}"),
        ("human", "你好"),
        ("ai", "我很好, 谢谢!"),
        ("human", "{user_input}"),
    }
)

messages = chat_template.format_messages(name="Bob", user_input="你的名字叫什么?")
print(messages)
