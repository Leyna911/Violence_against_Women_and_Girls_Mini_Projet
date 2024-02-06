import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from itertools import product
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
from pages.preprocessing import preprocessing_page, show_data_preprocessing_page, data_cleaning, load_data
import os
import pickle



st.set_page_config(page_title="Training and Evaluation", page_icon="📈")


st.markdown("# Training and Evaluation ")
st.sidebar.header("Training and Evaluation")
st.write(
    """This demo illustrates the Training and Evaluation phase. Where we displayed the Grouped Data by country name 🗺️."""
)



def generate_combinations(group):

    unique_values = {col: group[col].unique() for col in group.columns[3:10]}
    combinations = list(product(*unique_values.values()))

    result = pd.DataFrame(combinations, columns=unique_values.keys())

    result[group.columns[:3]] = group[group.columns[:3]].iloc[0]

    return result




@st.cache_data
def get_frequent_itemsets_and_rules_by_country(df, country_name, min_support=0.01, min_confidence=0.2, min_length=3):
  country_transactions = df[df['Country'] == country_name].values.tolist()

  te = TransactionEncoder()
  te_ary = te.fit(country_transactions).transform(country_transactions)
  df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

  frequent_itemset = apriori(df_encoded, min_support=min_support,use_colnames=True)
  frequent_itemset = frequent_itemset.sort_values(by="support", ascending=False)
  frequent_itemset['length'] = frequent_itemset['itemsets'].apply(lambda x:len(x))

  result_df = frequent_itemset[(frequent_itemset['length'] >= min_length) & (frequent_itemset['support'] >= min_support) & (frequent_itemset['itemsets'].apply(lambda x: country_name in str(x)))]

  rules = association_rules(frequent_itemset, metric = 'confidence', min_threshold=min_confidence)
  rules_for_country = rules[
    (rules['antecedents'].apply(lambda x: country_name in str(x))) | (rules['consequents'].apply(lambda x: country_name in str(x)))  ]
    
  return result_df, rules




@st.cache_data
def show_combinations_by_country(cleaned_data):
    st.title("Combinations Grouped by Country")
    
    result_df = cleaned_data.groupby(['Country']).apply(generate_combinations).reset_index(drop=True)
    result_df = result_df.dropna()
     
    result_df.drop('RecordID', axis=1, inplace=True)
    result_df = result_df.reset_index(drop=True)
    order_df = ['Country','Age','Education','Marital status','Employment','Residence','Question']
    result_df = result_df[order_df]

    st.write(result_df)

    return result_df


@st.cache_data
def training_page():
    preprocessed_df = preprocessing_page()

    grouped_df = show_combinations_by_country(preprocessed_df)

    return grouped_df



   

def export_model():
    df = training_page()
    if st.button("Export Models"):
      folder_name = 'ModelsStreamlit'
      countries = df['Country'].unique()

      for country in countries : 
          itemsets, rules = get_frequent_itemsets_and_rules_by_country(df, country)
          pickle_filename = os.path.join(folder_name,'model_for_'+ country.lower() + '.pkl')
          with open(pickle_filename, 'wb') as file: 
              pickle.dump((itemsets, rules), file)
              
          st.write(f'Model for {country} saved to {pickle_filename}')
      

export_model()