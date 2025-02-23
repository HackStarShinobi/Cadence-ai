# main_ai_system.py
from emotional_ai_module import EmotionAI_PathBased_DynamicIntensity_V3
from mind_ai_module import MindAI_Learning
from executor_ai_module import executor_ai_decision_dynamic_intensity
import time

def main():
    """
    Main function to run the integrated AI system with Emotion AI, Mind AI, and Executor AI.
    """
    # Initialize Emotion AI, Mind AI
    emotion_ai = EmotionAI_PathBased_DynamicIntensity_V3()
    mind_ai_learner = MindAI_Learning()

    # Example interaction loop
    print("Starting AI System Interaction...")
    user_input_history = []

    while True:
        user_input = input("User: ")
        user_input_history.append(user_input) # Keep history

        # 1. Emotion AI processes input and generates emotion path
        emotion_path = emotion_ai.generate_emotion_path(user_input)
        emotion_intensity_levels = emotion_ai.get_emotion_intensity() # Get current intensities

        print("Emotion Path:", emotion_path) # Output emotion path for this turn
        print("Current Emotion Intensities:", emotion_intensity_levels) # Output current emotion intensities


        # 2. Mind AI analyzes options (example options) - can be more complex in real application
        mind_ai_options = ["Provide a helpful response", "Ask clarifying questions", "Offer a concise answer"] # Example options relevant to user interaction

        # 3. Executor AI makes decision based on emotions and Mind AI
        chosen_option, decision_scores = executor_ai_decision_dynamic_intensity(
            mind_ai_options, emotion_path, emotion_intensity_levels, mind_ai_learner
        )

        print("Decision Scores:", decision_scores) # Output decision scores
        print("Chosen Option:", chosen_option) # Output chosen option

        # 4. Simulate AI response (replace with actual response generation logic in real system)
        if chosen_option == "Provide a helpful response":
            ai_response = "I will do my best to provide a helpful and detailed response."
        elif chosen_option == "Ask clarifying questions":
            ai_response = "To best assist you, could you please provide more details about your request?"
        elif chosen_option == "Offer a concise answer":
            ai_response = "Understood. I will provide a concise answer to your question."
        else:
            ai_response = "I am processing your request..." # Default fallback

        print(f"AI Response: {ai_response}")

        # 5. Emotion intensity decay over time (simulating emotional dynamics)
        emotion_ai.update_emotion_intensity()


        if user_input.lower() == "exit":
            print("Ending interaction.")
            break
        print("\n")
        time.sleep(0.5) # Pause for readability


if __name__ == "__main__":
    main()