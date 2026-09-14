import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("SuperKart Sales Revenue Predictor")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for property features
Product_Weight = st.number_input("Product Weight (in kg)", min_value=0.0, step=0.1)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Medium Sugar", "High Sugar"])
Product_Allocated_Area = st.number_input("Product Allocated Area", min_value=0.0, step=0.1)
Product_Type = st.selectbox("Product Type", ["Fruits and Vegetables", "Dairy"])
Product_MRP = st.number_input("Product MRP (Maximum Retail Price)",  min_value=0.0, step=0.5)
Store_Size = st.selectbox("Store Size", ["Small", "Medium", "Large"])
Store_Type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2"])
Store_Age = st.number_input("Store Age (In Years)", min_value=0, step=1)
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])

# Conditional Categorization: The function checks if the given product_type is present in the perishable_types list.
# If it is, the function returns the string 'Perishable'. Otherwise, it returns 'Non Perishable'.
# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'Product_Weight': Product_Weight,
    'Product_Sugar_Content': Product_Sugar_Content,
    'Product_Allocated_Area': Product_Allocated_Area,
    'Product_Type': Product_Type,
    'Product_MRP': Product_MRP,
    'Store_Size': Store_Size,
    'Store_Type': Store_Type,
    'Store_Age': Store_Age,
    'Store_Location_City_Type': Store_Location_City_Type,
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predict", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted Store Sales Total (in dollars)']
        st.success(f"Predicted Store Sales Total (in dollars): {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")
