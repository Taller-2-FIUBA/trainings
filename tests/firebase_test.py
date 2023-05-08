# pylint: disable= missing-module-docstring, missing-function-docstring
from trainings.firebase import save


def test_saving_blob_expect_a_firebase_id():
    assert save("blob") == "a_firebase_id"
