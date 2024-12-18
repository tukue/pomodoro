import os
from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 30
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')

# ---------------------------- GLOBAL VARIABLES ------------------------------- #
reps = 0
timer = None
work_sessions = 0
is_paused = False
remaining_time = 0
current_mode = ""

class PomodoroTimer:
    def __init__(self, testing_mode=False):
        self.testing_mode = testing_mode
        if not testing_mode:
            self.window = Tk()
            self.window.title("Pomodoro")
            self.window.config(padx=100, pady=50, bg=YELLOW)
            self.setup_ui()
        else:
            # Mock setup for testing
            self.window = None
            self.canvas = None
            self.text_label = None
            self.check_marks = None
            self.start_button = None
            self.stop_button = None
            self.timer_text = 1

    def setup_ui(self):
        if self.testing_mode:
            return
            
        # Load image
        self.tomato_img = PhotoImage(file=os.path.join(ASSETS_DIR, "tomato.png"))
        
        # Label
        self.text_label = Label(self.window, text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50, "bold"))
        self.text_label.grid(column=1, row=0)

        # Canvas
        self.canvas = Canvas(self.window, width=200, height=224, bg=YELLOW, highlightthickness=0)
        self.canvas.create_image(100, 112, image=self.tomato_img)
        self.timer_text = self.canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
        self.canvas.grid(column=1, row=1)

        # Buttons
        self.start_button = Button(self.window, text="Start", highlightthickness=0, command=self.start_timer)
        self.start_button.grid(column=0, row=2)

        self.stop_button = Button(self.window, text="Stop", highlightthickness=0, command=self.stop_timer, state=DISABLED)
        self.stop_button.grid(column=1, row=2)

        self.reset_button = Button(self.window, text="Reset", highlightthickness=0, command=self.reset_timer)
        self.reset_button.grid(column=2, row=2)

        # Checkmarks
        self.check_marks = Label(self.window, fg=GREEN, bg=YELLOW)
        self.check_marks.grid(column=1, row=3)

    def reset_timer(self):
        global timer, reps, work_sessions, is_paused, remaining_time, current_mode
        if timer is not None:
            self.window.after_cancel(timer)
            timer = None
        self.canvas.itemconfig(self.timer_text, text="00:00")
        self.text_label.config(text="Timer", fg=GREEN)
        self.check_marks.config(text="")
        reps = 0
        work_sessions = 0
        is_paused = False
        remaining_time = 0
        current_mode = ""
        self.start_button.config(state=NORMAL)
        self.stop_button.config(state=DISABLED)

    def start_timer(self):
        global reps, work_sessions, is_paused, remaining_time, current_mode
        self.start_button.config(state=DISABLED)
        self.stop_button.config(state=NORMAL)
        
        if is_paused:
            self.text_label.config(text="Restarted", fg=GREEN)
            self.window.after(1000, lambda: self.text_label.config(
                text=current_mode.capitalize(), 
                fg=GREEN if current_mode == "work" else (PINK if current_mode == "short_break" else RED)
            ))
            self.count_down(remaining_time)
            is_paused = False
        else:
            reps += 1
            if reps % 8 == 0:
                current_mode = "long_break"
                self.count_down(LONG_BREAK_MIN * 60)
                self.text_label.config(text="Break", fg=RED)
            elif reps % 2 == 0:
                current_mode = "short_break"
                self.count_down(SHORT_BREAK_MIN * 60)
                self.text_label.config(text="Break", fg=PINK)
            else:
                current_mode = "work"
                self.count_down(WORK_MIN * 60)
                self.text_label.config(text="Work", fg=GREEN)
                work_sessions += 1

    def count_down(self, count):
        global timer, remaining_time
        remaining_time = count
        count_min = math.floor(count / 60)
        count_sec = count % 60
        
        self.canvas.itemconfig(self.timer_text, text=f"{count_min:02d}:{count_sec:02d}")

        if count > 0:
            timer = self.window.after(1000, self.count_down, count - 1)
        else:
            self.start_timer()
            self.update_checkmarks()

    def update_checkmarks(self):
        marks = "✔" * work_sessions
        self.check_marks.config(text=marks)

    def stop_timer(self):
        global timer, is_paused
        if timer is not None:
            self.window.after_cancel(timer)
            timer = None
        is_paused = True
        self.start_button.config(state=NORMAL)
        self.stop_button.config(state=DISABLED)

    def run(self):
        if not self.testing_mode:
            self.window.mainloop()

def main():
    app = PomodoroTimer()
    app.run()

if __name__ == "__main__":
    main()
