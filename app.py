# -*- coding: utf-8 -*-
import os
import pandas as pd
from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

# === CONSTANTS ===
MODEL_PATH = "C:/Users/harsh/Desktop/projects/Churn Prediction/churn_model.pkl"
DATA_PATH = "C:/Users/harsh/Desktop/projects/Churn Prediction/Customer-Churn.csv"

# === LOAD DATASET ===
df_1 = pd.read_csv(DATA_PATH)
df_1['TotalCharges'] = pd.to_numeric(df_1['TotalCharges'], errors='coerce')
df_1['TotalCharges'].fillna(df_1['TotalCharges'].mean(), inplace=True)
df_1['SeniorCitizen'] = df_1['SeniorCitizen'].apply(lambda x: 'yes' if x == 1 else 'no')
df_1.drop(columns=['customerID'], axis=1, inplace=True)

# Create tenure_group
labels = ["{0} - {1}".format(i, i + 11) for i in range(1, 72, 12)]
df_1['tenure_group'] = pd.cut(df_1.tenure.astype(int), range(1, 80, 12), right=False, labels=labels)
df_1.drop(columns=['tenure'], axis=1, inplace=True)

@app.route("/")
def loadPage():
    return render_template('page.html', query="")


@app.route("/", methods=['POST'])
def predict():
    try:
        input_data = [
            request.form['query1'],
            float(request.form['query2']),
            float(request.form['query3']),
            request.form['query4'], request.form['query5'], request.form['query6'], request.form['query7'],
            request.form['query8'], request.form['query9'], request.form['query10'], request.form['query11'],
            request.form['query12'], request.form['query13'], request.form['query14'], request.form['query15'],
            request.form['query16'], request.form['query17'], request.form['query18'],
            int(request.form['query19'])
        ]

        # Build input dict
        input_dict = {
            'SeniorCitizen': 'yes' if input_data[0] == '1' else 'no',
            'MonthlyCharges': input_data[1],
            'TotalCharges': input_data[2],
            'gender': input_data[3],
            'Partner': input_data[4],
            'Dependents': input_data[5],
            'PhoneService': input_data[6],
            'MultipleLines': input_data[7],
            'InternetService': input_data[8],
            'OnlineSecurity': input_data[9],
            'OnlineBackup': input_data[10],
            'DeviceProtection': input_data[11],
            'TechSupport': input_data[12],
            'StreamingTV': input_data[13],
            'StreamingMovies': input_data[14],
            'Contract': input_data[15],
            'PaperlessBilling': input_data[16],
            'PaymentMethod': input_data[17],
        }

        tenure = input_data[18]
        labels = ["{0} - {1}".format(i, i + 11) for i in range(1, 72, 12)]
        input_dict['tenure_group'] = pd.cut([tenure], range(1, 80, 12), right=False, labels=labels)[0]

        # Convert to DataFrame
        new_df = pd.DataFrame([input_dict])
        df_2 = pd.concat([df_1, new_df], ignore_index=True)
        df_2 = pd.get_dummies(df_2)

        # Load model
        if not os.path.exists(MODEL_PATH):
            return render_template('page.html', output1="Model file not found.", output2="Please ensure 'churn_model.pkl' exists.")

        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)

        # Ensure all model input columns exist in df_2
        for col in model.feature_names_in_:
            if col not in df_2.columns:
                df_2[col] = 0  # Add missing dummy column with default 0

        # Reorder to match model's training input
        df_2 = df_2[model.feature_names_in_]
        final_input = df_2.tail(1)

        # Predict
        prediction = model.predict(final_input)[0]
        probability = model.predict_proba(final_input)[0][1]

        if prediction == 1:
            o1 = "This customer is likely to churn!"
            o2 = f"Confidence: {probability * 100:.2f}%"
        else:
            o1 = "This customer is likely to stay."
            o2 = f"Confidence: {probability * 100:.2f}%"

        return render_template('page.html', output1=o1, output2=o2, **request.form)

    except Exception as e:
        print("ERROR:", e)  # Debug in terminal
        return render_template('page.html', output1="Error Occurred", output2=str(e))

if __name__ == "__main__":
    app.run(debug=True)


