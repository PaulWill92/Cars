import pandas as pd
import sys
import streamlit as st
import numpy as np
import seaborn as sns


df = pd.read_csv("~/Desktop/capstone3/cars/Cleaned-Data/cleaned_cars.csv")
df2 = df.copy()
df.drop(columns="Unnamed: 0", inplace=True)
df.head()


df["price(£)"] = df.apply(lambda x: "{:,}".format(x["price(£)"]), axis=1)
df["mileage(mi)"] = df.apply(lambda x: "{:,}".format(x["mileage(mi)"]), axis=1)
df["engine_size(cc)"] = df.apply(lambda x: "{:,}".format(x["engine_size(cc)"]), axis=1)


st.markdown(" # Predicting Car Prices \n Using Machine Learning")
st.text(" ")

st.markdown("## __Dataframe__")
st.write("*Scrapped from [Auto Village](https://www.autovillage.co.uk/used-car)*")

if st.checkbox("Show data"):
    option1 = st.selectbox(
        "Which car brand do you like best?", df["brand"].sort_values().unique()
    )

"You selected: ", option1
filt = df["brand"] == option1
df[filt]
