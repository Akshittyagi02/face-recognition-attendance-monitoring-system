import streamlit as st
import cv2
import numpy as np
import face_recognition
import pandas as pd
import os
import base64
from PIL import Image

# Path to Haar Cascade XML file
cascade_path = 'path/to/haarcascade_frontalface_default.xml'  # Update this path
logo_path = "/Users/akshittyagi/Documents/python/Attendance-System-Project-main/deploy/download.jpeg"

# Function to convert image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Convert logo to base64
logo_base64 = image_to_base64(logo_path)

# Page configuration
st.set_page_config(page_title="Attendance System", page_icon="📊", layout="wide")

# Apply CSS for custom styling
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
    }
    .title {
        font-size: 2.5em;
        color: #4e73df;
        text-align: center;
        margin-top: 20px;
    }
    .divider {
        border-top: 2px solid #4e73df;
        margin: 20px 0;
    }
    .header {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .logo {
        height: 80px;
        width: 80px;
    }
    .name-input {
        margin-bottom: 20px;
    }
    .button {
        background-color: #4e73df;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .button:hover {
        background-color: #2e59d9;
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
        <div class='title'>Add New Student</div>
    </div>
    <div class='divider'></div>
    """,
    unsafe_allow_html=True
)

# Initialize flag to check if all required fields are filled
filled = True

with st.container():
    # Create two columns for name input and camera input
    c1, c2 = st.columns((1, 2))
    
    # Name input field
    with c1:
        name = st.text_input("Enter Student name", key="name_input")
        if name == "":
            filled = False
    
    # Camera input field
    with c2:
        img_file_buffer = st.camera_input("Take a picture For new Student", key="camera")

        if img_file_buffer is not None:
            # Read image file buffer with OpenCV
            bytes_data = img_file_buffer.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            
            # Convert the image to grayscale for face detection
            gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
            
            # Load the Haar cascade for face detection
            if os.path.exists(cascade_path):
                face_cascade = cv2.CascadeClassifier(cascade_path)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                st.write(f"Number of Faces Detected: {len(faces)}")
                
                if len(faces) > 1:
                    st.write("There is more than one face in the image, please take another image.")
                elif len(faces) < 1:
                    st.write("No face detected")
                else:
                    st.write("Image Taken, Please Click Save")
            else:
                st.write("Please enter student name and click Save Student")
    
    # Save Student button
    with c1:
        if st.button("Save Student"):
            if filled:
                # Construct the file path for saving the image
                path = f"/Users/akshittyagi/Documents/python/Attendance-System-Project-main/1. Dataset/{name}.jpg"
                
                # Resize the image
                height, width = cv2_img.shape[:2]
                cv2_resized_img = cv2.resize(cv2_img, (int(width / 2), int(height / 2)))
                
                # Save the image
                cv2.imwrite(path, cv2_resized_img)
                
                # Load the saved image and get the face encoding
                img = face_recognition.load_image_file(path)
                img_encoding = face_recognition.face_encodings(img)[0]
                
                # Load the existing encodings CSV file
                df = pd.read_csv("/Users/akshittyagi/Documents/python/Attendance-System-Project-main/5. Encodings/encodings.csv")
                
                # Append the new encoding and name to the dataframe
                en = df["Encodings"].tolist()
                n = df["Persons"].tolist()
                en.append(img_encoding)
                n.append(name)
                df = pd.DataFrame({"Persons": n, "Encodings": en})
                
                # Save the updated dataframe back to the CSV file
                df.to_csv("/Users/akshittyagi/Documents/python/Attendance-System-Project-main/5. Encodings/encodings.csv", index=False)
                st.write("Student Added")
            else:
                st.warning("Please Enter Student Name")
