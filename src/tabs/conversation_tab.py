# tabs/conversation_tab.py

import gradio as gr
from agents.conversation_agent import ConversationAgent
from utils.logger import LOG

# 初始化对话代理
conversation_agent = ConversationAgent()

def handle_conversation(user_input, chat_history):
    bot_message = conversation_agent.chat_with_history(user_input)
    LOG.info(f"[Conversation ChatBot]: {bot_message}")
    return bot_message

def create_conversation_tab():
    with gr.Tab("对话"):
        gr.Markdown("## 练习英语对话 ")  # 对话练习说明
        conversation_chatbot = gr.Chatbot(
            placeholder="<strong>你的英语私教 DjangoPeng</strong><br><br>想和我聊什么话题都可以，记得用英语哦！",  # 聊天机器人的占位符
            height=800,  # 聊天窗口高度
        )

        # 处理用户对话的函数
        def handle_conversation(user_input, chat_history):
            bot_message = conversation_agent.chat_with_history(user_input)  # 获取聊天机器人的回复
            LOG.info(f"[ChatBot]: {bot_message}")  # 记录聊天机器人的回复
            return bot_message  # 返回机器人的回复


        gr.ChatInterface(
            fn=handle_conversation,  # 处理对话的函数
            chatbot=conversation_chatbot,  # 聊天机器人组件
            retry_btn=None,  # 不显示重试按钮
            undo_btn=None,  # 不显示撤销按钮
            clear_btn="清除历史记录",  # 清除历史记录按钮文本
            submit_btn="发送",  # 发送按钮文本
        )