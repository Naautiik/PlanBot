from flask import Flask, request
from pymessenger import Bot
from keys import PAGE_ACCESS_TOKEN as token
import pandas as pd
from pandasql import sqldf
from datetime import datetime
from listaklas import listaklas
import csv

plan = pd.read_csv("lekcje.csv")
subskrypcje = pd.read_csv("subskrypcje.csv")

VERIFY_TOKEN = "fuckyes"

app = Flask(__name__)
bot = Bot(token)
#tylko na poczatek - przy pierwszym wyloaniu zostaja zmienione
today = weeknum = 0


# Dni:
# 0-4 - pon-pt
# tygodnie:
# 1 - pomaranczowy
# 0 - niebieski
def dateupdate():
    #jako że górna część kodu działa tylko raz to data by się nie zmieniała, więc funkcja będzie zmieniać ją kiedy trzeba
    global weeknum
    global today
    #numer tygodnia określający kolor, +1 wynika z tego że niebieski = 0 ale tygodnie mod 2 = 0 są pomarańczowe
    weeknum = int((datetime.today().strftime('%V')))
    weeknum = (weeknum+1) % 2
    #numer dnia w formacie 0-4 - pon-pt
    today = (datetime.today().weekday())
    print(f"updated datenums are {today} and {weeknum}")
def process_message(text, sender_id):
    global today
    global weeknum
    formatted_message = text
    #kod dodajacy subskrypcje do pliku subskrypcje.csv w formacie id,klasa
    if formatted_message[0:10] == "subskrybuj":
        print(formatted_message)
        if str(formatted_message[11:]) in listaklas:
            subskrypcje = pd.read_csv("subskrypcje.csv")
            czyjest = sqldf(f"SELECT klasa FROM subskrypcje where id = {sender_id}")
            czyjest = czyjest.values.tolist()
            print(czyjest)
            if len(czyjest) == 0:
                with open("subskrypcje.csv", "a", newline='') as csvf:
                    wr = csv.writer(csvf, delimiter=",")
                    wr.writerow([sender_id, formatted_message[11:]])
                    return(f"Od teraz codziennie będziesz dostawać plan lekcji dla klasy {formatted_message[11:]}")
            czyjest = str(czyjest[0]).strip("[']")
            return f"Znajdujesz się już na liście dla klasy {czyjest}. Możesz znajdować się tylko w jednej klasie jednocześnie."
        else:
            return("Nieznana klasa. Pamiętaj, ze przed podwójny rocznik nazwy uwzględniają wielkość liter")
    print(formatted_message[0:12])
    if formatted_message[0:12] == "odsubskrybuj":
        subs = []
        with open("subskrypcje.csv", "r") as csvf:
            for row in csvf:
                if str(sender_id) not in row:
                    subs.append(row)
        with open("subskrypcje.csv", "w", newline='') as csvf:
            print(subs)
            wr = csv.writer(csvf, delimiter=",")
            #wr.writerow(["id", "klasa"])
            for x in subs:
                x = str(x).split(",")
                print(x)
                wr.writerow([x[0].strip("[',]"), x[1][:-1].strip("[',]")])
        return"Nie subskrybujesz już żadnej klasy."

    #kod podajacy plan, wywolywany recznie przez uzytkownika lub przez scheduler
    if formatted_message[0:4].lower() == "plan":
        auto = False
        dateupdate()
        pay = ""
        formatted_message = formatted_message.split(" ")
        klasa = ustawklase(formatted_message, sender_id)
        if klasa == "SubError":
            return"Nie znajdujesz się na liście subskrypcji. Dołącz do jakiejś klasy lub, jeśli już to zrobiłeś, skontaktuj się z administratorem"
        if klasa == False:
            return 'Błędne sformułowanie komendy "plan".\nUżyj "plan klasa"\nlub "plan jutro"\nPamiętaj, że nazwy klas uwzględniają wielkość liter.'
        try:
            if formatted_message[2] == "auto":
                auto = True
                pay += "Dzień dobry! Twój plan lekcji na dzisiaj to:\n"
        except:
            pass
        try:
            arg = formatted_message[1]
            #do usunięcia po zglobalizowaniu
            if arg in listaklas and arg != "3F":
                return("Inne klasy nie są jeszcze wspierane")
        except:
            arg = False
        #Jeśli nie podano argumentu to po 15 da plan na dzień następny, a przed 15 na dzień dzisiejszy
        if (arg == False and (datetime.now().strftime('%H')) > '15') or arg == "jutro":
            pay += "Twój plan lekcji na jutro to: \n"
            today += 1
            if today == 7:
                today = 0
        elif arg == False:
            pay += "Twój plan lekcji na dzisiaj to: \n"
        elif arg in listaklas and auto == False:
            pay += f"Plan lekcji klasy {arg} na dzisiaj to: \n"
        print(today, weeknum)
        #weekend exception
        if today == 5 or today == 6:
            if arg == "jutro" or (datetime.now().strftime('%H')) > '15':
                return"Jutro nie ma żadnych lekcji. Śpij w spokoju!"
            else:
                return"Dzisiaj nie ma żadnych lekcji. Śpij w spokoju!"
        for x in range(1,9):
            #ladowanie lekcji o numerach 1-8 dla okreslonego dnia i koloru
            load = sqldf(f"SELECT lekcja{x} FROM plan where klasa = '{klasa}' and dzien = {today} and kolor = {weeknum}")
            load = load.values.tolist()
            # formatowanie dnia zeby dalo sie przeslac, dopisywanie cyferki etc
            if str(load) == "[[None]]":
                load = "Wolna"
            pay += f"{x}. "
            pay += str(load).strip("[']")
            pay += "\n"
        #usuwanie nadmiarowych lekcji od dolu
        testpay = pay.split("\n")
        print(testpay)
        for y in range (8,0,-1):
            print(testpay[y][3:])
            if testpay[y][3:] == "Wolna":
                testpay.pop(y)
            else:
                break
        testpay = "\n".join(testpay)
        return testpay
    formatted_message = formatted_message.lower()
    if formatted_message == "test":
        print("got here smh")
        return("I work!")
    if formatted_message[0:8] == "dziękuję":
        return"Do usług!"
    if "kocham cię" in formatted_message:
        return"Jestem tylko robotem. Nie mam uczuć. Chociaż dla kogoś takiego jak Ty chciałbym mieć. Szkoda."
    if "dzień dobry" in formatted_message:
        return"Miło Ciebie słyszeć!"
    if formatted_message[0:4] == "Doch":
        return"Doch"
    return("Beep boop. Nie znam tej komendy")

#kod odpowiadajacy za polaczenie z facebookiem
@app.route('/', methods=["POST", "GET"])
def webhook():
    #get message wysyla tylko facebook, wiec jest to kod sluzacy do tworzenia polaczenia
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return "Not connected"
    #post message pochodzi od uzytkownikow, wiec kod wywoluje funkcje tworzaca wiadomosc
    elif request.method == "POST":
        payload = request.get_json()
        event = payload['entry'][0]['messaging']
        #print(event)
        for msg in event:
            text = msg['message']['text']
            sender_id = msg['sender']['id']
            response=process_message(text, sender_id)
            with open("logs.csv", "a", newline='') as logs:
                wr = csv.writer(logs, delimiter=',')
                wr.writerow([sender_id, text, response, str(datetime.now())[0:18]])
                print(text, sender_id, response)
            #wysylanie wiadomosci za pomoca PyMessenger
            bot.send_text_message(sender_id, response)
        return ("received")
#Kod współpracujacy ze Scheduler.py do wysyłania regularnych wiadomości. Scheduler.py wywołuje go o 8 rano
def scheduled(sender_id,klasa):
    text = f"plan {klasa} auto"
    print(text,"st1")
    response = process_message(text,sender_id)
    bot.send_text_message(sender_id, response)
def ustawklase(formatted_message, sender_id):
    global today
    try:
        klasa = formatted_message[1]
    except:
        klasa = False
    if klasa not in listaklas and klasa != "jutro" and klasa != False:
        return False
    if klasa == "jutro" or klasa == False:
        try:
            subskrypcje = pd.read_csv("subskrypcje.csv")
            klasa = sqldf(f"SELECT klasa from subskrypcje where id = {sender_id}")
            klasa = klasa.values.tolist()
            klasa = str(klasa[0]).strip("[']")
        except:
            return"SubError"
        print(klasa, "ustawklase")
    return klasa

if __name__ == "__main__":
    app.run()