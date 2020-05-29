# Drawing

Este proyecto consiste de una api que contiene una red neuronal convolucional que clasifica dígitos, que ha sido entrenada usando el dataset MNIST. Además incluye una weba-app que haciendo uso de canvas de HTML permite dibujar dígitos con el mouse y que estos sean clasificados por el modelo que se encuentra en la API.

Este proyecto está inspirado en una de las lecciones del curso de Datacamp - Machine Learning for Everyone, la lección llamada Recognizing handwritten digits, ví eso y quise replicarlo. Dejo un enlace a la [lección](https://campus.datacamp.com/courses/machine-learning-for-everyone/what-is-machine-learning?ex=2).

## Inicio

El proyecto está dividido en dos carpetas, la carpeta api contiene el archivo con el modelo y una api desarrollada con flask. La carpeta web-app contiene una aplicación web que contiene la parte visual y realiza peticiones a la api para obtener el resultado de que número ha sido dibujado.

### Requisitos

Todos los requerimientos para que el proyecto funcione se encuentran los archivos requirements.txt en cada una de las carpetas.

### Despliegue

Actualmente ambos han sido desplegados en heroku
* [api](https://digits4app.herokuapp.com/)
* [web-app](https://digits4appf.herokuapp.com/)

### Próximo

Próximamente estaré subiendo el notebook con el entrenamiento y la evaluación del modelo.

## Reconocimientos

* [GioCode](https://www.youtube.com/watch?v=r4MkwQi-4rE) - El código que proporciona me sirvió como base para poder dibujar los dígitos en un lienzo.
* [Datacamp](https://learn.datacamp.com/courses/introduction-to-deep-learning-with-pytorch) - El curso de Introducción a Deep Learning con Pytorch me sirvió bastante.


