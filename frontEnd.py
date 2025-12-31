import streamlit as st
from email.message import EmailMessage
import smtplib

st.set_page_config(page_title="RIASEC Test", layout="centered")

# ---------------- SESSION STATE ----------------
if "show_test" not in st.session_state:
    st.session_state.show_test = False
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "email_sent" not in st.session_state:
    st.session_state.email_sent = False
if "responses" not in st.session_state:
    st.session_state.responses = {}
if "scores" not in st.session_state:
    st.session_state.scores = {"R":0,"I":0,"A":0,"S":0,"E":0,"C":0}
if "info" not in st.session_state:
    st.session_state.info = {}

# ---------------- USER INFO ----------------
st.title("RIASEC Career Interest Test")
with st.form("info_form"):
    Name = st.text_input("Full Name")
    Age = st.number_input("Age", min_value=10, max_value=100, step=1)
    Education = st.text_input("Education")
    School = st.text_input("School / University")
    Subjects = st.text_input("Subjects")
    Hobbies = st.text_area("Hobbies")
    Dream = st.text_area("Your 'Impossible' Dream")
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
        "Phone": Phone
    }
    st.session_state.show_test = True

if not st.session_state.show_test:
    st.stop()

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

# ---------------- CSS FOR BUTTON STYLE ----------------
st.markdown("""
<style>
.radio-horizontal .stRadio > div {
    display: flex;
    justify-content: space-between;
    width: 300px;
}
.stRadio input[type="radio"]:checked + label {
    background-color: red;
    color: white;
    border-radius: 4px;
}
.stRadio label {
    width: 40px;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    border: 1px solid black;
    cursor: pointer;
    margin: 2px;
}
</style>
""", unsafe_allow_html=True)

st.header("Answer each question (1 = Strongly Disagree, 5 = Strongly Agree)")

# ---------------- TEST FORM ----------------
with st.form("test_form"):
    all_answered = True
    for idx, (q, cat) in enumerate(questions):
        st.write(f"**{q}**")
        selected = st.radio("", [1,2,3,4,5], key=f"q_{idx}", horizontal=True)
        if selected is None:
            all_answered = False
        st.session_state.responses[idx] = selected

    submit_disabled = not all_answered
    submit = st.form_submit_button("Submit Test", disabled=submit_disabled)

# ---------------- PROCESS SUBMISSION ----------------
if submit and not st.session_state.submitted:
    scores = {"R":0,"I":0,"A":0,"S":0,"E":0,"C":0}
    for idx, (q, cat) in enumerate(questions):
        val = st.session_state.responses[idx]
        scores[cat] += val

    st.session_state.scores = scores
    st.session_state.submitted = True

# ---------------- EMAIL LOGIC ----------------
if st.session_state.submitted and not st.session_state.email_sent:
    info = st.session_state.info
    scores = st.session_state.scores

    email_body = f"""
Name: {info['Name']}
Age: {info['Age']}
Education: {info['Education']}
School: {info['School']}
Subjects: {info['Subjects']}
Hobbies: {info['Hobbies']}
Dream: {info['Dream']}
Email: {info['Email']}
Phone: {info['Phone']}

--- RIASEC SCORES ---
R: {scores['R']}
I: {scores['I']}
A: {scores['A']}
S: {scores['S']}
E: {scores['E']}
C: {scores['C']}
"""

    msg = EmailMessage()
    msg["From"] = st.secrets["EMAIL"]
    msg["To"] = st.secrets["RECEIVER"]
    msg["Subject"] = f"RIASEC Results – {info['Name']}"
    msg.set_content(email_body)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(st.secrets["EMAIL"], st.secrets["EMAIL_PASSWORD"])
            server.send_message(msg)
        st.session_state.email_sent = True
    except Exception as e:
        st.error("Failed to send email. Please check email credentials.")
        st.stop()

# ---------------- FINAL CONFIRMATION ----------------
if st.session_state.email_sent:
    st.success(
        "Your results have been securely sent to Tripti Chapper Careers Counselling.\n"
        "Please contact them to receive your personalized report."
    )

