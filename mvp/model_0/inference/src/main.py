from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, Response
import uvicorn
import argparse
from pydantic import BaseModel, ValidationError
from model_utils import input_data_ingestion, model_ingestion, feature_generation, point_prediction_generation
from app_schemas import PredictionRequest, PredictionResponse
from parameters import (
    input_data_ingestion_project_id, 
    input_data_ingestion_version, 
    input_data_ingestion_location, 
    input_data_ingestion_secret_path,
    input_data_ingestion_test_mode,
    input_data_ingestion_labels,
    feature_generation_project_id,
    feature_generation_version,
    feature_generation_location,
    feature_generation_secret_path,
    feature_generation_test_mode,
    feature_generation_labels,
    point_prediction_generation_project_id,
    point_prediction_generation_version,
    point_prediction_generation_location,
    point_prediction_generation_secret_path, 
    point_prediction_generation_test_mode,
    point_prediction_generation_labels,
    model_ingestion_project_id,
    model_ingestion_version,
    model_ingestion_location,
    model_ingestion_secret_path,
    model_ingestion_input_files_queries,
    model_ingestion_input_files_storage_uris,
    model_ingestion_test_mode,
    model_ingestion_labels
)


app = FastAPI(title='{{cookiecutter.applicationName}} API')

# Attempt to load the logistic regression model
try:
    model = model_ingestion(
        project_id=model_ingestion_project_id,
        version=model_ingestion_version,
        location=model_ingestion_location,
        secret_path=model_ingestion_secret_path,
        input_files_queries=model_ingestion_input_files_queries,
        input_files_storage_uris=model_ingestion_input_files_storage_uris,
        test_mode=model_ingestion_test_mode,
        labels=model_ingestion_labels,
    )
except Exception as e:
    # This will catch any model loading error
    app.state.model = None
    print(f"Error loading model: {e}")
else:
    app.state.model = model

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Error during validation of request data", "errors": exc.errors()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    # General error handler
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": f"An internal server error occurred: {str(exc)}"}
    )

@app.get("/health", response_class=Response)
async def health_check():
    if app.state.model is None:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "detail": "Model is not loaded"}
        )
    return Response(status_code=status.HTTP_200_OK, content="healthy")

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    if app.state.model is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Model is not loaded")

    try:
    # A need to add the parameters in the beganing of this script        
        input_data = input_data_ingestion(
            project_id=input_data_ingestion_project_id,
            version=input_data_ingestion_version,
            location=input_data_ingestion_location,
            secret_path=input_data_ingestion_secret_path,
            request=request,
            test_mode=input_data_ingestion_test_mode,
            labels=input_data_ingestion_labels,
        )
    
        feature_datasets = feature_generation(
            input_data=input_data,
            project_id=feature_generation_project_id,
            version=feature_generation_version,
            location=feature_generation_location,
            secret_path=feature_generation_secret_path,
            test_mode=feature_generation_test_mode,
            labels=feature_generation_labels,
        )
        prediction = point_prediction_generation(
            model=app.state.model,
            project_id=point_prediction_generation_project_id,
            version=point_prediction_generation_version,
            feature_datasets=feature_datasets,
            location=point_prediction_generation_location,
            secret_path=point_prediction_generation_secret_path,
            test_mode=point_prediction_generation_test_mode,
            labels=point_prediction_generation_labels,
        )
    
        return PredictionResponse(prediction=prediction)
    except Exception as e:
        # Catching any prediction related error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred during prediction: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--app_host',
        help='Bind socket to this host. Use default value to make the application available on your local network. IPv6 addresses are supported. Default: 0.0.0.0.',
        type=str,
        default="0.0.0.0"
    )
    parser.add_argument(
        "--app_port",
        help="Bind socket to this port. If 0, an available port will be picked. Default: 8080.",
        type=int,
        default=8080
    )
    
    args = parser.parse_args()
    uvicorn.run(app, host=args.app_host, port=args.app_port)
