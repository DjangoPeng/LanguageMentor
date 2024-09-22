import gradio as gr
from agents.conversation_agent import ConversationAgent
from agents.job_interview_agent import JobInterviewAgent
from agents.hotel_checkin_agent import HotelCheckInAgent
from agents.salary_negotiation_agent import SalaryNegotiationAgent
from agents.renting_agent import RentingAgent
from utils.logger import LOG

# 实现对话 Agent 和场景 Agent 的选择与调用
conversation_agent = ConversationAgent()
job_interview_agent = JobInterviewAgent()
hotel_checkin_agent = HotelCheckInAgent()
salary_negotiation_agent = SalaryNegotiationAgent()
renting_agent = RentingAgent()


# 对话 Agent 处理函数
def handle_conversation(user_input, chat_history):
    LOG.debug(f"[聊天记录]: {chat_history}")
    # bot_message = conversation_agent.chat(user_input)
    bot_message = conversation_agent.chat_with_history(user_input)
    LOG.info(f"[ChatBot]: {bot_message}")
    return bot_message



# 场景 Agent 处理函数，根据选择的场景调用相应的 Agent
def handle_scenario(user_input, history, scenario):
    agents = {
        "求职面试": job_interview_agent,
        "酒店入住": hotel_checkin_agent,
        "薪资谈判": salary_negotiation_agent,
        "租房": renting_agent
    }
    return agents[scenario].respond(user_input)

# Gradio 界面
with gr.Blocks(title="LanguageMentor 英语私教") as language_mentor_app:
    with gr.Tab("对话练习"):
        gr.Markdown("## 练习英语对话 ")
        conversation_chatbot = gr.Chatbot(
            placeholder="<strong>你的英语私教 DjangoPeng</strong><br><br>想和我聊什么话题都可以，记得用英语哦！",
            height=800,
        )

        gr.ChatInterface(
            fn=handle_conversation, 
            chatbot=conversation_chatbot,
            retry_btn=None,
            undo_btn=None,
            clear_btn="清除历史记录",
            submit_btn="发送",
        )

    with gr.Tab("场景训练"):
        gr.Markdown("## 选择一个场景学习并完成任务")
        scenario_dropdown = gr.Dropdown(choices=["求职面试", "酒店入住", "薪资谈判", "租房"], label="选择场景")
        scenario_chatbot = gr.Chatbot(
            placeholder="<strong>你的英语私教 DjangoPeng</strong><br><br>选择场景后开始对话吧！",
            height=800,
        )
        
        # 场景聊天界面
        gr.ChatInterface(
            fn=handle_scenario,
            chatbot=scenario_chatbot,
            additional_inputs=scenario_dropdown,
            retry_btn=None,
            undo_btn=None,
            clear_btn="清除历史记录",
            submit_btn="发送",
        )

if __name__ == "__main__":
    language_mentor_app.launch(share=True, server_name="0.0.0.0")

