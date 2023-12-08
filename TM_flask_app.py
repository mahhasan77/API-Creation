#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 10:58:04 2023

@author: mahrukhhasan
"""

import pandas as pd
import joblib
import requests
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from functools import wraps
import uuid
from collections import OrderedDict
import json

mean_account_age_score = 1.5299110767102855
SD_account_age_score = 2.2903028182999776
mean_new_account_score = 2.763762219415791
SD_new_account_score = 4.310618339417133
mean_first_transaction_score = 1.6981047712119515
SD_first_transaction_Score = 2.3695415972999574
mean_last_transaction_score = 0.10914066566876841
SD_last_transaction_Score = 0.6842631215209698
mean_sleeper_score = 0.006523605158640201
SD_sleeper_score = 0.381879261043099
mean_dormant_score = 0.006500225641189643
SD_dormant_score = 0.3811944745806706

mean_account_risk_score = 2.2812870125810236
SD_account_risk_score = 3.6700946354178523
mean_merchant_country_risk_score = 1.492853953584097
SD_merchant_country_risk_score = 0.9070733650418078
mean_mcc_risk_score = 2.7039763418249274
SD_mcc_risk_score = 2.3572213946892937
mean_currency_risk_score = 1.002916685298385
SD_currency_risk_score = 0.07936102792217964
mean_high_value_score = 1.549112199234456
SD_high_value_score = 1.016017898149702

mean_avg_txn_variance_score = 1.156495227895959
SD_avg_txn_variance_score = 58.0518405866223
mean_max_txn_variance_score = 0.24227509864307467
SD_max_txn_variance_score = 49.31320809563716
mean_daily_sum_variance_score = 0.6893351931197836
SD_daily_sum_variance_score = 33.755008025495755
mean_monthly_avg_count_variance_score = 1.3329202430608242
SD_monthly_avg_count_variance_score = 1.6195425051504726
mean_daily_avg_count_variance_score = 0.46733755311084163
SD_daily_avg_count_variance_score = 2.8053924082488364
mean_monthly_avg_sum_variance_score = 1.3195682179379236
SD_monthly_avg_sum_variance_score = 1.7945666428736924

mean_AML_daily_sum_score = 1.4547260738719876
SD_AML_daily_sum_score = 1.5407073861026022
mean_AML_daily_count_score = 1.4543980703419606
SD_AML_daily_count_score = 1.5029433990660512
mean_AML_monthly_sum_score = 1.745603286251853
SD_AML_monthly_sum_score = 1.7954580059789822
mean_AML_monthly_count_score = 1.7880452017953328
SD_AML_monthly_count_score = 1.8330969003344981

app = Flask(__name__)

# Initialize a variable to store received data
received_data = []

# Configure JWT
app.config['JWT_SECRET_KEY'] = '123456789'  # Replace with a strong, secret key
jwt = JWTManager(app)

# Your secret API key (replace with your actual key)
SECRET_API_KEY = "123456789"

# Middleware to check the API key
#def require_api_key(func):
    #@wraps(func)
   # def check_api_key(*args, **kwargs):
        #api_key = request.headers.get("APIKey")

       # if api_key == SECRET_API_KEY:
           #print(api_key, SECRET_API_KEY)
            #return func(*args, **kwargs)
       # else:
            #return jsonify({"error": "Authentication failed - Incorrect API KEY"}), 401

   # return check_api_key

# Define user authentication logic (you need to implement this)
#def authenticate(username, password):
    # Check the username and password against your user database
     #Return True if authentication is successful, otherwise return False
    #if username == 'MAHRUKH' and password == 'Mah@123456':
        #return True
   #return False


@app.route('/postman', methods=['GET', 'POST'])
#@require_api_key
def receive_postman_request():
    if request.method == 'GET':
        # Handle GET request to retrieve data
        return jsonify(received_data)  # Assuming received_data is a list of data
    elif request.method == 'POST':

        # Handle POST request to receive and store data
        try:
            data = request.get_json()
        except Exception as e:
            return {"error": f"Failed to parse JSON data: {str(e)}"}, 400
        
        # Authenticate the user
        #request_details = data.get('requestDetails', {})  # Get the requestDetails object
        #username = request_details.get('username')  # Access the username field
        #password = request_details.get('password')  # Access the password field

        #if not authenticate(username, password):
            #return {"error": "Authentication failed - Incorrect username or password"}, 401
        
        # Cleanse data 
        try:
            uncleaned_data = {
                "transaction_uuid": data["requestData"]["transaction_uuid"],
                "transaction_type": data["requestData"]["transaction_type"],  # Convert to float
                "account_age_score": float(data["requestData"]["account_age_score"]),  # Convert to float
                "new_account_score": float(data["requestData"]["new_account_score"]),  # Convert to float
                "AML_first_transaction_score": float(data["requestData"]["AML_first_transaction_score"]),  # Convert to float
                "AML_last_transaction_score": float(data["requestData"]["AML_last_transaction_score"]),  # Convert to float
                "sleeper_score": float(data["requestData"]["sleeper_score"]),  # Convert to float
                "dormant_score": float(data["requestData"]["dormant_score"]),  # Convert to float
                "account_risk_score": float(data["requestData"]["account_risk_score"]),  # Convert to float
                "merchant_country_risk_score": float(data["requestData"]["merchant_country_risk_score"]),  # Convert to float
                "mcc_risk_score": float(data["requestData"]["mcc_risk_score"]),  # Convert to float
                "currency_risk_score": float(data["requestData"]["currency_risk_score"]),  # Convert to float
                "high_value_score": float(data["requestData"]["high_value_score"]),  # Convert to float
                "avg_txn_variance_score": float(data["requestData"]["avg_txn_variance_score"]),  # Convert to float
                "max_txn_variance_score": float(data["requestData"]["max_txn_variance_score"]),  # Convert to float
                "daily_sum_variance_score": float(data["requestData"]["daily_sum_variance_score"]),  # Convert to float
                "monthly_avg_count_variance_score": float(data["requestData"]["monthly_avg_count_variance_score"]),  # Convert to float
                "daily_avg_count_variance_score": float(data["requestData"]["daily_avg_count_variance_score"]),  # Convert to float
                "monthly_avg_sum_variance_score": float(data["requestData"]["monthly_avg_sum_variance_score"]),  # Convert to float
                "AML_daily_sum_score": float(data["requestData"]["AML_daily_sum_score"]),  # Convert to float
                "AML_daily_count_score": float(data["requestData"]["AML_daily_count_score"]),  # Convert to float
                "AML_monthly_sum_score": float(data["requestData"]["AML_monthly_sum_score"]),  # Convert to float
                "AML_monthly_count_score": float(data["requestData"]["AML_monthly_count_score"]),  # Convert to float
                "weight": float(data["requestData"]["weight"]),  # Convert to float
            }
    
            cleaned_data = {
                "transaction_uuid": data["requestData"]["transaction_uuid"],
                "transaction_type": data["requestData"]["transaction_type"],  # Convert to float
                "account_age_score": float(data["requestData"]["account_age_score"]),  # Convert to float
                "new_account_score": float(data["requestData"]["new_account_score"]),  # Convert to float
                "AML_first_transaction_score": float(data["requestData"]["AML_first_transaction_score"]),  # Convert to float
                "AML_last_transaction_score": float(data["requestData"]["AML_last_transaction_score"]),  # Convert to float
                "sleeper_score": float(data["requestData"]["sleeper_score"]),  # Convert to float
                "dormant_score": float(data["requestData"]["dormant_score"]),  # Convert to float
                "account_risk_score": float(data["requestData"]["account_risk_score"]),  # Convert to float
                "merchant_country_risk_score": float(data["requestData"]["merchant_country_risk_score"]),  # Convert to float
                "mcc_risk_score": float(data["requestData"]["mcc_risk_score"]),  # Convert to float
                "currency_risk_score": float(data["requestData"]["currency_risk_score"]),  # Convert to float
                "high_value_score": float(data["requestData"]["high_value_score"]),  # Convert to float
                "avg_txn_variance_score": float(data["requestData"]["avg_txn_variance_score"]),  # Convert to float
                "max_txn_variance_score": float(data["requestData"]["max_txn_variance_score"]),  # Convert to float
                "daily_sum_variance_score": float(data["requestData"]["daily_sum_variance_score"]),  # Convert to float
                "monthly_avg_count_variance_score": float(data["requestData"]["monthly_avg_count_variance_score"]),  # Convert to float
                "daily_avg_count_variance_score": float(data["requestData"]["daily_avg_count_variance_score"]),  # Convert to float
                "monthly_avg_sum_variance_score": float(data["requestData"]["monthly_avg_sum_variance_score"]),  # Convert to float
                "AML_daily_sum_score": float(data["requestData"]["AML_daily_sum_score"]),  # Convert to float
                "AML_daily_count_score": float(data["requestData"]["AML_daily_count_score"]),  # Convert to float
                "AML_monthly_sum_score": float(data["requestData"]["AML_monthly_sum_score"]),  # Convert to float
                "AML_monthly_count_score": float(data["requestData"]["AML_monthly_count_score"]),  # Convert to float
            }
        except KeyError as e:
            return {"error": f"KeyError: {str(e)}"}, 400
        except ValueError as e:
            return {"error": f"ValueError: {str(e)}"}, 400

        # Convert to data frame
        dataDF = pd.DataFrame([cleaned_data])
        dataDF1 = pd.DataFrame([uncleaned_data])
        
        # Call function to perform calculations and get the response
        response_data = perform_calculations(dataDF, dataDF1)
        
        return jsonify(response_data)
    
# Add the @jwt_required decorator to protect this route
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected_resource():
    current_user = get_jwt_identity()
    return jsonify(message=f'Hello, {current_user}! This is a protected resource.')

def perform_calculations(dataDF, dataDF1):
    #generate a unique ID
    unique_id = str(uuid.uuid4())
    
    #Timeline Score
    new_timeline = pd.DataFrame(dataDF, columns=['account_age_score', 'new_account_score', 'AML_first_transaction_score', 'AML_last_transaction_score', 'sleeper_score', 'dormant_score'])
    new_timeline1 = pd.DataFrame(dataDF1, columns=['account_age_score', 'new_account_score', 'AML_first_transaction_score', 'AML_last_transaction_score', 'sleeper_score', 'dormant_score'])
    new_timeline_score = new_timeline1.sum(axis=1).at[0]

    # SituationScore
    new_situation = pd.DataFrame(dataDF, columns=['account_risk_score', 'merchant_country_risk_score', 'mcc_risk_score', 'currency_risk_score', 'high_value_score'])
    new_situation1 = pd.DataFrame(dataDF1, columns=['account_risk_score', 'merchant_country_risk_score', 'mcc_risk_score', 'currency_risk_score', 'high_value_score'])
    new_situation_score = new_situation1.sum(axis=1).at[0]

    # VarianceScore
    new_variance = pd.DataFrame(dataDF, columns=['avg_txn_variance_score', 'max_txn_variance_score', 'daily_sum_variance_score', 'monthly_avg_count_variance_score', 'daily_avg_count_variance_score', 'monthly_avg_sum_variance_score'])
    new_variance1 = pd.DataFrame(dataDF1, columns=['avg_txn_variance_score', 'max_txn_variance_score', 'daily_sum_variance_score', 'monthly_avg_count_variance_score', 'daily_avg_count_variance_score', 'monthly_avg_sum_variance_score'])
    new_variance_score = new_variance1.sum(axis=1).at[0]

    # VelocityScore
    new_velocity = pd.DataFrame(dataDF, columns=['AML_daily_sum_score', 'AML_daily_count_score', 'AML_monthly_sum_score', 'AML_monthly_count_score'])
    new_velocity1 = pd.DataFrame(dataDF1, columns=['AML_daily_sum_score', 'AML_daily_count_score', 'AML_monthly_sum_score', 'AML_monthly_count_score'])
    new_velocity_score = new_velocity1.sum(axis=1).at[0]

    # overallScore and Results
    new_AML_preliminary_Score = new_timeline_score + new_situation_score + new_variance_score + new_velocity_score
    
    # Loading saved models
    knn_TL = joblib.load('knn1_V1.pkl')
    knn_VS = joblib.load('knn3_V1.pkl')
    knn_VL = joblib.load('knn4_V1.pkl')
    knn_ST = joblib.load('knn2_V1.pkl')

    
    if knn_TL is None or knn_VS is None or knn_VL is None or knn_ST is None :
        return {"error": "Failed to load the model"}, 500

    # Call predict on the loaded model
    try:
        tl_result = knn_TL.predict(new_timeline)
        vs_result = knn_VS.predict(new_variance)
        vl_result = knn_VL.predict(new_velocity)
        st_result = knn_ST.predict(new_situation)
        
    except Exception as e:
        return {"error": f"Prediction error: {str(e)}"}, 500
    
    # formatting the results
    if tl_result[0] == 0:
        new_AML_Timeline_Result = "Accept"
    elif tl_result[0] == 1:
        new_AML_Timeline_Result = "Review"
    else:
        new_AML_Timeline_Result = "Reject"
   
    if vs_result[0] == 0:
        new_AML_Variance_Result = "Accept"
    elif vs_result[0] == 1:
        new_AML_Variance_Result = "Review"
    else:
        new_AML_Variance_Result = "Reject"
    
    if vl_result[0] == 0:
        new_AML_Velocity_Result = "Accept"
    elif vl_result[0] == 1:
        new_AML_Velocity_Result = "Review"
    else:
        new_AML_Velocity_Result = "Reject"
    
    if st_result[0] == 0:
        new_AML_Situation_Result = "Accept"
    elif st_result[0] == 1:
        new_AML_Situation_Result = "Review"
    else:
        new_AML_Situation_Result = "Reject"
    
    weight = dataDF1["weight"].iloc[0]
    new_AML_Score =  new_AML_preliminary_Score * weight
    
    #Calculation of Final result
    # Calculation of Final result
    if new_AML_Score <= 15.0:
        new_AML_Result = "Accept"
    elif (new_AML_Score > 12.0) and (new_AML_Score <= 17.0):
        new_AML_Result = "Review"
    elif (new_AML_Score > 17.0) and (new_AML_Score <= 27.5):
        new_AML_Result = "Review"
    else:
        new_AML_Result = "Reject"

    
    api_key = "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"
    content = "Can you please summarise: Merchant Level TimeLine result: " + new_AML_Timeline_Result + " Merchant Level Variance result: " + new_AML_Variance_Result + " Merchant Level Velocity result: " + new_AML_Velocity_Result +" Merchant Level Situation result: " + new_AML_Situation_Result + " Hence Merchant Final result: " + new_AML_Result
    endpoint = "https://api.openai.com/v1/chat/completions"
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a joke."},
        {"role": "assistant", "content": "Why did the chicken cross the road?"},
        {"role": "user", "content": "I don't know, why did the chicken cross the road?"}
    ]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "assistant",
                "content": content
            }
        ]
    }
    try:
        response = requests.post(endpoint, json=data, headers=headers)
        response.raise_for_status()  # Raise an exception for non-2xx responses
        response_data = response.json()
        assistant_reply = response_data["choices"][0]["message"]["content"]
        print("Assistant:", assistant_reply)
    except requests.exceptions.RequestException as e:
        return {"error": f"ChatGPT Request error: {str(e)}"}, 500
    
    # Perform some calculations or predictions using the loaded model
    # Replace this with your actual calculations
    result = {
        "TM_ID": unique_id,
        "ReferenceId": dataDF.loc[0, "transaction_uuid"],
        "AMLResult": new_AML_Result,
        "AMLScore" : new_AML_Score,
        "AMLPreliminaryScore": new_AML_preliminary_Score,
        "timelineResult": new_AML_Timeline_Result,
        "timelineScore": new_timeline_score,
        "varianceResult": new_AML_Variance_Result,
        "varianceScore": new_variance_score,
        "velocityResult": new_AML_Velocity_Result,
        "velocityScore": new_velocity_score,
        "situationResult": new_AML_Situation_Result,
        "situationScore": new_situation_score,
        "comment": assistant_reply,
        "alert": "Slot for Alerts",
    }
    
    # Return the JSON response with the correct content type
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9080, debug=True)
