import streamlit as st
import requests

st.set_page_config(
    page_title="AI Job Mailer Pro",
    page_icon="🚀",
    layout="wide"
)

# Sidebar User Settings
st.sidebar.title("⚙️ User Settings")

user_email = st.sidebar.text_input(
    "📧 Your Email",
    key="user_email"
)

app_password = st.sidebar.text_input(
    "🔑 App Password (Take it from Your Google Account)",
    type="password"
)

service_enable = st.sidebar.checkbox("Enable Auto Job Apply Service")

if st.sidebar.button("💾 Save Settings"):

    if user_email and app_password:
        st.session_state["app_password"] = app_password
        st.session_state["service"] = service_enable

        st.sidebar.success("Settings Saved ✅")
    else:
        st.sidebar.error("Email & Password required")


# Online Background Images
bg_image = "https://images.pexels.com/photos/531880/pexels-photo-531880.jpeg"
bg_image_1 = "https://images.pexels.com/photos/414171/pexels-photo-414171.jpeg"


# Custom Styling
st.markdown(
    f"""
    <style>

    .stApp {{
        background: linear-gradient(rgba(0,0,0,0), rgba(0,0,0,0)),
                    url("{bg_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(rgba(0,0,0,0.25), rgba(0,0,0,0.25)),
                    url("{bg_image_1}");
        background-size: cover;
        background-position: center;
    }}

    .main-title {{
        font-size: 44px;
        font-weight: 900;
        color: #ffffff;
        text-align: left;
        letter-spacing: 0.5px;
        text-shadow:
            0px 0px 10px rgba(168,85,247,0.6),
            0px 2px 6px rgba(0,0,0,0.7);
    }}

    .sub-text {{
        color: #d1d5db;
        font-size: 18px;
        text-align: left;
        margin-bottom: 20px;
    }}

    .block-container {{
        background: rgba(0, 0, 0, 0.0);
        padding: 2rem;
        border-radius: 20px;
        backdrop-filter: blur(0px);
    }}

    .stTextInput>div>div>input,
    .stTextArea textarea {{
        background-color: rgba(255,255,255,0.1);
        color: black;
        border-radius: 10px;
    }}

    .stButton>button {{
        background: linear-gradient(90deg, #6366f1, #a855f7);
        color: white;
        border-radius: 12px;
        height: 55px;
        font-weight: bold;
        font-size: 16px;
        border: none;
        transition: 0.3s ease-in-out;
    }}

    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0px 0px 20px rgba(168,85,247,0.6);
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# Header
st.markdown('<div class="main-title">🚀 AI Smart Job Application Sender</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Upload resume, paste job description & send optimized application instantly.</div>', unsafe_allow_html=True)

st.divider()


# Layout
col1, col2 = st.columns([1, 1])

with col1:

    sender_email = st.text_input("📧 HR Email")

    job_description = st.text_area(
        "📄 Job Description",
        height=250,
        placeholder="Paste the full job description here..."
    )

with col2:

    uploaded_file = st.file_uploader(
        "📎 Upload Resume (PDF only)",
        type=["pdf"]
    )

    if uploaded_file:
        st.success("Resume Uploaded Successfully ✅")


st.divider()


# Send Button
if st.button("✨ Generate & Send Application"):

    if not sender_email or not job_description or not uploaded_file:
        st.error("Please fill all three fields.")
    else:

        with st.spinner("Sending request to AI backend..."):

            # CHANGE THIS AFTER FASTAPI DEPLOY
            url = "https://ai-job-email-sender.onrender.com/Email-agent/"

            files = {
                "file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")
            }

            data = {
                "job_description": job_description,
                "hr_email": sender_email,
                "user_email": user_email,
                "app_password": app_password
            }

            try:

                response = requests.post(url, data=data, files=files)

                if response.status_code == 200:

                    result = response.json()

                    st.success("✅ Email Sent Successfully!")

                    if "result" in result and "email_body" in result["result"]:
                        st.subheader("📨 Generated Email Preview")

                        st.text_area(
                            "Email_body",
                            result["result"]["email_body"],
                            height=300
                        )

                else:
                    st.error("Server Error. Please check backend.")

            except Exception as e:
                st.error(f"Connection error: {e}")


st.divider()
st.caption("Built with LangGraph + Mistral AI | Advanced Automated Job Application System")
