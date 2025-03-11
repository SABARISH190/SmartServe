import streamlit as st
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import numpy as np



def show_ai_waste_prediction():
    st.title("🧠 AI Waste Prediction")
    st.write("💡 Use AI to estimate and manage food waste in your restaurant!")

    @st.cache_data
    def load_data():
        file_path = r"C:\Users\G6\Desktop\hackathon\data\Food Waste data and research - by country.csv"
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        else:
            st.error("Dataset not found. Please check the file path.")
            return None
    
    df = load_data()

    if df is not None:
        st.subheader("🌟 Dataset Preview")
        st.dataframe(df.head(75))  # Show first 75 rows

        def train_model(df):
            df = df.dropna()
            if not {'Household estimate (tonnes/year)', 'Retail estimate (tonnes/year)', 'Food service estimate (tonnes/year)'}.issubset(df.columns):
                st.error("Missing required columns in dataset.")
                return None
            
            X = df[['Household estimate (tonnes/year)', 'Retail estimate (tonnes/year)']]
            y = df['Food service estimate (tonnes/year)']

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = LinearRegression()
            model.fit(X_train, y_train)

            model_path = "waste_prediction_model.pkl"
            joblib.dump(model, model_path)
            return model

        model = train_model(df)
        
        @st.cache_resource
        def load_model():
            model_path = "waste_prediction_model.pkl"
            if os.path.exists(model_path):
                return joblib.load(model_path)
            else:
                st.error("Model not found. Please train the model first.")
                return None
        
        model = load_model()

        st.subheader("📌 Predict Food Waste for Your Restaurant")
        household_waste = st.number_input("Enter Estimated Household Waste (tonnes/year)", min_value=1000, max_value=100000, value=1000, step=10000)
        retail_waste = st.number_input("Enter Estimated Retail Waste (tonnes/year)", min_value=5000, max_value=5000000, value=5000, step=20000)
        
        if st.button("🔍 Predict Waste"):
            if model:
                input_data = np.array([[household_waste, retail_waste]])
                prediction = model.predict(input_data)
                st.success(f"Estimated Food Service Waste: **{prediction[0]:,.2f} tonnes/year**")
                
                st.subheader("💡 Recommendations")
                if prediction[0] > 50000:
                    st.warning("⚠️ High Waste Alert! Consider reducing overproduction and optimizing portion sizes.")
                else:
                    st.success("✅ Your waste level is under control. Keep using AI for better forecasting!")
            else:
                st.error("Prediction model is not available. Please train the model first.")


if __name__ == "__main__":
    show_ai_waste_prediction()