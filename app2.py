import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = tensorflow.keras.models.load_model('keras_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Replace this with the path to your image
image = Image.open('2.png')
#resize the image to a 224x224 with the same strategy as in TM2:
#resizing the image to be at least 224x224 and then cropping from the center
size = (224, 224)
image = ImageOps.fit(image, size, Image.ANTIALIAS)

#turn the image into a numpy array
image_array = np.asarray(image)

# display the resized image
image.show()

# Normalize the image
normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

# Load the image into the array
data[0] = normalized_image_array

# run the inference
prediction = model.predict(data)
print(prediction)
for i in prediction:
    if i[0] > 0.65:
        print("Es una señal de curva hacia la derecha.")
    elif i[1] > 0.65:
        print("Es una señal de zona de derrumbes.")
    elif i[2] > 0.65:
        print("Es una señal de doble sentido.")
    elif i[3] > 0.65:
        print("Es una señal de estrechamiento.")
    elif i[4] > 0.65:
        print("Es una señal de interseccion.")
    elif i[5] > 0.65:
        print("Es una señal de lateral.")
    elif i[6] > 0.65:
        print("Es una señal de cruce de peatones.")
    elif i[7] > 0.65:
        print("Es una señal de rotonda.")
    elif i[8] > 0.65:
        print("Es una señal de camino sinuoso.")
    elif i[9] > 0.65:
        print("Es una señal de tope.")
    elif i[10] > 0.65:
        print("Es una señal de tunel.")
    else:
        print("No pudimos interpretar la imagen, intenta de nuevo")

