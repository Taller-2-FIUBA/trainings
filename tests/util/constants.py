"""Constants used in tests."""

EXPECTED_TRAININGS = {
    "items": [
        {
            "id": 1,
            "trainer_id": "Ju6JXm1S8rVQfyC18mqL418JdgE2",
            "tittle": "The first training.",
            "description": "This is the first training.",
            "type": "Cardio",
            "difficulty": "Easy",
            "media": "a_firebase_id",
            "rating": 0,
            "exercises": [
                {
                    "name": "Walk",
                    "unit": "metre",
                    "type": "Cardio",
                    "count": 30,
                    "series": 1
                },
                {
                    "name": "Run",
                    "unit": "metre",
                    "type": "Cardio",
                    "count": 30,
                    "series": 1
                },
                {
                    "name": "Jumping jacks",
                    "type": "Cardio",
                    "count": 15,
                    "series": 3
                },
            ]
        },
    ],
    "offset": 0,
    "limit": 10
}


TRAINING_TO_BE_CREATED = {
    "trainer_id": "Ju6JXm1S8rVQf7C18mqL418JdgE2",
    "tittle": "A training created with POST.",
    "description": "A training created with POST.",
    "type": "Arm",
    "difficulty": "Medium",
    "media": "a_firebase_id",
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
