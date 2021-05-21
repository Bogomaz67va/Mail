from model.mail import Mail


if __name__ == '__main__':
    gmail_or_yandex = Mail('login', 'password')
    print(gmail_or_yandex.send_message('gmail.com', 'recipient@mail.ru', 'Subject', 'Text(body)'))
    print(gmail_or_yandex.read_message('gmail.com', 'INBOX', 10))