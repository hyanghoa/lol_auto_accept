import time
import tkinter as tk
import utils
import functions


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("매칭 자동 수락")
        self.accept_text = "자동 수락 시작"
        self.wait_text = "매칭 자동 수락을 하려면 자동 수락 시작 버튼을 클릭하세요!"
        self.window_width = 480
        self.window_height = 320
        self.center_window()
        self.thread = None

        self.label = tk.Label(self, text=self.wait_text, padx=10, pady=10)
        self.label.place(relx=0.5, rely=0.4, anchor="center")

        self.button = tk.Button(
            self, text=self.accept_text, padx=10, pady=5, command=self.toggle_button
        )
        self.button.place(relx=0.5, rely=0.6, anchor="center")

    def center_window(self):
        # 화면의 너비와 높이를 구합니다
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # 창의 x, y 좌표를 계산합니다
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2

        # 창의 위치를 설정합니다
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

    def toggle_button(self):
        if self.button.config("text")[-1] == self.accept_text:
            self.button.config(text="취소")
            self.label.config(text="수락 대기중...")
            self.button.config(state=tk.NORMAL)
            self.thread = self.start_thread(
                target=functions.main, callback=self.callback_function
            )
        else:
            self.button.config(text=self.accept_text)
            self.label.config(text=self.wait_text)
            self.button.config(state=tk.NORMAL)
            self.thread.flag.set()

    def callback_function(self):
        self.button.config(text=self.accept_text)
        self.label.config(text=self.wait_text)
        self.button.config(state=tk.NORMAL)
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
