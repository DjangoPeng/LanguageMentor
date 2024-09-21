from .base_scenario_agent import ScenarioAgent

class SalaryNegotiationAgent(ScenarioAgent):
    def __init__(self):
        super().__init__()
        self.name = "Salary Negotiation Agent"

    def respond(self, user_input):
        # 调用与薪资谈判相关的对话逻辑
        return f"Salary Negotiation Agent Response: {user_input}"
