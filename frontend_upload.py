import tkinter as tk
from tkinter import filedialog
import requests

def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        files = {'image': open(file_path, 'rb')}
        url = "http://127.0.0.1:5000/upload"  # BURASI ÖNEMLİ
        try:
            response = requests.post(url, files=files)
            print(response.json())
        except Exception as e:
            print(f"HATA: {e}")

root = tk.Tk()
root.title("FeelArt AI")

button = tk.Button(root, text="Görsel Yükle", command=upload_image)
button.pack(pady=20)

root.mainloop()
