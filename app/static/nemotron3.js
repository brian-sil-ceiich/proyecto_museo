// ==================================================
// IMÁGENES
// ==================================================

const images = [
    "/static/images/feliz.png",
    "/static/images/nino_llorando.png",
    "/static/images/triste.png"
];


// ==================================================
// ELEMENTOS HTML
// ==================================================

const form =
    document.getElementById(
        "nemotron-form"
    );


const carouselTrack =
    document.getElementById(
        "carousel-track"
    );


const imagePreview =
    document.getElementById(
        "image-preview"
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


    selectedIndex =
        index;


    const carouselImages =
        document.querySelectorAll(
            ".carousel-image"
        );


    carouselImages.forEach(
        image => {

            image.classList.remove(
                "selected"
            );

        }
    );


    const selectedImage =
        carouselImages[index];


    if (!selectedImage) {

        return;

    }


    selectedImage.classList.add(
        "selected"
    );


    imagePreview.src =
        images[index];


    imagePreview.style.display =
        "block";


    selectedImage.scrollIntoView({
        behavior: "smooth",
        block: "nearest",
        inline: "center"
    });


    resultContainer.hidden =
        true;


    hideError();

}


// ==================================================
// ANTERIOR
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
// SIGUIENTE
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
// ANALIZAR
// ==================================================

form.addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();


        hideError();


        resultContainer.hidden =
            true;


        try {

            setLoading(true);


            const imageUrl =
                images[selectedIndex];


            // ------------------------------------------
            // Obtener imagen
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
                "Hi"
            );


            // ------------------------------------------
            // Endpoint Nemotron 3
            // ------------------------------------------

            const response =
                await fetch(
                    "/analyze/nemotron3",
                    {
                        method: "POST",
                        body: formData
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Error al analizar la imagen."
                );

            }


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
// NOMBRE DEL ARCHIVO
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
            <strong>Respuesta de Nemotron 3:</strong>
        </p>

        <p>
            ${escapeHtml(data.analysis)}
        </p>
    `;


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
// LOADING
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
// ERROR
// ==================================================

function showError(message) {

    errorContainer.textContent =
        message;


    errorContainer.hidden =
        false;

}


function hideError() {

    errorContainer.hidden =
        true;


    errorContainer.textContent =
        "";

}


// ==================================================
// INICIALIZAR
// ==================================================

createCarousel();

selectImage(0);