import streamlit as st 
import streamlit as st
from pages.preprocessing import preprocessing_page
from pages.trainingevaluation import get_frequent_itemsets_and_rules_by_country
import os 
import pickle


def load_model(country):
    folder_name='ModelsStreamlit'
    pickle_filename = os.path.join(folder_name,'model_for_' + country.lower() + '.pkl')
    with open(pickle_filename, 'rb') as file:
        return pickle.load(file)
    

def get_countries():
    folder_name = 'ModelsStreamlit'
    countries = []
    for filename in os.listdir(folder_name):
        if filename.endswith('.pkl') and filename.startswith('model_for_'):
            country = filename.split('_')[-1].split('.')[0].capitalize()
            countries.append(country)
    return countries


def main():
    st.set_page_config(page_title="SEDS Project App", page_icon=":rocket:")
    
    st.write("# Welcome to our Project! 👋")

    st.markdown(
    """
    This App demonstrates an unsupervised learning model using Association technique 🤖.
    The goal was to find the frequent Itemsets and rules that provoqued violence against women and girls 👩👧 all around the world 

""")
    countries = get_countries()

    selected_country = st.sidebar.selectbox("Select a country", countries)

    st.title(f"Frequent Itemsets and Rules for {selected_country}")

    itemsets, rules = load_model(selected_country)

    st.subheader("Frequent Itemsets:")
    filtered_itemsets = itemsets[itemsets['support'] > 0.16]
    st.write(filtered_itemsets)

    st.subheader("Association Rules:")
    filtered_rules = rules[rules['support'] >= 0.3333]
    st.write(filtered_rules)

if __name__ == "__main__":
    main()

