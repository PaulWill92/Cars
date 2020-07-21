import pandas as pd
import sys
import streamlit as st
import pickle

df = pd.read_csv("~/Desktop/capstone3/cars/Cleaned-Data/cleaned_cars.csv")
df.drop(columns="Unnamed: 0", inplace=True)


st.markdown("# Predict Car Prices")
st.markdown("## Using Machine Learning")
st.markdown("##### by Paul Aleksis Williams")
st.markdown("\n")
st.markdown("\n")

st.image("./streamlit_app_picture.jpg")
st.write(
    "Cars Data Frame scrapped from [Autovillage](https://www.autovillage.co.uk/used-car)"
)
st.dataframe(df)

# median_brand_price = df.groupby(["brand", "model"]).agg(
#     Price=("price(£)", "median"),
#     Quantity=("brand", "count"),
#     Model_Avg_Miles=("mileage(mi)", "median"),
# )



# st.dataframe(median_brand_price)

# Load my regressor model
model = pickle.load(open('../../../pickle_files/pkl_objects/KnnRegressor.pkl', 'rb'))

#User inputs

