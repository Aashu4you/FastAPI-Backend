from pydantic import BaseModel , EmailStr , AnyHttpUrl , computed_field
from pydantic import Field # this is used for custom data validation and it can also be used for attaching the metadeta
from typing import List , Dict , Optional , Annotated

#this is the pydantic model
#by default all the fields in our pydantic model are required


# computed fields are the fields that we dont take input from the user or the user is not responsible for giving the information about those fields , we calculate it using the information given by the patient and store it along with the information given by the user
# this field is dynamically created at the time of computation

class Patient(BaseModel):
    
    name : str
    email : EmailStr
    linkedin_url : AnyHttpUrl
    age : int
    weight : float
    height : float
    married : bool
    allergies : List[str]# this makes the default required field into an optional field
    contact_details : Dict[str,str]
    
    @computed_field
    @property
    def bmi_value(self)->float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    
def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.height)
    print('BMI ' , patient.bmi_value)
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
patient_info = {'name':'Aashutosh' ,'email':'abc@gmail.com','linkedin_url':'http://linkedin.com/123', 'age':23 , 'weight':50.2 ,'height' : 1.7, 'married':False , 'allergies':['pollen' , 'dust'] , 'contact_details' : {'email':'ats4219511@gmail.com' , 'Mobile no':'6261616601'}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)