# mind_ai_module.py
import time

class MindAI_Learning:
    """
    Mind AI module with basic learning capabilities.
    """
    def __init__(self):
        self.decision_history = []
        self.learning_rate = 0.1

    def analyze_options(self, stimulus_text, emotion_path_from_executor): # Added emotion_path input for context
        """Analyzes options with basic learning adjustment."""
        options = ["Option A", "Option B", "Option C"]
        base_priority = {"Option A": 5, "Option B": 7, "Option C": 3}

        if "[EMOTION_FEAR]" in emotion_path_from_executor:
            for history_item in self.decision_history:
                if "[EMOTION_FEAR]" in history_item["emotion_path"] and history_item["chosen_option"] == "Option C" and history_item["outcome"] == "negative":
                    base_priority["Option C"] -= self.learning_rate * 2

        return options, base_priority

    def record_decision_outcome(self, emotion_path, chosen_option, outcome):
        """Records decision and outcome for learning."""
        self.decision_history.append({
            "emotion_path": emotion_path,
            "chosen_option": chosen_option,
            "outcome": outcome,
            "timestamp": time.time()
        })