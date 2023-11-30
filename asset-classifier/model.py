import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB7
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Set up GPU usage configuration to not consume all memory
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(f"{len(gpus)} Physical GPU(s), {len(logical_gpus)} Logical GPU(s)")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)

# Define a training image data generator with data augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Define a validation image data generator with only rescaling
validation_datagen = ImageDataGenerator(rescale=1./255)

# Assuming the paths are set correctly to where the images are stored
train_dir = 'C:/Users/alexa/Desktop/frostgiant-ai/datasets/test_dataset'
validation_dir = 'C:/Users/alexa/Desktop/frostgiant-ai/datasets/train_dataset'

# Create the train generator
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(600, 600),
    batch_size=32,
    class_mode='categorical'
)

# Create the validation generator
validation_generator = validation_datagen.flow_from_directory(
    validation_dir,
    target_size=(600, 600),
    batch_size=32,
    class_mode='categorical'
)

# Load the EfficientNetB7 model, pretrained on ImageNet
base_model = EfficientNetB7(weights='imagenet', include_top=False, input_shape=(600, 600, 3))

# Freeze the base_model
base_model.trainable = False

# Add new layers on top for our specific task
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(150, activation='softmax')(x)  # Set num_classes to the number of your tank types

# This is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model with the training data generator
model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=10,
    steps_per_epoch=100,  # Adjust based on the size of your dataset
    validation_steps=50   # Adjust based on the size of your validation dataset
)

# Unfreeze some layers of the base_model for fine-tuning
for layer in base_model.layers[-20:]:
    if not isinstance(layer, tf.keras.layers.BatchNormalization):
        layer.trainable = True

# Recompile the model to make the changes effective
model.compile(optimizer=Adam(lr=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

# Continue training the model with a smaller learning rate
model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=10,
    steps_per_epoch=100,  # Adjust based on the size of your dataset
    validation_steps=50   # Adjust based on the size of your validation dataset
)

# Save the model
model.save('C:/Users/alexa/Desktop/frostgiant-ai/models')