import streamlit as st
import pandas as pd
from itertools import product


st.set_page_config(page_title="Preprocessing", page_icon="📈")


st.markdown("# Preprocessing ")
st.sidebar.header("Preprocessing")
st.write(
    """This demo illustrates the pre-processing phase. Where we displayed the original Data and the cleaned Data. Enjoy!"""
)



def load_data():
    return pd.read_csv('violence_data.csv')

df = load_data()

def data_cleaning(df):
    df['Residence'] = df['Demographics Response'].apply(lambda response: response if response in ['Rural', 'Urban'] else None)
    df['Marital status'] = df['Demographics Response'].apply(lambda response: response if response in ['Never married', 'Widowed, divorced, separated'] else None)
    df['Education'] = df['Demographics Response'].apply(lambda response: response if response in ['No education','Primary','Secondary','Higher'] else None)
    df['Employment'] = df['Demographics Response'].apply(lambda response: response if response in ['Employed for kind', 'Unemployed','Employed for cash'] else None)
    df['Age'] = df['Demographics Response'].apply(lambda response: response if response in ['15-24','25-34','35-49'] else None)

    df = df.drop('Demographics Response', axis=1)
    df = df.drop('Demographics Question', axis=1)
    desired_order = ['RecordID','Gender','Country','Age','Education','Marital status','Employment','Residence','Survey Year','Question','Value']

    
    
    cleaned_data = df[desired_order]

    return cleaned_data

    

def preprocessing_page():
    df = load_data()
    preprocessed_df = data_cleaning(df)
    return preprocessed_df



def show_data_preprocessing_page(df):
    st.title("Data Pre-processing")
   
    st.subheader("Original Data:")
    st.write(df.head(20))

    cleaned_data = data_cleaning(df)
    
    st.subheader("Cleaned Data:")
    st.write(cleaned_data.head(20))
    
    return cleaned_data

show_data_preprocessing_page(df)