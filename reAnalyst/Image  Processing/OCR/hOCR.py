import subprocess
import os
from PIL import Image

def upscale_image(img):
    width, height = img.size
    new_width = width * 2
    new_height = height * 2
    return img.resize((new_width, new_height), Image.LANCZOS)

input_directory = 'toOCR'
output_directory = 'toOCR'
os.makedirs(output_directory, exist_ok=True)

for filename in os.listdir(input_directory):
    if filename.endswith(".jpg"):
        input_path = os.path.join(input_directory, filename)

        # Open and upscale the image
        img = Image.open(input_path)
        upscaled_img = upscale_image(img)

        # Convert RGBA to RGB if necessary
        if upscaled_img.mode == 'RGBA':
            upscaled_img = upscaled_img.convert('RGB')

        # Save the upscaled image temporarily
        temp_path = os.path.join(input_directory, 'temp_' + filename)
        upscaled_img.save(temp_path)

        output_base = os.path.splitext(filename)[0]
        output_path = os.path.join(output_directory, output_base)

        command = [
            'tesseract', temp_path, output_path,
            '--psm', '1', '--oem', '1',
            '-c', 'load_system_dawg=F', '-c', 'load_freq_dawg=F',
            '-c', 'thresholding_method=2',
            '-c', 'tessedit_create_hocr=1',  # Command to create hOCR file


            '-c', 'tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789{}[]()<>.,;:!#%^&*-_+=/|\\`~"\'?'
        ]

        subprocess.run(command, check=True)
        print(f'Processed: {filename}')

        # Optionally, delete the temporary upscaled image
        os.remove(temp_path)

print("OCR processing complete.")

