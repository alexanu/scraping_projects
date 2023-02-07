from twilio.rest import Client

    def send_msg(self, msg):
        # Your Account SID from twilio.com/console
        account_sid = "AC0dadb0ce3f1db887ecf2cc5209932676"
        # Your Auth Token from twilio.com/console
        auth_token = "7eb9f55beeb3cfea278ccc183cf0f46a"

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            to="+601128174379",
            from_="+17067395816",
            body=msg)
        return message.sid
        
    def create_msg(self, time_to_send):
        if time_to_send in self.time_list:
            data = self.final_data.loc[
                self.final_data['tmsp_3_min'] == time_to_send].copy()
            data = json.loads(data.to_json(orient='records'))
            main_body = str()
            for each in data:
                body = "Based: "+each['economy']+"\n"\
                    + "Info: "+each['name']+"\n"\
                    + "Impact: "+str(each['impact'])+"\n"\
                    + "Time: "+each['timestamp_af']
                main_body = main_body + "\n"+body
            code = self.send_msg(msg=body)
            print(code)
            
            
# ------------------------------------------------------------------------------------------------------------------------            
# ------------------------------------------------------------------------------------------------------------------------

import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

SUBSCRIBE_LIST = [
    'weiyi.alan.chen@gmail.com',
    'wchen7@baml.com'
]

def email_login():
    me = raw_input("Your Gmail Address: ")
    import getpass
    password = getpass.getpass("Password: ")
    return me, password

def send_mail(send_from, send_to, subject, text, files=[], server="localhost", port=587, username='', password='', isTls=True):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime = True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(f,"rb").read() )
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(f)))
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if isTls: smtp.starttls()
    smtp.login(username,password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()

    
import pandas
import urllib2
from emails import SUBSCRIBE_LIST, email_login, send_mail

def get_ETF_fr_YH(filename):
    ls_etf = []
    the_page = urllib2.urlopen('http://finance.yahoo.com/etf/lists/?mod_id=mediaquotesetf&tab=tab3&rcnt=50').read()    
    splits = the_page.split('<a href=\\"\/q?s=')
    etf_symbols = [split.split('\\')[0] for split in splits[1:]]
    for etf in etf_symbols:
        ls_etf.append(etf)
    df = pandas.DataFrame({'ETF': ls_etf})
    df.set_index('ETF').to_csv(filename)

def run(me, password):
    get_ETF_fr_YH('ETF.csv')
    send_mail(
        send_from = 'NoReply@gmail.com', 
        send_to = SUBSCRIBE_LIST, 
        subject = 'Suggested ETF', 
        text = """Hello,
Attachment includes the ETFs.
Sincerely,
""", 
        files = ['ETF.csv'], 
        server = 'smtp.gmail.com',
        username = me,
        password = password
    )

if __name__ == '__main__':
    me, password = email_login()
    run(me, password)    

    
    
# ------------------------------------------------------------------------------------------------------------------------            
# ------------------------------------------------------------------------------------------------------------------------

import urllib2
import time
import smtplib, random
import os, sys
import personal

SECOND_PER_MINUTE = 60


def send_mail(subject):
# The below code never changes, though obviously those variables need values.
  GMAIL_USERNAME = personal.gmail_address
  GMAIL_PASSWORD = personal.password
  RECIPIENT = personal.recipient
  session = smtplib.SMTP('smtp.gmail.com', 587)
  session.ehlo()
  session.starttls()
  session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
  
  headers = "\r\n".join(["from: " + "Do hackme",
                         "subject: " + subject,
                         "to: " + "me",
                         "mime-version: 1.0",
                         "content-type: text/html"])

  # body_of_email can be plaintext or html!                    
  content = headers + "\r\n\r\n" 
  session.sendmail(GMAIL_USERNAME, RECIPIENT, content)

pwd = personal.pwd
# print(pwd)
# read product names;
pfile = open(pwd + '/products.txt', 'r')
products = [line.strip() for line in pfile]

# read deal websites;
webFile = open(pwd + '/websites.txt', 'r')
webs = [line.strip() for line in webFile]

need = [True] * len(products)
count = 1

while True in need:
  for i in range(len(products)):
    if need[i]:
      product = products[i].lower()
      
      for address in webs:
        page = urllib2.urlopen(address).read()
        page = page.lower()
        if product in page:
          title = address + ' has ' + product
          send_mail(title)
          need[i] = False

  LB = 5
  UB = 15
  minute = random.randint(LB, UB)
  time.sleep(SECOND_PER_MINUTE * minute)
    
    
# ----------------------------------------------------------------------------------------------------------------------
# Source: https://github.com/muthash/flight-booking-flask/blob/develop/app/helpers/send_email.py

import os
import atexit
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask_mail import Message

from app import mail
from app.helpers.query_helpers import get_tomorrow_flights


def get_booked_flights():
    logging.info('Fetching tomorrows flights from the database')
    flights = []
    flights_to = get_tomorrow_flights()
    for flight in flights:
        total_booked = flight.booked_business + flight.booked_economy
        total_seats = flight.airplane.total_seats
        if (total_seats - total_booked) != total_seats:
            flights.append(flight)
    return flights


def create_message_list(flights):
    messages = []
    for flight in flights:
        message = Message(
            subject='Flight Reservation Reminder',
            recipients=[flight.bookings.owner.email],
            html=(f'Hello {flight.bookings.owner.email.name},'
                  f'<p> This is to remind you of your scheduled flight <b>{flight.airplane.reg_number}</b>'
                  f'from <b>{flight.airport.name}</b> on <b>{flight.departure_date}</b> </p>'
                  f'<p> Please check in for your flight three hours before departure time</p>'
                  f'<p> Thank you </p>')
                )
        messages.append(message)
    return messages


def send_reminder_email():
    flights = get_booked_flights()
    if not flights:
        logging.info("There are no bookings for tommorrow flights yet")
    else:
        logging.info("creating the mailing lists ...")
        messages = create_message_list(flights)

        logging.info("connecting to the mail server ...")
        with mail.connect() as conn:
            for message in messages:
                try:
                    conn.send(message)
                    "sending success: " + message.recipients
                except Exception as e:
                    logging.exception("sending failed: " + message.recipients)


def background_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=send_reminder_email,
        trigger=IntervalTrigger(start_date='2019-07-02 03:00:00', days=1),
        id='reminder_email_job',
        name='sending emails in the background',
        replace_existing=True)
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    atexit.register(lambda: scheduler.shutdown())
    
#######################################################################################################

import smtplib

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from sysdata.private_config import get_list_of_private_config_values

def send_mail_file(textfile, subject):
    """
    Sends an email of a particular text file with subject line

    """

    fp = open(textfile, 'rb')
    # Create a text/plain message
    msg = MIMEText(fp.read())
    fp.close()

    msg['Subject'] = subject

    _send_msg(msg)


def send_mail_msg(body, subject):
    """
    Sends an email of particular text file with subject line

    """

    # Create a text/plain message
    msg = MIMEMultipart()

    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    _send_msg(msg)

def send_mail_pdfs(preamble, filelist, subject):
    """
    Sends an email of files with preamble and subject line

    """

    # Create a text/plain message
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg.preamble = preamble

    for file in filelist:
        fp = open(file, 'rb')
        attach = MIMEApplication(fp.read(), 'pdf')
        fp.close()
        attach.add_header('Content-Disposition', 'attachment', filename='file.pdf')
        msg.attach(attach)

    _send_msg(msg)



def _send_msg(msg):
    """
    Send a message composed by other things

    """

    email_server, email_address, email_pwd = get_email_details()

    me = email_address
    you = email_address
    msg['From'] = me
    msg['To'] = you

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP(email_server, 587)
    s.login(email_address, email_pwd)
    s.sendmail(me, [you], msg.as_string())
    s.quit()


def get_email_details():
    yaml_dict = get_list_of_private_config_values(['email_address', 'email_pwd', 'email_server'])

    email_address = yaml_dict['email_address']
    email_pwd = yaml_dict['email_pwd']
    email_server = yaml_dict['email_server']

    return email_server, email_address, email_pwd



if __name__ == "__main__":
    send_mail_msg("testing", "test subject")


###################################################################################

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import boto3

class Email(object):

    def __init__(self,subject, to=['mark.refermat@gmail.com']):
        self.to = to
        self.subject = subject
        self.text = None
        self.attachment = None
        self.msg = MIMEMultipart()
        
    def add_text(self, text):
        msgText = MIMEText(text,'html')
        self.msg.attach(msgText)

    def add_attachment(self, file_name):
        msgText = MIMEText('<br><img src="cid:%s"><br>' %  file_name, 'html')  
        self.msg.attach(msgText) 
        fp=open(file_name,'rb')
        self.attachment = MIMEImage(fp.read())
        fp.close()
        self.attachment.add_header('Content-ID', '<{}>'.format(file_name))
        self.msg.attach(self.attachment)
        
    def add_attachments(self, list_of_files):
        m=''
        for file_name in list_of_files:
            m=m+'<br><img src="cid:%s"><br>' %  file_name       
        msgText = MIMEText(m, 'html')  
        self.msg.attach(msgText) 
        for file_name in list_of_files:    
            fp=open(file_name,'rb')
            self.attachment = MIMEImage(fp.read())
            fp.close()
            self.attachment.add_header('Content-ID', '<{}>'.format(file_name))
            self.msg.attach(self.attachment)
        
    def send(self):
        from_addr='mrefermat@hotmail.com'
        connection = boto3.client('ses',region_name="us-east-1")
        self.msg['Subject'] = self.subject
        self.msg['From'] = from_addr
        #self.msg['To'] = self.to
        self.msg['To'] = ','.join(self.to)

        return connection.send_raw_email(RawMessage={'Data': self.msg.as_string()},
                                         Source=from_addr,
                                         Destinations=self.to)

# -------------------------------------------------------------------------------------------------
# email top-movers stocks

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import yahoo_fin.stock_info as si
import time
import datetime
from config import *
import os

df = si.get_day_gainers()
df_filtered = df[df['% Change']>=5]

today = datetime.date.today()
file_name = '/Users/shashank/Documents/Code/Python/Outputs/movers/' + "Top Gainers " + str(today) +".csv"
df_filtered.to_csv(file_name)

def send_email():
   email_sender = junk_email_username()
   email_recipient = good_email_username()
   msg = MIMEMultipart()
   email_message = "Attached are today's market movers"
   attachment_location= file_name
   msg['From'] = email_sender
   msg['To'] = email_recipient
   msg['Subject'] = "Stock Market Movers"
   msg.attach(MIMEText(email_message, 'plain'))
   if attachment_location != '':
      filename = os.path.basename(attachment_location)
      attachment = open(attachment_location, 'rb')
      part = MIMEBase('application', 'octet-stream')
      part.set_payload(attachment.read())
      encoders.encode_base64(part)
      part.add_header('Content-Disposition', "attachment; filename=%s" % filename)
      msg.attach(part)
   try:
      server = smtplib.SMTP('smtp.gmail.com', 587)
      server.ehlo()
      server.starttls()
      server.login(junk_email_username(), junk_email_password())
      text = msg.as_string()
      server.sendmail(email_sender, email_recipient, text)
      print('email sent')
      server.quit()
   except Exception as e:
      print(e)
   return schedule.CancelJob

import schedule
schedule.every().day.at("4:00").do(send_email)
while schedule.jobs:
   schedule.run_pending()
   time.sleep(1)


##################################################################################################
import os
import smtplib
import getpass
import sys
import time
email = raw_input('Attacker Gmail Address : ')
user = raw_input('Anonymous name : ')
passwd = getpass.getpass('Password: ')
to = raw_input('\nTo: ')
body = raw_input('Message: ')
total = input('Number of send: ')

smtp_server = 'smtp.gmail.com'
port = 587

try:
    server = smtplib.SMTP(smtp_server,port) 
    server.ehlo()
    server.starttls()
    server.login(email,passwd)
    for i in range(1, total+1):
        subject = os.urandom(9)
        msg = 'From: ' + user + '\nSubject: ' + '\n' + body
        server.sendmail(email,to,msg)
        print "\rE-mails sent: %i" % i
        time.sleep(1)
        sys.stdout.flush()
    server.quit()
    print '\n Done !!!'
except KeyboardInterrupt:
    print '[-] Canceled'
    sys.exit()
except smtplib.SMTPAuthenticationError:
    print '\n[!] The username or password you entered is incorrect.'
sys.exit()

###############################################################################################################
import pandas as pd
import smtplib

SenderAddress = "<Email Address of sender>"
password = "password of sender"

e = pd.read_excel("Email.xlsx")
emails = e['Emails'].values
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(SenderAddress, password)
msg = "Hello this is a email form python"
subject = "Hello world"
body = "Subject: {}\n\n{}".format(subject,msg)
for email in emails:
    server.sendmail(SenderAddress, email, body)
server.quit()