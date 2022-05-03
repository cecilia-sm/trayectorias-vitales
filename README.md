# Trayectorias vitales: los insectos viajeros de la tierra
Trayectorias vitales es un proyecto colaborativo que pretende mapear la trayectoria, viajes y aleteos de los insectos con quienes cohabitamos el cotidiano. Los objetivos son poner sobre nuestros ojos esos caminos, rutas, desplazamientos de estos seres que sostienen los ecosistemas, hacernos conscientes de su existencia y su labor, pero también ayudar a los estudios de entomólogos, que son pocos en proporción a los estudios sobre las especies de vertebrados, dedicados a medir la población de insectos en el mundo. 
El proyecto utilizará dos herramientas de mapeo: el mapeo colectivo en el espacio público y el dispositivo de tracking con tecnología de visión artificial. El mapeo en el espacio público nos permitirá situar el proyecto en un contexto afectivo, geográfico y político entre los insectos y las dinámicas sociales. Los archivos generados vía entrevistas, derivas y métodos de observación, nos permitirán construir las condiciones precisas para el mapeo vía tracking de las trayectorias de los invertebrados. Posteriormente se plantearán las dinámicas en que la información obtenida por las dos herramientas de mapeo será utilizada para cumplir los objetivos del proyecto. Estas dinámicas podrán ser ejecutadas en el mundo digital y en el real, podrán ser notificaciones de mensajería, tuits, instrucciones, etc.  
Nos gustaría que el mapeo estuviera centrado en los cuatros insectos que corren mayor peligro: las abejas, las hormigas, las mariposas y los escarabajos, pero también nos es importante incluir un mapeo de los insectos que ya no podemos percibir en la ciudad.  

# Descripción técnica

Para trazar algunas trayectorias, hemos usado la librería de procesamiento de imágenes OpenCV desde Python. Hemos abordado el problema con dos distintos algorítmos de detección de bordes, uno que comienza con un filtro de color y otro que comienza con una substracción del fondo. Por último, hemos construido un dispositivo con Raspberry Pi para llevarlo a lugares donde pudieramos trazar caminos de insectos. Todo esto será descrito a continuación.

# Algorítmo con filtro de color


