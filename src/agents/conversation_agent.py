
from langchain_ollama.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage


class ConversationAgent:
    def __init__(self):
        self.name = "Conversation Agent"
        with open("prompts/conversation_prompt.txt", "r", encoding="utf-8") as file:
            self.system_prompt = file.read().strip()

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ])

        self.chatbot = self.prompt | ChatOllama(
            model="llama3.1:8b-instruct-q8_0",
            max_tokens=8192,
            temperature=1.2,
        )

    def respond(self, user_input):
        message = self.chatbot.invoke({"messages": [HumanMessage(content=user_input)]})
        return message.content