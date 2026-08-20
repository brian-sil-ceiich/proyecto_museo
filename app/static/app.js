// ==================================================
// LISTA DE IMÁGENES
// ==================================================

const images = [
    "/static/images/feliz.png",
    "/static/images/nino_llorando.png",
    "/static/images/triste.png"
];


// ==================================================
// ELEMENTOS DEL HTML
// ==================================================

const form =
    document.getElementById(
        "analysis-form"
    );


const imagePreview =
    document.getElementById(
        "image-preview"
    );


const carouselTrack =
    document.getElementById(
        "carousel-track"
    );


const prevButton =
    document.getElementById(
        "prev-button"
    );


const nextButton =
    document.getElementById(
        "next-button"
    );


const analyzeButton =
    document.getElementById(
        "analyze-button"
    );


const loading =
    document.getElementById(
        "loading"
    );


const errorContainer =
    document.getElementById(
        "error"
    );


const resultContainer =
    document.getElementById(
        "result-container"
    );


const summaryContainer =
    document.getElementById(
        "summary"
    );


const elementsContainer =
    document.getElementById(
        "elements"
    );


const jsonResult =
    document.getElementById(
        "json-result"
    );


// ==================================================
// ESTADO
// ==================================================

let selectedIndex = 0;


// ==================================================
// CREAR CARRUSEL
// ==================================================

function createCarousel() {

    carouselTrack.innerHTML = "";


    images.forEach(
        (imageUrl, index) => {

            const image =
                document.createElement(
                    "img"
                );


            image.src =
                imageUrl;


            image.alt =
                `Persona ${index + 1}`;


            image.classList.add(
                "carousel-image"
            );


            image.dataset.index =
                index;


            image.addEventListener(
                "click",
                () => {

                    selectImage(index);

                }
            );


            carouselTrack.appendChild(
                image
            );

        }
    );

}


// ==================================================
// SELECCIONAR IMAGEN
// ==================================================

function selectImage(index) {

    if (
        index < 0 ||
        index >= images.length
    ) {
        return;
    }


    selectedIndex = index;


    const carouselImages =
        document.querySelectorAll(
            ".carousel-image"
        );


    // Quitar selección anterior

    carouselImages.forEach(
        image => {

            image.classList.remove(
                "selected"
            );

        }
    );


    // Obtener imagen seleccionada

    const selectedImage =
        carouselImages[index];


    if (!selectedImage) {
        return;
    }


    // Marcar como seleccionada

    selectedImage.classList.add(
        "selected"
    );


    // Mostrar vista previa

    imagePreview.src =
        images[index];


    imagePreview.style.display =
        "block";


    // Llevar la imagen seleccionada
    // al centro del carrusel

    selectedImage.scrollIntoView({
        behavior: "smooth",
        block: "nearest",
        inline: "center"
    });


    // Ocultar resultado anterior

    resultContainer.hidden =
        true;


    // Limpiar error

    hideError();

}


// ==================================================
// BOTÓN ANTERIOR
// ==================================================

prevButton.addEventListener(
    "click",
    () => {

        let newIndex =
            selectedIndex - 1;


        if (newIndex < 0) {

            newIndex =
                images.length - 1;

        }


        selectImage(
            newIndex
        );

    }
);


// ==================================================
// BOTÓN SIGUIENTE
// ==================================================

nextButton.addEventListener(
    "click",
    () => {

        let newIndex =
            selectedIndex + 1;


        if (
            newIndex >=
            images.length
        ) {

            newIndex = 0;

        }


        selectImage(
            newIndex
        );

    }
);


// ==================================================
// ENVIAR IMAGEN A LLAVA
// ==================================================

form.addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();


        hideError();


        resultContainer.hidden =
            true;


        // Obtener la URL de la imagen
        // actualmente seleccionada

        const imageUrl =
            images[selectedIndex];


        const prompt =
            "Hi";


        try {

            setLoading(true);


            // ------------------------------------------
            // Descargar la imagen seleccionada
            // ------------------------------------------

            const imageResponse =
                await fetch(
                    imageUrl
                );


            if (!imageResponse.ok) {

                throw new Error(
                    "No se pudo cargar la imagen seleccionada."
                );

            }


            // ------------------------------------------
            // Convertir la imagen a Blob
            // ------------------------------------------

            const imageBlob =
                await imageResponse.blob();


            // ------------------------------------------
            // Crear FormData
            // ------------------------------------------

            const formData =
                new FormData();


            formData.append(
                "file",
                imageBlob,
                getFileName(imageUrl)
            );


            formData.append(
                "prompt",
                prompt
            );


            // ------------------------------------------
            // Enviar al backend
            // ------------------------------------------

            const response =
                await fetch(
                    "/analyze/llava",
                    {
                        method: "POST",
                        body: formData
                    }
                );


            // ------------------------------------------
            // Obtener respuesta JSON
            // ------------------------------------------

            const data =
                await response.json();


            // ------------------------------------------
            // Comprobar errores
            // ------------------------------------------

            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Error al analizar la imagen."
                );

            }


            // ------------------------------------------
            // Mostrar resultado
            // ------------------------------------------

            showResult(
                data
            );

        } catch (error) {

            showError(
                error.message
            );

        } finally {

            setLoading(false);

        }

    }
);


// ==================================================
// OBTENER NOMBRE DEL ARCHIVO
// ==================================================

function getFileName(url) {

    return url
        .split("/")
        .pop();

}


// ==================================================
// MOSTRAR RESULTADO
// ==================================================

function showResult(data) {

    resultContainer.hidden =
        false;


    summaryContainer.innerHTML = `
        <p>
            <strong>Edad:</strong>
            ${escapeHtml(data.analysis.age)}
        </p>

        <p>
            <strong>Emoción:</strong>
            ${escapeHtml(data.analysis.emocion)}
        </p>
    `;


    elementsContainer.innerHTML =
        "";


    jsonResult.textContent =
        JSON.stringify(
            data,
            null,
            2
        );

}


// ==================================================
// ESCAPAR HTML
// ==================================================

function escapeHtml(value) {

    const div =
        document.createElement(
            "div"
        );


    div.textContent =
        value;


    return div.innerHTML;

}


// ==================================================
// ESTADO DE CARGA
// ==================================================

function setLoading(isLoading) {

    loading.hidden =
        !isLoading;


    analyzeButton.disabled =
        isLoading;


    analyzeButton.textContent =
        isLoading
            ? "Analizando..."
            : "Analizar fotografía";

}


// ==================================================
// MOSTRAR ERROR
// ==================================================

function showError(message) {

    errorContainer.textContent =
        message;


    errorContainer.hidden =
        false;

}


// ==================================================
// OCULTAR ERROR
// ==================================================

function hideError() {

    errorContainer.hidden =
        true;


    errorContainer.textContent =
        "";

}


// ==================================================
// INICIALIZAR APLICACIÓN
// ==================================================

createCarousel();

selectImage(0);