from fastapi import FastAPI , Path , HTTPException , Query
import json

app = FastAPI()

#this is the function to load the json file
def load_data():
    with open("patients.json",'r') as f:
        data = json.load(f)
    
    return data

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