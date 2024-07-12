import streamlit as st
import base64

# Function to convert image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Path to the logo image
logo_path = "/Users/akshittyagi/Documents/python/Attendance-System-Project-main/deploy/download.jpeg"
logo_base64 = image_to_base64(logo_path)

# Configure the page
st.set_page_config(
    page_title="Attendance System",
    page_icon="🎓",
    layout="wide"
)

# Apply CSS for custom styling
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
    }
    .title {
        font-size: 3em;
        color: #4e73df;
        text-align: center;
    }
    .description {
        font-size: 1.5em;
        color: #4e73df;
        text-align: center;
    }
    .header {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
    }
    .logo {
        height: 80px;
        width: 80px;
        margin-right: 20px;
    }
    .learn-more {
        font-size: 1.2em;
        color: #4e73df;
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header with logo and title
st.markdown(
    f"""
    <div class="header">
        <img src="data:image/jpeg;base64,{logo_base64}" class="logo"/>
        <div class='title'>Welcome to the Face Recognition Attendance Monitoring System</div>
    </div>
    <div class='description'>Made by Akshit, Ayush, and Arjun.</div>
    """,
    unsafe_allow_html=True
)

# Adding a button for interactivity
if st.button("Learn More"):
    st.markdown("""
    ### About the Face Recognition Attendance Monitoring System

    This system utilizes advanced face recognition technology to monitor attendance efficiently. It is designed to accurately recognize faces in real-time, enabling seamless attendance management in various educational and organizational settings.

    #### Features:
    - Real-time face detection and recognition.
    - Automatic attendance marking based on recognized faces.
    - User-friendly interface for easy operation.
    - Scalable and adaptable to different environments.

    #### Benefits:
    - Reduces administrative workload.
    - Improves accuracy and transparency in attendance tracking.
    - Enhances overall efficiency in educational and organizational processes.

    For more details, contact us at [akshitt022@gmail.com](mailto:akshitt022@email.com).
    """)
