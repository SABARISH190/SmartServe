# Inventory Management
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from donation import update_donation_data
# File path for inventory data

inventory_file = r"C:\Users\G6\Desktop\hackathon\data\inventory_expiry_tracking.csv"
def load_inventory():
    try:
        df = pd.read_csv(inventory_file)
        df["Expiry Date"] = pd.to_datetime(df["Expiry Date"], errors='coerce').dt.date  # Remove time part
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Item", "Purchase Date", "Expiry Date", "Quantity", "Storage Method"])

def save_inventory(df):
    df.to_csv(inventory_file, index=False)
inventory_df = load_inventory()

def check_expiry_alerts(df):
    today = datetime.today()
    if 'Expiry Date' not in df.columns:
        st.error("'Expiry Date' column not found in the inventory.")
        return pd.DataFrame(), pd.DataFrame()

    df["Expiry Date"] = pd.to_datetime(df["Expiry Date"], errors='coerce')  # Handle invalid dates
    soon_to_expire = df[df["Expiry Date"] <= today + timedelta(days=3)]
    expired = df[df["Expiry Date"] < today]
    return soon_to_expire, expired


def show_inventory():
    st.title("📦 Inventory & Expiry Alerts")
    inventory_df = load_inventory()
    st.subheader("📋 Current Inventory")
    st.dataframe(inventory_df)

    st.subheader("➕ Add New Item")
    item = st.text_input("Item Name")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    storage_method = st.text_input("Storage Method")
    purchase_date = st.date_input("Purchase Date", value=datetime.today())
    expiry_date = st.date_input("Expiry Date", value=datetime.today() + timedelta(days=7))

    if st.button("Add to Inventory"):
        new_entry = pd.DataFrame([[item, purchase_date, expiry_date, quantity, storage_method]],
                                columns=inventory_df.columns)
        inventory_df = pd.concat([inventory_df, new_entry], ignore_index=True)
        save_inventory(inventory_df)
        st.success(f"{item} added to inventory!")
        st.rerun()

    st.subheader("⚠️ Expiry Alerts")
    today = datetime.today().date()
    expiring_soon = inventory_df[inventory_df["Expiry Date"] <= today + timedelta(days=2)]
    if not expiring_soon.empty:
        st.table(expiring_soon)
        if st.button("Add Expiring Items to Donation List"):
            update_donation_data(expiring_soon)
            st.success("New expiring items added to the donation list (duplicates skipped)!")
            st.rerun()
    else:
        st.info("No items expiring soon.")


if __name__ == "__main__":
    show_inventory()