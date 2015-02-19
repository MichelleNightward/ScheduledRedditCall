__author__ = 'mthepyromaniac'

import twilio
import twilio.rest
from twilio.rest import TwilioRestClient
import twilio.twiml
import praw
from apscheduler.schedulers.blocking import BlockingScheduler

account_sid = "sid"
auth_token = "token"
toNumber = "number"
fromNumber = "number"
headline = "something"


sched = BlockingScheduler()
client = TwilioRestClient(account_sid, auth_token)
userAgent = praw.Reddit(user_agent='headline_call v1.0')


@sched.scheduled_job('interval', minutes=3) #testing schedule stuff here
def timed_job():
    print('testing every three minutes.')
    #MakeCall()

@sched.scheduled_job('cron', day_of_week='thu', hour=17) #here choose when the call should be placed
def scheduled_job():
    print('on the hour by the day.')
    MakeCall()


def MakeCall(): #ask twilio to place a call
    headline = str(RedditHeadline()) #use reddit headline function to pull in headline then change it to string
    headline = headline[7:] #remove the xxxx :: at the beginning of each headline
    headline = headline.replace(" ","%20") #format leftover string so it fits into twimlet url properly
    try:
        call = client.calls.create(to=toNumber, #place actual call
                           from_=fromNumber,
                           url="http://twimlets.com/echo?Twiml=%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%3F%3E%3CResponse%3E%3CSay%20voice%3D%22alice%22%3EHello.%20Michelle%20Rooy.%20The%20top%20reddit%20headline%20for%20today%20is%20%7B%7B%20"+ headline + "%20%7D%7D%20%3C%2FSay%3E%3C%2FResponse%3E&")
        print(headline)
    except twilio.rest.TwilioException as e: #error handling
        print e


def RedditHeadline(): #pull in headline
    submissions = userAgent.get_front_page(limit=1) #look at front page, pull in the number of headlines detailed by the limit
    for item in submissions:
        return item


sched.start() #Start the schedule
#MakeCall() #for testing purposes