import streamlit as st
import pandas as pd

st.title("📧 Email Spam Detection (Keyword-Based)")

# Define spam keywords
spam_keywords = [
    "win", "free", "offer", "click", "urgent",
    "money", "reward", "claim", "limited", "prize"
]

# Spam detection function
def detect_spam(row):
    subject = str(row['subject']).lower()
    
    keyword_flag = any(word in subject for word in spam_keywords)
    link_flag = row['num_links'] > 2
    special_char_flag = row['num_special_chars'] > 10

    if keyword_flag or link_flag or special_char_flag:
        return "Spam"
    else:
        return "Not Spam"

# Upload dataset
uploaded_file = st.file_uploader("Upload Email Dataset", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.write(df.head())

    # Apply spam detection
    df['prediction'] = df.apply(detect_spam, axis=1)

    st.success("Spam detection applied!")

    # Show full dataset
    st.subheader("📊 Results")
    st.write(df)

    # Filter section
    st.subheader("🔍 Filter Emails")

    filter_option = st.selectbox("Filter by:", ["All", "Spam", "Not Spam"])

    if filter_option == "Spam":
        filtered_df = df[df['prediction'] == "Spam"]
    elif filter_option == "Not Spam":
        filtered_df = df[df['prediction'] == "Not Spam"]
    else:
        filtered_df = df

    st.write(filtered_df)

# Manual input prediction
st.subheader("✉️ Test Custom Email")

subject = st.text_input("Enter Email Subject")
num_links = st.slider("Number of Links", 0, 10, 1)
num_special_chars = st.slider("Special Characters", 0, 50, 5)

if st.button("Check Email"):
    temp_df = pd.DataFrame([{
        "subject": subject,
        "num_links": num_links,
        "num_special_chars": num_special_chars
    }])

    result = detect_spam(temp_df.iloc[0])

    if result == "Spam":
        st.error("🚨 Spam Email Detected")
    else:
        st.success("✅ Not Spam")