from fastapi import APIRouter
from pydantic import BaseModel, Field
import numpy as np
import joblib
import logging
import pandas as pd

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


router = APIRouter()

recommendations = [

    ["No recommendations"], #rating 0
    ["University of Akron", "University of Alabama at Birmingham", "University of Alabama in Huntsville", "University of Alaska Anchorage", "University of Arkansas at Little Rock", "University of Arkansas for Medical Sciences", "University of Baltimore", "University of Bridgeport"], #rating 1
    ["University of Alabama", "University of Alaska Fairbanks", "University of Arkansas", "University of California, Merced", "University of Central Florida", "University of Cincinnati", "University of Colorado Colorado Springs", "University of Colorado Denver"], #rating 2
    ["University of Arizona", "University of Colorado Boulder", "University of Connecticut", "University of Delaware", "University of Houston", "University of Iowa", "University of Kansas", "University of Kentucky"], #rating 3
    ["University of Illinois Urbana-Champaign", "University of Wisconsin-Madison", "University of Washington", "University of Texas at Austin", "University of Florida", "University of Georgia", "University of Maryland, College Park", "University of Minnesota, Twin Cities"], #rating 4
    ["University of California, Berkeley", "University of California, Los Angeles", "University of California, San Diego", "University of California, Santa Barbara", "University of California, Irvine", "University of California, Davis", "University of California, Riverside", "University of California, Merced"], #rating 5
]

class PredictionRequest(BaseModel):
    greScore: int = Field(..., ge=0, le=340)
    toeflScore: int = Field(..., ge=92, le=120)
    sop: float = Field(..., ge=0.0, le=5.0)
    lor: float = Field(..., ge=0.0, le=5.0)
    cgpa: float = Field(..., ge=0.0, le=10.0)
    research: bool

with open("app/model.pkl", "rb") as f:
    model = joblib.load(f)

def predict (request: PredictionRequest):

    X_input = [request["greScore"], request["toeflScore"], request["universityRating"], request["sop"], request["lor"], request["cgpa"], request["research"]]
    X_input = np.array(X_input).reshape(1, -1)
    X_input = pd.DataFrame(X_input, columns=["GRE Score", "TOEFL Score", "University Rating", "SOP", "LOR ", "CGPA", "Research"])
    logging.info(f"X_input: {X_input}")
    prediction = model.predict(X_input)

    prediction = round(prediction[0]*100, 2)

    return prediction

@router.post("/predict")
async def predict_endpoint(request: PredictionRequest):

    predictions = []

    for universityRating in range(1, 6):
        predictions.append(predict({
            "greScore":request.greScore,
            "toeflScore":request.toeflScore,
            "universityRating":universityRating,
            "sop":request.sop,
            "lor":request.lor,
            "cgpa":request.cgpa,
            "research":request.research
        }))

    safeSchool = 0
    targetSchool = 0
    reachSchool = 0

    predictSafeSchool = 0
    predictTargetSchool = 0
    predictReachSchool = 0

    logging.info(f"Predictions: {predictions}")

    for i, prediction in enumerate(predictions):

        if prediction >= 70:
            safeSchool = i+1
            predictSafeSchool = prediction
        elif prediction >= 50:
            targetSchool = i+1
            predictTargetSchool = prediction
        else:
            reachSchool = i+1
            predictReachSchool = prediction

    
    if targetSchool == 0:
        targetSchool = safeSchool
        predictTargetSchool = predictSafeSchool

    if reachSchool == 0:
        reachSchool = targetSchool
        predictReachSchool = predictTargetSchool

    if predictTargetSchool < 70:
        targetSchool = 4
    elif predictReachSchool < 50:
        reachSchool = 3
    elif predictSafeSchool < 40:
        reachSchool = 1

    return {

        "safeSchool": {

            "probability": predictSafeSchool,
            "recommendations": recommendations[safeSchool],
            "rating": safeSchool
        },
        "targetSchool": {

            "probability": predictTargetSchool,
            "recommendations": recommendations[targetSchool],
            "rating": targetSchool
        },
        "reachSchool": {

            "probability": predictReachSchool,
            "recommendations": recommendations[reachSchool],
            "rating": reachSchool
        }
    }
    
