import smtplib

emailLogin = "python.send"
emailDomen = "python.send@mail.ru"
emailPassword = "smotri4toyamogy"

def sendMail(FROM, TO, NAME, CODE, SERVER):

    message = "---Password recovery---\
              \n\n\nHi {} your recovery code is {}\
              \n\n\nSupport @JayseSs tg".format(NAME, CODE)

    server = smtplib.SMTP(SERVER)
    server.starttls()
    server.login('{}', '{}').format(emailLogin, emailPassword)
    server.sendmail(FROM, TO, message)
    server.quit()

#sendMail("pythontestsender@mail.ru", "softelele@mail.ru", "Jayse", "J3SD4","smtp.mail.ru" )
