import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB7
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Set up GPU usage configuration to not consume all memory
import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))