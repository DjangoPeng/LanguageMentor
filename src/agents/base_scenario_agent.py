class ScenarioAgent:
    def __init__(self):
        self.name = "Scenario Agent"

    def respond(self, user_input):
        raise NotImplementedError("Subclasses should implement this method!")
