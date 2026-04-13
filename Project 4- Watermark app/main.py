
from tkinter import filedialog, Tk, Label, Button, StringVar, Radiobutton, Entry
from PIL import Image, ImageTk, ImageDraw, ImageFont


image_label= None
original_image= None
watermarked_image= None
file_path= None
logo_image= None

def upload_image():
    global file_path
    file_path=filedialog.askopenfilename(
        filetypes=[("Image files", "*.png *.jpg *.jpeg")]
    )
    #opening and converting image using pillow
    global image_label
    # Save the original resolution before converting to thumbnail
    global original_image
    original_image= Image.open(file_path)
    preview= Image.open(file_path)
    preview.thumbnail((400,400))

    img_tk= ImageTk.PhotoImage(preview)
    image_label.config(image=img_tk)
    image_label.image = img_tk

def apply_watermark():

    text= text_entry.get()
    img = Image.open(file_path)

    if watermark_type.get()=="text":
        draw= ImageDraw.Draw(img)
        width, height= img.size
        position= (width-200, height-150)
        draw.text(position,text,fill=(255,255,255) )

    else:
        img= img.convert("RGBA")
        logo= logo_image.convert("RGBA")
        width, height= img.size
        position= (width-logo.width-10, height-logo.height-10)
        img.paste(logo, position, logo)

    global watermarked_image
    watermarked_image = img

    # update the preview
    preview= img.copy()
    preview.thumbnail((400,400))
    img_tk= ImageTk.PhotoImage(preview)
    image_label.config(image=img_tk)
    image_label.image= img_tk

def upload_logo():
    global logo_image
    logo_file= filedialog.askopenfilename(
        filetypes=[("Image files", "*.png *.jpg *.jpeg")]
    )
    logo_image= Image.open(logo_file)
    logo_image.thumbnail((100,100))

def toggle_watermark_type():
    if watermark_type.get() =="text":
        text_label.grid()
        logo_button.grid_remove()
        text_entry.grid()
    else:
        text_entry.grid_remove()
        text_label.grid_remove()
        logo_button.grid()

def save():

    save_path= filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files","*.jpg")]
    )
    if save_path:
        watermarked_image.save(save_path)


#---------------------------------------
window = Tk()
window.title("Image Watermarking")
window.minsize(width=400, height=500)
window.config(pady=50, padx=50)

watermark_type= StringVar()
watermark_type.set("text")

upload_button= Button(text= "Upload Image", command= upload_image)
upload_button.grid(column=1, row=0)

radio_text= Radiobutton(window, text= "Text Watermark", variable= watermark_type, value="text", command=toggle_watermark_type )
radio_text.grid(column=1, row=3)
radio_logo= Radiobutton(window, text= "Logo Watermark", variable= watermark_type, value="logo", command=toggle_watermark_type)
radio_logo.grid(column=1, row=4)

logo_button= Button(text="Logo", command=upload_logo)
logo_button.grid(column=1, row=5)
logo_button.grid_remove()

text_label= Label(window, text="Enter watermark text:")
text_label.grid(column=1, row=5)

text_entry= Entry(window, width=30)
text_entry.grid(column=1, row=6)

image_label= Label(window)
image_label.grid(column=1, row=1)

apply_button= Button(text="Apply", command= apply_watermark)
apply_button.grid(column=1, row=7)

save_button= Button(text="Save", command= save)
save_button.grid(column=1, row=8)

window.mainloop()