import os
import shutil

archive_dir = 'C:/Users/alexa/Desktop/frostgiant-ai/archive/images'

# Define the new dataset directories
train_dir = 'C:/Users/alexa/Desktop/frostgiant-ai/datasets/train_dataset'
test_dir = 'C:/Users/alexa/Desktop/frostgiant-ai/datasets/test_dataset'

# Create new directories for the training and testing datasets
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Go through each tank type in the 'archive' directory
for tank_type in os.listdir(archive_dir):
    # Create subdirectories for training and testing datasets
    tank_train_dir = os.path.join(train_dir, tank_type)
    tank_test_dir = os.path.join(test_dir, tank_type)
    os.makedirs(tank_train_dir, exist_ok=True)
    os.makedirs(tank_test_dir, exist_ok=True)
    
    # Path to the tank type directory
    tank_type_dir = os.path.join(archive_dir, tank_type)
    
    # Move 'l#' images to the training directory and 'main' image to the testing directory
    for filename in os.listdir(tank_type_dir):
        if filename.startswith(tank_type + '_l'):
            # This is a learning image
            shutil.move(os.path.join(tank_type_dir, filename), tank_train_dir)
        elif filename.endswith('_main.jpg'):
            # This is the main image for testing
            shutil.move(os.path.join(tank_type_dir, filename), tank_test_dir)
