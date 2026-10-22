import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_test_email():
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    sender_email = "sig-sectt@nixi.in"
    sender_password = "D2gBFz36ieL5"

    receiver_email = "abhishek.suthar@nixi.in"

    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = "Test Email"

        msg.attach(MIMEText("Hi", "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        print("Email sent successfully")

    except Exception as e:
        print(f"Error: {e}")

send_test_email()