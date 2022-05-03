# Trayectorias vitales: los insectos viajeros de la tierra
Trayectorias vitales es un proyecto colaborativo que pretende mapear la trayectoria, viajes y aleteos de los insectos con quienes cohabitamos el cotidiano. Los objetivos son poner sobre nuestros ojos esos caminos, rutas, desplazamientos de estos seres que sostienen los ecosistemas, hacernos conscientes de su existencia y su labor, pero también ayudar a los estudios de entomólogos, que son pocos en proporción a los estudios sobre las especies de vertebrados, dedicados a medir la población de insectos en el mundo. 
El proyecto utilizará dos herramientas de mapeo: el mapeo colectivo en el espacio público y el dispositivo de tracking con tecnología de visión artificial. El mapeo en el espacio público nos permitirá situar el proyecto en un contexto afectivo, geográfico y político entre los insectos y las dinámicas sociales. Los archivos generados vía entrevistas, derivas y métodos de observación, nos permitirán construir las condiciones precisas para el mapeo vía tracking de las trayectorias de los invertebrados. Posteriormente se plantearán las dinámicas en que la información obtenida por las dos herramientas de mapeo será utilizada para cumplir los objetivos del proyecto. Estas dinámicas podrán ser ejecutadas en el mundo digital y en el real, podrán ser notificaciones de mensajería, tuits, instrucciones, etc.  
Nos gustaría que el mapeo estuviera centrado en los cuatros insectos que corren mayor peligro: las abejas, las hormigas, las mariposas y los escarabajos, pero también nos es importante incluir un mapeo de los insectos que ya no podemos percibir en la ciudad.  

# Descripción técnica

Para trazar algunas trayectorias, hemos usado la librería de procesamiento de imágenes OpenCV desde Python. Hemos abordado el problema con dos distintos algorítmos de detección de bordes, uno que comienza con un filtro de color y otro que comienza con una substracción del fondo. Por último, hemos construido un dispositivo con Raspberry Pi para llevarlo a lugares donde pudieramos trazar caminos de insectos. Todo esto será descrito a continuación.

# Algorítmo con filtro de color
Para este tipo de filtrado, se necesita que haya una diferencia en color del fondo con respecto a los insectos a trazar. Por ejemplo si el fondo es brilloso y los insectos oscuros, el filtro funcionará. Si los insectos fueran de color rojo y el fondo fuera verde, el filtro también funcionaría. Una vez que los insectos han sido filtrados se puede aplicar el algoritmo de detección de contornos para trazar la huella de los insectos. Esto se hace en el codigo TrazosConFiltroColor.py
Puedes saber más de los filtros de color en el siguiente link: https://docs.opencv.org/3.4/da/d97/tutorial_threshold_inRange.html

Ejemplo con insectos:
En este video se ha trazado la huella de unas moscas con facilidad, ya que el cielo es el fondo y por lo tanto es muy iluminado. Las moscas al hacer sombra lucen oscuras en la toma, por ello se puede aplicar un filtro que solo deje pasar a los pixeles con un valor V del espectro HSV bajo.

https://vimeo.com/705848738

<iframe src="https://player.vimeo.com/video/705848738?h=59d274161d" width="640" height="341" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>
<p><a href="https://vimeo.com/705848738">Moscas detectadas por filtro de color</a> from <a href="https://vimeo.com/user173775396">trayectorias vitales</a> on <a href="https://vimeo.com">Vimeo</a>.</p>

# Algoritmo con substracción del fondo

En este método primero se aplica una substracción del fondo para detectar después los objetos que se han movido. Para este método se necesita que la toma se mantenga estática y que el fondo no cambie su nivel de iluminación, mientras mas estático sea el fondo mejor funcionará el algoritmo. Hemos hecho algunas pruebas colocando la cámara sobre un fondo estático para luego trazar las trayectorias de algunos insectos.
Puedes saber más de los algoritmos de substracción de fondo en el siguiente link: https://docs.opencv.org/4.x/d1/dc5/tutorial_background_subtraction.html

Ejemplo con hormigas 
(insertar video 220425 pinkwall )

(insertar otro video de toma estática )

# Dispositivo con Raspberry Pi

Hemos construido un dispositivo con una Raspberry Pi 3 y una Raspberry Pi Camera V2, hemos ejecutado el código que usa filtro de color para trazar algunas trayectorias de insectos. Ya que el filtro de color requiere que haya un contraste entre el fondo y el insecto hemos colocado una hoja de papel blanca en algunos lugares donde podrían pasar insectos, aquí les mostramos el resultado.

(insertar video Tracker_1 y videos de pruebas con el dispositivo de raspberry )



