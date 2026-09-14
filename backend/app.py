# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
sk_sales_predicator_api = Flask("SuperKart Sales Revenue Predictor")

# Load the trained machine learning model
model = joblib.load("superkart_sales_prediction_model_v1_0.joblib")

# Define a route for the home page (GET request)
@sk_sales_predicator_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Sales Revenue Prediction API!"

# Define an endpoint for single property prediction (POST request)
@sk_sales_predicator_api.post('/v1/predict')
def predict_sales_revenue():
    """
    This function handles POST requests to the '/v1/predict' endpoint.
    It expects a JSON payload containing property details and returns
    the predicted rental price as a JSON response.
    """
    # Get the JSON data from the request body
    data = request.get_json()

    # Extract relevant features from the JSON data
    input_df = pd.DataFrame([{
        'Product_Weight': data['Product_Weight'],
        'Product_Sugar_Content': data['Product_Sugar_Content'],
        'Product_Allocated_Area': data['Product_Allocated_Area'],
        'Product_Type': data['Product_Type'],
        'Product_MRP': data['Product_MRP'],
        'Store_Size': data['Store_Size'],
        'Store_Type': data['Store_Type'],
        'Store_Age': data['Store_Age'],
        'Store_Location_City_Type': data['Store_Location_City_Type'],
    }])

    # Make prediction (get log_price)
    predicted_sales = model.predict(input_df)[0]

    # Convert predicted_price to Python float
    predicted_sales = round(float(predicted_sales), 2)

    # When we send this value directly within a JSON response, Flask's jsonify function encounters a datatype error

    # Return the actual price
    return jsonify({'Predicted Product Store Sales Total': predicted_sales,
                    "message": "Prediction generated successfully"})
    

    # Define an endpoint to predict price for a batch of houses
@sk_sales_predicator_api.post('/v1/predictbatch')
def predict_sales_batch():
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the file into a DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for the batch data
    predictions = model.predict(input_data).tolist()

    # Add predictions to the DataFrame
    input_data['Predicted_sales'] = predictions

    # Convert results to dictionary
    result = input_data.to_dict(orient="records")

    return jsonify(result)



# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    sk_sales_predicator_api.run(debug=True, port=7860)
