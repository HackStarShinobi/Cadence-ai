# emotional_ai_module.py
import time

class EmotionAI_PathBased_DynamicIntensity_V3:
    """
    Emotion AI module using path-based emotion generation and dynamic intensity.
    Version 3: Intensity decay and appraisal intensity multipliers added.
    """
    def __init__(self, intensity_decay_rates=None, appraisal_intensity_multiplier=1.2):
        # Core emotion categories (Plutchik's Wheel)
        self.emotion_categories = ["JOY", "SADNESS", "ANGER", "FEAR", "TRUST", "DISGUST", "ANTICIPATION", "SURPRISE"]
        self.emotion_intensity_levels = {emotion: 0.0 for emotion in self.emotion_categories}
        self.intensity_decay_rates = intensity_decay_rates if intensity_decay_rates else {emotion: 0.01 for emotion in self.emotion_categories} # Default decay rate
        self.appraisal_intensity_multiplier = appraisal_intensity_multiplier # Multiplier for appraisal intensity

        # Emotion pathways - simplified examples, can be expanded
        self.emotion_pathways = {
            "positive_stimulus": {
                "valence": "[APPRAISAL_VALENCE_POSITIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_GOAL]",
                "physiological": "[PHYSIO_AROUSAL_LOW]",
                "expression": "[EXPR_SMILE]",
                "emotion": "[EMOTION_JOY]",
                "intensity": "[INTENSITY_MEDIUM]"
            },
            "negative_stimulus_threat": {
                "valence": "[APPRAISAL_VALENCE_NEGATIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_THREAT]",
                "physiological": "[PHYSIO_AROUSAL_HIGH]",
                "expression": "[EXPR_FROWN]",
                "emotion": "[EMOTION_FEAR]",
                "intensity": "[INTENSITY_HIGH]"
            },
             "social_positive_feedback": {
                "valence": "[APPRAISAL_VALENCE_POSITIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_SOCIAL]",
                "physiological": "[PHYSIO_AROUSAL_LOW]",
                "expression": "[EXPR_SMILE_NOD]",
                "emotion": "[EMOTION_TRUST]", # Or JOY, depending on nuance
                "intensity": "[INTENSITY_MEDIUM]"
            },
            "social_negative_feedback": {
                "valence": "[APPRAISAL_VALENCE_NEGATIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_SOCIAL]",
                "physiological": "[PHYSIO_AROUSAL_MEDIUM]",
                "expression": "[EXPR_FROWN_SHAKE_HEAD]",
                "emotion": "[EMOTION_SADNESS]", # Or ANGER/FEAR depending on context
                "intensity": "[INTENSITY_MEDIUM]"
            },
            "neutral_stimulus": {
                "valence": "[APPRAISAL_VALENCE_NEUTRAL]",
                "relevance": "[APPRAISAL_RELEVANCE_NONE]",
                "physiological": "[PHYSIO_AROUSAL_NONE]",
                "expression": "[EXPR_NEUTRAL]",
                "emotion": "[EMOTION_NONE]",
                "intensity": "[INTENSITY_NONE]"
            },
            "intellectual_stimulus": { # Stimulus that is thought-provoking
                "valence": "[APPRAISAL_VALENCE_NEUTRAL]", # Could be positive if curious, negative if confusing
                "relevance": "[APPRAISAL_RELEVANCE_COGNITIVE]",
                "physiological": "[PHYSIO_AROUSAL_LOW]", # Or medium if very engaging
                "expression": "[EXPR_THINKING]",
                "emotion": "[EMOTION_ANTICIPATION]", # Or SURPRISE/INTEREST
                "intensity": "[INTENSITY_LOW]" # Or medium
            },
            "aesthetic_positive": { # e.g., beautiful music, art
                "valence": "[APPRAISAL_VALENCE_POSITIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_AESTHETIC]",
                "physiological": "[PHYSIO_AROUSAL_MEDIUM]", # Or low, depending on intensity
                "expression": "[EXPR_APPRECIATION]",
                "emotion": "[EMOTION_JOY]", # Or TRUST, SURPRISE, depending on art form
                "intensity": "[INTENSITY_MEDIUM]"
            },
            "moral_violation": { # e.g., witnessing injustice
                "valence": "[APPRAISAL_VALENCE_NEGATIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_MORAL]",
                "physiological": "[PHYSIO_AROUSAL_HIGH]",
                "expression": "[EXPR_ANGER_FROWN]",
                "emotion": "[EMOTION_ANGER]", # Or DISGUST, SADNESS
                "intensity": "[INTENSITY_HIGH]"
            },
             "stimulus_fear": { # Explicit fear stimulus
                "valence": "[APPRAISAL_VALENCE_NEGATIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_THREAT]",
                "physiological": "[PHYSIO_AROUSAL_VERY_HIGH]",
                "expression": "[EXPR_EYES_WIDEN_MOUTH_OPEN]",
                "emotion": "[EMOTION_FEAR]",
                "intensity": "[INTENSITY_VERY_HIGH]"
            },
            "stimulus_sadness": { # Explicit sadness stimulus
                "valence": "[APPRAISAL_VALENCE_NEGATIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_LOSS]",
                "physiological": "[PHYSIO_AROUSAL_LOW]",
                "expression": "[EXPR_SAD_FACE]",
                "emotion": "[EMOTION_SADNESS]",
                "intensity": "[INTENSITY_MEDIUM]"
            },
             "stimulus_joy": { # Explicit joy stimulus
                "valence": "[APPRAISAL_VALENCE_POSITIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_GOAL_ACHIEVED]",
                "physiological": "[PHYSIO_AROUSAL_MEDIUM]",
                "expression": "[EXPR_WIDE_SMILE_LAUGH]",
                "emotion": "[EMOTION_JOY]",
                "intensity": "[INTENSITY_HIGH]"
            },
             "stimulus_anger": { # Explicit anger stimulus - provocation
                "valence": "[APPRAISAL_VALENCE_NEGATIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_OFFENSIVE_AGENT]",
                "physiological": "[PHYSIO_AROUSAL_HIGH]",
                "expression": "[EXPR_FROWN_CLENCHED_JAW]",
                "emotion": "[EMOTION_ANGER]",
                "intensity": "[INTENSITY_HIGH]"
            },
            "stimulus_disgust": { # Explicit disgust stimulus - something offensive
                "valence": "[APPRAISAL_VALENCE_NEGATIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_OFFENSIVE_OBJECT]",
                "physiological": "[PHYSIO_AROUSAL_MEDIUM]", # or low, depending on disgust type
                "expression": "[EXPR_NOSE_WRINKLE_LIP_CURL]",
                "emotion": "[EMOTION_DISGUST]",
                "intensity": "[INTENSITY_MEDIUM]"
            },
             "stimulus_surprise": { # Explicit surprise stimulus - unexpected event
                "valence": "[APPRAISAL_VALENCE_NEUTRAL]", # Surprise itself is valence neutral
                "relevance": "[APPRAISAL_RELEVANCE_UNEXPECTED_EVENT]",
                "physiological": "[PHYSIO_AROUSAL_MEDIUM_HIGH]", # Surprise can be arousing
                "expression": "[EXPR_EYEBROWS_RAISED_MOUTH_OPEN_SIGHTLY]",
                "emotion": "[EMOTION_SURPRISE]",
                "intensity": "[INTENSITY_MEDIUM]"
            },
             "stimulus_trust": { # Explicit trust/bond stimulus - positive social connection
                "valence": "[APPRAISAL_VALENCE_POSITIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_SOCIAL_BOND]",
                "physiological": "[PHYSIO_AROUSAL_LOW]",
                "expression": "[EXPR_WARM_SMILE_EYE_CONTACT]",
                "emotion": "[EMOTION_TRUST]",
                "intensity": "[INTENSITY_MEDIUM]"
            },
            "stimulus_anticipation": { # Explicit anticipation stimulus - upcoming event
                "valence": "[APPRAISAL_VALENCE_NEUTRAL]", # Anticipation can be positive or negative leaning
                "relevance": "[APPRAISAL_RELEVANCE_FUTURE_EVENT]",
                "physiological": "[PHYSIO_AROUSAL_MEDIUM]", # Arousal depends on what is anticipated
                "expression": "[EXPR_ATTENTIVE_LOOK]",
                "emotion": "[EMOTION_ANTICIPATION]",
                "intensity": "[INTENSITY_MEDIUM]"
            },
            "stimulus_sad_news": {
                "valence": "[APPRAISAL_VALENCE_NEGATIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_LOSS]",
                "physiological": "[PHYSIO_AROUSAL_LOW]",
                "expression": "[EXPR_SAD_FACE_TEARS]",
                "emotion": "[EMOTION_SADNESS]",
                "intensity": "[INTENSITY_HIGH]"
            },
            "stimulus_good_news": {
                "valence": "[APPRAISAL_VALENCE_POSITIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_GOAL_ACHIEVED]",
                "physiological": "[PHYSIO_AROUSAL_MEDIUM]",
                "expression": "[EXPR_BRIGHT_SMILE_EXCITED]",
                "emotion": "[EMOTION_JOY]",
                "intensity": "[INTENSITY_HIGH]"
            },
            "stimulus_threat_imminent": {
                "valence": "[APPRAISAL_VALENCE_NEGATIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_IMMINENT_DANGER]",
                "physiological": "[PHYSIO_AROUSAL_VERY_HIGH]",
                "expression": "[EXPR_PANICKED_LOOK]",
                "emotion": "[EMOTION_FEAR]",
                "intensity": "[INTENSITY_VERY_HIGH]"
            },
            "stimulus_insult": {
                "valence": "[APPRAISAL_VALENCE_NEGATIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_SOCIAL_OFFENSE]",
                "physiological": "[PHYSIO_AROUSAL_MEDIUM_HIGH]",
                "expression": "[EXPR_FROWN_GLARE]",
                "emotion": "[EMOTION_ANGER]",
                "intensity": "[INTENSITY_MEDIUM_HIGH]"
            },
             "stimulus_social_praise": {
                "valence": "[APPRAISAL_VALENCE_POSITIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_SOCIAL_APPROVAL]",
                "physiological": "[PHYSIO_AROUSAL_LOW]",
                "expression": "[EXPR_SMILE_NOD_APPROVINGLY]",
                "emotion": "[EMOTION_JOY]", # or TRUST, PRIDE
                "intensity": "[INTENSITY_MEDIUM]"
            },
            "stimulus_social_rejection": {
                "valence": "[APPRAISAL_VALENCE_NEGATIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_SOCIAL_DISAPPROVAL]",
                "physiological": "[PHYSIO_AROUSAL_MEDIUM]",
                "expression": "[EXPR_SAD_FACE_AVOID_EYE_CONTACT]",
                "emotion": "[EMOTION_SADNESS]", # or ANGER, FEAR depending on context
                "intensity": "[INTENSITY_MEDIUM]"
            },
             "stimulus_unfairness": {
                "valence": "[APPRAISAL_VALENCE_NEGATIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_MORAL_VIOLATION]", # Unfairness is a moral violation
                "physiological": "[PHYSIO_AROUSAL_MEDIUM_HIGH]",
                "expression": "[EXPR_FROWN_DISAPPROVAL]",
                "emotion": "[EMOTION_ANGER]", # or DISGUST
                "intensity": "[INTENSITY_MEDIUM_HIGH]"
            },
             "stimulus_betrayal": {
                "valence": "[APPRAISAL_VALENCE_NEGATIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_SOCIAL_BETRAYAL]",
                "physiological": "[PHYSIO_AROUSAL_HIGH]",
                "expression": "[EXPR_SAD_ANGER_MIXED]", # Complex expression
                "emotion": "[EMOTION_ANGER]", # or SADNESS, TRUST broken
                "intensity": "[INTENSITY_HIGH]"
            },
             "stimulus_disappointment": {
                "valence": "[APPRAISAL_VALENCE_NEGATIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_UNMET_EXPECTATION]",
                "physiological": "[PHYSIO_AROUSAL_LOW]",
                "expression": "[EXPR_SAD_FACE_SLIGHT]",
                "emotion": "[EMOTION_SADNESS]", # or ANGER if expectation violated by agent
                "intensity": "[INTENSITY_LOW]"
            },
             "stimulus_challenge": {
                "valence": "[APPRAISAL_VALENCE_NEUTRAL]", # Challenge can be positive or negative depending on framing
                "relevance": "[APPRAISAL_RELEVANCE_TASK_DIFFICULTY]",
                "physiological": "[PHYSIO_AROUSAL_MEDIUM]", # Arousal for focus/effort
                "expression": "[EXPR_CONCENTRATION]",
                "emotion": "[EMOTION_ANTICIPATION]", # or SURPRISE, depending on nature of challenge
                "intensity": "[INTENSITY_MEDIUM]"
            },
             "stimulus_confusion": {
                "valence": "[APPRAISAL_VALENCE_NEGATIVE]", # Confusion is often negatively valenced
                "relevance": "[APPRAISAL_RELEVANCE_UNCERTAINTY]",
                "physiological": "[PHYSIO_AROUSAL_LOW_MEDIUM]", # Mild arousal, cognitive effort
                "expression": "[EXPR_CONFUSED_LOOK]",
                "emotion": "[EMOTION_FEAR]", # or SURPRISE, depending on context of confusion
                "intensity": "[INTENSITY_LOW]"
            },
             "stimulus_boredom": {
                "valence": "[APPRAISAL_VALENCE_NEGATIVE]", # Boredom is negative valence
                "relevance": "[APPRAISAL_RELEVANCE_LACK_OF_STIMULATION]",
                "physiological": "[PHYSIO_AROUSAL_VERY_LOW]", # Low arousal
                "expression": "[EXPR_LISTLESS_LOOK_YAWN]",
                "emotion": "[EMOTION_DISGUST]", # or SADNESS, ANGER (at situation)
                "intensity": "[INTENSITY_LOW]"
            },
            "stimulus_overload": {
                "valence": "[APPRAISAL_VALENCE_NEGATIVE]", # Overload is negative
                "relevance": "[APPRAISAL_RELEVANCE_PROCESSING_LIMIT_EXCEEDED]",
                "physiological": "[PHYSIO_AROUSAL_HIGH]", # High arousal, stress response
                "expression": "[EXPR_STRESSED_LOOK]",
                "emotion": "[EMOTION_FEAR]", # or ANGER, SADNESS
                "intensity": "[INTENSITY_HIGH]"
            },
             "stimulus_frustration": {
                "valence": "[APPRAISAL_VALENCE_NEGATIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_GOAL_BLOCKAGE]", # Goal is blocked
                "physiological": "[PHYSIO_AROUSAL_MEDIUM_HIGH]", # Arousal from blocked goal
                "expression": "[EXPR_FROWN_CLENCHED_FIST]",
                "emotion": "[EMOTION_ANGER]", # or SADNESS, depending on type of blockage
                "intensity": "[INTENSITY_MEDIUM_HIGH]"
            },
             "stimulus_social_connection": {
                "valence": "[APPRAISAL_VALENCE_POSITIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_SOCIAL_BONDING]",
                "physiological": "[PHYSIO_AROUSAL_LOW]",
                "expression": "[EXPR_WARM_SMILE_RELAXED]",
                "emotion": "[EMOTION_TRUST]", # or JOY, LOVE
                "intensity": "[INTENSITY_MEDIUM]"
            },
             "stimulus_achievement": {
                "valence": "[APPRAISAL_VALENCE_POSITIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_GOAL_ACHIEVED]",
                "physiological": "[PHYSIO_AROUSAL_MEDIUM]",
                "expression": "[EXPR_PROUD_SMILE]",
                "emotion": "[EMOTION_JOY]", # or PRIDE, TRUST in self
                "intensity": "[INTENSITY_MEDIUM]"
            },
             "stimulus_curiosity": {
                "valence": "[APPRAISAL_VALENCE_NEUTRAL]", # Curiosity itself neutral, can be positive or negative context
                "relevance": "[APPRAISAL_RELEVANCE_NEW_INFORMATION]",
                "physiological": "[PHYSIO_AROUSAL_MEDIUM]", # Arousal for attention, exploration
                "expression": "[EXPR_INTERESTED_LOOK]",
                "emotion": "[EMOTION_ANTICIPATION]", # or SURPRISE, depending on what is discovered
                "intensity": "[INTENSITY_MEDIUM]"
            },
             "stimulus_humor": {
                "valence": "[APPRAISAL_VALENCE_POSITIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_FUNNY]",
                "physiological": "[PHYSIO_AROUSAL_MEDIUM]", # Arousal from laughter, amusement
                "expression": "[EXPR_SMILE_LAUGH]",
                "emotion": "[EMOTION_JOY]", # or SURPRISE, if humor is unexpected
                "intensity": "[INTENSITY_MEDIUM]"
            },
             "stimulus_challenge_met": {
                "valence": "[APPRAISAL_VALENCE_POSITIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_TASK_COMPLETED]", # Overcoming challenge
                "physiological": "[PHYSIO_AROUSAL_LOW_MEDIUM]", # Arousal subsides after challenge met
                "expression": "[EXPR_SATISFIED_SMILE]",
                "emotion": "[EMOTION_JOY]", # or PRIDE, RELIEF
                "intensity": "[INTENSITY_MEDIUM]"
            },
             "stimulus_social_cue": { # Generic social cue, e.g., greeting, positive tone
                "valence": "[APPRAISAL_VALENCE_POSITIVE]", # Social cues often positive unless negative tone
                "relevance": "[APPRAISAL_RELEVANCE_SOCIAL_INTERACTION]",
                "physiological": "[PHYSIO_AROUSAL_LOW]", # Social interaction baseline arousal
                "expression": "[EXPR_NEUTRAL_NOD]", # Or smile if positive cue
                "emotion": "[EMOTION_TRUST]", # Baseline social trust
                "intensity": "[INTENSITY_LOW]"
            },
            "stimulus_reassurance": {
                "valence": "[APPRAISAL_VALENCE_POSITIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_THREAT_REMOVED]", # Reassurance removes threat
                "physiological": "[PHYSIO_AROUSAL_LOWERED]", # Arousal decreases
                "expression": "[EXPR_RELIEF_SMILE]",
                "emotion": "[EMOTION_JOY]", # or TRUST, RELIEF
                "intensity": "[INTENSITY_MEDIUM]"
            },
             "stimulus_comfort": {
                "valence": "[APPRAISAL_VALENCE_POSITIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_WELLBEING]", # Comfort related to wellbeing
                "physiological": "[PHYSIO_AROUSAL_VERY_LOW]", # Very low arousal, relaxation
                "expression": "[EXPR_RELAXED_SMILE]",
                "emotion": "[EMOTION_JOY]", # or TRUST, CONTENTMENT
                "intensity": "[INTENSITY_LOW]"
            },
             "stimulus_gratitude": {
                "valence": "[APPRAISAL_VALENCE_POSITIVE]",
                "relevance": "[APPRAISAL_RELEVANCE_BENEFIT_RECEIVED]", # Gratitude for benefit
                "physiological": "[PHYSIO_AROUSAL_LOW]", # Low arousal, warm feeling
                "expression": "[EXPR_GRATEFUL_SMILE]",
                "emotion": "[EMOTION_TRUST]", # or JOY, LOVE, depending on depth of gratitude
                "intensity": "[INTENSITY_MEDIUM]"
            },
        }


    def generate_emotion_path(self, stimulus_text):
        """
        Generates an emotion path based on keywords in the stimulus text and updates emotion intensities.
        """
        stimulus_text_lower = stimulus_text.lower()
        emotion_path = []

        # Appraisal - Simplified keyword-based appraisal for demonstration
        if any(keyword in stimulus_text_lower for keyword in ["excellent", "good job", "doing well", "validated", "praise", "thank you", "joyful", "won an award", "surprise party", "good news", "social praise", "challenge met", "social connection", "achievement", "humor", "comfort", "gratitude", "reassurance"]):
            pathway = "positive_stimulus" # Default positive, more specific paths below
            if any(keyword in stimulus_text_lower for keyword in ["excellent", "good job", "doing well", "validated", "praise",  "social praise", "thank you", "gratitude"]):
                pathway = "stimulus_social_praise"
            elif "joyful" in stimulus_text_lower or "won award" in stimulus_text_lower or "good news" in stimulus_text_lower:
                pathway = "stimulus_good_news"
            elif "surprise party" in stimulus_text_lower or "surprise" in stimulus_text_lower:
                pathway = "stimulus_surprise"
            elif "challenge met" in stimulus_text_lower:
                pathway = "stimulus_challenge_met"
            elif "social connection" in stimulus_text_lower:
                pathway = "stimulus_social_connection"
            elif "achievement" in stimulus_text_lower:
                pathway = "stimulus_achievement"
            elif "humor" in stimulus_text_lower:
                pathway = "stimulus_humor"
            elif "comfort" in stimulus_text_lower:
                pathway = "stimulus_comfort"
            elif "reassurance" in stimulus_text_lower:
                pathway = "stimulus_reassurance"


        elif any(keyword in stimulus_text_lower for keyword in ["scary", "threat", "danger", "fear", "scared", "afraid", "threat imminent", "overload", "confusion"]):
             pathway = "negative_stimulus_threat" # Default threat, more specific paths below
             if "scary threat" in stimulus_text_lower or "threat imminent" in stimulus_text_lower or "danger" in stimulus_text_lower or "threat" in stimulus_text_lower or "fear" in stimulus_text_lower or "afraid" in stimulus_text_lower:
                 pathway = "stimulus_threat_imminent"
             elif "confusion" in stimulus_text_lower:
                 pathway = "stimulus_confusion"
             elif "overload" in stimulus_text_lower:
                 pathway = "stimulus_overload"


        elif any(keyword in stimulus_text_lower for keyword in ["sad", "loss", "disappointed", "sad news", "betrayal", "social rejection", "boredom", "disappointment"]):
            pathway = "stimulus_sadness" # Default sadness, more specific paths below
            if "sad news" in stimulus_text_lower or "loss" in stimulus_text_lower or "sad" in stimulus_text_lower:
                pathway = "stimulus_sad_news"
            elif "betrayal" in stimulus_text_lower:
                pathway = "stimulus_betrayal"
            elif "social rejection" in stimulus_text_lower:
                pathway = "stimulus_social_rejection"
            elif "boredom" in stimulus_text_lower:
                pathway = "stimulus_boredom"
            elif "disappointment" in stimulus_text_lower or "disappointed" in stimulus_text_lower:
                pathway = "stimulus_disappointment"


        elif any(keyword in stimulus_text_lower for keyword in ["angry", "insult", "unfair", "frustrated", "anger", "disgust", "disgusting", "moral violation", "stimulus_anger", "stimulus_disgust", "unfairness", "frustration"]):
            pathway = "moral_violation" # Default anger/disgust, more specific paths below
            if "angry" in stimulus_text_lower or "insult" in stimulus_text_lower or "anger" in stimulus_text_lower or "stimulus_anger" in stimulus_text_lower:
                pathway = "stimulus_insult" # Or stimulus_anger
            elif "unfair" in stimulus_text_lower or "unfairness" in stimulus_text_lower or "moral violation" in stimulus_text_lower:
                 pathway = "stimulus_unfairness" # Or moral_violation
            elif "disgust" in stimulus_text_lower or "disgusting" in stimulus_text_lower or "stimulus_disgust" in stimulus_text_lower:
                pathway = "stimulus_disgust"
            elif "frustrated" in stimulus_text_lower or "frustration" in stimulus_text_lower:
                pathway = "stimulus_frustration"


        elif any(keyword in stimulus_text_lower for keyword in ["interesting", "question", "intellectual", "curious", "challenge"]):
            pathway = "intellectual_stimulus" # Default intellectual, more specific paths below
            if "interesting question" in stimulus_text_lower or "question" in stimulus_text_lower or "intellectual" in stimulus_text_lower:
                pathway = "intellectual_stimulus"
            elif "curious" in stimulus_text_lower or "curiosity" in stimulus_text_lower:
                pathway = "stimulus_curiosity"
            elif "challenge" in stimulus_text_lower:
                pathway = "stimulus_challenge"


        elif any(keyword in stimulus_text_lower for keyword in ["mozart", "music", "aesthetic", "beautiful", "art", "song"]):
            pathway = "aesthetic_positive"
            if "mozart" in stimulus_text_lower or "music" in stimulus_text_lower or "song" in stimulus_text_lower:
                pathway = "aesthetic_positive" # More specific music path if needed


        elif any(keyword in stimulus_text_lower for keyword in ["constitution", "law", "government", "justice", "liberty", "tranquility", "welfare"]):
            pathway = "social_positive_feedback" # Could be refined, using social_positive for now as placeholder


        elif any(keyword in stimulus_text_lower for keyword in ["bible", "king james version", "genesis", "exodus", "psalms", "gospels", "revelation", "christian"]): # Broader religious/spiritual stimuli
            pathway = "intellectual_stimulus" # Or could create a "spiritual_stimulus" path


        elif any(keyword in stimulus_text_lower for keyword in ["tell-tale heart", "edgar allan poe", "horror", "dark", "disturbing", "unsettling", "madness", "murder", "fearful", "vulture eye"]):
            pathway = "stimulus_fear" # Or could create a "fiction_horror_stimulus" path


        elif any(keyword in stimulus_text_lower for keyword in ["hello", "hi", "greetings", "how are you", "cadence", "gemini"]):
            pathway = "stimulus_social_cue" # Social greeting/cue


        else:
            pathway = "neutral_stimulus" # Default neutral pathway


        if pathway in self.emotion_pathways:
            selected_path = self.emotion_pathways[pathway]
            emotion_path.extend([
                selected_path["valence"],
                selected_path["relevance"],
                selected_path["physiological"],
                selected_path["expression"],
                selected_path["emotion"],
                selected_path["intensity"]
            ])
            # Dynamic Intensity Adjustment - Apply intensity and decay only if emotion is triggered
            triggered_emotion = selected_path["emotion"].strip("[]EMOTION_") # Extract emotion name
            intensity_level_str = selected_path["intensity"].strip("[]INTENSITY_") # Extract intensity level

            if triggered_emotion and triggered_emotion.lower() != 'none':
                intensity_value = 0.0
                if intensity_level_str.lower() == "very_low":
                    intensity_value = 0.1
                elif intensity_level_str.lower() == "low":
                    intensity_value = 0.2
                elif intensity_level_str.lower() == "medium":
                    intensity_value = 0.35 * self.appraisal_intensity_multiplier # Adjusted base, multiplier applied
                elif intensity_level_str.lower() == "high":
                    intensity_value = 0.6 * self.appraisal_intensity_multiplier # Adjusted base, multiplier applied
                elif intensity_level_str.lower() == "very_high":
                    intensity_value = 0.85 * self.appraisal_intensity_multiplier # Adjusted base, multiplier applied


                if triggered_emotion.upper() in self.emotion_intensity_levels:
                    self.emotion_intensity_levels[triggered_emotion.upper()] += intensity_value # Apply intensity

        return emotion_path


    def update_emotion_intensity(self):
        """
        Decays emotion intensity levels over time.
        """
        for emotion in self.emotion_categories:
            if self.emotion_intensity_levels[emotion] > 0:
                self.emotion_intensity_levels[emotion] -= self.intensity_decay_rates[emotion]
                if self.emotion_intensity_levels[emotion] < 0:
                    self.emotion_intensity_levels[emotion] = 0.0 # Ensure intensity doesn't go negative


    def get_emotion_intensity(self):
        """
        Returns current emotion intensity levels.
        """
        return self.emotion_intensity_levels