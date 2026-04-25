import os, wx, threading
from wx.lib.stattext import GenStaticText


#-----------------Timer Class----------------
class PomodoroTimer(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)

        #creating labels for time, mode, and cycles
        self.time_label = GenStaticText(self, label="--:--", style=wx.ALIGN_CENTER)
        self.mode_label = GenStaticText(self, label="Study Time!", style=wx.ALIGN_CENTER)
        self.cycles_label = GenStaticText(self, style = wx.ALIGN_CENTER)

        #setting fonts for labels
        self.time_label.SetFont(wx.Font(48, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.mode_label.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.cycles_label.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        #setting up the layout of the labels
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.mode_label, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        sizer.Add(self.time_label, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        sizer.Add(self.cycles_label, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        self.SetSizer(sizer)

        #setting up buttons for Set Timer
        self.set_btn = wx.Button(self, label = "Set Timer")
        self.Bind(wx.EVT_BUTTON, self.on_set_timer, self.set_btn)
        sizer.Add(self.set_btn, 0, wx.ALIGN_CENTER | wx.TOP, 10)

    
    def on_set_timer(self, event):
        #user prompts for minutes, break time, and repeats
        self.minutes = wx.GetNumberFromUser("Enter the time you want to study:", "Minutes:", "Study Timer", 25, 1, 120)
        self.break_min = wx.GetNumberFromUser("Enter break time:", "Minutes:", "Study Timer", 5, 1, 60)
        self.repeats = wx.GetNumberFromUser("How many cycles?", "Repeats:", "Study Timer", 3, 1, 20)

        if self.minutes == -1 or self.break_min == -1 or self.repeats == -1:
            return  # User cancelled any of the dialogs

        self.start_timer(self.minutes, self.break_min, self.repeats)

    #function to play alarm sound
    def play_alarm(self):
        os.system("afplay /System/Library/Sounds/Ping.aiff")

    #function to update timer every second and switch between study and break modes
    def on_tick(self, event):

        if self.total_seconds > 0:
            min, sec = divmod(self.total_seconds, 60)  
            self.time_label.SetLabel(f"{min:02d}:{sec:02d}")
            self.total_seconds -= 1
            self.cycles_label.SetLabel(f"Cycle {self.repeats - self.cycles_left + 1} of {self.repeats}")
            self.cycles_label.GetParent().Layout()

        elif self.total_seconds == 0:
            self.time_label.SetLabel("00:00")

            if self.is_study:
                self.mode_label.SetLabel("Break time!")
                self.is_study = False
                self.total_seconds = self.break_min * 60
                t = threading.Thread(target=self.play_alarm)
                t.start()
            else:
                self.mode_label.SetLabel("Study time!")
                self.is_study = True
                self.total_seconds = self.minutes * 60
                self.cycles_left -= 1
                
                if self.cycles_left == 0:
                    self.mode_label.SetLabel("Finished!")
                    self.wx_timer.Stop()
                    #enabling the set timer button again
                    self.set_btn.Enable(True)
                    
                if self.cycles_left > 0:
                    self.cycles_label.SetLabel(f"Cycle {self.repeats - self.cycles_left + 1} of {self.repeats}")
                    self.cycles_label.GetParent().Layout()

                t = threading.Thread(target=self.play_alarm)
                t.start()   
    
    def start_timer(self, minutes, break_min, repeats):
        self.minutes = minutes
        self.break_min = break_min
        self.repeats = repeats
        self.total_seconds = minutes * 60
        self.cycles_left = repeats
        self.is_study = True

        #start timer and play initial alarm
        self.wx_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_tick, self.wx_timer)
        self.wx_timer.Start(1000) #update every second
        threading.Thread(target=self.play_alarm).start()

        #disabling btn
        self.set_btn.Enable(False)
# -----------------Music Class----------------
class MusicPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        label = wx.StaticText(self, label="Music Player Coming Soon!", style=wx.ALIGN_CENTER)
        label.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

# --------------Setup the GUI----------------
theApp = wx.App()
f = wx.Frame(None, title="Study Timer", size=(400, 300))
notebook = wx.Notebook(f)

pomodoro = PomodoroTimer(notebook)

# adding the pomodoro timer panel to the notebook
notebook.AddPage(pomodoro, "Pomodoro Timer") 
music = MusicPanel(notebook)
notebook.AddPage(music, "Music Player")

f.Show()
       
theApp.MainLoop()

