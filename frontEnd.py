import streamlit as st
from email.message import EmailMessage
import smtplib

st.set_page_config(page_title="RIASEC Test", layout="centered")

# ---------------- SESSION STATE ----------------
if "info" not in st.session_state:
    st.session_state.info = {}
if "responses" not in st.session_state:
    st.session_state.responses = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "email_sent" not in st.session_state:
    st.session_state.email_sent = False

# ---------------- USER INFO FORM ----------------
if not st.session_state.info:
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

st.markdown("### Rate each statement (1 = Strongly Disagree → 5 = Strongly Agree)")

# ---------------- BUTTON STYLE FUNCTION ----------------
def render_button(num, selected):
    """Render a fake button with red box if selected"""
    style = "border: 2px solid red; padding: 10px; display:inline-block; width:40px; text-align:center; font-weight:bold; margin:2px; cursor:pointer;"
    normal = "border: 1px solid #000; padding: 10px; display:inline-block; width:40px; text-align:center; margin:2px; cursor:pointer;"
    return f'<div style="{style if selected else normal}">{num}</div>'

# ---------------- QUESTIONS WITH BUTTONS ----------------
for idx, (q, _) in enumerate(questions):
    st.write(f"**{q}**")
    cols = st.columns(5)
    for i in range(1, 6):
        selected = st.session_state.responses.get(idx) == i
        if cols[i-1].button("", key=f"{idx}_{i}"):
            st.session_state.responses[idx] = i
    # Render red box above selected
    html_buttons = "    ".join([render_button(i, st.session_state.responses.get(idx) == i) for i in range(1,6)])
    st.markdown(html_buttons, unsafe_allow_html=True)

# ---------------- SUBMIT BUTTON ----------------
all_answered = len(st.session_state.responses) == len(questions)
submit = st.button("Submit Test", disabled=not all_answered)

# ---------------- PROCESS SUBMISSION ----------------
if submit and not st.session_state.submitted:
    # Calculate scores
    scores = {"R":0,"I":0,"A":0,"S":0,"E":0,"C":0}
    for idx, (_, cat) in enumerate(questions):
        scores[cat] += st.session_state.responses[idx]

    # Build email
    info = st.session_state.info
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

    # Send email
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
        st.session_state.submitted = True

    except Exception:
        st.error("❌ Failed to send email. Check credentials.")
        st.stop()

# ---------------- SUCCESS MESSAGE ----------------
if st.session_state.email_sent:
    st.success(
        "✅ Results sent successfully!\n\n"
        "Please contact **mycareerhorizons@gmail.com** to receive your full report."
    )
