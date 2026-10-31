from pydantic import BaseModel

class Address(BaseModel):
    street : str
    city : str
    state : str
    pin : int

class Patient(BaseModel):
    name : str
    age : int
    gender : str
    location : Address
    
add_dict = {'street':'lane 2' , 'city':'sehore' , 'state':'MP' , 'pin':466001}

address1 = Address(**add_dict)

patient_dict = {'name': 'Aashu' , 'age': 23 , 'gender':'male' , 'location':address1}

patient1 = Patient(**patient_dict)

temp = patient1.model_dump() #this will store your object as a dictionary in temp , very useful when you want to export the data  , 
# patient1.model_dump_json() will convert it into json and type will be str in that case

#use of include and exlude parameters 
temp2 = patient1.model_dump(include=['name', 'age']) # now it will only export name and age
temp3 = patient1.model_dump(exclude=['name','age']) # it will export everything except name and age

print(temp3)
print(type(temp2))