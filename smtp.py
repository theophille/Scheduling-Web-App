import smtplib

sender = 'at.proiect.iap4@gmail.com'
rec = 'theophille.developing@gmail.com'
password = 'wtanegntkxtysgkf'
message = 'Hello from SMTP script'

server = smtplib.SMTP('smtp.gmail.com', 587)

server.starttls()
server.login(sender, password)
print('Login success')
server.sendmail(sender, rec, message)
print('Mail sent')