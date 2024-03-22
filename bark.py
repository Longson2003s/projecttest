import tkinter as tk
from tkinter import ttk
import pyttsx3
import tkinter.filedialog as fd
import json

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to Speech App")
        self.root.geometry("800x600")

        # Tạo tiêu đề cho ô nhập text
        text_label = ttk.Label(root, text="Nhập văn bản:", font=("Helvetica", 14))
        text_label.pack(pady=10)

        self.text_entry = ttk.Entry(root, width=70, font=("Helvetica", 12))
        self.text_entry.pack(pady=(0, 10))  # padding chỉ áp dụng ở phía dưới

        # Tạo ô nhập tốc độ đọc
        speed_label = ttk.Label(root, text="Tốc độ đọc:", font=("Helvetica", 14))
        speed_label.pack()

        self.speed_scale = ttk.Scale(root, from_=50, to=300, orient=tk.HORIZONTAL, length=200)
        self.speed_scale.set(150)
        self.speed_scale.pack(pady=(0, 10))

        # Tạo combobox để chọn giọng nói
        voices_label = ttk.Label(root, text="Chọn giọng nói:", font=("Helvetica", 14))
        voices_label.pack()

        self.voices_combobox = ttk.Combobox(root, values=[], font=("Helvetica", 12), width=50)
        self.voices_combobox.pack(pady=(0, 10))

        # Tạo thanh trượt điều chỉnh âm lượng
        volume_label = ttk.Label(root, text="Âm lượng:", font=("Helvetica", 14))
        volume_label.pack()

        self.volume_scale = ttk.Scale(root, from_=0.0, to=1.0, orient=tk.HORIZONTAL, length=200)
        self.volume_scale.set(0.5)
        self.volume_scale.pack(pady=(0, 10))

        # Tạo các nút
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=(0, 20))  # padding chỉ áp dụng ở phía dưới

        style = ttk.Style()
        style.configure('TButton', font=("Helvetica", 12))

        self.upload_button = ttk.Button(button_frame, text="Upload", command=self.upload_file, style='TButton')
        self.upload_button.grid(row=0, column=2, padx=10, pady=5)

        self.play_button = ttk.Button(button_frame, text="Play", command=self.play_text, style='TButton')
        self.play_button.grid(row=0, column=0, padx=10, pady=5)

        self.replay_button = ttk.Button(button_frame, text="Replay", command=self.replay_text, style='TButton')
        self.replay_button.grid(row=0, column=1, padx=10, pady=5)

        self.history_button = ttk.Button(button_frame, text="Lịch sử", command=self.show_history, style='TButton')
        self.history_button.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.voices_combobox['values'] = [voice.name for voice in self.voices]

        self.voices_combobox.current(0)  # Chọn giọng đọc mặc định

        self.history_list = []  # Biến lưu lịch sử

    def play_text(self):
        text = self.text_entry.get()
        speed = float(self.speed_scale.get())
        voice_index = self.voices_combobox.current()

        if text:
            self.engine.setProperty('volume', 0.5)
            self.engine.setProperty('rate', speed)
            voice_id = self.voices[voice_index].id
            self.engine.setProperty('voice', voice_id)
            print(f"Selected voice ID: {voice_id}")  # In ID giọng đọc để debug
            self.engine.say(text)
            self.engine.runAndWait()

    def replay_text(self):
        text = self.text_entry.get()
        speed = float(self.speed_scale.get())
        voice_index = self.voices_combobox.current()

        if text:
            self.engine.setProperty('volume', 0.5)
            self.engine.setProperty('rate', speed)
            voice_id = self.voices[voice_index].id
            self.engine.setProperty('voice', voice_id)
            self.engine.say(text)
            self.engine.runAndWait()

    def upload_file(self):
        file_path = fd.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                self.text_entry.delete(0, tk.END)
                self.text_entry.insert(0, text)

    def save_history(self):
        with open("history.json", "w", encoding="utf-8") as file:
            json.dump(self.history_list, file, indent=4)

    def show_history(self):
        with open("history.json", "r", encoding="utf-8") as file:
            self.history_list = json.load(file)

        history_window = tk.Toplevel(self.root)
        history_window.title("Lịch sử đọc")

        history_text = tk.Text(history_window, width=80, height=20)
        for entry in self.history_list:
            text = f"- Văn bản: {entry['text']}\n  Tốc độ: {entry['speed']}\n  Giọng đọc: {self.voices[entry['voice_index']].name}\n\n"
            history_text.insert(tk.END, text)
        history_text.pack()

        close_button = ttk.Button(history_window, text="Đóng", command=history_window.destroy)
        close_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()