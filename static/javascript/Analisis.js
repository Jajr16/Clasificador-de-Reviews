function enviarComentario() {
    // Obtén el nombre de la columna y el archivo seleccionado
    const input_column = document.querySelector('.Comentarios');
    const comentario = input_column.value;

    if (!comentario) {
        alert("Debe ingresar un comentario");
    } else {
        const sendComment = new FormData();

        sendComment.append('comment-evaluate', comentario);

        fetch('/comentario', {
            method: 'POST',
            body: sendComment,
            headers: {
                'Accept': 'application/json'
            }
        }).then(response => response.json())
            .then(result => {
                const commentResult = document.querySelector('.Resultado');
                commentResult.innerHTML = result.message; 
            })
            .catch(error => {
                console.error(error);
            });
    }
}

function enviarSolicitud() {
    // Obtén el nombre de la columna y el archivo seleccionado
    const input_column = document.querySelector('.nom_Column');
    const cvs_file = document.querySelector('#file-1');

    const column_name = input_column.value;
    const csvFile = cvs_file.files[0];

    // Verifica si la columna y el archivo están definidos
    if (column_name && csvFile) {
        // Verifica que el archivo sea un archivo CSV
        if (csvFile.name.endsWith('.csv')) {
            const Csv_diccionario = new FormData();
            Csv_diccionario.append('file-1', csvFile);

            // Agrega el nombre de la columna como un campo en FormData
            Csv_diccionario.append('nom_Column', column_name);

            // Realiza la solicitud POST a Flask
            fetch('/cargar_csv', {
                method: 'POST',
                body: Csv_diccionario,
                headers: {
                    'Accept': 'application/json'
                }
            })
                .then(response => response.json())
                .then(result => {
                    Graficar(result);
                })
                .catch(error => {
                    console.error(error);
                });
        } else {
            alert('El archivo debe tener extensión .csv');
        }

        // Limpia los valores para futuras manipulaciones
        input_column.value = '';
        cvs_file.value = null;
    } else {
        alert('Por favor, ingrese el nombre de la columna y seleccione un archivo CSV.');
    }
}


function Graficar(Data) {

    // Calcula los porcentajes
    const total = Data.data.reduce((a, b) => a + b, 0);
    const porcentajePositivo = (Data.data[0] / total) * 100;
    const porcentajeNegativo = (Data.data[1] / total) * 100;

    // Añade la clase 'visible' al div del gráfico para mostrarlo
    const graficoDiv = document.querySelector('.Grafico');
    graficoDiv.classList.add('visible');

    // Desplaza el contenedor hacia la derecha
    const contenedorDiv = document.querySelector('.contenedor');
    contenedorDiv.style.transform = 'translateX(4%)';

    // Desplaza el contenedor hacia la izquierda
    const PresentacionDiv = document.querySelector('.Presentacion');
    PresentacionDiv.style.transform = 'translateX(-10%)';
    //////////////// Gráfico //////////////////
    let pie = d3.pie();
    let graficpie = pie(Data.data);

    const etiquetas = ["Reseñas positivas", "Reseñas negativas"];
    const colores = ['#2874A6', '#B03A2E'];

    let Arco = d3.arc();
    Arco.innerRadius(0).outerRadius(100);

    // Selecciona el elemento SVG en el que deseas dibujar el gráfico
    const svg = d3.select("svg");

    svg.append("g")
        .attr("transform", "translate(250,250)")
        .selectAll("path")
        .data(graficpie)
        .enter()
        .append("path")
        .attr('d', Arco)
        .style("fill", (d, i) => colores[i])
        .style("stroke", "black");

    // Etiquetas de porcentaje
    svg.selectAll("text")
        .data(graficpie)
        .enter()
        .append("text")
        .text((d, i) => i === 0 ? `${porcentajePositivo.toFixed(1)}%` : `${porcentajeNegativo.toFixed(1)}%`)
        .attr("transform", d => {
            const centro = Arco.centroid(d);
            for (var k = 0; k < centro.length; k++) {
                centro[k] += 250
            }
            return `translate(${centro[0]}, ${centro[1]})`;
        })
        .style("text-anchor", "middle")
        .style("font-size", "12px");

    // Crear una leyenda
    const legend = svg.append("g")
        .attr("transform", "translate(400, 100)"); // Ajusta la posición de la leyenda

    const legendRectSize = 18;
    const legendSpacing = 4;

    const legendItems = legend.selectAll(".legend-item")
        .data(etiquetas)
        .enter()
        .append("g")
        .attr("class", "legend-item")
        .attr("transform", function (d, i) {
            const height = legendRectSize + legendSpacing;
            const offset = height * etiquetas.length / 2;
            const horz = -2 * legendRectSize;
            const vert = i * height - offset;
            return "translate(" + horz + "," + vert + ")";
        });

    legendItems.append("rect")
        .attr("width", legendRectSize)
        .attr("height", legendRectSize)
        .style("fill", (d, i) => colores[i]);

    legendItems.append("text")
        .attr("x", legendRectSize + legendSpacing)
        .attr("y", legendRectSize - legendSpacing)
        .text((d) => d);
}
