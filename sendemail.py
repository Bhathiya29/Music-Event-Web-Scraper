import smtplib
import ssl


def send_email(message):
    host = 'smtp.gmail.com'
    port = 465

    username = 'abcdef@gmail.com'
    password = 'abcdef123#'

    receiver = 'abc@gmail.com'
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print('Email was sent')
