import json
import random

from langchain_ollama.chat_models import ChatOllama  # 导入 ChatOllama 模型
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # 导入提示模板相关类
from langchain_core.messages import HumanMessage, AIMessage  # 导入人类消息和 AI 消息类
from langchain_core.runnables.history import RunnableWithMessageHistory  # 导入带有消息历史的可运行类

from .session_history import get_session_history  # 导入会话历史相关方法
from utils.logger import LOG  # 导入日志工具

class ConversationAgent:
    """
    对话代理类，负责处理与用户的对话。
    """
    def __init__(self, session_id=None):
        self.name = "conversation"  # 设置代理名称为 "conversation"
        self.session_id = session_id if session_id else self.name  # 如果未提供会话ID，则使用代理名称作为会话ID
        self.prompt_file = "prompts/conversation_prompt.txt"  # 系统提示语文件路径
        self.prompt = self.load_prompt()  # 加载系统提示语

        self.create_chatbot()  # 创建聊天机器人

    def load_prompt(self):
        """
        加载系统提示语。
        """
        try:
            with open(self.prompt_file, "r", encoding="utf-8") as file:
                return file.read().strip()  # 读取文件并去除首尾空格
        except FileNotFoundError:
            raise FileNotFoundError(f"找不到提示文件 {self.prompt_file}!")

    def create_chatbot(self):
        """
        初始化聊天机器人，包含系统提示和消息历史记录。
        """
        # 创建聊天提示模板，包括系统提示和消息占位符
        system_prompt = ChatPromptTemplate.from_messages([
            ("system", self.prompt),  # 系统提示部分
            MessagesPlaceholder(variable_name="messages"),  # 消息占位符
        ])

        # 初始化 ChatOllama 模型，配置参数
        self.chatbot = system_prompt | ChatOllama(
            model="llama3.1:8b-instruct-q8_0",  # 使用的模型名称
            max_tokens=8192,  # 最大生成的 token 数
            temperature=0.8,  # 随机性配置
        )

        # 将聊天机器人与消息历史记录关联
        self.chatbot_with_history = RunnableWithMessageHistory(self.chatbot, get_session_history)


    def start_new_session(self):
        """
        开始一个新的聊天会话，发送初始的 AI 消息。
        """
        # 获取当前会话的历史记录
        history = get_session_history(self.session_id)
        LOG.debug(f"[history]:{history}")

        # 如果历史记录为空，则发送初始 AI 消息
        if not history.messages:
            initial_ai_message = "欢迎！今天有什么我能帮忙的吗？"  # 初始消息
            history.add_message(AIMessage(content=initial_ai_message))  # 将初始消息添加到历史记录
            return initial_ai_message
        else:
            return history.messages[-1].content  # 返回历史记录中的最后一条消息

    def chat_with_history(self, user_input):
        """
        处理用户输入，生成包含聊天历史的回复。
        
        参数:
            user_input (str): 用户输入的消息
        
        返回:
            str: AI 生成的回复
        """
        # 生成回复并考虑消息历史
        response = self.chatbot_with_history.invoke(
            [HumanMessage(content=user_input)],  # 将用户输入封装为 HumanMessage
            {"configurable": {"session_id": self.session_id}},  # 传入配置，包括会话ID
        )
        
        LOG.debug(response)  # 记录调试日志
        return response.content  # 返回生成的回复内容
