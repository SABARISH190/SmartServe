import streamlit as st
import os
import base64
import time

# Function to show home page
def show_home():
    # --- Custom Styling ---
    st.markdown(
        """
        <style>
            .center { text-align: center; }
            .stApp { background-color: black; }
            .card {
                background: black;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                text-align: center;
                width: 60%;
                margin: auto;
            }
            .carousel-container {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 400px; /* Adjusted height */
                overflow: hidden;
            }
            .carousel-container img {
                max-height: 300px;
                border-radius: 10px;
                transition: opacity 1s ease-in-out;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- Logo ---
    logo_path = r"C:\Users\G6\Desktop\hackathon\assets\images\logo final.png"  # Use a relative path
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as img_file:
            logo_base64 = base64.b64encode(img_file.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" width="120"/>'
    else:
        logo_html = ""

    # --- Centered Logo and Title ---
    

    # --- Image Carousel ---
    image_paths = [
        r"C:\Users\G6\Desktop\hackathon\assets\images\1.png",
    r"C:\Users\G6\Desktop\hackathon\assets\images\4.png",
    r"C:\Users\G6\Desktop\hackathon\assets\images\robo.png",
    r"C:\Users\G6\Desktop\hackathon\assets\images\serve.png",
    r"C:\Users\G6\Desktop\hackathon\assets\images\13.png",
    r"C:\Users\G6\Desktop\hackathon\assets\images\14.png",
    r"C:\Users\G6\Desktop\hackathon\assets\images\kitchen.png",
    r"C:\Users\G6\Desktop\hackathon\assets\images\16.png",
    r"C:\Users\G6\Desktop\hackathon\assets\images\17.png",
    r"C:\Users\G6\Desktop\hackathon\assets\images\fridge.png",
    r"C:\Users\G6\Desktop\hackathon\assets\images\19.png",
    r"C:\Users\G6\Desktop\hackathon\assets\images\20.png"
    ]
    image_paths = [img for img in image_paths if os.path.exists(img)]

    def image_carousel(images, delay=2):
        if images:
            img_slot = st.empty()
            for img in images:
                img_slot.image(img, use_container_width=True)
                time.sleep(delay)  # This is still blocking, see alternative below
        else:
            st.warning("No images found for the carousel.")

    # Run the carousel
    image_carousel(image_paths)
    
    st.markdown("## Donate & Earn Points 🎉", unsafe_allow_html=True)
    st.write(
        "Contribute excess food and earn reward points. Together, we can reduce food waste and help the community!"
    )

    # Example Donation Button
    if st.button("Donate Now"):
        st.success("Thank you for your donation! 🎊 You've earned 10 points!")

# Run Streamlit App
if __name__ == "__main__":
    show_home()
