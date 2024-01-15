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


@app.post("/predict")
def get_frequent_itemsets_and_rules_by_country(country_input: CountryInput):
    print(f"Received POST request for country: {country_input.Country}")
    country_name = country_input.Country
    
    if country_name not in loaded_Models:
            raise HTTPException(status_code=404, detail="Country not found in dataset")
    try:
        country_model = loaded_Models[country_name]
        itemsets = country_model["itemsets"]
        rules = country_model["rules"]
        # antecedents = rules["antecedents"].apply(lambda x: list(x))
        # consequents = rules["consequents"].apply(lambda x: list(x))
        support = itemsets["support"]
        confidence = rules["confidence"].astype(str)
        lift = rules["lift"].astype(str)


        itemsets_as_list = [list(itemset) for itemset in itemsets['itemsets']]
        support_as_list = support.tolist()
        confidence_as_list = confidence.tolist()
        lift_as_list = lift.tolist()


        
        
        
    
        
        

        response_data = {
            "country": country_name,
            "frequent_itemsets": itemsets_as_list,
            "support":support_as_list,
            "confidence": confidence_as_list,
            "lift": lift_as_list,
            # "antecedents": antecedents.tolist(),
            # "consequents": consequents.tolist()
            # # "rules": rules.to_dict(orient="records")
            
           
        }
        return JSONResponse( response_data)
    except Exception as e:
        return e

    
if __name__ == '__main__': 
    uvicorn.run(app, host='127.0.0.1', port=8000)