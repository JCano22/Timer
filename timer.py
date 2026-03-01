import time
import os

def clear():
    os.system("clear")

def play_alarm():
    os.system("afplay /System/Library/Sounds/Glass.aiff")

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
    play_alarm()
    print("Time is up.") 
    
def breakTimer(minutes):
    break_sec = minutes * 60

    while(break_sec):
        m, s = divmod(break_sec, 60)
        timer = f"{m:02d}:{s:02d}"

        clear()
        print("Break time")
        print("--------------")
        print(timer)

        time.sleep(1)
        break_sec -= 1

    clear()
    play_alarm()
    play_alarm()
    print("Break is up, time to get back to studying.")


minutes = int(input("Enter the time you want to study: "))
break_min = int(input("Enter the time you want in between study times: "))
repeats = int(input("How many times would you like to repeat the cycle: "))

for i in range(repeats):
    studyTimer(minutes)
    if i < repeats - 1:
        breakTimer(break_min)
        


