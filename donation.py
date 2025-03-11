import os
import json
import pandas as pd
import numpy as np
import streamlit as st


food_donation_file = r"C:\Users\G6\Desktop\hackathon\data\food_donation_data.json"
def load_donation_data():
    try:
        with open(food_donation_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def update_donation_data(expiring_items):
    donation_data = load_donation_data()

    # Convert current donation list into a set for quick lookups
    existing_donations = {(entry["Available_Food"], entry["Quantity"]) for entry in donation_data}

    for _, row in expiring_items.iterrows():
        new_entry = (row["Item"], int(row["Quantity"]))

        # Only add new items that are NOT already in the donation list
        if new_entry not in existing_donations:
            donation_data.append({
                "Restaurant": "Your Business Name",
                "City": "Your City",
                "Available_Food": row["Item"],
                "Quantity": int(row["Quantity"]),
                "NGO_Contact": "NGO Contact Placeholder"
            })
    
    # Save only if there are new additions
    with open(food_donation_file, "w") as file:
        json.dump(donation_data, file, indent=4)

def show_donation():
    st.title("🤝 Food Donation")

    # Load existing donation data
    def load_donation_data():
        if os.path.exists(food_donation_file):
            with open(food_donation_file, "r") as file:
                return json.load(file)
        return []

    def save_donation_data(data):
        with open(food_donation_file, "w") as file:
            json.dump(data, file, indent=4)

    donation_data = load_donation_data()

    st.subheader("📦 Available Food Donations")
    if donation_data:
        donation_df = pd.DataFrame(donation_data)
        st.dataframe(donation_df)
    else:
        st.info("No food donations available at the moment.")

    # Form to add a new food donation
    st.subheader("➕ Add Food Donation")
    restaurant = st.text_input("Restaurant Name")
    city = st.text_input("City")
    available_food = st.text_input("Available Food")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    ngo_contact = st.text_input("NGO Contact Information")

    if st.button("Donate Food"):
        if restaurant and city and available_food and quantity and ngo_contact:
            new_donation = {
                "Restaurant": restaurant,
                "City": city,
                "Available_Food": available_food,
                "Quantity": quantity,
                "NGO_Contact": ngo_contact
            }
            donation_data.append(new_donation)
            save_donation_data(donation_data)
            st.success("Food donation added successfully! ✅")
            st.experimental_rerun()
        else:
            st.error("Please fill in all fields before submitting.")

    st.subheader("📞 Contact NGOs for Pickup")
    if donation_data:
        for entry in donation_data:
            st.markdown(
                f"""📍 **{entry['City']}** - {entry['Available_Food']} ({entry['Quantity']} servings)  
                🏬 **{entry['Restaurant']}**  
                📞 **Contact:** {entry['NGO_Contact']}""",
                unsafe_allow_html=True
            )
            st.markdown("---")
