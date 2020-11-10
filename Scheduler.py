from PlanBot import scheduled, Subskrypcje, db
from datetime import datetime
from time import sleep



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


godzina = "2243"
while True:
    if (datetime.today().weekday()) != 5 and (datetime.today().weekday()) != 6:
        if (datetime.now().strftime('%H%M')) == godzina:
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
        print("waiting", (datetime.now().strftime('%H%M')))
        sleep(50)
    else:
        print("weekend!")
        sleep(3600)