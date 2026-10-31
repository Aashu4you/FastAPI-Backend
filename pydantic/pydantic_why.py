from pydantic import BaseModel , EmailStr , AnyHttpUrl
from pydantic import Field # this is used for custom data validation and it can also be used for attaching the metadeta
from typing import List , Dict , Optional , Annotated

#this is the pydantic model
#by default all the fields in our pydantic model are required

class Patient(BaseModel):
    
    name : Annotated[str, Field(max_length=50 , title="Name of the Patient" , description="Give the name of the patient" , examples=['Aashu' , 'Salman'])]
    email : EmailStr
    linkedin_url : AnyHttpUrl
    age : int
    weight : float = Field(gt=0 , lt=200)
    married : bool
    allergies : Annotated[Optional[List[str]],  Field(default=None , max_length=5)]# this makes the default required field into an optional field
    contact_details : Dict[str,str]
    
    
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
patient_info = {'name':'Aashutosh' ,'email':'abc@gmail.com','linkedin_url':'http://linkedin.com/123', 'age':23 , 'weight':50.2 , 'married':False , 'allergies':['pollen' , 'dust'] , 'contact_details' : {'email':'ats4219511@gmail.com' , 'Mobile no':'6261616601'}}

patient1 = Patient(**patient_info)

update_patient_data(patient1)