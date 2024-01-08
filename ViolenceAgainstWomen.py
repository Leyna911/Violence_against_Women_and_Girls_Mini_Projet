from pydantic import BaseModel, constr, conint


class ViolenceAgainstWomen(BaseModel):
    Country: constr(strip_whitespace=True)
    Age:constr(strip_whitespace=True)
    Education:	constr(strip_whitespace=True) 
    MaritalStatus:	constr(strip_whitespace=True, alias="Marital Status")
    Employment: constr(strip_whitespace=True)
    Residence: constr(strip_whitespace=True) 
    SurveyYear:	conint(ge=0, alias="Survey Year")
    Question:constr(strip_whitespace=True)