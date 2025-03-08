# #This is password strength meter that i build with python and streamlit

import streamlit as st
import re
import random
import string

COMMON_PASSWORDS = [
    "password", 
    "123456", 
    "12345678", 
    "qwerty", 
    "abc123", 
    "password1", 
    "admin"
    ]

# generate a strong password
def generate_strong_password():
    """Generate a strong password that meets all criteria."""
    length = 12
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Function to check password strength
def check_password_strength(password):
    """Evaluate the strength of the password and provide feedback."""
    score = 0
    feedback = []

    # Length Check
    if len(password) >= 8:
        score += 1
        feedback.append("✅ At least 8 characters long.")
    else:
        feedback.append("❌ Password should be at least 8 characters long.")

    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
        feedback.append("✅ Contains both uppercase and lowercase letters.")
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")

    # Digit Check
    if re.search(r"\d", password):
        score += 1
        feedback.append("✅ Contains at least one number (0-9).")
    else:
        feedback.append("❌ Add at least one number (0-9).")

    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
        feedback.append("✅ Contains at least one special character (!@#$%^&*).")
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")

    # Blacklist Check
    if password.lower() in COMMON_PASSWORDS:
        feedback.append("❌ Password is too common and easily guessable.")
        score = 0  

    return score, feedback

# this will provide tips for creating memorable passwords
def get_password_tip():
    """Provide a creative tip for creating a memorable password."""
    tips = [
        "🌟 Use a phrase: Turn 'I love hiking in the mountains!' into 'ILh!tM@2023'.",
        "🌟 Combine words: Mix 'Sunshine' and 'Rainbow' to create 'SunBow!2023'.",
        "🌟 Use acronyms: 'My favorite color is blue' becomes 'Mfc!b@2023'.",
        "🌟 Add numbers and symbols: Replace letters with numbers, like 'P@ssw0rd!'.",
        "🌟 Use a pattern: Create a pattern like 'Aa1!Bb2@Cc3#' for easy recall."
    ]
    return random.choice(tips)

# Streamlit App
def main():
   
    st.title("Password Strength Meter")
    st.write("Check the strength of your password and get suggestions to improve it.")

    # Initialize state for password history
    if "password_history" not in st.session_state:
        st.session_state.password_history = []

    
    password = st.text_input("Enter your password:", type="password", key="password_input", help="Start typing to see real-time feedback.")

    # Real-time feedback section
    if password:
        # Check password strength and get feedback
        score, feedback = check_password_strength(password)

        # Display progress bar
        st.subheader("Password Strength Progress:")
        progress = score / 4  # 4 criteria in total
        st.progress(progress)

        # Display feedback messages
        st.subheader("Password Analysis:")
        for message in feedback:
            if "❌" in message:
                st.error(message)  
            elif "✅" in message:
                st.success(message) 
            else:
                st.warning(message)  

        # Display strength score
        st.subheader("Strength Score:")
        if score == 4:
            st.success("✅ Strong Password!")
        elif score == 3:
            st.warning("⚠️ Moderate Password - Consider adding more security features.")
        else:
            st.error("❌ Weak Password - Improve it using the suggestions above.")

    # Password generator section
    st.subheader("Need a Strong Password?")
    if st.button("Generate Strong Password"):
        strong_password = generate_strong_password()
        st.code(strong_password)
        if st.button("Copy to Clipboard"):
            st.session_state.generated_password = strong_password
            st.success("Password copied to clipboard!")

    # Password tip section
    st.subheader("Password Tip:")
    tip = get_password_tip()
    st.info(tip)  

    # Password history section
    st.subheader("Password History:")
    if st.session_state.password_history:
        for idx, pwd in enumerate(st.session_state.password_history, start=1):
            st.write(f"{idx}. {pwd}")
    else:
        st.write("No passwords saved in history.")

    # Save password to history
    if st.button("Save Password to History"):
        if password:
            st.session_state.password_history.append(password)
            st.success("Password saved to history!")
        else:
            st.warning("No password entered to save.")

    # Clear password history
    if st.button("Clear Password History"):
        st.session_state.password_history = []
        st.success("Password history cleared!")

if __name__ == "__main__":
    main()