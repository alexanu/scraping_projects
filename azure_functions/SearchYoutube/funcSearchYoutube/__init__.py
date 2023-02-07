import datetime
import logging

import azure.functions as func
from youtubesearchpython import *
import pandas as pd

from keys_config import *

regions = ['AR','AT','AU','BR','CA','CH','CN','DE','ES','FI','FR','GB','GR','HK','IL','IN','IT','KR','KZ','NL','NO','NZ','PL','PT','RO','SE','SI','SK','TH','TR','UA','US']
search_words =['Azure Function', 'Logic App', 'Power App', 'Alpaca Trading']

from keys_config import *

import smtplib
from email.mime.multipart import MIMEMultipart # standard python library
from email.mime.text import MIMEText

def send_email(df_to_send):
    msg = MIMEMultipart() #Setup the MIME
    msg['From'] = 'BTFD'
    msg['To'] = receiver_address
    msg['Subject'] = 'Youtube search result for today'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls() #enable security
    server.login(sender_address, sender_pass) # login with mail_id and password

    html = """\
    <html>
    <head></head>
    <body>
        {0}
    </body>
    </html>
    """.format(df_to_send.to_html())
    part1 = MIMEText(html, 'html')
    msg.attach(part1)
    server.sendmail(sender_address, receiver_address, msg.as_string())
    server.quit()


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    search_result = pd.DataFrame([])
    for word in search_words:
        for reg in regions:
            titles = []
            publ = []
            dur = []
            links = []
            customSearch = CustomSearch(word, VideoUploadDateFilter.today,region = reg)
            for video in customSearch.result()['result']:
                titles.append(video['title'])
                publ.append(video['publishedTime'])
                dur.append(video['duration'])
                links.append(video['link'])
                # print(f"{video['title']} ({video['publishedTime']}, {video['duration']}, {video['link']})")
            temp_df=pd.DataFrame({'Topic': word, 'Title':titles, 'Published':publ, 'Duration':dur, 'Link':links, 'Region':reg})
            search_result =pd.concat([search_result, temp_df])

    search_result.drop_duplicates(subset='Title', keep="last", inplace=True)
    search_result.reset_index(inplace=True, drop=True)
    send_email(search_result)
