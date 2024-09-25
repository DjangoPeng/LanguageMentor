import json
import random

from langchain_ollama.chat_models import ChatOllama  # 导入 ChatOllama 模型
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # 导入提示模板相关类
from langchain_core.messages import HumanMessage, AIMessage  # 导入人类消息类和AI消息类
from langchain_core.runnables.history import RunnableWithMessageHistory  # 导入带有消息历史的可运行类

from .session_history import get_session_history  # 导入会话历史相关方法
from utils.logger import LOG

class ScenarioAgent:
    def __init__(self, scenario_name):
        self.name = scenario_name
        self.prompt_file = f"prompts/{self.name}_prompt.txt"
        self.intro_file = f"content/intro/{self.name}.json"
        self.prompt = self.load_prompt()
        self.intro_messages = self.load_intro()

        self.create_chatbot()

    
    def load_prompt(self):
        try:
            with open(self.prompt_file, "r", encoding="utf-8") as file:
                return file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file {self.prompt_file} not found!")

    def load_intro(self):
        try:
            with open(self.intro_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Intro file {self.intro_file} not found!")
        except json.JSONDecodeError:
            raise ValueError(f"Intro file {self.intro_file} contains invalid JSON!")


    def create_chatbot(self):
            # 创建聊天提示模板，包括系统提示和消息占位符
            system_prompt = ChatPromptTemplate.from_messages([
                ("system", self.prompt),  # 系统提示部分
                MessagesPlaceholder(variable_name="messages"),  # 消息占位符
            ])

            # 初始化 ChatOllama 模型，配置模型参数
            self.chatbot = system_prompt | ChatOllama(
                model="llama3.1:8b-instruct-q8_0",  # 使用的模型名称
                max_tokens=8192,  # 最大生成的token数
                temperature=0.8,  # 生成文本的随机性
            )

            # 将聊天机器人与消息历史记录关联起来
            self.chatbot_with_history = RunnableWithMessageHistory(self.chatbot, get_session_history)

    def start_new_session(self, session_id: str = None):
        """
        开始一个新的聊天会话，并发送初始AI消息。
        
        参数:
            session_id (str): 会话的唯一标识符
        """
        if session_id is None:
            session_id = self.name

        history = get_session_history(session_id)
        LOG.debug(f"[history]:{history}")

        if not history.messages:  # 检查历史记录是否为空
            initial_ai_message = random.choice(self.intro_messages)  # 随机选择初始AI消息
            history.add_message(AIMessage(content=initial_ai_message))  # 添加初始AI消息到历史记录
            return initial_ai_message
        else:
            return history.messages[-1].content  # 返回历史记录中的最后一条消息


    def chat_with_history(self, user_input, session_id: str = None):
        """
        处理用户输入并生成包含聊天历史的回复，同时记录日志。
        
        参数:
            user_input (str): 用户输入的消息
            session_id (str): 会话的唯一标识符
        
        返回:
            str: 代理生成的回复内容
        """
        # TODO: InMemoryStore -> DB
        if session_id is None:
            session_id = self.name

        response = self.chatbot_with_history.invoke(
            [HumanMessage(content=user_input)],  # 将用户输入封装为 HumanMessage
            {"configurable": {"session_id": session_id}},  # 传入配置，包括会话ID
        )
        
        return response.content  # 返回生成的回复内容
