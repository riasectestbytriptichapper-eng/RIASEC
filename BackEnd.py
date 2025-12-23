from email.message import EmailMessage
import smtplib

Name = input("Enter Name: ")
Education = input("Enter Education: ")
School = input("Enter School/University: ")
Subjects = input("Enter Subjects: ")
Email = input("Enter Email Id: ")
Phone = input("Enter Phone Number:")

R,Realistic = "R", 0
I,Investigative = "I", 0
A,Artistic = "A", 0
S,Social = "S", 0
E,Enterprising = "E", 0
C,Conventional = "C", 0
questions = [
    ("I like to work on cars",R),
    ("I like to do puzzles",I),
    ("I am good at working independently",A),
    ("I like to work in teams",S),
    ("I am an ambitious person, I set goals for myself",E),
    ("I like to organize things, (files, desks/offices)", C),            
    ("I like to build things",R),
    ("I like to read about art and music",A),
    ("I like to have clear instructions to follow",C),
    ("I like to try to influence or persuade people",E),
    ("I like to do experiments",I),
    ("I like to teach or train people",S),
    ("I like trying to help people solve their problems",S),
    ("I like to take care of animals",R),
    ("I wouldn’t mind working 8 hours per day in an office",C),
    ("I like selling things",E),
    ("I enjoy creative writing",A),
    ("I enjoy science",I),
    ("I am quick to take on new responsibilities",E),
    ("I am interested in healing people",S),
    ("I enjoy trying to figure out how things work",I),
    ("I like putting things together or assembling things",R),
    ("I am a creative person",A),
    ("I pay attention to details",C),
    ("I like to do filing or typing",C),
    ("I like to analyze things (problems/situations)",I),
    ("I like to play instruments or sing",A),
    ("I enjoy learning about other cultures",S),
    ("I would like to start my own business",E),
    ("I like to cook",R),
    ("I like acting in plays",A),
    ("I am a practical person",R),
    ("I like working with numbers or charts",I),
    ("I like to get into discussions about issues",S),
    ("I am good at keeping records of my work",C),
    ("I like to lead",E),
    ("I like working outdoors",R),
    ("I would like to work in an office",C),
    ("I’m good at math",I),
    ("I like helping people",S),
    ("I like to draw",A),
    ("I like to give speeches",E)
]

Ans = []

print("this is a RIASEC test answer each question on range of 1 to 5 (1 least like me, 5 is most like me)")

for i in range(len(questions)):
    currentQusetion = questions[i][0]
    currentType = questions[i][1]
    print(currentQusetion)
    currentAns = int(input("Enter Number: "))

    while int(currentAns) not in [1,2,3,4,5]:
        print("Invalid Input Try Again")
        currentQusetion = questions[i][0]
        print(currentQusetion)
        currentAns = int(input("Enter Number: "))
   
    toAppend = [currentQusetion,currentType,currentAns]
    Ans.append(toAppend)

    if i == len(questions) - 1 :
        print("\n Test Complete")
    else:
        print("\n Next Question") 
    

for i in range(len(Ans)):
    if Ans[i][1] == R:
        Realistic += Ans[i][2]
    elif Ans[i][1] == I:
        Investigative += Ans[i][2]
    elif Ans[i][1] == A:
        Artistic += Ans[i][2]
    elif Ans[i][1] == S:
        Social += Ans[i][2]
    elif Ans[i][1] == E:
        Enterprising += Ans[i][2]
    elif Ans[i][1] == C:
        Conventional += Ans[i][2]
    else:
        print("Error 404")

totalCategories = f"""Total for Realistic {Realistic}
Total for Investigative {Investigative}
Total for Artistic {Artistic}
Total for Social {Social}
Total for Enterprising {Enterprising}
Total for Conventional {Conventional}"""

Info = f"""Name: {Name}\n
Education: {Education}\n
School: {School}\n
Subjects: {Subjects}\n
Email: {Email}\n
Phone: {Phone}\n"""

table = "\n".join(",".join(map(str, row)) for row in Ans)

msg = EmailMessage()
msg["From"] = "riasec.test.by.tripti.chapper@gmail.com"
msg["To"] = "mycareerhorizons@gmail.com"
msg["Subject"] = f"RIASEC Test Results for {Name}"

msg.set_content(f"{Info} \n {totalCategories}\n Results:\n {table}")

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login("riasec.test.by.tripti.chapper@gmail.com", "hopb uips tekq tvaq")
    server.send_message(msg)
#RIASEC4231@Tripti_Chapper