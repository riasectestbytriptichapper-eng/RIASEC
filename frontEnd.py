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

# ---------------- TITLE ----------------
st.title("RIASEC Career Interest Test")

# ---------------- USER INFO FORM ----------------
with st.form("info_form"):
    Name = st.text_input("Full Name")
    Age = st.number_input("Age", min_value=10, max_value=100)
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

st.header("Answer all questions (1 = Strongly Disagree → 5 = Strongly Agree)")

with st.form("test_form"):
    for i, (q, cat) in enumerate(questions):
        st.session_state.responses[i] = st.radio(
            q,
            [1, 2, 3, 4, 5],
            index=None,
            key=f"q_{i}"
        )

    all_answered = len(st.session_state.responses) == len(questions) and all(
        v is not None for v in st.session_state.responses.values()
    )

    submit = st.form_submit_button(
        "Submit Test",
        disabled=not all_answered
    )

# ---------------- PROCESS & EMAIL ----------------
if submit and not st.session_state.submitted:
    for i, (q, cat) in enumerate(questions):
        st.session_state.scores[cat] += st.session_state.responses[i]

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

--- RIASEC RESULTS ---
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

    except Exception as e:
        st.error("❌ Email failed to send. Please try again later.")
        st.stop()

# ---------------- SUCCESS MESSAGE ----------------
if st.session_state.email_sent:
    st.success(
        "✅ The Administrator has received your results.\n\n"
        "Please contact them to receive your personalized report."
    )
