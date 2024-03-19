import time
import tkinter as tk
import utils
import functions
import customtkinter


customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: blue (default), dark-blue, green


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        customtkinter.CTk.__init__(self, *args, **kwargs)
        self.title("매칭 자동 수락")
        self.accept_text = "자동 수락 시작"
        self.wait_text = "매칭 자동 수락을 하려면 자동 수락 시작 버튼을 클릭하세요!"
        self.window_width = 480
        self.window_height = 320
        self.center_window()
        self.thread = None

        self.label = customtkinter.CTkLabel(master=self, text=self.wait_text)
        self.label.place(relx=0.5, rely=0.4, anchor="center")

        self.button = customtkinter.CTkButton(
            master=self,
            text=self.accept_text,
            command=self.toggle_button,
        )
        self.button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2

        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

    def toggle_button(self):
        if self.button.cget("text") == self.accept_text:
            self.button.configure(text="취소")
            self.label.configure(text="수락 대기중...")
            self.button.configure(state=tk.NORMAL)
            self.thread = self.start_thread(
                target=functions.main, callback=self.callback_function
            )
        else:
            self.button.configure(text=self.accept_text)
            self.label.configure(text=self.wait_text)
            self.button.configure(state=tk.NORMAL)
            self.thread.flag.set()

    def callback_function(self):
        self.button.configure(text=self.accept_text)
        self.label.configure(text=self.wait_text)
        self.button.configure(state=tk.NORMAL)
        self.thread.flag.set()

    def start_thread(self, target, callback=None):
        t = utils.Thread(target=target, callback=callback)
        t.daemon = True
        t.start()
        return t

    def check_state(self, thread):
        while thread.is_alive():
            time.sleep(1)


app = App()
app.mainloop()
