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
                    "unit": "None",
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
