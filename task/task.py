import subprocess
import sys
from datetime import timedelta, datetime

# def end(stoptime):
#     print(datetime.now() + " " + stoptime)
#     if (datetime.now() == stoptime):
#         Popen.kill()


# def start(timeToHardFork):
#     stoptime = datetime.now() + timedelta(seconds=int(timeToHardFork))
#     subprocess.Popen("python3 manage.py runserver")
#     return stoptime

# if __name__ == "__main__":
#     stoptime = start(sys.argv[1])
#     while True:
#         print("jopa")
#         end(stoptime)

def test(time):
    nowtime = datetime.now()
    stoptime = str(nowtime + timedelta(seconds=int(time)))
    args = ["python3", "manage.py", "runserver"]
    proc = subprocess.Popen(args)
    i = 0
    while i != 1000:
        i+=1
        print(i)
        if (str(datetime.now())[:-7] == str(stoptime)):
           proc.kill()
        


if __name__ == "__main__":
    test(sys.argv[1])
