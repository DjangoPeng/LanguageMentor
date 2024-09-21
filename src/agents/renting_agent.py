from .base_scenario_agent import ScenarioAgent

class RentingAgent(ScenarioAgent):
    def __init__(self):
        super().__init__()
        self.name = "Renting Agent"

    def respond(self, user_input):
        # 调用与租房相关的对话逻辑
        return f"Renting Agent Response: {user_input}"
