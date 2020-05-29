    var color = "#ffffff";
    var tamano = 40;
    var pintura = false;

    var canvas = document.getElementById("canvas");
    var ctx = canvas.getContext("2d");
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    function limpiar() {
        var canvas = document.getElementById("canvas");
        ctx.fillStyle = "black";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        console.log('limpiando');
    }

    function recorte() {
        var imageData = ctx.getImageData(0, 0, 500, 500);
        console.log(imageData);
        console.log(typeof imageData);
        console.log(typeof imageData.data);
        ctx.putImageData(imageData, 50, 50);
    }

    function pintar(event) {
        var canvas = document.getElementById("canvas");
        var ctx = canvas.getContext("2d");
        var x = event.clientX - 10;
        var y = event.clientY + 5;

        if (pintura) {
            ctx.fillStyle = color;
            ctx.fillRect(x, y, tamano, tamano);
        }
    }

    function activar() {
        pintura = true;
    }

    function desactivar() {
        pintura = false;
    }

    function borrador() {
        document.getElementById("canvas").style.cursor = "url(/static/img/borradorcursor.png), default";
        // color = "#FFFFFF";
        console.log(document.getElementById("canvas").style.cursor);
        color = "#000000";
        document.getElementById("colores").setAttribute("disabled", "");
    }

    function lapiz() {
        document.getElementById("canvas").style.cursor = "url(/static/img/cursor.gif), default";
        console.log(document.getElementById("canvas").style.cursor);

        color = document.getElementById("colores").value;
        document.getElementById("colores").removeAttribute("disabled");
    }

    function scolor() {
        color = document.getElementById("colores").value;

    }

    function stamano(numero) {
        tamano = numero;
    }

    // Esta función permite descargar la imagen que has dibujado
    function guardari() {
        var canvas = document.getElementById("canvas");
        var imagen = canvas.toDataURL("image/png");

        console.log('descargando');
        this.href = imagen;
    }

    //Esta función realiza la petición a la API en la que se encuntra el 
    //modelo que realiza la clasificación
    function solicitud() {
        var canvas = document.getElementById("canvas");
        var imagen = canvas.toDataURL("image/png");

        var formdata = new FormData();

        formdata.append("imagen", imagen);

        var requestOptions = {
            method: 'POST',
            body: formdata,
            redirect: 'follow'
        };

        // Petición post a la API que se encuentra desplegada en heroku
        // Esta era la url que usaba en local http://127.0.0.1:5000/imagen"
        fetch("https://digits4app.herokuapp.com/imagen", requestOptions)
            .then(response => response.text())
            .then(result => {

                document.getElementById(`resultados`).style.display = "block";
                var actualData = JSON.parse(result);

                console.log(actualData);
                clases = actualData.clases;
                probabilidades = actualData.probabilidades;


                for (let i = 0; i < clases.length; i++) {
                    res = `${clases[i]} : ${probabilidades[i]} %`
                    document.getElementById(`res${i+1}`).innerHTML = res;
                }

                let clase_resultado = 0;
                let maximo = 0;
                let maximo_pos = 0;
                maximo = Math.max.apply(null, probabilidades);
                maximo_pos = probabilidades.indexOf(maximo);
                clase_resultado = clases[maximo_pos]

                document.getElementById('resultado').innerHTML = clase_resultado;
            })
            .catch(error => console.log('error', error));

    }

    function solicitud2() {
        //peticion get de prueba
        fetch('http://127.0.0.1:5000/prueba')
            .then(
                function(response) {
                    if (response.status !== 200) {
                        console.log('Looks like there was a problem. Status Code: ' +
                            response.status);
                        return;
                    }

                    // Examine the text in the response
                    response.json().then(function(data) {
                        console.log(data);
                    });
                }
            )
            .catch(function(err) {
                console.log('Fetch Error :-S', err);
            });

    }

    var canvas = document.getElementById("guardarimagen").addEventListener("click", guardari, false);