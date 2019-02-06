import smtplib

def sendMail(FROM, TO, NAME, CODE, SERVER):

    message = "---Password recovery---\
              \n\n\nHi {} your recovery code is {}\
              \n\n\nSupport @JayseSs tg".format(NAME, CODE)

    server = smtplib.SMTP(SERVER)
    server.starttls()
    server.login('python.send', 'smotri4toyamogy')
    server.sendmail(FROM, TO, message)
    server.quit()

#sendMail("pythontestsender@mail.ru", "softelele@mail.ru", "Jayse", "J3SD4","smtp.mail.ru" )
