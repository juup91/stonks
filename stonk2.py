import yfinance as yf
from datetime import date, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

weekno = date.today().weekday()
fivedays = date.today() - timedelta(2)

if weekno < 5:
        now = date.today()
        daybefore = date.today() - timedelta(5)
        print now
        print daybefore
elif weekno == 5:
        today = date.today() - timedelta(1)
        daybefore == date.today() - timedelta(2)
        print (today)
        print (daybefore)
elif weekno == 6:
        today = date.today() - timedelta(2)
        daybefore = date.today() - timedelta(3)
        print (today)
        print (daybefore)



gme = yf.Ticker("gme")
gme_historical = gme.history(period='5d', interval="1m")
print type(gme_historical)

with open('/home/pi/yfinance/out.txt',  'w') as f:
        f.write(gme_historical.to_string())

#for i in range(0, gme_historical.size):
#       if i == gme_historical.size-1:
#               print(gme_historical[i])
lastrecord = gme_historical.tail(1)
latestprice = str(lastrecord['Open'].values[0])


with open('/home/pi/yfinance/latestprice.txt') as r:
        lines = r.readlines()


previousprice = str(lines)
removechar = "[']"

for character in removechar:
        previousprice = previousprice.replace(character,"")

cleanpreviousprice = previousprice[:-3]
olderprice = float(str(cleanpreviousprice))

Increase = float(latestprice) - olderprice
percentincrease = (Increase / olderprice) * 100
print(olderprice)
print type(olderprice)
print(percentincrease)
print type(percentincrease)

with open('/home/pi/yfinance/latestprice.txt', 'w') as h:
        h.write(latestprice)


first = ("The current price of GME is ")
stringlatestprice = str(latestprice)
second = (". It went up/down ")
stringpercentincrease = str(percentincrease)
third = (" percent since the last price of ")
stringolderprice = str(olderprice)
last = (".")
emailbody = (first + stringlatestprice + second + stringpercentincrease + third + stringolderprice + last) 


fromaddr = "YOUREMAILADDRESS"
toaddr = "supmeat@protonmail.com;jnavarrojr@hotmail.com"

msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "GME Update"

body = emailbody

msg.attach(MIMEText (body,'plain'))

filename = "out.txt"
f = file(filename)


attachment = MIMEText(f.read())

part = MIMEBase('application', 'octet-stream')

encoders.encode_base64(part)

attachment.add_header('Content-Disposition', 'attachment', filename=filename)

msg.attach(attachment)

server = smtplib.SMTP('smtp.gmail.com', 587)

server.starttls()

server.login(fromaddr, "YOURPASSWORD")

text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)

server.quit()