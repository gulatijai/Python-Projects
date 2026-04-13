from tkinter import *
from tkinter import filedialog
import winsound

secs= 5
job_id= None

def start_writing():
    global secs
    secs= timer_choice.get()
    timer_label.config(text=secs)
    welcome_frame.grid_remove()
    writing_frame.grid(column=0, row =0)

def on_key_press(event):
    global secs, job_id
    timer_label.config(text=secs)
    status_label.config(text='Keep Writing..')
    if job_id:
        window.after_cancel(job_id)
    job_id= window.after(1000, countdown)
    text= input_text.get(1.0, END).strip()
    words= len(text.split())
    word_count.config(text=f"Words:{words}")

def countdown():
    global secs, job_id
    secs-=1
    timer_label.config(text= secs)
    if secs<=2:
        timer_label.config(text=secs, fg="red")
        status_label.config(text='⚠️ Hurry up!')
        winsound.Beep(1000, 200)

    else:
        status_label.config(text='Keep Writing..')
    if secs>0:
        job_id= window.after(1000, countdown)
    else:
        delete_text()

def delete_text():
    global secs
    input_text.delete(1.0, END)
    status_label.config(text= "Too Slow.... start again")
    secs= timer_choice.get()
    timer_label.config(text= secs, fg='black')
    word_count.config(text=f"Words:0")

def safe_text():
    text= input_text.get(1.0, END).strip()
    if text:
        file_path= filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        if file_path:
            with open(file_path, 'w') as f:
                f.write(text)
            status_label.config(text="✅ Saved successfully!" )
    else:
        status_label.config(text="Nothing to save!")

#__________________________________________________________________
window= Tk()
window.title("Type Type Baby")
window.minsize(width= 400, height=800)
window.config(padx=100, pady=100)

welcome_frame= Frame(window)
welcome_frame.grid(column=0, row =0)
title_label= Label(welcome_frame, text='The Dangerous Writer', font= ('Arial', 40))
title_label.grid(column=0, row=0)
instruction_label= Label(welcome_frame, text= 'Continue typing, if you stop for continuous 5 seconds, you will loose the text', font= ('Arial',20))
instruction_label.grid(column=0, row=1)
start_button= Button(welcome_frame, text= "Start Writing", command=start_writing)
start_button.grid(column=0, row=6)

writing_frame= Frame(window)
writing_frame.grid(column=0, row =0)
writing_frame.grid_remove()
timer_label= Label(writing_frame, text=secs, font= ('Arial', 40))
timer_label.grid(column=1, row=0)
status_label= Label(writing_frame, text='Keep Writing..', font= ('Arial', 16))
status_label.grid(column=1, row=1)
input_text= Text(writing_frame)
input_text.grid(column=1, row=2)
word_count= Label(writing_frame, text= 'Word:', font= ('Arial', 16))
word_count.grid(column=1, row=3)

save_button = Button(writing_frame, text="💾 Save", command= safe_text)
save_button.grid(column=1, row=4)

window.bind('<KeyPress>', on_key_press)

timer_choice= IntVar()
timer_choice.set(5)

timer_label_welcome= Label(welcome_frame, text="Choose your timer:", font=('Arial', 16))
timer_label_welcome.grid(column=0, row=2)

radio_5= Radiobutton(welcome_frame, text='5 secs', variable=timer_choice, value=5)
radio_5.grid(column=0, row=3)

radio_10= Radiobutton(welcome_frame, text='10 secs', variable=timer_choice, value=10)
radio_10.grid(column=0, row=4)

radio_15= Radiobutton(welcome_frame, text='15 secs', variable=timer_choice, value=15)
radio_15.grid(column=0, row=5)

window.mainloop()