import pandas as pd
import datetime
import time
import random
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from config import sender_info


class Birthday:
    
    def listBirthdays(self):
        """Extracts birthday information from CSV file"""
        df = pd.read_csv('CSV/birthdays.csv')
        df.fillna('', inplace=True)
        df['last_sent'] = df['last_sent'].astype(str) # Casting column to string 
        return df

    def isToday(self, df, today):
        birthdays_today = df.loc[df['date'] == today]
        return birthdays_today


class Email:

    email_template = 'main.txt'

    def setEmailSenderInfo(self):
        """Sets email sender info"""
        ffullname = sender_info['fromName']
        ffname = sender_info['fromFname']
        flname = sender_info['fromLname']
        femail = sender_info['fromEmail']
        password = sender_info['emailPass']
        return ffullname, ffname, flname, femail, password
    
    def deployEmail(self, file, femail, password, ffname, flname, ffullname, tfname, temail, tmsg):
        """Builds email and deploys over secure connection"""

        # Log into email server, open connection 
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(femail,password)

        # specify login email address
        fromaddr = femail

        # specify headers for adding Send Name
        fromname = formataddr((str(Header(ffullname, 'utf-8')), femail))

        msg = MIMEMultipart()
        msg['From'] = fromname
        msg['To'] = temail
        msg['Subject'] = "HAPPY BIRTHDAY, %s!!" %tfname

        # Get email contents from .txt file
        with open('templates/'+file, "rb") as f:
            email_body = f.read()

        # Note: important to decode
        html = email_body.decode("utf-8").format(tfname=tfname,ffname=ffname,tmsg=tmsg)
        html = str(html)

        try:
            # encoding utf-8 forced necessary for foreign characters
            msg.attach(MIMEText(html, 'html','utf-8'))

            text = msg.as_string()
            # sendmail requires from address, target email and message content as arguments
            server.sendmail(fromaddr, temail, text)

            time.sleep(random.randint(10,20))

        except smtplib.SMTPServerDisconnected:
            print(sys.exc_info())

        # log out of email when finished
        server.quit()

        # kill program
        sys.exit()


def main():
    birthday = Birthday()
    df = birthday.listBirthdays()
    today = str(datetime.datetime.today().date()) # as string for comparison

    # Compare today's date with birthdates listed 
    birthdays_today = birthday.isToday(df, today)
    
    if birthdays_today is not None:
        email = Email()
        for i, row in birthdays_today.iterrows():

            # Check that this person has not had a message sent to them this year
            last_sent = row['last_sent']

            if pd.isnull(last_sent) == True or last_sent is None or last_sent == '': # This needs work to catch all cases
                tfname = row['first_name']
                temail = row['email']
                tmsg = row['msg']

                # Get sender info
                ffullname, ffname, flname, femail, password = email.setEmailSenderInfo()
                # Deploy the email
                email.deployEmail(email.email_template, femail, password, ffname, flname, ffullname, tfname, temail, tmsg)

                # Finally, mark when the email was sent to the person
                df.set_value(i,'last_sent', str(today)) # This method is deprecated, needs to be replaced
            
            else:
                continue

    # Update dataframe, overwrite existing CSV
    df = df.to_csv('CSV/birthdays.csv', encoding="utf-8")

if __name__== "__main__" :
    main()