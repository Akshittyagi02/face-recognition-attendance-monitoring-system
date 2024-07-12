import streamlit as st
import pandas as pd
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
        padding: 20px;
        color: #4e73df;
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
        <div>
            <div class='title'>Attendance System</div>
            <hr class='divider'>
            <div class='info'>Manual Attendance</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Define the base path for attendance sheets
base_path = "/Users/akshittyagi/Documents/python/Attendance-System-Project-main/6. Attendence"

# Create New Attendance Sheet expander
with st.expander("Create New Attendance Sheet"):
    name_of_attendance_sheet = st.text_input("Enter Name of Attendance Sheet")
    if st.button("Create New Attendance Sheet"):
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        df = pd.DataFrame(columns=['Date', 'Time', 'Name', 'Status'])
        sheet = f"{name_of_attendance_sheet} {date}.csv"
        df.to_csv(os.path.join(base_path, sheet), index=False)
        st.success(f"Attendance sheet '{sheet}' created successfully!")

# Current date and time
now = datetime.now()
date = now.strftime("%d-%m-%Y")
time = now.strftime("%H:%M:%S")

# View Sheet and Add Record tabs
tab1, tab2 = st.columns(2)

with tab1:
    st.markdown("<h2>View Sheet</h2>", unsafe_allow_html=True)
    d_l = glob.glob(os.path.join(base_path, "*.csv"))
    d_l = [os.path.basename(f).split(".")[0] for f in d_l]
    sheet = st.selectbox("Select Date", d_l)
    if sheet:
        df = pd.read_csv(os.path.join(base_path, f"{sheet}.csv"))
        st.dataframe(df)

with tab2:
    st.markdown("<h2>Add Record</h2>", unsafe_allow_html=True)
    if sheet:
        df = pd.read_csv(os.path.join(base_path, f"{sheet}.csv"))
        name = st.text_input("Enter Student Name")
        status = st.selectbox("Status", ["Present", "Absent"])
        if name:
            new_row = pd.DataFrame({'Date': [date], 'Time': [time], 'Name': [name], 'Status': [status]})
            df = pd.concat([df, new_row], ignore_index=True)
            if st.button("Save Record"):
                df.to_csv(os.path.join(base_path, f"{sheet}.csv"), index=False)
                st.success("Record Saved")
                st.experimental_rerun()
