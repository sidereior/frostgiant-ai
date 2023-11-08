import os
import shutil
from PIL import Image, ImageOps

def resize_and_pad(img, size, fill_color=(0, 0, 0)):
    # Resize the image so that the longest edge is equal to the target size
    img.thumbnail((size, size), Image.Resampling.LANCZOS)
    
    # Calculate the size to pad to make the image square
    x, y = img.size
    larger_side = max(x, y)
    
    # Create a new square image with the fill color
    new_im = Image.new("RGB", (larger_side, larger_side), fill_color)
    
    # Paste the resized image onto the center of the square canvas
    new_im.paste(img, (int((larger_side - x) / 2), int((larger_side - y) / 2)))
    
    # Finally, resize to the desired output size
    return new_im.resize((size, size), Image.Resampling.LANCZOS)

archive_dir = 'C:/Users/alexa/Desktop/frostgiant-ai/archive/images'
train_dir = 'C:/Users/alexa/Desktop/frostgiant-ai/datasets/train_dataset'
test_dir = 'C:/Users/alexa/Desktop/frostgiant-ai/datasets/test_dataset'

os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

for tank_type in os.listdir(archive_dir):
    tank_train_dir = os.path.join(train_dir, tank_type)
    tank_test_dir = os.path.join(test_dir, tank_type)
    os.makedirs(tank_train_dir, exist_ok=True)
    os.makedirs(tank_test_dir, exist_ok=True)
    
    tank_type_dir = os.path.join(archive_dir, tank_type)
    
    for filename in os.listdir(tank_type_dir):
        file_path = os.path.join(tank_type_dir, filename)
        new_path = tank_train_dir if filename.startswith(tank_type + '_l') else tank_test_dir
        
        # Open the image
        with Image.open(file_path) as img:
            # Resize and pad the image
            processed_img = resize_and_pad(img, 600)
            
            # Save the processed image to the new path
            processed_img.save(os.path.join(new_path, filename))
        
        # Remove the original image
        os.remove(file_path)
