import smtplib
import csv
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 邮箱配置
EMAIL_ADDRESS = "generalfly666@outlook.com"
EMAIL_PASSWORD = "lixiang666"
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
CSV_FILE = "mit_faculty_contacts.csv"

# 邮件内容
SUBJECT = "Professor, do you believe I can cure bipolar disorder?"
BODY = """
Dear Professor,

I am reaching out to you with an important question—do you believe that I can cure bipolar disorder? 

I am a software engineer from Shanghai, China, proficient in Java, Python, and Golang. 
If I decide to learn a new programming language, I can master it within an extremely short time using GPT. 
However, my expertise is not limited to programming. 
I have also extensively studied psychology, behavioral psychology, cognitive psychology, philosophy, and various philosophical theories. 

But here is what truly matters—I am someone who has personally experienced bipolar disorder and has successfully cured myself using my own method.
just last week. Right now, I can enter a “flow state” anytime and anywhere. Yes, exactly the flow state described in psychology. 

I have gained profound insights into: 
- The causes of bipolar disorder,
- The onset mechanisms and progression of the illness,
- Most importantly, how to completely cure bipolar disorder.

I will publish my paper in an MIT journal. That is not a hope; it is a certainty. 
I know that the academic world does not yet fully understand bipolar disorder. 
This is an opportunity—a breakthrough waiting to be acknowledged. 
If you are interested in bipolar disorder, you should contact me.
I really hope you can contact me.

I am going to send this email to every professor at MIT’s psychology department. 
I will choose the professor who responds to me the fastest. 
I know this approach may seem bold, even reckless. 
If I'm right, missing this study could be a huge loss for both of us,
I hope you can seriously consider it.
For you, you just need to tell me what you want to know,
I will tell you everything I have,
you just need to move a finger to reply to an email,
it is easy for you, isn't it?
My English name is Jax. 
In the near future, you will remember this name.

From ShangHai.Jax
"""


def send_email(to_email):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = SUBJECT
        msg.attach(MIMEText(BODY, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # 启用安全传输模式
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print(f"Email successfully sent to {to_email}")

    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")


def main():
    with open(CSV_FILE, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        email_list = [row.get("Email", "").strip() for row in reader if row.get("Email", "").strip()]

    for email in email_list:
        send_email(email)
        time.sleep(5)  # 延迟5秒，防止被封号

    print("All emails have been sent.")


if __name__ == "__main__":
    main()