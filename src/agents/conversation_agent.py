# 导入所需的模块和类
from langchain_ollama.chat_models import ChatOllama  # 导入 ChatOllama 模型
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # 导入提示模板相关类
from langchain_core.messages import HumanMessage  # 导入人类消息类
from utils.logger import LOG  # 导入日志工具

from langchain_core.chat_history import (
    BaseChatMessageHistory,  # 基础聊天消息历史类
    InMemoryChatMessageHistory,  # 内存中的聊天消息历史类
)
from langchain_core.runnables.history import RunnableWithMessageHistory  # 导入带有消息历史的可运行类

# 用于存储会话历史的字典
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """
    获取指定会话ID的聊天历史。如果该会话ID不存在，则创建一个新的聊天历史实例。
    
    参数:
        session_id (str): 会话的唯一标识符
    
    返回:
        BaseChatMessageHistory: 对应会话的聊天历史对象
    """
    if session_id not in store:
        # 如果会话ID不存在于存储中，创建一个新的内存聊天历史实例
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

class ConversationAgent:
    """
    对话代理类，负责处理与用户的对话。
    """
    def __init__(self):
        self.name = "Conversation Agent"  # 代理名称
        
        # 读取系统提示语，从文件中加载
        with open("prompts/conversation_prompt.txt", "r", encoding="utf-8") as file:
            self.system_prompt = file.read().strip()

        # 创建聊天提示模板，包括系统提示和消息占位符
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),  # 系统提示部分
            MessagesPlaceholder(variable_name="messages"),  # 消息占位符
        ])

        # 初始化 ChatOllama 模型，配置模型参数
        self.chatbot = self.prompt | ChatOllama(
            model="llama3.1:8b-instruct-q8_0",  # 使用的模型名称
            max_tokens=8192,  # 最大生成的token数
            temperature=0.8,  # 生成文本的随机性
        )

        # 将聊天机器人与消息历史记录关联起来
        self.chatbot_with_history = RunnableWithMessageHistory(self.chatbot, get_session_history)

        # 配置字典，包含会话ID等可配置参数
        self.config = {"configurable": {"session_id": "abc123"}}

    def chat(self, user_input):
        """
        处理用户输入并生成回复。
        
        参数:
            user_input (str): 用户输入的消息
        
        返回:
            str: 代理生成的回复内容
        """
        response = self.chatbot.invoke(
            [HumanMessage(content=user_input)],  # 将用户输入封装为 HumanMessage
        )  
        return response.content  # 返回生成的回复内容

    def chat_with_history(self, user_input):
        """
        处理用户输入并生成包含聊天历史的回复，同时记录日志。
        
        参数:
            user_input (str): 用户输入的消息
        
        返回:
            str: 代理生成的回复内容
        """
        response = self.chatbot_with_history.invoke(
            [HumanMessage(content=user_input)],  # 将用户输入封装为 HumanMessage
            self.config,  # 传入配置，包括会话ID
        )
        LOG.debug(response)  # 记录调试日志
        return response.content  # 返回生成的回复内容
