import streamlit as st
import requests
from datetime import datetime, timedelta
from inventory import inventory_df


API_KEY = "fcfcb66b35cb46e1b487e2f3ab922bad"
def get_recipes_from_api(ingredients):
    ingredient_query = ",".join(ingredients)
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredient_query}&apiKey={API_KEY}&number=5"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []
    
def show_recipes():
    st.title("🎭 Recipe Suggestions")
    st.write("Find recipes using ingredients that are expiring soon.")
    
    today = datetime.today().date()
    expiring_items = inventory_df[inventory_df["Expiry Date"] <= today + timedelta(days=3)]["Item"].tolist()
    
    if expiring_items:
        st.subheader("🔄 Expiring Ingredients")
        st.write(", ".join(expiring_items))
        
        suggested_recipes = get_recipes_from_api(expiring_items)
        
        if suggested_recipes:
            st.subheader("🍽️ Suggested Recipes")
            for recipe in suggested_recipes:
                st.markdown(f"### {recipe['title']}")
                st.image(recipe['image'], width=300)
                st.markdown(f"[View Recipe](https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-')}-{recipe['id']})", unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.info("No matching recipes found. Try adding more ingredients.")
    else:
        st.info("No ingredients are expiring soon.")
    
    st.subheader("🔍 Search for Recipes")
    search_term = st.text_input("Enter an ingredient:")
    
    if search_term:
        search_results = get_recipes_from_api([search_term])
        if search_results:
            for recipe in search_results:
                st.markdown(f"### {recipe['title']}")
                st.image(recipe['image'], width=300)
                st.markdown(f"[View Recipe](https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-')}-{recipe['id']})", unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.warning("No recipes found for that ingredient.")