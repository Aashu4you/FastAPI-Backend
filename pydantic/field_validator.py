from pydantic import BaseModel , EmailStr , AnyHttpUrl 
from pydantic import Field , field_validator# this is used for custom data validation and it can also be used for attaching the metadeta
from typing import List , Dict , Optional , Annotated

#this is the pydantic model
#by default all the fields in our pydantic model are required


# now suppose you want to do treatment only to the people who have certain domain name in their email . i.e. custom email validation is what you need , in that case you will have to use fieldvalidator and build a custom function for that purpose
class Patient(BaseModel):
    
    name : str
    email : EmailStr
    linkedin_url : AnyHttpUrl
    age : int
    weight : float 
    married : bool
    allergies : List[str]
    contact_details : Dict[str,str]
    
    #only a certain domain emails are allowed , i.e custom email validation
    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains = ['hdfc.com' , 'icici.com' , 'sbi.com']
        #abc@hdfc.com
        domain_name = value.split('@')[-1] # splitting the value at @ and getting the last part
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        return value
    
    # suppose the name of the person should be in capital letters only , this will transform the name entered into capital letters only
    @field_validator('name')
    @classmethod
    def transform_name(cls,value):
        return value.upper()
        
    
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
patient_info = {'name':'Aashutosh' ,'email':'abc@hdfc.com','linkedin_url':'http://linkedin.com/123', 'age':23 , 'weight':50.2 , 'married':False , 'allergies':['pollen' , 'dust'] , 'contact_details' : {'email':'ats4219511@gmail.com' , 'Mobile no':'6261616601'}}

patient1 = Patient(**patient_info)

update_patient_data(patient1)