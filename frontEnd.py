import streamlit as st
from email.message import EmailMessage
import smtplib

st.set_page_config(page_title="RIASEC Test", layout="centered")

# ---------------- SESSION STATE ----------------
if "responses" not in st.session_state:
    st.session_state.responses = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "email_sent" not in st.session_state:
    st.session_state.email_sent = False
if "info" not in st.session_state:
    st.session_state.info = {}

st.title("RIASEC Career Interest Test")

# ---------------- USER INFO ----------------
with st.form("info_form"):
    Name = st.text_input("Full Name")
    Age = st.number_input("Age", 10, 100)
    Education = st.text_input("Education")
    School = st.text_input("School / University")
    Subjects = st.text_input("Subjects")
    Hobbies = st.text_area("Hobbies")
    Dream = st.text_area("Your Dream Career")
    Email = st.text_input("Email")
    Phone = st.text_input("Phone Number")

    start = st.form_submit_button("Start Test")

if start:
    st.session_state.info = {
        "Name": Name,
        "Age": Age,
        "Education": Education,
        "School": School,
        "Subjects": Subjects,
        "Hobbies": Hobbies,
        "Dream": Dream,
        "Email": Email,
        "Phone": Phone,
    }

# ---------------- QUESTIONS ----------------
questions = [
    ("I like to work on cars", "R"),
    ("I like to do puzzles", "I"),
    ("I am good at working independently", "A"),
    ("I like to work in teams", "S"),
    ("I am ambitious and goal-oriented", "E"),
    ("I like organizing things", "C"),
    ("I enjoy creative writing", "A"),
    ("I like helping people", "S"),
    ("I enjoy science", "I"),
    ("I like leading others", "E"),
    ("I like working outdoors", "R"),
    ("I enjoy problem solving", "I"),
    ("I like artistic activities", "A"),
    ("I like structured work", "C"),
    ("I like influencing others", "E"),
]

st.markdown("### Rate each statement (1 = Strongly Disagree → 5 = Strongly Agree)")

# ---------------- CUSTOM BUTTON FUNCTION ----------------
def colored_button(label, key, selected=False):
    color = "#ff4d4d" if selected else "#e0e0e0"
    btn_html = f"""
    <style>
    div.stButton > button#{key} {{
        background-color: {color};
        color: black;
        width: 50px;
        height: 40px;
        font-weight: bold;
        border-radius: 5px;
        margin-right:5px;
    }}
    div.stButton > button#{key}:hover {{
        background-color: #ff9999;
    }}
    </style>
    """
    st.markdown(btn_html, unsafe_allow_html=True)
    return st.button(label, key=key)

# ---------------- DISPLAY QUESTIONS ----------------
for idx, (question, _) in enumerate(questions):
    st.write(f"**{question}**")
    cols = st.columns(5)
    for i in range(1, 6):
        selected = st.session_state.responses.get(idx) == i
        with cols[i-1]:
            if colored_button(str(i), key=f"{idx}_{i}", selected=selected):
                st.session_state.responses[idx] = i
    if idx in st.session_state.responses:
        st.caption(f"Selected: {st.session_state.responses[idx]}")
    else:
        st.caption("Not answered")

# ---------------- SUBMIT BUTTON ----------------
all_answered = len(st.session_state.responses) == len(questions)
st.markdown("---")
submit = st.button("Submit Test", disabled=not all_answered)

# ---------------- PROCESS SUBMISSION ----------------
if submit and not st.session_state.submitted:
    scores = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}
    for i, (_, cat) in enumerate(questions):
        scores[cat] += st.session_state.responses[i]

    info = st.session_state.info

    email_body = f"""
Name: {info['Name']}
Age: {info['Age']}
Education: {info['Education']}
School: {info['School']}
Subjects: {info['Subjects']}
Hobbies: {info['Hobbies']}
Dream: {info['Dream']}

--- RIASEC SCORES ---
R: {scores['R']}
I: {scores['I']}
A: {scores['A']}
S: {scores['S']}
E: {scores['E']}
C: {scores['C']}
"""

    try:
        msg = EmailMessage()
        msg["From"] = st.secrets["EMAIL"]
        msg["To"] = st.secrets["RECEIVER"]
        msg["Subject"] = f"RIASEC Results – {info['Name']}"
        msg.set_content(email_body)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(st.secrets["EMAIL"], st.secrets["EMAIL_PASSWORD"])
            server.send_message(msg)

        st.session_state.email_sent = True

    except Exception:
        st.error("❌ Failed to send email. Check credentials.")

# ---------------- SUCCESS MESSAGE ----------------
if st.session_state.email_sent:
    st.success(
        "✅ Results sent successfully!\n\n"
        "Please contact **mycareerhorizons@gmail.com** to receive your full report."
    )
