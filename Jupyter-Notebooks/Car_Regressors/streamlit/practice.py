import pandas as pd
import sys
import streamlit as st

df = pd.read_csv("~/Desktop/capstone3/cars/Cleaned-Data/cleaned_cars.csv")

df.head()


st.write("# Predict Car Prices")
st.write("## Using Machine Learning")
