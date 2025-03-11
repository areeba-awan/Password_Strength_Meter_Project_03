# Description: This is a simple password strength meter tool that allows users to check the strength of their passwords, generate secure passwords, and save them securely.

import streamlit as st
import re
import random
import string
import pandas as pd

# Initialize password history if not set
if 'password_history' not in st.session_state:
    st.session_state.password_history = []

# List of commonly used weak passwords
COMMON_PASSWORDS = {"password123", "12345678", "qwerty", "admin", "letmein"}

# Function to check password strength
def evaluate_password(password):
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("🔴 Password should be at least 8 characters long.")
    
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("🟠 Use a mix of uppercase and lowercase letters.")
    
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("🟡 Include at least one number.")
    
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("🔵 Add a special character (!@#$%^&*).")
    
    if password in COMMON_PASSWORDS:
        score = 1  # Automatically weak if it's too common
        feedback = ["🔴 This password is too common. Choose something unique!"]
    
    return score, feedback

# Function to generate a secure password
def generate_secure_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

# Prevent saving duplicate passwords
def is_password_duplicate(password):
    return any(p["password"] == password for p in st.session_state.password_history)

# Streamlit UI
st.set_page_config(page_title="🔐 Ultimate Password Strength Meter", layout="centered")
st.markdown("""
    <style>
        body {
            background-color: #1e1e2f;
            color: white;
        }
        .stTextInput, .stButton>button, .stSlider {
            border-radius: 10px;
            font-size: 16px;
        }
        .stButton>button {
            background: linear-gradient(90deg, #ff6ec4, #7873f5); /* Pink to Purple */
            color: white;
            border: none;
            padding: 10px 20px;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #7873f5, #ff6ec4); /* Purple to Pink */
            
        }
        .stSuccess {
            color: #4caf50;
        }
        .stWarning {
            color: #ff9800;
        }
        .stError {
            color: #f44336;
        }
        .stInfo {
            color: #2196f3;
        }
    </style>
""", unsafe_allow_html=True)


st.title("🔐 Ultimate Password Strength Meter")
st.write("**Welcome to the Areeba's Ultimate Password Strength Checker!**")
st.write("**Use this tool to check the strength of your passwords, generate secure passwords, and save them securely.**")

# Sidebar menu
menu_choice = st.sidebar.selectbox("📋 Menu", ["Check Password", "Generate Password", "Saved Passwords"])

if menu_choice == "Check Password":
    password = st.text_input("🔑 Enter your password", type="password")
    account = st.text_input("📌 Account name (optional)")
    
    if st.button("🔍 Check Strength"):
        if password:
            score, feedback = evaluate_password(password)
            
            # Display progress bar with color-coded strength levels
            st.progress(score / 4)
            if score == 4:
                st.success("✅ Strong Password!")
            elif score == 3:
                st.warning("⚠️ Moderate Password. Consider improving it.")
            else:
                st.error("❌ Weak Password. Improve it using the suggestions below.")
            
            for tip in feedback:
                st.write(tip)
        else:
            st.warning("⚠️ Please enter a password to check.")
    
    if st.button("💾 Save Password"):
        if password and account:
            if is_password_duplicate(password):
                st.error("🚫 This password is already saved. Choose a different one!")
            else:
                st.session_state.password_history.append({"account": account, "password": password})
                st.success("✅ Password saved securely!")

elif menu_choice == "Generate Password":
    length = st.slider("🔢 Choose password length", min_value=8, max_value=20, value=12)
    if st.button("🔄 Generate Password"):
        new_password = generate_secure_password(length)
        st.text_area("🔑 Your Secure Password", new_password)
    
elif menu_choice == "Saved Passwords":
    st.subheader("🔒 Your Saved Passwords")
    if st.session_state.password_history:
        df = pd.DataFrame(st.session_state.password_history)
        st.dataframe(df.style.set_properties(**{'background-color': '#1e2f2f', 'color': 'white'}))
    else:
        st.info("ℹ️ No passwords saved yet.")

st.markdown(
    """
    <hr>
    <p style='text-align: center; color: #555;'>
        Made with ❤️ by Areeba Awan | Stay Safe Stay Happy ! 🔐
    </p>
    """,
    unsafe_allow_html=True
)