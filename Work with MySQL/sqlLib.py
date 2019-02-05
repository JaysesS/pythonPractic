import mysql.connector
import sys, string
import hashlib

#Jayse Anime1337
#Evas NeAnime1337
#Yasha KitKat0999
#Alexsey JopaKota123


class MySQL():

    def __init__(self, host, user, passwd, database):

        self.host = str(host)
        self.user = str(user)
        self.passwd = str(passwd)
        self.database = str(database)
        self.table = 'users'
        self.mydb = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.passwd,
            database = self.database
        )
        self.mycursor = self.mydb.cursor()
        x = self.getLastIdInTable()
        if (x != None):
            self.maxIdInTable = x
        else:
            self.maxIdInTable = 0

    def createTable(self):

        command = "CREATE TABLE {} (id INT NOT NULL, login CHAR(25), pass CHAR(128));".format(self.table)
        self.mycursor.execute(command)
        self.mydb.commit()
        self.maxIdInTable = 0

    def deleteTable(self):

        command = "DROP TABLE IF EXISTS {}".format(self.table)
        self.mycursor.execute(command)
        self.maxIdInTable = 0

    def checkPassword(self, passwd):

        passwd = passwd.strip()
        has_no = set(passwd).isdisjoint
        return not (len(passwd) < 6
                or has_no(string.digits)
                or has_no(string.ascii_lowercase)
                or has_no(string.ascii_uppercase))

    def addRegisterUser(self):

        print("Registration.")
        id = self.maxIdInTable + 1
        login = str(input("Enter login: "))
        passwd = str(input("Enter password: "))
        if self.checkPassword(passwd) and not self.validUser(login):
            passwd = self.hashPassword(passwd)
            command = "INSERT INTO {} (id, login, pass) VALUES ('{}', '{}', '{}');".format(self.table, id, login, passwd)
            self.mycursor.execute(command)
            self.mydb.commit()
            self.printTable()
        else:
            print("Enter good password or your username is already taken!")

    def loginUser(self):

        print("Login.")
        login = str(input("Enter login: "))
        passwd = self.hashPassword(str(input("Enter password: ")))
        command = "SELECT 'id' FROM {}.{} where login = '{}' and pass = '{}';".format(self.database, self.table, login, passwd)
        self.mycursor.execute(command)
        try:
            for i in self.mycursor:
                res = i[0]
            if res != None:
                print("Login!")
        except Exception as e:
            print("Сheck your input..")

    def validUser(self, login):

        command = "SELECT id FROM {}.{} where login = '{}';".format(self.database, self.table, login)
        self.mycursor.execute(command)
        try:
            for i in self.mycursor:
                res = i
            if res != None:
                return True
        except Exception as e:
            return False

    def getLastIdInTable(self):

        command = "SELECT MAX(id) FROM {}".format(self.table)
        self.mycursor.execute(command)
        for res in self.mycursor:
            return res[0]

    def clearAllUser(self):

        command = "DELETE FROM {}".format(self.table)
        self.mycursor.execute(command)
        self.mydb.commit()
        self.maxIdInTable = 0

    def printTable(self):

        command = "SELECT * FROM {}".format(self.table)
        self.mycursor.execute(command)
        print("\n------TABLE----------")
        for res in self.mycursor:
            print(res)
            print("---------------------")

    def hashPassword(self, passwd):

        h_object = hashlib.sha512(passwd.encode())
        h_dig = h_object.hexdigest()
        return str(h_dig)

def main():

    workTest = MySQL("localhost","root","passwd","python_test")
    print("\n1. Register\n2. Login\n3. Print Table\n4. Clear Table\n5. Exit")
    ans = str(input("Choose: "))
    print()
    if(ans == "1"):
        workTest.addRegisterUser()
    if(ans == "2"):
        workTest.loginUser()
    if(ans == "3"):
        workTest.printTable()
    if(ans == "4"):
        workTest.clearAllUser()
    if(ans == "5"):
        sys.exit(0)

if __name__ == '__main__':
    while(True):
        main()

#host="localhost",
#user="root",
#passwd="passwd",
#database="python_test"
#mycursor.execute("CREATE DATABASE test_db_from_python")
#mycursor.execute("CREATE TABLE students (name VARCHAR(255), age INTEGER(10))")
#CREATE TABLE users (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, login CHAR(25), pass CHAR(25));
#INSERT INTO users (id, login, pass) VALUES (NULL, 'Jayse', '12345');
