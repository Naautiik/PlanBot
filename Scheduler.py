from PlanBot import scheduled, Subskrypcje, db
from datetime import datetime
from time import sleep
#subskrypcje = pd.read_csv("subskrypcje.csv")



# while True:
#     if (datetime.now().strftime('%H')) == '17':
#         print("sending")
#         load = sqldf("SELECT * FROM subskrypcje")
#         load = load.values.tolist()
#         for x in load:
#             scheduled(x[0], x[1])
#         sleep(3600)
#     print("Waiting for the right time")
#     sleep(60)


# u1 = Subskrypcje(fb_id = '3519832014751515', klasa = '3F')
# db.session.add(u1)
# db.session.commit()
# db.session.delete(u1)
# db.session.commit()
#
# #user = Subskrypcje.query.filter_by(fb_id='3519832014751515').delete()
# #print(user)
# # db.session.delete(user)
# db.session.commit()
# f = Subskrypcje.query.all()
# print(f)
# for x in f:
#     x = str(x)
#     x = x.split(",")
#     scheduled(x[0], x[1])


godzina = "12"
while True:
    if (datetime.today().weekday()) != 5 and (datetime.today().weekday()) != 6:
        if (datetime.now().strftime('%H')) == godzina:
            print("sending")
            f = Subskrypcje.query.all()
            print(f)
            for x in f:
                x = str(x)
                x = x.split(",")
                print(x)
                scheduled(x[0], x[1])
                sleep(1)
            sleep(1690)
            scheduled("skrr", "skrr")
            sleep(1690)
            scheduled("skrr", "skrr")
            #możliwy błąd jeśli scheduler się obudzi o np. 830 to zapomni o sleepie
        sleep(150)
        if (datetime.now().strftime('%H')) == str(int(godzina)-1):
            print("waiter")
            scheduled("skrr", "skrr")
    else:
        print("weekend!")
        sleep(3600)