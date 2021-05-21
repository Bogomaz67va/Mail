# КОД ПОЛНОСТЬЮ ПЕРЕРАБОТАН
# FAQ
* для yandex желательно создать приложение, https://passport.yandex.ru/profile/ Пароли Приложения Почта или https://yandex.ru/support/mail/mail-clients/others.html
* для gmail либо включить небезопасные приложения и использовать пароль https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4N_fZ64Mf7eB2x4rZ9fJcGG_hBimURUgg86TgpacWI7Nu8c-PmDm3GTgwo-xlwwi7zEWOLJgXwCtNMoO-FIcF_i327Ahg либо Аккаунт Google, Безопасность, Настроить двухэтапную аутентификацию, Пароли приложений, создать новое приложение Почта, имя любое, и паролем будет 16ти символьный код
* для остальный все работает в штатном режиме, логин пароль
##### send_message: mail_smtp: str, recipient: str, subject: str, text: str 
* mail_smtp - параметр smtp, например **mail.com**, **yandex.ru** и т.д
* recipient - отправитель test@mail.ru
* subject - тема письма
* text - текст письма

##### read_message: self, imap_mail: str, select_folder: str, count_message: int
* imap_mail - параметр imap, например **mail.com**, **yandex.ru** и т.д
* select_folder - INBOX
* count_message - кол-во сообщений по которым будет записана информация в файл message.txt

Мы устроились на новую работу. Бывший сотрудник начал разрабатывать модуль для работы с почтой, но не успел доделать его. Код рабочий. Нужно только провести рефакторинг кода.

1. Создать класс для работы с почтой;
2. Создать методы для отправки и получения писем;
3. Убрать "захардкоженный" код. Все значения должны определяться как аттрибуты класса, либо аргументы методов;
4. Переменные должны быть названы по стандарту PEP8;
5. Весь остальной код должен соответствовать стандарту PEP8;
6. Класс должен инициализироваться в конструкции.
```python
if __name__ == '__main__'
```


Скрипт для работы с почтой.
```python
import email
import smtplib
import imaplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart


GMAIL_SMTP = "smtp.gmail.com"
GMAIL_IMAP = "imap.gmail.com"

l = 'login@gmail.com'
passwORD = 'qwerty'
subject = 'Subject'
recipients = ['vasya@email.com', 'petya@email.com']
message = 'Message'
header = None


#send message
msg = MIMEMultipart()
msg['From'] = l
msg['To'] = ', '.join(recipients)
msg['Subject'] = subject
msg.attach(MIMEText(message))

ms = smtplib.SMTP(GMAIL_SMTP, 587)
# identify ourselves to smtp gmail client
ms.ehlo()
# secure our email with tls encryption
ms.starttls()
# re-identify ourselves as an encrypted connection
ms.ehlo()

ms.login(l, passwORD)
ms.sendmail(l,
ms, msg.as_string())

ms.quit()
#send end


#recieve
mail = imaplib.IMAP4_SSL(GMAIL_IMAP)
mail.login(l, passwORD)
mail.list()
mail.select("inbox")
criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
result, data = mail.uid('search', None, criterion)
assert data[0], 'There are no letters with current header'
latest_email_uid = data[0].split()[-1]
result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
raw_email = data[0][1]
email_message = email.message_from_string(raw_email)
mail.logout()
#end recieve

```    