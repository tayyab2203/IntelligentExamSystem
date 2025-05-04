from engine.knowledge_base import difficulty_weights, importance_weights

def calculate_priority(topic, learner_type="average"):
    difficulty = topic.get("difficulty", "easy").lower()
    importance = topic.get("importance", "optional").lower()
    score = topic.get("score", 50)

    d_weight = difficulty_weights.get(difficulty, 1)
    i_weight = importance_weights.get(importance, 1)

    base_priority = (d_weight + i_weight) * (100 - score)

    learner_scale = {
        "fast": 0.8,
        "average": 1.0,
        "needs support": 1.2
    }
    scale = learner_scale.get(learner_type.lower(), 1.0)
    return round(base_priority * scale, 2)