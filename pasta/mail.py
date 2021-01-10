import smtplib, ssl
import pandas as pd
import os
import sys
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess
import json
import re


SENDER_EMAIL = "financeiro@lincxcorretora.com"
SUBJECT = "PAGAMENTO DE COMISSÃO"
TEXT = """Prezado(a),

Segue em anexo o extrato da comissão e o recibo de pagamento.

Atenciosamente,
Lincx Corretora"""


# Windows
# SPREADSHEET_PATH = "G:\\Meu Drive\\LINCX\\FINANCEIRO\\Registro de vendedores.xlsx"
# BROKERS_RECEIPTS_PATH = "G:\\Meu Drive\\LINCX\\FINANCEIRO\RECIBO DE PAGAMENTO\\COMISSÃO CORRETOR\\"
# BOT_FILES_SENT_PATH = "G:\\Meu Drive\\LINCX\\FINANCEIRO\RECIBO DE PAGAMENTO\\COMISSÃO CORRETOR\\bot_email_comprovante\\files_sent.txt"


# Mac
SPREADSHEET_PATH = (
    "/Users/cursedappleofsaggi/Documents/LINCX_BOT/Registro de vendedores.xlsx"
)
BROKERS_RECEIPTS_PATH = "/Users/cursedappleofsaggi/Documents/LINCX_BOT/pasta/"
BOT_FILES_SENT_PATH = (
    "/Users/cursedappleofsaggi/Documents/LINCX_BOT/pasta/files_sent.txt"
)
WHATSAPP_API_PATH = "/Users/cursedappleofsaggi/Documents/LINCX_BOT/pasta/mail.js"
WHATSAPP_FILES_SENT_PATH = "/Users/cursedappleofsaggi/Documents/LINCX_BOT/pasta/wpp_files_sent.txt"

def send_gmail_email(sender_email, password, receiver_email, message):
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = sender_email
    password = password

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


def create_email_text_message(subject, text):
    message = MIMEMultipart()
    message["Subject"] = subject

    part = MIMEText(text, "plain")
    message.attach(part)

    return message


def add_file_to_email_message(message, file, filename):
    with open(file, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition", f"attachment; filename={filename}",
    )

    message.attach(part)

    return message


def generate_broker_info(broker):
    df = pd.read_excel(SPREADSHEET_PATH, header=1)
    info = df.loc[
        df["Codigo do Corretor"] == int(broker),
        ["Codigo do Corretor", "Nome", "E-mail", "Telefone"],
    ].to_dict("records")
    return info[0]


def get_files_to_send_and_to_whom():
    """
    Example of return:
    {
        1005: [
            '1005_Giovanni/1005051120_COMPROVANTE.pdf', 
            '1005_Giovanni/1005051120_RECIBO.pdf'
        ],
        1006: [
            '1006_Rafaella/1006051120_COMPROVANTE.pdf', 
            '1006_Rafaella/1006051120_RECIBO.pdf'
        ],
    }
    """
    folders = filter(os.path.isdir, os.listdir(BROKERS_RECEIPTS_PATH))
    # folders = os.listdir(BROKERS_RECEIPTS_PATH)
    # folders.remove("desktop.ini")
    # folders.remove("bot_email_comprovante")
    # folder.remove()
    brokers = {}
    for folder in folders:
        broker = folder[:4]
        if broker not in brokers:
            brokers[broker] = []

        files = os.listdir(f"{BROKERS_RECEIPTS_PATH}{folder}")

        dates = []
        for file in files:
            if file.split(".")[-1] == "pdf":
                dates.append(file[4:].split("_")[0])
        dates.sort(key=lambda date: datetime.strptime(date, "%d%m%y"))
        brokers[broker] = [
            # CHANGE HERE DEPENDING ON OS
            f"{folder}/{broker}{dates[-1]}_COMPROVANTE.pdf",
            f"{folder}/{broker}{dates[-1]}_RECIBO.pdf",
        ]

    return brokers


def check_already_sent(files_to_send, file_to_check):
    files_sent = set(line.strip() for line in open(file_to_check))
    for file in files_to_send:
        if file in files_sent:
            return True

    return False


def save_files_as_sent(files):
    with open(BOT_FILES_SENT_PATH, "a") as files_sent:
        for file in files:
            files_sent.write(f"{file}\n")


def send_whatsapp_message(brokers_to_be_contacted_info):
    data = json.dumps(brokers_to_be_contacted_info)
    subprocess.call(["node", WHATSAPP_API_PATH, data])        


def send_multiple_emails(brokers_to_be_contacted_info):
    count_emails = 0

    for broker_info in brokers_to_be_contacted_info:
        receiver_email = broker_info["E-mail"]
        receiver_name = broker_info["Nome"]
        files_to_send = broker_info["Files To Be Send"]

        message = create_email_text_message(SUBJECT, TEXT)

        for file in files_to_send:
            # CHANGE HERE DEPENDING ON OS
            filename = file.split("/")[-1]
            message = add_file_to_email_message(message, file, filename)

        print(f"\nSending email to {receiver_name}'s email ({receiver_email})...")
        try:
            send_gmail_email(SENDER_EMAIL, PASSWORD, receiver_email, message)
            save_files_as_sent(files_to_send)
            count_emails += 1
            print("Done.")
        except Exception as e:
            print(
                "Failed sending email. Please check your password or internet connection."
            )
            input("\nPress any key to continue...")
            sys.exit()

    print(f"\nFinished sending {count_emails} emails.")


if __name__ == "__main__":
    brokers_to_be_contacted_by_email_info = []
    brokers_to_be_contacted_by_wpp_info = []

    most_up_to_date_broker_files = get_files_to_send_and_to_whom().items()
    
    for broker, files_to_send, in most_up_to_date_broker_files:
        if check_already_sent(files_to_send, BOT_FILES_SENT_PATH):
            continue
        else:
            broker_info = generate_broker_info(broker)
            broker_info["Files To Be Send"] = files_to_send
            brokers_to_be_contacted_by_email_info.append(broker_info)

    for broker, files_to_send, in most_up_to_date_broker_files:
        if check_already_sent(files_to_send, WHATSAPP_FILES_SENT_PATH):
            continue
        else:
            broker_info = generate_broker_info(broker)
            broker_info["Files To Be Send"] = files_to_send
            brokers_to_be_contacted_by_wpp_info.append(broker_info)


    if len(brokers_to_be_contacted_by_email_info) == 0:
        print("\nEverything is up to date for emails.")
    else:
        send_to_email = input(f"\nYou have {len(brokers_to_be_contacted_by_email_info)} emails to send.\nEnter 'Y' to send.\n")
        if send_to_email == 'y' or send_to_email == 'Y':
            print(f"\nSending from {SENDER_EMAIL}")
            PASSWORD = input("Enter your email password and press 'Enter': \n")
            send_multiple_emails(brokers_to_be_contacted_by_email_info)
        else: 
            print('Not sending to email.')

    if len(brokers_to_be_contacted_by_wpp_info) == 0:
        print("\nEverything is up to date for Whatsapp messages.")
    else:
        send_to_wpp = input(f"\nYou have {len(brokers_to_be_contacted_by_wpp_info)} Whatsapp messages to send.\nEnter 'Y' to send.\n")
        if send_to_wpp == 'y' or send_to_wpp == 'Y':
            send_whatsapp_message(brokers_to_be_contacted_by_wpp_info)
        else: 
            print('Not sending to Whatsapp.')

    input("\nPress 'Enter' to continue...")
