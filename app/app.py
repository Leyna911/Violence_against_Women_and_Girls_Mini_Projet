import uvicorn
from fastapi import FastAPI, HTTPException
import joblib
import pickle 
from app.ViolenceAgainstWomen import CountryInput
import pandas as pd 
import os 
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models_folder = "Models"

loaded_Models = {}

for filename in os.listdir(models_folder):
    if filename.endswith(".pkl"):
        country_name = filename.split('_')[-1].split('.')[0].capitalize()
        pickle_filepath = os.path.join(models_folder, filename)

        with open(pickle_filepath, 'rb') as file:
            itemsets, rules = pickle.load(file)

            loaded_Models[country_name] = {"itemsets": itemsets, "rules": rules}


@app.get('/')
def index():
    return {"message":"home page"}


@app.get('/{name}')
def get_name(name: str):
    return {'Welcome This dataset represent Violence Against Women and Girls in the world':f'{name}'}

@app.post("/predict")
def get_frequent_itemsets_and_rules_by_country(country_input: CountryInput):
    print(f"Received POST request for country: {country_input.Country}")

    country_name = country_input.Country

    try:
        if country_name not in loaded_Models:
            raise HTTPException(status_code=404, detail="Country not found in dataset")

        country_model = loaded_Models[country_name]
        itemsets = country_model["itemsets"]
        rules = country_model["rules"]

        itemsets_as_list = [list(itemset) for itemset in itemsets['itemsets']]
        rules_as_list = [list(rule) for rule in rules['itemsets']]
        
        response_data = {
            "country": country_name,
            "frequent_itemsets": itemsets_as_list,
            "association_rules": rules_as_list
        }

        return JSONResponse(content=response_data)

    except RequestValidationError as e:
        print(f"Validation error: {e}")
        return JSONResponse(content={"error": "Invalid request payload"}, status_code=400)

    except HTTPException as e:
        print(f"HTTPException: {e}")
        return JSONResponse(content={"error": str(e.detail)}, status_code=e.status_code)

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return JSONResponse(content={"error": "Internal server error"}, status_code=500)

    
if __name__ == '__main__': 
    uvicorn.run(app, host='127.0.0.1', port=8000)