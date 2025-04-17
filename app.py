import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_email(to_email, subject, message):
    # Get credentials from environment variables
    sender_email = os.getenv('SENDER_EMAIL')
    password = os.getenv('EMAIL_PASSWORD')
    
    if not sender_email or not password:
        raise ValueError("Email credentials not found in environment variables")
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Add body
    msg.attach(MIMEText(message, 'plain'))
    
    # Create SMTP session
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")

# Set page config
st.set_page_config(
    page_title="Email Sender",
    page_icon="📧",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS with dark theme and Tailwind-inspired styling
st.markdown("""
    <style>
    .stApp {
        background: #1a1a1a;
        color: #ffffff;
    }
    .main {
        padding: 2rem;
    }
    /* Input fields styling */
    .stTextInput>div>div>input {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #404040;
        border-radius: 0.5rem;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    .stTextInput>div>div>input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    }
    .stTextArea>div>div>textarea {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #404040;
        border-radius: 0.5rem;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    .stTextArea>div>div>textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    }
    /* Button styling */
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        padding: 0.75rem;
        background: linear-gradient(45deg, #3b82f6, #2563eb);
        color: white;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #2563eb, #1d4ed8);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transform: translateY(-1px);
    }
    /* Card styling */
    .email-info {
        background: #2d2d2d;
        padding: 1.25rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.5rem;
        border: 1px solid #404040;
    }
    /* Success message */
    .stAlert {
        background-color: #064e3b;
        border: 1px solid #059669;
        border-radius: 0.5rem;
    }
    /* Error message */
    .stError {
        background-color: #7f1d1d;
        border: 1px solid #dc2626;
        border-radius: 0.5rem;
    }
    /* Label styling */
    .stMarkdown p {
        color: #9ca3af;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Get sender email from environment variables
sender_email = os.getenv('SENDER_EMAIL')

# Main content
st.markdown("<h1 style='text-align: center; color: #ffffff; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;'>📧 Email Sender</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 1.1rem; margin-bottom: 2rem;'>Send emails quickly and securely</p>", unsafe_allow_html=True)

# Email info card
st.markdown(f"""
    <div class='email-info'>
        <p style='margin: 0; color: #9ca3af;'><strong style='color: #ffffff;'>From:</strong> {sender_email}</p>
    </div>
""", unsafe_allow_html=True)

# Input fields with empty defaults
receiver_email = st.text_input("To:", placeholder="Enter recipient's email address")
subject = st.text_input("Subject:", placeholder="Enter email subject")
body = st.text_area("Message:", placeholder="Type your message here...", height=200)

# Send button with icon
if st.button("🚀 Send Email"):
    if not all([receiver_email, subject, body]):
        st.error("Please fill in all the fields.")
    else:
        try:
            send_email(receiver_email, subject, body)
            st.success("✅ Email sent successfully!")
            # Clear the form
            st.experimental_rerun()
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #6b7280; font-size: 0.9rem;'>Made with ❤️ using Streamlit</p>", unsafe_allow_html=True)
