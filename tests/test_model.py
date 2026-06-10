import joblib
import os

def test_model_exists():
    assert os.path.exists("model.pkl")

def test_model_loads():
    model = joblib.load("model.pkl")
    assert model is not None