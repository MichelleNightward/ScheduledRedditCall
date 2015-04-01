
import twilio
import twilio.rest
from twilio.rest import TwilioRestClient
import twilio.twiml
import praw
import re
from apscheduler.schedulers.blocking import BlockingScheduler
import urllib

account_sid = "sid"
auth_token = "token"
toNumber = "number"
fromNumber = "number"


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


ddef MakeCall(): #ask twilio to place a call
    url = "http://twimlets.com/message?Message%5B0%5D=" #first portion of twilio message URL
    headline = urllib.quote("Hello. Michelle Rooy. The top reddit headline for today is " + re.sub(r'[^a-zA-Z ]+', '', RedditHeadline()).encode('utf8')) #URL encode the message to be played once call is picked up
    try:
        call = client.calls.create(to=toNumber, #place actual call
                           from_=fromNumber,
                           url=url + headline) #concatenate url and headline strings to create a complete twilio message url
        print(headline)
    except twilio.rest.TwilioException as e: #error handling
        print e


def RedditHeadline(): #pull in headline
    submissions = userAgent.get_front_page(limit=1) #look at front page, pull in the number of headlines detailed by the limit
    for item in submissions:
        return item.title

if __name__ == '__main__':
    sched.start() #Start the schedule
#MakeCall() #for testing purposes
