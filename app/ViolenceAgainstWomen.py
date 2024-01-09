from pydantic import BaseModel


class CountryInput(BaseModel):
    Country: str
    