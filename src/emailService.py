import imaplib
import base64
import os
import email

def logon():
    print("Logging email")
    email_user = 'federico.rivarola@vivatia.com' #input('federico.rivarola@vivatia.com')
    email_pass = 'SoyPowa123' #input('SoyPowa123')
    mail = imaplib.IMAP4_SSL("outlook.office365.com",993)
    mail.login(email_user, email_pass)
    return mail

def getMails(response_part):
    if isinstance(response_part, tuple):
        msg = email.message_from_string(response_part [1].decode('utf-8'))
        email_subject = msg['subject']
        email_from = msg['from']
        print ('From : ' + email_from + '\n')
        print ('Subject : ' + email_subject + '\n')
        print(msg.get_payload(decode=True))      

def getAttachments(email_message):
    for part in email_message.walk():
        # this part comes from the snipped I don't understand yet... 
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
        if bool(fileName):
            filePath = os.path.join('/attachments/', fileName)
            if not os.path.isfile(filePath) :
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
                print('Downloaded '+fileName+ 'from ' + subject)


def main():
    mail = logon()
    print('logged')
    mail.select(mailbox='INBOX/PRISMA')
    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()
    print(id_list)
    print('result mailservice: ' + type)
    if type == 'OK':
        for num in data[0].split():
            type, data = mail.fetch(num, '(RFC822)' )
            raw_email = data[0][1]
            # converts byte literal to string removing b''
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)
            for part in email_message.walk():
                #getMails(part)
                if part.get('Content-Disposition') is not None:
                    continue
                if part.get('Subject') != None:
                    subject = str(part.get('Subject'))
                    #Es respuesta?
                    if(subject.find('RE: ') != -1):
                        print('es rta -> ' + subject)
                    else:
                        #No es respuesta
                        print('No es rta -> ' + subject)
                    continue

main()