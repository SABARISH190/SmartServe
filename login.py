import streamlit as st
import pandas as pd
import os

# File path for storing user credentials
user_data_file = r"C:\Users\G6\Desktop\hackathon\data\users.json"

def load_users():
    try:
        return pd.read_csv(user_data_file)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Username", "Phone Number", "Restaurant Name", "City", "Password"])

def save_users(df):
    df.to_csv(user_data_file, index=False)

def signup():
    st.subheader("🔐 Sign Up")
    username = st.text_input("Username")
    phone = st.text_input("Phone Number")
    restaurant = st.text_input("Restaurant Name")
    city = st.text_input("City")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Sign Up"):
        if password == confirm_password:
            users = load_users()
            if username in users["Username"].values:
                st.error("Username already exists. Choose a different one.")
            else:
                new_user = pd.DataFrame([[username, phone, restaurant, city, password]],
                                        columns=users.columns)
                users = pd.concat([users, new_user], ignore_index=True)
                save_users(users)
                st.success("Account created successfully! Please log in.")
        else:
            st.error("Passwords do not match!")

def login():
    st.subheader("🔑 Log In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Log In"):
        users = load_users()
        user = users[(users["Username"] == username) & (users["Password"] == password)]
        
        if not user.empty:
            st.success(f"Welcome back, {username}!")
            st.session_state["logged_in"] = True
            st.session_state["user_data"] = user.iloc[0].to_dict()
            st.rerun()
        else:
            st.error("Invalid username or password!")

def login_page():
    st.title("🍽️ Food Waste Management - Authentication")
    option = st.radio("Select an option", ["Log In", "Sign Up"])
    if option == "Log In":
        login()
    else:
        signup()

if __name__ == "__main__":
    login_page()