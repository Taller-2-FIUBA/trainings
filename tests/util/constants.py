"""Constants used in tests."""

FIRST_TRAINING = {
    "id": 1,
    "trainer_id": "Ju6JXm1S8rVQfyC18mqL418JdgE2",
    "tittle": "The first training.",
    "description": "This is the first training.",
    "type": "Cardio",
    "difficulty": "Easy",
    "rating": 0,
    "blocked": False,
    "exercises": [
        {
            "name": "Walk",
            "unit": "metre",
            "type": "Cardio",
            "count": 30,
            "series": 1,
        },
        {
            "name": "Run",
            "unit": "metre",
            "type": "Cardio",
            "count": 30,
            "series": 1,
        },
        {
            "name": "Jumping jacks",
            "type": "Cardio",
            "count": 15,
            "series": 3,
        },
    ]
}

TOMATO_TRAINING = {
    "id": 2,
    "trainer_id": "tomato",
    "tittle": "The tomato training.",
    "description": "This is the tomato training.",
    "type": "Leg",
    "difficulty": "Medium",
    "rating": 0,
    "blocked": False,
    "exercises": [
        {
            "name": "Squat",
            "type": "Leg",
            "count": 15,
            "series": 3,
        },
    ]
}

TO_BLOCK_TRAINING = {
    "id": 3,
    "trainer_id": "naughty_trainer",
    "tittle": "The training to be blocked.",
    "description": "This is going to be blocked and unblocked.",
    "type": "Arm",
    "difficulty": "Hard",
    "rating": 0,
    "blocked": False,
    "exercises": [
        {
            "name": "Hammer curl",
            "type": "Arm",
            "count": 15,
            "series": 3,
        },
    ]
}

TO_EDIT_TRAINING = {
    "id": 4,
    "trainer_id": "indecisive_trainer",
    "tittle": "This training will be modified, trainer is indecisive.",
    "description": "This is going to change.",
    "type": "Arm",
    "difficulty": "Hard",
    "rating": 0,
    "blocked": False,
    "exercises": [
        {
            "name": "Hammer curl",
            "type": "Arm",
            "count": 15,
            "series": 3,
        },
    ]
}

EMPTY_RESPONSE_WITH_PAGINATION = {
    "items": [],
    "offset": 0,
    "limit": 10,
}


TRAINING_TO_BE_CREATED = {
    "trainer_id": "Ju6JXm1S8rVQf7C18mqL418JdgE2",
    "tittle": "A training created with POST.",
    "description": "A training created with POST.",
    "type": "Arm",
    "difficulty": "Medium",
    "exercises": [
        {
            "name": "Hammer curl",
            "type": "Arm",
            "count": 15,
            "series": 3
        },
        {
            "name": "Arnold press",
            "type": "Arm",
            "count": 10,
            "series": 4
        }
    ]
}

EXPECTED_TRAINING_TYPES = {
    "items": [
        "Cardio",
        "Leg",
        "Arm",
        "Chest",
        "Back",
        "Abdomen",
    ]
}

EXPECTED_EXERCISES = {
    "items": [
        {"name": "Walk", "type": "Cardio", "unit": "metre"},
        {"name": "Walk", "type": "Cardio", "unit": "second"},
        {"name": "Run", "type": "Cardio", "unit": "metre"},
        {"name": "Run", "type": "Cardio", "unit": "second"},
        {"name": "Jumping jacks", "type": "Cardio"},
        {"name": "Squat", "type": "Leg"},
        {"name": "Lunge", "type": "Leg"},
        {"name": "Deadlift", "type": "Leg"},
        {"name": "Bicep curl", "type": "Arm"},
        {"name": "Hammer curl", "type": "Arm"},
        {"name": "Tricep dips", "type": "Arm"},
        {"name": "Close grip push up", "type": "Arm"},
        {"name": "Push-down", "type": "Arm"},
        {"name": "Lateral raise", "type": "Arm"},
        {"name": "Front raise", "type": "Arm"},
        {"name": "Arnold press", "type": "Arm"},
        {"name": "Push up", "type": "Chest"},
        {"name": "Bench press", "type": "Chest"},
        {"name": "Fly", "type": "Chest"},
        {"name": "Pull-down", "type": "Back"},
        {"name": "Pull-up", "type": "Back"},
        {"name": "Bent-over row", "type": "Back"},
        {"name": "Crunch", "type": "Abdomen"},
        {"name": "Bicycle crunch", "type": "Abdomen"},
        {"name": "Plank", "type": "Abdomen"},
    ]
}
