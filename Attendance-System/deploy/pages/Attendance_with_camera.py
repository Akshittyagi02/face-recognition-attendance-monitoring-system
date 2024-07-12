import csv
import streamlit as st
import cv2
import pandas as pd
import face_recognition
import numpy as np
from datetime import datetime
import glob
import os
import base64

# Function to convert image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Path to the logo image
logo_path = "/Users/akshittyagi/Documents/python/Attendance-System-Project-main/deploy/download.jpeg"
logo_base64 = image_to_base64(logo_path)

# Streamlit page configuration
st.set_page_config(
    page_title="Attendance System", page_icon="📊", layout="wide"
)

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
        justify-content: left;
        margin-bottom: 20px;
    }
    .logo {
        height: 80px;
        width: 80px;
        margin-right: 20px;
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
    .info {
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
        <div class='title'>Attendance with Camera</div>
    </div>
    <div class='divider'></div>
    """,
    unsafe_allow_html=True
)

# Load saved encodings
encodings_file_path = "/Users/akshittyagi/Documents/python/Attendance-System-Project-main/5. Encodings/encodings.csv"
saved_df = pd.read_csv(encodings_file_path)
encodings = [np.array([float(num) for num in i.strip('[]').split()]) for i in saved_df["Encodings"]]
persons = saved_df["Persons"]

# Function to detect known faces
def detect_known_faces(img, image_encodings=encodings, persons=persons):
    # Ensure the image is properly formatted
    if img is None:
        st.error("Image not loaded properly.")
        return [], []

    resized_img = cv2.resize(img, (img.shape[1] // 4, img.shape[0] // 4))
    rgb_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
    
    # Debug statement to check image format
    st.text(f"Image shape: {rgb_img.shape}, dtype: {rgb_img.dtype}")

    if rgb_img.dtype != np.uint8:
        st.error(f"Unexpected image dtype: {rgb_img.dtype}, expected uint8")
        return [], []

    if rgb_img.ndim != 3 or rgb_img.shape[2] != 3:
        st.error(f"Unexpected image shape: {rgb_img.shape}, expected (height, width, 3)")
        return [], []

    try:
        face_locations = face_recognition.face_locations(rgb_img)
        face_encodings = face_recognition.face_encodings(rgb_img, face_locations, model="small")
    except RuntimeError as e:
        st.error(f"Runtime error: {e}")
        return [], []

    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(image_encodings, face_encoding)
        name = "Unknown"
        if True in matches:
            name = persons[matches.index(True)]
        face_names.append(name)

    return face_locations, face_names

# Load attendance sheet filenames
attendance_path = "/Users/akshittyagi/Documents/python/Attendance-System-Project-main/6. Attendence/With_Camera"
attendance_files = [os.path.splitext(os.path.basename(f))[0] for f in glob.glob(attendance_path + "/*.csv")]

# Create new attendance sheet
with st.expander("Create New Attendance Sheet"):
    new_sheet_name = st.text_input("Enter Name of Attendance Sheet")
    if st.button("Create New Attendance Sheet"):
        date_str = datetime.now().strftime("%d-%m-%Y")
        sheet_name = f"{new_sheet_name} {date_str}.csv"
        pd.DataFrame(columns=['Date', 'Time', 'Name', 'Status']).to_csv(os.path.join(attendance_path, sheet_name), index=False)
        st.success(f"Attendance sheet '{sheet_name}' created successfully!")
        # Update the list of attendance files
        attendance_files.append(os.path.splitext(sheet_name)[0])

# View existing sheets
with st.expander("View Sheets"):
    if attendance_files:
        selected_sheet = st.selectbox("Select Sheet", attendance_files)
        sheet_path = os.path.join(attendance_path, f"{selected_sheet}.csv")
    else:
        st.write("No attendance sheets found.")
        selected_sheet = None
        sheet_path = None

# Start and stop attendance recording
start_button, stop_button = st.columns(2)
with start_button:
    start = st.button("Start Taking Attendance")
with stop_button:
    stop = st.button("Stop Taking Attendance")

FRAME_WINDOW = st.image([])
camera = cv2.VideoCapture(0)

# Attendance recording
if start and selected_sheet:
    field_names = ['Date', 'Time', 'Name', 'Status']

    while True:
        ret, frame = camera.read()
        if not ret:
            st.error("Failed to capture image from camera.")
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Debug statement to check image capture
        st.text(f"Captured frame shape: {frame.shape}, dtype: {frame.dtype}")

        face_locations, face_names = detect_known_faces(frame)

        if face_names:
            date_str = datetime.now().strftime("%d-%m-%Y")
            time_str = datetime.now().strftime("%H:%M:%S")
            for face_loc, name in zip(face_locations, face_names):
                y1, x2, y2, x1 = face_loc
                cv2.putText(frame, name, (x1*4, y1*4 - 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                cv2.rectangle(frame, (x1*4, y1*4), (x2*4, y2*4), (0, 0, 200), 4)

                new_row = {'Date': date_str, 'Time': time_str, 'Name': name, 'Status': 'Present'}
                with open(sheet_path, 'a', newline='') as csv_file:
                    dict_writer = csv.DictWriter(csv_file, fieldnames=field_names)
                    dict_writer.writerow(new_row)

        FRAME_WINDOW.image(frame)
        if cv2.waitKey(20) & 0xFF == ord('q') or stop:
            break

    camera.release()
    cv2.destroyAllWindows()
else:
    if start:
        st.error("No attendance sheet selected. Please create or select an attendance sheet first.")
