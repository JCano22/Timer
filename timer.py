import os, wx, threading
from wx.lib.stattext import GenStaticText

theApp = wx.App()
f = wx.Frame(None, title="Study Timer", size=(400, 300))
panel = wx.Panel(f)

time_label = GenStaticText(panel, label="00:00", style=wx.ALIGN_CENTER)
mode_label = GenStaticText(panel, label="Study Time!", style=wx.ALIGN_CENTER)

time_label.SetFont(wx.Font(48, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
mode_label.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

sizer = wx.BoxSizer(wx.VERTICAL)
sizer.Add(mode_label, 0, wx.ALIGN_CENTER | wx.TOP, 20)
sizer.Add(time_label, 0, wx.ALIGN_CENTER | wx.TOP, 10)
panel.SetSizer(sizer)

total_seconds = 10
is_study = True
cycles_left = 0

def play_alarm():
    os.system("afplay /System/Library/Sounds/Ping.aiff")

def on_tick(event):
    global total_seconds, is_study, cycles_left, break_min, minutes, wx_timer

    if total_seconds > 0:
        min, sec = divmod(total_seconds, 60)  
        time_label.SetLabel(f"{min:02d}:{sec:02d}")
        total_seconds -= 1
    elif total_seconds == 0:
        time_label.SetLabel("00:00")
        if is_study:
            mode_label.SetLabel("Break time!")
            is_study = False
            total_seconds = break_min * 60
            t = threading.Thread(target=play_alarm)
            t.start()
        else:
            mode_label.SetLabel("Study time!")
            is_study = True
            total_seconds = minutes * 60
            cycles_left -= 1
            if cycles_left == 0:
                mode_label.SetLabel("Finished!")
                wx_timer.Stop()
            t = threading.Thread(target=play_alarm)
            t.start()
f.Show()

#setting timer
wx_timer = wx.Timer(f)
f.Bind(wx.EVT_TIMER, on_tick, wx_timer)

#user prompts for minutes, break time, and repeats
minutes = wx.GetNumberFromUser("Enter the time you want to study:", "Minutes:", "Study Timer", 25, 1, 120)
break_min = wx.GetNumberFromUser("Enter break time:", "Minutes:", "Study Timer", 5, 1, 60)
repeats = wx.GetNumberFromUser("How many cycles?", "Repeats:", "Study Timer", 4, 1, 20)

total_seconds = minutes * 60 #setting total_seconds to the amount of seconds in the minutes the user inputted
cycles_left = repeats #setting cycles 
wx_timer.Start(1000) #update every second

        
theApp.MainLoop()

