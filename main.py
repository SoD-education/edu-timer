import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb


class CountdownApp:
    def __init__(self, master):
        self.master = master
        self.setup_master()
        self.initialize_variables()
        self.setup_layout()
        self.create_widgets()
        self.bind_events()

    def setup_master(self):
        self.master.title("Countdown Timer")
        self.master.geometry("1000x600")
        self.master.minsize(600, 300)

    def initialize_variables(self):
        self.hours, self.minutes, self.seconds = (tk.StringVar() for _ in range(3))
        self.timer = "00:00:00"
        self.running = False
        self.paused = False
        self.initial_timer = "00:00:00"

    def setup_layout(self):
        self.entry_frame = ttk.Labelframe(self.master, text="Set Timer")
        self.entry_frame.grid(row=0, column=0, sticky="nw", padx=10)
        self.master.columnconfigure(0, weight=1)

        self.timer_display_frame = ttk.Frame(self.master)
        self.timer_display_frame.grid(row=2, column=0, sticky="nsew", pady=(20, 0))
        self.master.rowconfigure(2, weight=1)
        self.timer_display_frame.columnconfigure(0, weight=1)
        self.timer_display_frame.rowconfigure(0, weight=1)

    def create_widgets(self):
        time_units = [
            ("hours", self.hours),
            ("minutes", self.minutes),
            ("seconds", self.seconds),
        ]
        for index, (unit, var) in enumerate(time_units, start=1):
            ttk.Entry(
                self.entry_frame, textvariable=var, width=5, justify="center"
            ).grid(row=0, column=index * 2 - 1, padx=5, pady=10)
            if unit != "seconds":
                ttk.Label(self.entry_frame, text=":").grid(row=0, column=index * 2)

        self.create_control_buttons()
        self.setup_timer_display()

    def create_control_buttons(self):
        buttons = [
            ("SET", self.set_timer, "primary"),
            ("CLEAR", self.clear_timer, "danger"),
        ]
        for index, (text, command, style) in enumerate(buttons, start=7):
            ttk.Button(
                self.entry_frame, text=text, command=command, bootstyle=style
            ).grid(row=0, column=index, padx=5)

    def setup_timer_display(self):
        self.timer_inner_frame = ttk.Frame(self.timer_display_frame)
        self.timer_inner_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.timer_display = ttk.Label(
            self.timer_inner_frame,
            text=self.timer,
            font=("Arial", 100),
            anchor="center",
        )
        self.timer_display.pack()

        self.timer_buttons_frame = ttk.Frame(self.timer_inner_frame)
        self.timer_buttons_frame.pack(pady=10)

        self.start_button = ttk.Button(
            self.timer_buttons_frame,
            text="START",
            command=self.start_timer,
            bootstyle="success",
            state="disabled",
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))

        self.pause_button = ttk.Button(
            self.timer_buttons_frame,
            text="PAUSE",
            command=self.pause_timer,
            bootstyle="warning",
            state="disabled",
        )
        self.pause_button.pack(side=tk.LEFT)

    def bind_events(self):
        self.master.bind("<Configure>", self.on_resize)

    def set_timer(self):
        # Get the values from the input, ensuring they don't exceed max allowed values
        hours = min(int(self.hours.get() if self.hours.get() else 0), 23)
        minutes = min(int(self.minutes.get() if self.minutes.get() else 0), 59)
        seconds = min(int(self.seconds.get() if self.seconds.get() else 0), 59)

        # Update the StringVars to reflect the validated values
        self.hours.set(f"{hours:02d}")
        self.minutes.set(f"{minutes:02d}")
        self.seconds.set(f"{seconds:02d}")

        # Form the initial_timer string with validated values
        self.initial_timer = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.timer = self.initial_timer
        self.update_display()
        self.evaluate_start_button_state()

    def clear_timer(self):
        self.hours.set("")
        self.minutes.set("")
        self.seconds.set("")
        self.timer = "00:00:00"
        self.update_display()
        self.running = False
        self.paused = False
        self.start_button.config(text="START")
        self.pause_button.config(text="PAUSE", state="disabled")
        self.evaluate_start_button_state()

    def reset_timer(self):
        self.running = False
        self.paused = False
        self.timer = self.initial_timer
        self.update_display()
        self.start_button.config(text="START")
        self.pause_button.config(text="PAUSE", state="disabled")
        self.evaluate_start_button_state()

    def start_timer(self):
        if not self.running and (
            self.hours.get() or self.minutes.get() or self.seconds.get()
        ):
            self.running = True
            self.paused = False
            self.start_button.config(text="RESET")
            self.pause_button.config(state="enabled")
            self.countdown()
        else:
            self.reset_timer()

    def pause_timer(self):
        if not self.paused:
            self.paused = True
            self.pause_button.config(text="CONTINUE")
        else:
            self.paused = False
            self.pause_button.config(text="PAUSE")
            if self.running:
                self.countdown()

    def countdown(self):
        if self.running and not self.paused:
            h, m, s = map(int, self.timer.split(":"))
            if s > 0 or m > 0 or h > 0:
                s -= 1
                if s < 0:
                    s = 59
                    m -= 1
                    if m < 0:
                        m = 59
                        h -= 1
            else:
                self.running = False
                self.timer = "Time's up!"
                self.start_button.config(text="RESET", state="enabled")
                self.pause_button.config(state="disabled")
                self.update_display()
                return
            self.timer = f"{h:02d}:{m:02d}:{s:02d}"
            self.update_display()
            self.master.after(1000, self.countdown)

    def update_display(self):
        self.timer_display.config(text=self.timer)
        self.evaluate_start_button_state()

    def on_resize(self, event):
        self.resize_display()

    def resize_display(self):
        window_width = self.master.winfo_width()
        font_size = int((window_width * 0.9) / len(self.timer))
        self.timer_display.config(font=("Arial", font_size))

    def evaluate_start_button_state(self):
        if (
            self.hours.get() == ""
            and self.minutes.get() == ""
            and self.seconds.get() == ""
        ):
            self.start_button.config(state="disabled")
        else:
            self.start_button.config(state="enabled")

    def update_timer_frame_position(self):
        self.timer_frame.place(relx=0.5, rely=0.5, anchor="center")


def main():
    root = ttkb.Window(themename="superhero")
    CountdownApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
