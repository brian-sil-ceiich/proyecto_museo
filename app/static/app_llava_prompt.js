
// ==================================================
// ELEMENTOS DEL HTML
// ==================================================

const form =
    document.getElementById(
        "analysis-form"
    );


const prompt_text =
    document.getElementById(
        "prompt"
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


    // Ocultar resultado anterior

    resultContainer.hidden =
        true;


    // Limpiar error

    hideError();


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


        const prompt =
            prompt_text.value;


        try {

            setLoading(true);


            // ------------------------------------------


            // ------------------------------------------
            // Crear FormData
            // ------------------------------------------

            const formData =
                new FormData();


            formData.append(
                "prompt",
                prompt
            );


            // ------------------------------------------
            // Enviar al backend
            // ------------------------------------------

            const response =
                await fetch(
                    "/analyze/llava_prompt",
                    {
                        method: "POST",
                        body: formData
                    }
                );

            const responseText =
                await response.text();


            // console.log(
            //     "Status:",
            //     response.status
            // );


            // console.log(
            //     "Respuesta:",
            //     responseText
            // );


            // if (!response.ok) {

            //     throw new Error(
            //         `Error del servidor (${response.status}): ${responseText}`
            //     );

            // }


            let data;

            try {

                data =
                    JSON.parse(
                        responseText
                    );

            } catch (error) {

                throw new Error(
                    "El servidor no devolvió JSON: " +
                    responseText
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
            <strong>Respuesta de Llava:</strong>
        </p>

        <p>
            ${escapeHtml(data.analysis)}
        </p>
        
        <p>
            <strong>Tiempo de análisis:</strong>
            ${data.ollama_time} segundos
        </p>
        
        <p>
            <strong>Tiempo total:</strong>
            ${data.total_time} segundos
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