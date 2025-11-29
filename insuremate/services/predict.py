"""Service layer for prediction logic.
Loads the ML model once and exposes helper functions used by routers.
"""
from pathlib import Path
import pickle
import pandas as pd
import sys
import importlib
from typing import Dict, Any

# Add compatibility for missing _RemainderColsList
import sklearn.compose._column_transformer

class _RemainderColsList(list):
    """Mock class for backward compatibility with older scikit-learn versions."""
    pass

# Make the class available in the module
setattr(sklearn.compose._column_transformer, '_RemainderColsList', _RemainderColsList)

from insuremate.models import Userinput
from insuremate.db.database import save_prediction_result
from insuremate.core.config import MODEL_PATH

# Prefer the env-driven MODEL_PATH from config, fallback to package/root locations
_MODEL_PATH = Path(MODEL_PATH)
if not _MODEL_PATH.exists():
    potential = Path(__file__).resolve().parent.parent / "model.pkl"
    if potential.exists():
        _MODEL_PATH = potential
    else:
        root_fallback = Path.cwd() / "model.pkl"
        _MODEL_PATH = root_fallback

try:
    with open(_MODEL_PATH, "rb") as f:
        _MODEL = pickle.load(f)
    print(f"Model loaded successfully from {_MODEL_PATH}")
except AttributeError as e:
    print(f"Error loading model: {e}")
    print("This is likely due to a version mismatch with scikit-learn.")
    print("Please ensure you're using the same version of scikit-learn that was used to train the model.")
    raise


def predict_from_user(user: Userinput):
    """Run prediction and persist result to DB.
    Returns (prediction, db_record)
    """
    input_df = pd.DataFrame([{
        "bmi": user.bmi,
        "lifestyle_risk": user.lifestyle_risk,
        "age_group": user.age_group,
        "city_tier": user.city_tier,
        "occupation": user.occupation,
        "income_lpa": user.income_lpa
    }])

    prediction = _MODEL.predict(input_df)[0]
    db_record = save_prediction_result(user, prediction)
    return prediction, db_record
