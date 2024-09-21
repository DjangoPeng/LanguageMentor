from .base_scenario_agent import ScenarioAgent

class HotelCheckInAgent(ScenarioAgent):
    def __init__(self):
        super().__init__()
        self.name = "Hotel Check-in Agent"

    def respond(self, user_input):
        # 调用与酒店入住相关的对话逻辑
        return f"Hotel Check-in Agent Response: {user_input}"
