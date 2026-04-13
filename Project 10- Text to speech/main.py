import pyttsx3
from pypdf import PdfReader
from tkinter import filedialog

engine= pyttsx3.init()
engine.setProperty('rate', 150)    # speed - default is 200
engine.setProperty('volume', 0.9)  # volume 0-1

file_path= filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
if not file_path:
    print("File not selected")
    exit()
reader= PdfReader(file_path)

full_text= ""

for i, page in enumerate(reader.pages):
    print (f"Reading page {i+1} of {len(reader.pages)}")
    text= page.extract_text()
    if not text:
        continue
    full_text += text
    engine.say(text)
    engine.runAndWait()

engine.save_to_file(full_text, 'output.wav')
engine.runAndWait()