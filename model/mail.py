import smtplib
import re
from email.header import decode_header, make_header
import imaplib
import email.message
import os


class Mail:
    _MAIL_PATTERNS = r'^\D[a-z]+\.[a-z]+'
    _PORT = 587
    _FILE_NAME = 'message.txt'
    _ROOT_DIR = os.path.abspath(os.curdir).replace('model', '').replace('\\', '/')

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password

    @staticmethod
    def valid_mail_smtp_imap(valid_mail: str):
        if not re.search(Mail._MAIL_PATTERNS, valid_mail):
            return f'Неправильно указан smtp: {valid_mail}\nПравильно: [.com, .ru]'

    def send_message(self, mail_smtp: str, recipient: str, subject: str, text: str):
        if not Mail.valid_mail_smtp_imap(mail_smtp):
            smtp_obj = smtplib.SMTP(f'smtp.{mail_smtp}', Mail._PORT)
            smtp_obj.ehlo()
            smtp_obj.starttls()
            try:
                smtp_obj.login(self.login, self.password)
            except smtplib.SMTPAuthenticationError:
                return f'Неверно указан логин: {self.login} или пароль: {self.password}'
            message = f"Subject: {subject}\n{text}".encode('utf-8')
            smtp_obj_sendmail = smtp_obj.sendmail(self.login, recipient, message)
            if len(smtp_obj_sendmail) == 0:
                smtp_obj.quit()
                return f'Сообщение успешно отправлено, {recipient}'
            else:
                smtp_obj.quit()
                return 'Неверно указан email'
        else:
            return Mail.valid_mail_smtp_imap(mail_smtp)

    def read_message(self, imap_mail: str, select_folder: str, count_message: int):
        if not Mail.valid_mail_smtp_imap(imap_mail):
            mail = imaplib.IMAP4_SSL(f'imap.{imap_mail}')
            mail.login(self.login, self.password)
            mail.select(select_folder)
            result, data = mail.search(None, "ALL")
            len_uid_s_message = len(data[0].split())
            if len_uid_s_message >= count_message > 0:
                message_list = data[0].split()[-count_message:]
            elif count_message <= 0:
                return f'Кол-во сообщений не может быть меньше 0, у вас {count_message}'
            else:
                return f'Всего сообщений: {len_uid_s_message}'
            for uid_s in sorted(message_list, reverse=True):
                status, data = mail.fetch(uid_s, '(RFC822)')
                msg = email.message_from_bytes(data[0][1], _class=email.message.EmailMessage)
                subject = make_header(decode_header(msg['Subject']))
                from_email = make_header(decode_header(msg['From']))
                to_email = make_header(decode_header(msg['To']))
                date_email = make_header(decode_header(msg['Date']))
                with open(f'{Mail._ROOT_DIR}{Mail._FILE_NAME}', 'a', encoding='utf-8') as f:
                    f.write(f"Date: {date_email}\n"
                            f"Subject: {str(subject)}\n"
                            f"From: {from_email}\n"
                            f"To: {to_email}\n\n")
            mail.logout()
            return f'Сохранено, открой файл {Mail._ROOT_DIR}{Mail._FILE_NAME}'
        else:
            return Mail.valid_mail_smtp_imap(imap_mail)
