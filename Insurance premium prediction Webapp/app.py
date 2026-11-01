from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.prediction_response import PredictionResponse
from schema.user_input import UserInput # we are importing the pydantic model from the schema
from model.predict import predict_output , model , MODEL_VERSION

# create a FastAPI App
app = FastAPI()

      
# simple home page
@app.get('/')
def home():
    return {'message':'Insurance Premium Prediction API'}

# to make the code machine readable for services like ELB and Kubernetes
@app.get('/health')
def health_check():
    return {
        'status': 'OK' ,
        'version' : MODEL_VERSION
    }

  
# now we will create an endpoint for the prediction
@app.post('/predict', response_model=PredictionResponse)
def predict_premium(data : UserInput):
    
    # we will be passing the value to our endpoint in a dataframe as model is built to handle the data in that format only
    user_input ={
        'bmi':data.bmi,
        'age_group' : data.age_group,
        'lifestyle_risk' : data.lifestyle_risk ,
        'city_tier' : data.city_tier ,
        'income_lpa' : data.income_lpa ,
        'occupation' : data.occupation
    }
    
    try:
        prediction = predict_output(user_input)
            
        return JSONResponse(status_code=200 , content={'Predicted_category ': prediction})
    except Exception as e:
        return JSONResponse(status_code=500 , content=str(e))