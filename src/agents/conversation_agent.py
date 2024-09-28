from langchain_core.messages import AIMessage  # 导入消息类

from .session_history import get_session_history  # 导入会话历史相关方法
from .agent_base import AgentBase
from utils.logger import LOG

class ConversationAgent(AgentBase):
    """
    对话代理类，负责处理与用户的对话。
    """
    def __init__(self, session_id=None):
        super().__init__(
            name="conversation",
            prompt_file="prompts/conversation_prompt.txt",
            session_id=session_id
        )
