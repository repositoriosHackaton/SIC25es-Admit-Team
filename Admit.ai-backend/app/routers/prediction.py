from fastapi import APIRouter
from pydantic import BaseModel, Field
import numpy as np
import joblib
import logging
import pandas as pd
from numpyro.infer import Predictive
import numpyro
import numpyro.distributions as dist  # Importación necesaria
from sklearn.preprocessing import StandardScaler
import jax
import jax.numpy as jnp
from functools import partial

rng_key = jax.random.PRNGKey(0)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

router = APIRouter()

recommendations = [
    ["No recommendations"],  # rating 0
    ["University of Akron", "University of Alabama at Birmingham", "University of Alabama in Huntsville", "University of Alaska Anchorage", "University of Arkansas at Little Rock", "University of Arkansas for Medical Sciences", "University of Baltimore", "University of Bridgeport"],  # rating 1
    ["University of Alabama", "University of Alaska Fairbanks", "University of Arkansas", "University of California, Merced", "University of Central Florida", "University of Cincinnati", "University of Colorado Colorado Springs", "University of Colorado Denver"],  # rating 2
    ["University of Arizona", "University of Colorado Boulder", "University of Connecticut", "University of Delaware", "University of Houston", "University of Iowa", "University of Kansas", "University of Kentucky"],  # rating 3
    ["University of Illinois Urbana-Champaign", "University of Wisconsin-Madison", "University of Washington", "University of Texas at Austin", "University of Florida", "University of Georgia", "University of Maryland, College Park", "University of Minnesota, Twin Cities"],  # rating 4
    ["University of California, Berkeley", "University of California, Los Angeles", "University of California, San Diego", "University of California, Santa Barbara", "University of California, Irvine", "University of California, Davis", "University of California, Riverside", "University of California, Merced"],  # rating 5
]

class PredictionRequest(BaseModel):
    greScore: int = Field(..., ge=0, le=340)
    toeflScore: int = Field(..., ge=0, le=120)
    sop: float = Field(..., ge=0.0, le=5.0)
    lor: float = Field(..., ge=0.0, le=5.0)
    cgpa: float = Field(..., ge=0.0, le=10.0)
    research: bool

with open("app/model.pkl", "rb") as f:
    model = joblib.load(f)

with open("app/scaler.pkl", "rb") as f:
    scaler = joblib.load(f)

def hierarchical_model(X, groups, n_groups, y=None):
    n_samples, n_features = X.shape

    mu_intercept = numpyro.sample("mu_intercept", dist.Normal(0, 10))
    sigma_intercept = numpyro.sample("sigma_intercept", dist.HalfNormal(5))
    mu_beta = numpyro.sample("mu_beta", dist.Normal(jnp.zeros(n_features), 10 * jnp.ones(n_features)))
    sigma_beta = numpyro.sample("sigma_beta", dist.HalfNormal(5 * jnp.ones(n_features)))

    intercept = numpyro.sample("intercept", dist.Normal(mu_intercept, sigma_intercept).expand([n_groups]))
    beta = numpyro.sample("beta", dist.Normal(mu_beta, sigma_beta).expand([n_groups, n_features]))

    mu = intercept[groups] + jnp.sum(beta[groups] * X, axis=-1)

    sigma = numpyro.sample("sigma", dist.HalfNormal(5))
    numpyro.sample("obs", dist.StudentT(df=4, loc=mu, scale=sigma), obs=y)

# Endpoint de predicción
@router.post("/predict")
async def predict_endpoint(request: PredictionRequest):
    predictions = []

    for universityRating in range(1, 6):
        
        values = np.array([[request.greScore, request.toeflScore, request.sop, request.lor, request.cgpa, request.research]])
        escalado = scaler.transform(values)
        rating = np.array([universityRating - 1])
        predictive = Predictive(hierarchical_model, model)
        predictions_dict = predictive(rng_key, X=escalado, groups=rating, n_groups=5)
        predictions.append(jnp.mean(predictions_dict["obs"]) * 100)
    
    safeSchool = 0
    targetSchool = 0
    reachSchool = 0

    predictSafeSchool = 0
    predictTargetSchool = 0
    predictReachSchool = 0

    logging.info(f"Predictions: {predictions}")

    for i, prediction in enumerate(predictions):
        if prediction >= 70:
            safeSchool = i + 1
            predictSafeSchool = prediction
        elif prediction >= 50:
            targetSchool = i + 1
            predictTargetSchool = prediction
        else:
            reachSchool = i + 1
            predictReachSchool = prediction

    if targetSchool == 0:
        targetSchool = safeSchool
        predictTargetSchool = predictSafeSchool

    if reachSchool == 0:
        reachSchool = targetSchool
        predictReachSchool = predictTargetSchool

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
