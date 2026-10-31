from pydantic import BaseModel , EmailStr , AnyHttpUrl , model_validator
from pydantic import Field # this is used for custom data validation and it can also be used for attaching the metadeta
from typing import List , Dict , Optional , Annotated

#this is the pydantic model
#by default all the fields in our pydantic model are required


# suppose hame multiple fields ke through data validation karna hai , tab hum model_validator ka use karenge
# suppose if patients age is greater than 60 , then they should have an emergency contact number as mandatory
class Patient(BaseModel):
    
    name : str
    email : EmailStr
    linkedin_url : AnyHttpUrl
    age : int
    weight : float
    married : bool
    allergies : List[str]# this makes the default required field into an optional field
    contact_details : Dict[str,str]
    
    @model_validator(mode = 'after')
    def validate_emergency_contact(cls,model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError("Patients older than 60 must have an emergency contact")
        return model
    
    
def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("Inserted successfully")

def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.linkedin_url)
    print(patient.contact_details)
    print(patient.weight)
    print("Updated successfully")

#raw data
patient_info = {'name':'Aashutosh' ,'email':'abc@gmail.com','linkedin_url':'http://linkedin.com/123', 'age':62 , 'weight':50.2 , 'married':False , 'allergies':['pollen' , 'dust'] , 'contact_details' : {'email':'ats4219511@gmail.com' , 'Mobile no':'6261616601' , 'emergency':'12334'}}

patient1 = Patient(**patient_info)

update_patient_data(patient1)