import time
from tkinter import *
import random


secs =60

sample_texts = [
    "The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs. How vexingly quick daft zebras jump.",
    "Python is a versatile programming language that emphasizes code readability. It is widely used in web development, data science, artificial intelligence, and automation.",
    "The sun sets slowly over the horizon, painting the sky in shades of orange and pink. Birds return to their nests as the world prepares for the quiet of night.",
    "Technology is changing the way we live and work. Artificial intelligence and machine learning are transforming industries and creating new opportunities for innovation.",
    "A good programmer writes code that humans can understand. Clean code is not written for machines alone but for the people who will read and maintain it in the future."
]
sample_text= random.choice(sample_texts)


def start_test():
    global secs
    input_text.config(state=NORMAL)
    input_text.delete(1.0, END)
    secs = 60
    update_timer(secs)


def end_test():
    input_text.config(state= DISABLED)
    wpm= calculate_wpm()
    result_label.config(text=f"WPM result is: {wpm}")

def update_timer(count):
    global secs
    timer_label.config(text=count)
    if secs>0:
        secs-=1
        window.after(1000,lambda:update_timer(secs))
    else:
        end_test()


def calculate_wpm():
    text= input_text.get(1.0, END).strip()
    typed_words= text.split()
    sample_words= sample_text.split()
    correct_words=0
    for i in range(min(len(typed_words), len(sample_words))):
        if typed_words[i]== sample_words[i]:
            correct_words +=1

    return correct_words

def restart():
    global sample_text
    global secs
    secs= 60
    sample_text= random.choice(sample_texts)
    text_display.config(text=sample_text)
    timer_label.config(text= secs)
    input_text.config(state=NORMAL)
    input_text.delete(1.0, END)
    input_text.config(state=DISABLED)
    result_label.config(text= "WPM result")

#---------------------------------------------------------------------

window= Tk()
window.title("Check your typing speed")
window.minsize(width= 400, height=800)
window.config(padx=100, pady=100)

timer_label= Label(window, text= secs, font=("Arial", 40))
timer_label.grid(column=1, row=0)

start_button= Button(text="Start Timer", command=start_test)
start_button.grid(column=1, row=3)

text_display= Label(window,text=sample_text, wraplength=400 )
text_display.grid(column=1, row=1)

input_text= Text(window)
input_text.grid(column=1, row=2)
input_text.config(state= DISABLED)

result_label= Label(window, text= "WPM result")
result_label.grid(column=1, row=5)

reset_button= Button(text="Reset", command= restart)
reset_button.grid(column=1, row=4)

window.mainloop()