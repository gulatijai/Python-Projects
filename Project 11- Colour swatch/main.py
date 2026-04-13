from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from PIL import Image, ImageDraw, ImageFont
from werkzeug.utils import secure_filename
import numpy as np
import os
from io import BytesIO
from collections import Counter

app= Flask(__name__)

app.config['UPLOAD_FOLDER']= 'static/uploads'
app.config['SECRET_KEY']= 'jaijaijai'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['GET','POST'])
def analyze_image():
    file = request.files["file"]
    if not file:
        flash('No file uploaded', 'danger')
        return redirect(url_for('home'))
    #save file
    filename= secure_filename(file.filename)
    file_path= os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    #open file
    image= Image.open(file_path)
    image= image.convert('RGB')

    #convert to numpy array
    img_array= np.array(image)

    #reshaping into pixels
    pixels= img_array.reshape(-1,3)
    #Counter needs tuples not arrays
    # Convert each pixel to tuple first
    pixels_tuples= [tuple(pixel) for pixel in pixels]

    counter= Counter(pixels_tuples)
    top_10= counter.most_common(10)

    colors=[]
    for color, count in top_10:
        r,g,b= color
        hex_code= '#{:02x}{:02x}{:02x}'.format(r, g, b)
        colors.append({
            'hex': hex_code,
            'rgb': (int(r), int(g), int(b)),
            'count':int(count)
        })
    session['colors'] = colors
    return render_template('results.html', colors= colors, image_path= file_path)

@app.route('/download')
def download_image():
    palette_img= Image.new('RGB', (500,300), color='white')
    draw= ImageDraw.Draw(palette_img)
    colors= session.get('colors')
    for i, color in enumerate(colors):
        x1= i*50
        x2=x1+50
        draw.rectangle([x1, 0, x2, 300], fill=color['rgb'])
    buffer= BytesIO()
    palette_img.save(buffer, 'PNG')
    buffer.seek(0)
    return send_file(buffer, mimetype='image/png', download_name='pallete.png', as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)