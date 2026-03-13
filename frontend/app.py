import streamlit as st
import requests

st.set_page_config(
    page_title="AI Job Mailer Pro",
    page_icon="🚀",
    layout="wide"
)

# ---------------- SIDEBAR ----------------

st.sidebar.title("⚙️ User Settings")

user_email = st.sidebar.text_input("📧 Your Email")

app_password = st.sidebar.text_input(
    "🔑 App Password (Google App Password)",
    type="password"
)

service_enable = st.sidebar.checkbox("Enable Auto Job Apply Service")

if st.sidebar.button("💾 Save Settings"):
    if user_email and app_password:
        st.session_state["user_email"] = user_email
        st.session_state["app_password"] = app_password
        st.session_state["service"] = service_enable
        st.sidebar.success("Settings Saved ✅")
    else:
        st.sidebar.error("Email & Password required")


# ---------------- BACKGROUND ----------------

bg_image = "https://images.pexels.com/photos/531880/pexels-photo-531880.jpeg"
bg_image_1 = "https://images.pexels.com/photos/414171/pexels-photo-414171.jpeg"

st.markdown(
    f"""
<style>

.stApp {{
background: url("{bg_image}");
background-size: cover;
background-position: center;
background-attachment: fixed;
}}

section[data-testid="stSidebar"] {{
background: url("{bg_image_1}");
background-size: cover;
background-position: center;
}}

.main-title {{
font-size: 44px;
font-weight: 900;
color: white;
text-shadow: 0px 0px 10px rgba(168,85,247,0.6);
}}

</style>
""",
    unsafe_allow_html=True,
)

# ---------------- HEADER ----------------

st.markdown('<div class="main-title">🚀 AI Smart Job Application Sender</div>', unsafe_allow_html=True)

st.write("Upload resume, paste job description & send AI generated job application instantly.")

st.divider()

# ---------------- INPUT SECTION ----------------

col1, col2 = st.columns(2)

with col1:

    sender_email = st.text_input("📧 HR Email")

    job_description = st.text_area(
        "📄 Job Description",
        height=250
    )

with col2:

    uploaded_file = st.file_uploader(
        "📎 Upload Resume (PDF)",
        type=["pdf"]
    )

    if uploaded_file:
        st.success("Resume Uploaded Successfully")

st.divider()

# ---------------- SEND BUTTON ----------------

if st.button("✨ Generate & Send Application"):

    if not sender_email or not job_description or not uploaded_file:
        st.error("Please fill all fields")
    else:

        with st.spinner("Sending request to AI backend..."):

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

                        st.subheader("📨 Generated Email")

                        st.text_area(
                            "Email Preview",
                            result["result"]["email_body"],
                            height=300
                        )

                else:
                    st.error(f"Backend Error : {response.text}")

            except Exception as e:
                st.error(f"Connection Error: {e}")

st.divider()
st.caption("Built with LangGraph + Mistral AI")
