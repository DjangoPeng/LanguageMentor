from .base_scenario_agent import ScenarioAgent

class JobInterviewAgent(ScenarioAgent):
    def __init__(self):
        super().__init__()
        self.name = "Job Interview Agent"

    def respond(self, user_input):
        # 调用与求职面试相关的对话逻辑
        return f"Job Interview Agent Response: {user_input}"
