import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
import time

#handle the third level of the tournament
def handle_third_level(each_vs, findcharacter):
    #this gets the first 2 tournaments
    tourneys = each_vs[:2]
    #which side is winning?
    losers = find_losing_tourneys(tourneys, findcharacter)
    assert len(losers) == 1
    loser = losers[0]

#handle the second level of the tournament
def handle_second_level(eachvs, findcharacter):
    #there are 6 tournaments, get the first 4!
    print(eachvs)

#handle the first level of the tournament
def handle_first_level(eachvs, findcharacter):
    #there are 4 tournaments, get the first 8!
    print(eachvs)

#send an email with body s!
def send_message(message):
    msg = EmailMessage()
    msg.set_content(message)

    me = 'feheroesalertbypthon@gmail.com'
    emaillist = ['feheroesalertbypthon@gmail.com']
    msg['Subject'] = 'Fire Emblem Heroes Alert!'
    msg['From'] = me
    msg['To'] = emaillist[0]

    msg = msg.as_string()

    # Send the message via gmail
    smtp = smtplib.SMTP('smtp.gmail.com:587')
    smtp.starttls()
    smtp.login(me, 'Abc12345!')
    smtp.sendmail(me,
               emaillist,
               msg)
    smtp.quit()

def find_losing_tourneys(tournaments, findcharacter):
    #which side is winning?
    losers = [
        tourney
        for tourney in tournaments
        if "lose" in str(tourney) and findcharacter in str(tourney)
    ]
    return losers

#Start of program
while True:
    #This uses a lot of processing power. Figure out way to make it use less?5
    t = (int(time.strftime("%H"))*60+ int(time.strftime("%M")))%60
    if t == 4:
        with open("inputgauntlet.txt", "r") as input_file:
            url = input_file.readline()
            findcharacter = input_file.readline()
        headers = {"Accept-Language": "en-US,en;q=0.5"}
        page = requests.get(url, headers=headers)
        if str(page) == "<Response [404]>":
            print("fail")
        else:
            soup = BeautifulSoup(page.content, 'html.parser')
            all_tournaments = soup.find_all(class_='body-section-tournament')
            each_tournament = []
            for tournament_body_section in all_tournaments:
                each_tournament += tournament_body_section.find_all(class_='tournaments-battle')
            each_vs = []
            for n in each_tournament:
                each_vs += n.find_all(class_='tournaments-art-left')
                each_vs += n.find_all(class_='tournaments-art-right')
            number_of_battles = len(each_vs)
            if number_of_battles == 14:
                print('3RD Level')
                handle_third_level(each_vs, findcharacter)
            elif number_of_battles == 12:
                print('2ND Level')
                handle_second_level(each_vs, findcharacter)
            elif number_of_battles == 8:
                print('1ST Level')
                handle_first_level(each_vs, findcharacter)
            else:
                print('Error!')
        #Wait until next hour!
        #time.sleep(3420)


