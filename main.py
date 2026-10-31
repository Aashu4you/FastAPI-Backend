from fastapi import FastAPI , Path , HTTPException , Query
from pydantic import BaseModel , Field , computed_field
from typing import Annotated , Literal
from fastapi.responses import JSONResponse
import json

app = FastAPI()

class Patient(BaseModel):
    
    id : Annotated[str, Field(...,description="ID of the patient" , examples=['P001'])]
    name : Annotated[str, Field(...,description="Name of the patient")]
    city : Annotated[str , Field(...,description="City where the patient is living")]
    age : Annotated[int , Field(...,gt=0,lt=120,description="Age of the patient ")]
    gender : Annotated[Literal['male', 'female','others'], Field(...,description="Gender of the patient")]
    height : Annotated[float , Field(...,gt=0, description="Height of the patient in mtr")]
    weight : Annotated[float, Field(...,gt=0,description="Weight of the patient in kgs")]
    
    @computed_field
    @property
    def bmi(self)->float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return 'Underweight'
        elif self.bmi<25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'

#this is the function to load the json file
def load_data():
    with open("patients.json",'r') as f:
        data = json.load(f)
    
    return data

# this is the function to save the data back or load the data into our json file
def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data,f)

@app.get("/") 
# decorator ki help se ek endpoint define kiya
def hello():
    return {"message":"Patient Management System"}

#isko run karne ke liye we will write uvicor main:app --reload // uvicorn filekanaam:appkanaam --reload

@app.get("/about") #this is known as endpoint
def about():
    return {'message': 'Patient Management System using CRUD OPERATIONS'}

#endpoint to get all the entries from the json file

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")# here {patient_id} is the dynamic path parameter
def view_patient(patient_id : str = Path(...,description="ID of the patient in the DB" , example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404 , detail="Patient Not Found")

#sorting the patient data based on height , weight or bmi using Query parameters

@app.get("/sort")
def sort_patients(sort_by : str = Query(...,description="Sort the patients based on height , weight or bmi"), order: str =Query('asc' , description='Sort in ascending or descending order')):
    
    valid_fields = ['height' , 'weight' , 'bmi']
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400 , detail=f"Invalid field , select from {valid_fields}")
    
    if order not in ['asc' , 'desc']:
        raise HTTPException(status_code=400 , detail="Invalid Field , select from asc or desc")
    
    data = load_data()
    
    sort_order = True if order=='desc' else False
    
    sorted_data = sorted(data.values(),key = lambda x: x.get(sort_by,0) , reverse=sort_order)
    
    return sorted_data

# POST endpoint for the creation of new patient and store it in our exisiting json file
@app.post('/create')
def create_patient(patient : Patient):
    
    # load data
    data = load_data()
    
    # check whether the patient with the same patient ID already exists in our json file
    if patient.id in data :
        raise HTTPException(status_code=400 , detail="Patient already exists")
    
    # convert the data into a dictionary with ID as the key 
    data[patient.id] = patient.model_dump(exclude=['id'])
    
    # save the data in the json file
    save_data(data)
    
    return JSONResponse(status_code=201 , content={'message':'Patient created successfully'})