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


print(patient1)
print(patient1.name)
print(patient1.age)
print(patient1.location)
print(patient1.location.city)
print(patient1.location.pin)


# benefits

# better organization of data

# Reusability , readability , Validation me help

# nested models are validated automatically , no manual work is needed