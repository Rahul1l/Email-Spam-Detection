import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText

st.title("📧 Email Spam Detection + Dataset + SMTP")

# -------------------------------
# Secure credentials
# -------------------------------
SENDER_EMAIL = st.secrets["EMAIL"]
APP_PASSWORD = st.secrets["PASSWORD"]

# -------------------------------
# Spam keywords
# -------------------------------
spam_keywords = [
    "win", "free", "offer", "click", "urgent",
    "money", "reward", "claim", "limited", "prize"
]

# -------------------------------
# Spam detection function
# -------------------------------
def detect_spam(subject, num_links, num_special_chars):
    subject = str(subject).lower()

    keyword_flag = any(word in subject for word in spam_keywords)
    link_flag = num_links > 2
    special_char_flag = num_special_chars > 10

    if keyword_flag or link_flag or special_char_flag:
        return "Spam"
    else:
        return "Not Spam"

# -------------------------------
# Send Email Function
# -------------------------------
def send_email(receiver_email, subject_text, result):
    body = f'The email with subject: "{subject_text}" is {result}.'

    msg = MIMEText(body)
    msg["Subject"] = "Spam Detection Result"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        return str(e)

# =====================================================
# 📂 SECTION 1: DATASET UPLOAD + ANALYSIS
# =====================================================
st.header("📂 Upload Dataset")

uploaded_file = st.file_uploader("Upload Email Dataset (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.write(df.head())

    # Apply spam detection
    df['prediction'] = df.apply(
        lambda row: detect_spam(row['subject'], row['num_links'], row['num_special_chars']),
        axis=1
    )

    st.success("✅ Spam detection applied on dataset")

    # Filter
    st.subheader("🔍 Filter Emails")

    filter_option = st.selectbox("Filter by:", ["All", "Spam", "Not Spam"])

    if filter_option == "Spam":
        filtered_df = df[df['prediction'] == "Spam"]
    elif filter_option == "Not Spam":
        filtered_df = df[df['prediction'] == "Not Spam"]
    else:
        filtered_df = df

    st.write(filtered_df)

# =====================================================
# ✉️ SECTION 2: MANUAL INPUT + SMTP
# =====================================================
st.header("✉️ Check & Send Email")

receiver_email = st.text_input("Enter Receiver Email")

subject = st.text_input("Enter Email Subject")
num_links = st.slider("Number of Links", 0, 10, 1)
num_special_chars = st.slider("Special Characters", 0, 50, 5)

if st.button("Check Email"):

    if not receiver_email:
        st.warning("⚠️ Please enter receiver email")
    elif not subject:
        st.warning("⚠️ Please enter subject")
    else:
        result = detect_spam(subject, num_links, num_special_chars)

        # Show result
        if result == "Spam":
            st.error("🚨 Spam Email Detected")
        else:
            st.success("✅ Not Spam")

        # Send email
        status = send_email(receiver_email, subject, result)

        if status == True:
            st.info("📨 Email sent successfully!")
        else:
            st.error(f"❌ Error sending email: {status}")