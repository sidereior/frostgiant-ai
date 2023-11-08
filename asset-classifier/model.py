import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB7
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

# Load the EfficientNetB7 model, pretrained on ImageNet
base_model = EfficientNetB7(weights='imagenet', include_top=False, input_shape=(600, 600, 3))  # EfficientNetB7 expects 600x600 input size

# Freeze the base_model
base_model.trainable = False

# Add new layers on top for our specific task in order to fine tune the modelj
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(150, activation='softmax')(x)  # num_classes should be the number of your tank types

# This is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)

# Compile the model
model.compile(optimizer=Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model with the training data generator
model.fit(train_generator, validation_data=validation_generator, epochs=10, steps_per_epoch=100, validation_steps=50)

# Unfreeze some layers of the base_model for fine-tuning
# You may need to experiment with how many layers to unfreeze
for layer in base_model.layers[-20:]:
    if not isinstance(layer, tf.keras.layers.BatchNormalization):  # Don't unfreeze Batch Normalization layers
        layer.trainable = True

# Recompile the model to make the changes effective
model.compile(optimizer=Adam(lr=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

# Continue training the model with a smaller learning rate
model.fit(train_generator, validation_data=validation_generator, epochs=10, steps_per_epoch=100, validation_steps=50)

# Save the model
model.save('path/to/save/your/model.h5')
