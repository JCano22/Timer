import time
import os

def clear():
    os.system("clear")

def studyTimer(minutes):
    total_seconds = minutes * 60 #converting minutes to seconds to count down until 0

    while(total_seconds):
        min, sec = divmod(total_seconds, 60)
        timer = f"{min:02d}:{sec:02d}"

        clear()
        print("Study time")
        print("--------------")
        print(timer)

        time.sleep(1)
        total_seconds -= 1

    clear()
    print("Time is up.") 

minutes = int(input("Enter time you want to study: "))
studyTimer(minutes)
        


