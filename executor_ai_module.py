# executor_ai_module.py
from emotional_ai_module import EmotionAI_PathBased_DynamicIntensity_V3 # Import EmotionAI
from mind_ai_module import MindAI_Learning # Import MindAI (though not directly used in function, module is needed for type hinting/structure if desired)


def executor_ai_decision_dynamic_intensity(mind_ai_options, emotion_path, emotion_intensity_levels, mind_ai_learner):
    """
    Executor AI decision making using dynamic intensity and Mind AI learning.
    """
    chosen_option = None
    priority_score = {"Option A": 0, "Option B": 0, "Option C": 0}
    mind_ai_priority = {"Option A": 5, "Option B": 7, "Option C": 3}

    mind_ai_options, mind_ai_priority = mind_ai_learner.analyze_options("Current situation", emotion_path) # Pass emotion_path to MindAI

    for option in ["Option A", "Option B", "Option C"]:
        priority_score[option] += mind_ai_priority[option]

    emotion_override_active = False

    if "[EMOTION_FEAR]" in emotion_path:
        priority_score["Option C"] -= 3

        if emotion_intensity_levels["FEAR"] > 0.5:
            emotion_override_active = True


    if "[EMOTION_JOY]" in emotion_path: # Changed to JOY to match Plutchik
        priority_score["Option B"] += 2


    if emotion_override_active:
        if "[EMOTION_FEAR]" in emotion_path:
            priority_score["Option C"] += 2

    chosen_option = max(priority_score, key=priority_score.get)

    outcome_example = "positive" if chosen_option == "Option B" else "neutral"
    mind_ai_learner.record_decision_outcome(emotion_path, chosen_option, outcome_example)

    return chosen_option, priority_score