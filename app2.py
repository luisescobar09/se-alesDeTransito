import web, shutil
from web import form
import os
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import json

urls = ('/index', 'Index')

class Index(object):

    def POST(self):
        x = web.input(myfile={})
        filedir = '/workspace/se-alesDeTransito/senales/static/'
        if 'myfile' in x:
            filepath=x.myfile.filename.replace('\\','/')
            filename=filepath.split('/')[-1]
            fout = open(filedir +'/'+ filename,'wb')
            fout.write(x.myfile.file.read())
            fout.close()
            np.set_printoptions(suppress=True)

            # Load the model
            model = tensorflow.keras.models.load_model('/workspace/se-alesDeTransito/senales/static/keras_model.h5')

            # Create the array of the right shape to feed into the keras model
            # The 'length' or number of images you can put into the array is
            # determined by the first position in the shape tuple, in this case 1.
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

            # Replace this with the path to your image
            image = Image.open('/workspace/se-alesDeTransito/senales/static/'+filename)
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

            for i in prediction: 
                if i[0] > 0.85:
                    titulo = "derrumbes"
                    resultado = "La imagen es una señal de zona de derrumbes."
                    descripcion = "Advierte sobre una zona en la cual pueden ocurrir derrumbes."
                    status = 200

                elif i[1] > 0.85:
                    titulo = "doble"
                    resultado = "La imagen es una señal de doble circulación."
                    descripcion = "El señalamiento se utiliza para marcar el camino de circulación en un solo sentido o en doble sentido."
                    status = 200

                elif i[2] > 0.85:
                    titulo = "intersección"
                    resultado = "La imagen es una señal de intersección (entronque) de 4 vías."
                    descripcion = "La línea mas ancha señalara el camino principal, mientras que la mas angosta el camino secundario."
                    status = 200

                elif i[3] > 0.85:
                    titulo = "lateral"
                    resultado = "La imagen es una señal de incorporación de transito."
                    descripcion = "Este tipo de señalamiento avisa sobre la incorporación de transito que va en la misma."
                    status = 200

                elif i[4] > 0.85:
                    titulo = "peatón"
                    resultado = "La imagen es una señal de peatón."
                    descripcion = "Indica un camino con constante paso peatonal o cruce peatonal en específico."
                    status = 200

                elif i[5] > 0.85:
                    titulo = "tope"
                    resultado = "La imagen es una señal de tope."
                    descripcion = "Advierte la proximidad de una protuberancia en la superficie de la vía"
                    status = 200

                else:  
                    titulo = "error"
                    resultado = "No pudimos interpretar la imagen, intenta de nuevo."
                    descripcion = "La imagen no pertenece a una señal o aún no es entrenada."
                    status = 404
        
        datos = {
            titulo: [
            ]
        }

        senal = {}
        senal["resultado"] = resultado
        senal["descripcion"] = descripcion
        senal["status"] = status
        datos[titulo].append(senal)
        return json.dumps(datos)

if __name__ == "__main__":
   app = web.application(urls, globals()) 
   app.run()