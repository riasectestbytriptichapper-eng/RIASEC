import streamlit as st
from email.message import EmailMessage
import smtplib
import traceback

st.set_page_config(page_title="RIASEC Test", layout="centered")

# --- Session-state defaults ---
if "show_test" not in st.session_state:
    st.session_state.show_test = False

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "email_sent" not in st.session_state:
    st.session_state.email_sent = False

if "responses" not in st.session_state:
    st.session_state.responses = []

if "scores" not in st.session_state:
    st.session_state.scores = {""R"": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}

if "info" not in st.session_state:
    st.session_state.info = {}

st.title("RIASEC Career Interest Test")

# ---------- User Info Form ----------
with st.form("info_form"):
    Name = st.text_input("Name", key="name_input")
    Education = st.text_input("Education", key="education_input")
    School = st.text_input("School / University", key="school_input")
    Subjects = st.text_input("Subjects", key="subjects_input")
    Email = st.text_input("Email", key="email_input")
    Phone = st.text_input("Phone Number", key="phone_input")
    start = st.form_submit_button("Start Test")

if start:
    # Save info into session_state so it survives reruns
    st.session_state.info = {
        "Name": Name.strip(),
        "Education": Education.strip(),
        "School": School.strip(),
        "Subjects": Subjects.strip(),
        "Email": Email.strip(),
        "Phone": Phone.strip(),
    }
    st.session_state.show_test = True
    # Rerun will continue to test form

# If the user hasn't started, stop here
if not st.session_state.show_test:
    st.info("Please fill your info above and click 'Start Test' to begin.")
    st.stop()

# ---------- Questions (all included) ----------
questions = [
    ("I like to work on cars","R"),
    ("I like to do puzzles","I"),
    ("I am good at working independently","A"),
    ("I like to work in teams","S"),
    ("I am an ambitious person, I set goals for myself","E"),
    ("I like to organize things, (files, desks/offices)", "C"),            
    ("I like to build things","R"),
    ("I like to read about art and music","A"),
    ("I like to have clear instructions to follow","C"),
    ("I like to try to influence or persuade people","E"),
    ("I like to do experiments","I"),
    ("I like to teach or train people","S"),
    ("I like trying to help people solve their problems","S"),
    ("I like to take care of animals","R"),
    ("I wouldn’t mind working 8 hours per day in an office","C"),
    ("I like selling things","E"),
    ("I enjoy creative writing","A"),
    ("I enjoy science","I"),
    ("I am quick to take on new responsibilities","E"),
    ("I am interested in healing people","S"),
    ("I enjoy trying to figure out how things work","I"),
    ("I like putting things together or assembling things","R"),
    ("I am a creative person","A"),
    ("I pay attention to details","C"),
    ("I like to do filing or typing","C"),
    ("I like to analyze things (problems/situations)","I"),
    ("I like to play instruments or sing","A"),
    ("I enjoy learning about other cultures","S"),
    ("I would like to start my own business","E"),
    ("I like to cook","R"),
    ("I like acting in plays","A"),
    ("I am a practical person","R"),
    ("I like working with numbers or charts","I"),
    ("I like to get into discussions about issues","S"),
    ("I am good at keeping records of my work","C"),
    ("I like to lead","E"),
    ("I like working outdoors","R"),
    ("I would like to work in an office","C"),
    ("I’m good at math","I"),
    ("I like helping people","S"),
    ("I like to draw","A"),
    ("I like to give speeches","E")
]

st.header("Answer each question (1 = least like you, 5 = most like you)")

# Build the test form (all sliders)
with st.form("test_form"):
    # Use a temporary structure to collect the answers before saving
    temp_responses = []
    for idx, (q, cat) in enumerate(questions):
        # Use a safe unique key for each slider
        slider_key = f"q_{idx}"
        val = st.slider(q, 1, 5, 3, key=slider_key)
        temp_responses.append((q, cat, int(val)))

    submit = st.form_submit_button("Submit Test")

# If the test was submitted, compute scores and trigger email flow once
if submit and not st.session_state.submitted:
    # Reset score counters
    scores = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}
    for q, cat, val in temp_responses:
        if cat in scores:
            scores[cat] += int(val)

    # Save into session_state
    st.session_state.responses = temp_responses
    st.session_state.scores = scores
    st.session_state.submitted = True
    # Rerun will continue to email/send banner below

# If already submitted, ensure we use session state values (prevents recomputation/resend on rerun)
if st.session_state.submitted:
    # If email not yet sent, attempt to send
    if not st.session_state.email_sent:
        # Prepare info, totals, and response table
        info = st.session_state.info
        scores = st.session_state.scores
        responses = st.session_state.responses

        totals_text = (
            f"Realistic: {scores['R']}\n"
            f"Investigative: {scores['I']}\n"
            f"Artistic: {scores['A']}\n"
            f"Social: {scores['S']}\n"
            f"Enterprising: {scores['E']}\n"
            f"Conventional: {scores['C']}\n"
        )

        info_text = (
            f"Name: {info.get('Name','')}\n"
            f"Education: {info.get('Education','')}\n"
            f"School: {info.get('School','')}\n"
            f"Subjects: {info.get('Subjects','')}\n"
            f"Email: {info.get('Email','')}\n"
            f"Phone: {info.get('Phone','')}\n"
        )

        table_text = "\n".join(f"{q},{c},{s}" for q, c, s in responses)

        email_body = f"""{info_text}

{totals_text}

Responses:
{table_text}
"""

        # Build the message
        msg = EmailMessage()
        # From and To come from secrets
        try:
            sender = st.secrets["EMAIL"]
            receiver = st.secrets["RECEIVER"]
        except Exception as e:
            st.error("Email configuration missing. Please set EMAIL and RECEIVER in Streamlit secrets.")
            st.stop()

        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = f"RIASEC Test Results – {info.get('Name','(no name)')}"
        msg.set_content(email_body)

        # Attempt to send email (only once)
        try:
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
                server.starttls()
                # login using secret password
                try:
                    passwd = st.secrets["EMAIL_PASSWORD"]
                except Exception:
                    st.error("EMAIL_PASSWORD missing from Streamlit secrets. Add EMAIL_PASSWORD (app password).")
                    st.stop()
                server.login(sender, passwd)
                server.send_message(msg)
            st.session_state.email_sent = True
        except Exception as e:
            # Mark as not sent so the user can try again if desired
            st.session_state.email_sent = False
            # Show a helpful error including traceback for debugging (you can remove traceback in production)
            st.error("Failed to send results by email. Please check your email configuration and network.")
            st.code(traceback.format_exc())
            st.stop()

    # At this point, the email has been sent successfully.
    if st.session_state.email_sent:
        st.success(
            "Results Have Been Sent to mycareerhorizons@gmail.com /n"
            "Please contact Tripti Chapper at the Same Email to get your Detailed report."
        )
        # Optionally stop further execution so the banner remains and nothing else changes
        st.stop()

# If user hasn't submitted yet (normal flow), show a neutral hint
st.info("Fill the sliders and click Submit Test to complete. Your answers will be emailed to Tripti Chapper Careers Counselling.")
