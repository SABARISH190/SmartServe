import streamlit as st
import pandas as pd
import os


leaderboard_file = r"C:\Users\G6\Desktop\hackathon\data\user_points.csv"

def load_leaderboard():
    try:
        df = pd.read_csv(leaderboard_file)
        if "Points" in df.columns:
            df = df.sort_values(by="Points", ascending=False)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Username", "Points", "Level"])

def save_leaderboard(df):
    df.to_csv(leaderboard_file, index=False)

def update_points(username, points):
    df = load_leaderboard()
    if username in df["Username"].values:
        df.loc[df["Username"] == username, "Points"] += points
    else:
        new_entry = pd.DataFrame([[username, points, "Beginner"]], columns=df.columns)
        df = pd.concat([df, new_entry], ignore_index=True)
    
    # Assign Levels Based on Points
    df["Level"] = df["Points"].apply(lambda x: "Expert" if x > 100 else "Intermediate" if x > 50 else "Beginner")
    
    save_leaderboard(df)

def show_leaderboard():
    st.title("🏆 Food Waste Warriors Leaderboard")
    df = load_leaderboard()

    if df.empty:
        st.info("No leaderboard data available.")
    else:
        st.write("### Top Contributors")
        for i, row in df.iterrows():
            st.write(f"**{i+1}. {row['Username']}** - {row['Points']} Points ({row['Level']})")

# Example: Update Points when a user donates food
if st.button("Donate Food & Earn Points"):
    username = st.text_input("Enter Your Username:")
    if username:
        update_points(username, 10)
        st.success(f"🎉 {username} earned 10 points! Check the leaderboard.")