import os, wx, threading, webbrowser, sqlite3
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
        self.set_btn = wx.Button(self, label = "Set Timer", size = (170, 40))
        self.set_btn.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.Bind(wx.EVT_BUTTON, self.on_set_timer, self.set_btn)

        #setting up button for Stop Timer
        self.stop_btn = wx.Button(self, label = "Stop Timer")
        self.Bind(wx.EVT_BUTTON, self.on_stop_timer, self.stop_btn)
        self.stop_btn.Hide()  # Hide the stop button until the timer starts

        #settup up layout for buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(self.set_btn, 0, wx.RIGHT, 10)
        btn_sizer.Add(self.stop_btn, 0)
        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        #pause button logic
        self.is_paused = False
        self.pause_btn = wx.Button(self, label = "Pause Timer")
        self.Bind(wx.EVT_BUTTON, self.on_pause_timer, self.pause_btn)
        btn_sizer.Add(self.pause_btn, 0, wx.LEFT, 10)
        self.pause_btn.Hide()  # Hide the pause button until the timer starts
    
    def on_set_timer(self, event):
        #user prompts for minutes, break time, and repeats
        self.minutes = wx.GetNumberFromUser("Enter the time you want to study:", "Minutes:", "Study Timer", 25, 1, 120)
        self.break_min = wx.GetNumberFromUser("Enter break time:", "Minutes:", "Study Timer", 5, 1, 60)
        self.repeats = wx.GetNumberFromUser("How many cycles?", "Repeats:", "Study Timer", 3, 1, 20)

        if self.minutes == -1 or self.break_min == -1 or self.repeats == -1:
            return  # User cancelled any of the dialogs

        self.start_timer(self.minutes, self.break_min, self.repeats)

        # Show the pause button when the timer starts
        self.pause_btn.Show()
        self.stop_btn.Show()  # Show the stop button when the timer starts
        self.Layout()  # Update the layout to show the pause button
    
    def on_stop_timer(self, event):
        if hasattr(self, 'wx_timer'):
            self.wx_timer.Stop()
            self.time_label.SetLabel("--:--")
            self.mode_label.SetLabel("Timer Stopped")
            self.cycles_label.SetLabel("")
            self.set_btn.Enable(True)  # Enabling the set timer button again
            self.pause_btn.Hide()
            self.stop_btn.Hide()  # Hide the stop button when the timer is stopped
            self.set_btn.Show()
            self.Layout()  # Update the layout to hide the pause button

    #function to pause and resume timer
    def on_pause_timer(self, event):
        if self.is_paused:
            self.wx_timer.Start(1000)  # Resume the timer
            self.pause_btn.SetLabel("Pause Timer")
            self.is_paused = False
        else:
            self.wx_timer.Stop()  # Pause the timer
            self.pause_btn.SetLabel("Resume Timer")
            self.is_paused = True

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
        self.set_btn.Hide()
        self.Layout()  # Update the layout to hide the set button

# -----------------Music Class----------------
class MusicPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        label = GenStaticText(self, label="Music Player ", style=wx.ALIGN_CENTER)
        label.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        sizer.Add(label, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        #buttons to open music playlist
        self.lofi_btn = wx.Button(self, label="Lofi", size=(200, 40))
        self.Bind(wx.EVT_BUTTON, lambda e, url = "https://www.youtube.com/results?search_query=lofi": self.play_music(url), self.lofi_btn)
        self.classical_btn = wx.Button(self, label="Classical", size=(200, 40))
        self.Bind(wx.EVT_BUTTON, lambda e, url = "https://www.youtube.com/results?search_query=classical+study+music": self.play_music(url), self.classical_btn)
        self.jazz_btn = wx.Button(self, label="Jazz", size=(200, 40))
        self.Bind(wx.EVT_BUTTON, lambda e, url ="https://www.youtube.com/results?search_query=jazz+guitar+study": self.play_music(url), self.jazz_btn)

        #adding buttons to sizer
        sizer.Add(self.lofi_btn, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        sizer.Add(self.classical_btn, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        sizer.Add(self.jazz_btn, 0, wx.ALIGN_CENTER | wx.TOP, 10)

    #function to open music playlist in web browser
    def play_music(self, url):
        webbrowser.open(url)

#-----------------To-Do List Class-------------
class TodoPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_db() # Create the database and table if they don't exist

        # setting up the layout for the to-do list
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        label = GenStaticText(self, label="To-Do List", style=wx.ALIGN_CENTER)
        label.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sizer.Add(label, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        # input field, add button, remove button for adding/removing tasks to the to-do list
        input_sizer = wx.BoxSizer(wx.VERTICAL)
        self.task_input = wx.TextCtrl(self, size=(250, 30))
        input_sizer.Add(self.task_input, 1, wx.EXPAND |wx.RIGHT, 5)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.add_btn = wx.Button(self, label="Add")
        self.remove_btn = wx.Button(self, label="Remove")
        self.Bind(wx.EVT_BUTTON, self.on_add_task, self.add_btn)
        self.Bind(wx.EVT_BUTTON, self.on_remove_task, self.remove_btn)
        btn_sizer.Add(self.add_btn, 0, wx.RIGHT, 5)
        btn_sizer.Add(self.remove_btn, 0)

        input_sizer.Add(btn_sizer, 0)
        sizer.Add(input_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # checklist box to display tasks in the to-do list
        self.checklist = wx.CheckListBox(self)
        sizer.Add(self.checklist, 1, wx.EXPAND | wx.ALL, 10)

        self.load_tasks() # Load tasks from the database and display them in the checklist


    def create_db(self):
        self.conn = sqlite3.connect("todo.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)")
        self.conn.commit()
    
    def on_add_task(self, event):
        task = self.task_input.GetValue().strip()
        if task:
            self.cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
            self.conn.commit()
            self.checklist.Append(task)
            self.task_input.SetValue("")  # Clear the input field after adding the task

    def load_tasks(self):
        self.cursor.execute("SELECT task FROM tasks")
        tasks = self.cursor.fetchall()
        for task in tasks:
            self.checklist.Append(task[0])

    def on_remove_task(self, event):
        selected_indices = self.checklist.GetCheckedItems()
        for index in reversed(selected_indices):  # Remove from the end to avoid index shifting
            task = self.checklist.GetString(index)
            self.cursor.execute("DELETE FROM tasks WHERE task = ?", (task,))
            self.conn.commit()
            self.checklist.Delete(index)
# --------------Setup the GUI----------------
theApp = wx.App()
f = wx.Frame(None, title="Study Timer", size=(400, 300))
notebook = wx.Notebook(f)

# adding the pomodoro timer and music panel to the notebook
pomodoro = PomodoroTimer(notebook)
notebook.AddPage(pomodoro, "Pomodoro Timer") 
music = MusicPanel(notebook)
notebook.AddPage(music, "Music Player")
todo = TodoPanel(notebook)
notebook.AddPage(todo, "To-Do List")

f.Show()
       
theApp.MainLoop()

