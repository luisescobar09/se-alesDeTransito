import web, shutil
from web import form
import os
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

#URLS = ('/upload', 'Upload')
render = web.template.render("senales/")
fileForm = form.Form(form.File('myfile'))

class Index(object):

    def GET(self):
        f = fileForm()
        return render.index(f)
        #self.datos = None
        #return render.index(self.datos)

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
            print(prediction)
            cabeza = "<html lang='es'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'><title>Señales de transito</title><!-- CSS only --> <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css' rel='stylesheet' integrity='sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1' crossorigin='anonymous'><link rel='icon' href='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Mexico_traffic_signal_sr7.svg/1200px-Mexico_traffic_signal_sr7.svg.png' type='image/png' /></head><body>    <div class='container bg-light '>      <div class='row justify-content-center mt-4 pt-4'>          <div class='col-md-8 '>"
            final = "</div>        </div>    </div></body></html>"
            for i in prediction: 
                if i[0] > 0.85:
                    #print("Es una señal de zona de derrumbes.")
                    titulo= cabeza+"<h1 class='text-danger text-center'>La imagen es una señal de zona de derrumbes.</h1> <br> <br> <h2 class='text-info'>Descripción:</h2> <h3>Advierte sobre una zona en la cual pueden ocurrir derrumbes.</h3><br> <img src='https://www.sigo.com.gt/wp-content/uploads/2017/07/sp-30.png' align='center' width='300' height='275'> <br><br>"+final
                elif i[1] > 0.85:
                    #print("Es una señal de doble sentido.")
                    titulo= cabeza+"<h1 class='text-danger text-center'>La imagen es una señal de doble circulación.</h1> <br> <br> <h2 class='text-info'>Descripción:</h2> <h3>El señalamiento se utiliza para marcar el camino de circulación en un solo sentido o en doble sentido.</h3><br> <img src='https://lh3.googleusercontent.com/proxy/zkG_8nlSfo3smpmkAlDlFBPpoS-bfjSsQcxb8Wrmrj0S7b1TOTbmCLg5tlo9fjJnMBsRXdiI8jHLEhgUQwdqpfRaoUFn37KCnOYzXZNeVEF6IfmlrbkvirwkbqqnADbLgjRfFVzsxbELU5HjorW4PbIQQX49mjrwS1jJQ6c' align='center' width='300' height='275'> <br><br>"+final

                elif i[2] > 0.85:
                    #print("Es una señal de interseccion.")
                    titulo = "La imagen es una señal de interseccion."
                    titulo= cabeza+"<h1 class='text-danger text-center'>La imagen es una señal de interscción (entronque).</h1> <br> <br> <h2 class='text-info'>Descripción:</h2> <h3>La línea mas ancha señalara el camino principal, mientras que la mas angosta el camino secundario.</h3><br> <img src='https://www.puedomanejar.com/wp-content/uploads/2020/12/4wayintersection.png' align='center' width='300' height='275'> <br><br>"+final
                elif i[3] > 0.85:
                    #print("Es una señal de salida por lateral")
                    titulo= cabeza+"<h1 class='text-danger text-center'>La imagen es una señal de Incorporación de transito.</h1> <br> <br> <h2 class='text-info'>Descripción:</h2> <h3>Este tipo de señalamiento avisa sobre la incorporación de transito que va en la misma.</h3><br> <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Argentina_MSV_2017_road_sign_P-22.svg/1200px-Argentina_MSV_2017_road_sign_P-22.svg.png' align='center' width='300' height='275'> <br><br>"+final
                elif i[4] > 0.85:
                    #print("Es una señal de peatón.")
                    titulo= cabeza+"<h1 class='text-danger text-center'>La imagen es una señal de peatón.</h1> <br> <br> <h2 class='text-info'>Descripción:</h2> <h3>Indica un camino con constante paso peatonal o cruce peatonal en específico.</h3><br> <img src='https://lh3.googleusercontent.com/proxy/PuaYJPyit2CUmkOHFSTlLoNcdTIsQYStXSqMvDabwUzoHoV5M79x3zMkpkrWOJav6Z54IHqQRzNyKXL7-LL73QLqVrczp5auzIzm0Cx5E_R-F29oGMND__wZQxED4OLkqL3L2IhMb2h6lD97rQ' align='center' width='300' height='275'> <br><br>"+final
                elif i[5] > 0.85:
                    #print("Es una señal de tope.")
                    titulo= cabeza+"<h1 class='text-danger text-center'>La imagen es una señal de tope.</h1> <br> <br> <h2 class='text-info'>Descripción:</h2> <h3>Advierte la proximidad de una protuberancia en la superficie de la vía.</h3><br> <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Mexico_road_sign_SP-41.svg/1024px-Mexico_road_sign_SP-41.svg.png' align='center' width='300' height='275'> <br><br>"+final
                else:  
                    #print("No pudimos interpretar la imagen, intenta de nuevo")
                    titulo= cabeza+"<h1 class='text-danger text-center'>No pudimos interpretar la imagen, intenta de nuevo.</h1> <br> <br>  <img src='https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/a8eeb0c9-ea86-40dd-8a7a-91912aab7fc2/de2npbi-77dd5cf3-83d9-41bf-9839-8b595c550c9d.png/v1/fill/w_1035,h_772,strp/quico_marciano_by_xocotzin_r_de2npbi-pre.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3siaGVpZ2h0IjoiPD05NTUiLCJwYXRoIjoiXC9mXC9hOGVlYjBjOS1lYTg2LTQwZGQtOGE3YS05MTkxMmFhYjdmYzJcL2RlMm5wYmktNzdkZDVjZjMtODNkOS00MWJmLTk4MzktOGI1OTVjNTUwYzlkLnBuZyIsIndpZHRoIjoiPD0xMjgwIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmltYWdlLm9wZXJhdGlvbnMiXX0.0BeLYI-HZ4ZdrYUerJWoFeZGjKeg5VzFuLjPVPkaXCw' align='center' width='850' height='475'> <br><br>"+final
                    
        return titulo