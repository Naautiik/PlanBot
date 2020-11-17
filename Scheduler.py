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

godzina = "0700"

g2 = str(godzina[0:3] + str(int(godzina[3])+1))

while True:
    if (datetime.today().weekday()) != 5 and (datetime.today().weekday()) != 6:
        if (datetime.now().strftime('%H%M')) == godzina or (datetime.now().strftime('%H%M')) == g2:
            print("sending")
            f = Subskrypcje.query.all()
            print(f)
            scheduled("skrr", "skrr")
            for x in f:
                x = str(x)
                x = x.split(",")
                print(x)
                scheduled(x[0], x[1])
                sleep(2)
            sleep(3600)
        print("waiting", (datetime.now().strftime('%H%M')))
        if (datetime.now().strftime('%H')) == '07':
            sleep(20)
        else:
            sleep(40)
    else:
        print("weekend!")
        sleep(3600)