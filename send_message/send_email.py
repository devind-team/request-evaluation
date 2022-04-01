import smtplib
from datetime import date, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


async def send_file(login: str, password: str, sender: str, receivers: str,
                    attachment_path: str, smtp_server: str, port: int):
    current_date = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')
    message = MIMEMultipart()
    message['Subject'] = 'Отчет о состоянии IT-инфраструктуры и результатах ' \
                         'мониторинга инцидентов в области кибербезопасности.'
    message['From'] = sender
    message['To'] = receivers

    msg_content = f'<h4>Добрый день,<br> Отчет о состоянии IT-инфраструктуры за {current_date}.</h4>\n'
    body = MIMEText(msg_content, 'html')
    message.attach(body)

    with open(attachment_path, "rb") as attachment:
        file = MIMEApplication(attachment.read(), _subtype="docx")
        file.add_header('Content-Disposition', f'attachment; filename= {current_date}.docx')
        message.attach(file)

    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender, receivers.split(', '), message.as_string())
        server.quit()
