const video = document.getElementById(
    "camera"
);

const canvas = document.getElementById(
    "canvas"
);

const startButton = document.getElementById(
    "start-camera"
);

const captureButton = document.getElementById(
    "capture"
);

const sendButton = document.getElementById(
    "send"
);

const capturedImage = document.getElementById(
    "captured-image"
);

const capturedContainer =
    document.getElementById(
        "captured-container"
    );

/* const promptInput = document.getElementById(
    "prompt"
); */

const loading = document.getElementById(
    "loading"
);

const errorContainer =
    document.getElementById(
        "error"
    );

const summaryContainer = document.getElementById(
    "summary"
);

const resultContainer =
    document.getElementById(
        "result-container"
    );

const elementsContainer = document.getElementById(
    "elements"
);

const jsonResult =
    document.getElementById(
        "json-result"
    );

let cameraStream = null;

let capturedBlob = null;

startButton.addEventListener(
    "click",
    async () => {

        hideError();

        try {

            cameraStream =
                await navigator.mediaDevices
                    .getUserMedia({
                        video: true,
                        audio: false
                    });

            video.srcObject =
                cameraStream;

            captureButton.disabled =
                false;

            startButton.disabled =
                true;

        } catch (error) {

            showError(
                "No fue posible acceder a la cámara: "
                + error.message
            );
        }
    }
);

captureButton.addEventListener(
    "click",
    () => {

        if (!cameraStream) {
            showError(
                "La cámara no está activa."
            );

            return;
        }

        const width = video.videoWidth;

        const height = video.videoHeight;

        if (!width || !height) {

            showError(
                "La cámara todavía no está lista."
            );

            return;
        }

        canvas.width = width;

        canvas.height = height;

        const context =
            canvas.getContext("2d");

        context.drawImage(
            video,
            0,
            0,
            width,
            height
        );

        canvas.toBlob(
            (blob) => {

                if (!blob) {

                    showError(
                        "No fue posible capturar la imagen."
                    );

                    return;
                }

                capturedBlob = blob;

                const imageUrl =
                    URL.createObjectURL(
                        blob
                    );

                capturedImage.src =
                    imageUrl;

                capturedContainer.hidden =
                    false;

                sendButton.disabled =
                    false;
            },
            "image/jpeg",
            0.90
        );
    }
);

sendButton.addEventListener(
    "click",
    async () => {

        hideError();

        if (!capturedBlob) {

            showError(
                "Primero debes capturar una fotografía."
            );

            return;
        }

        const prompt = "Hi";
        /* const prompt =
            promptInput.value.trim();

        if (!prompt) {

            showError(
                "Debes introducir un prompt."
            );

            return;
        } */

        const formData =
            new FormData();

        formData.append(
            "file",
            capturedBlob,
            "camera.jpg"
        );

        formData.append(
            "prompt",
            prompt
        );

        try {

            setLoading(true);

            resultContainer.hidden =
                true;

            const response =
                await fetch(
                    "/analyze/camera",
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

            /* resultJson.textContent =
                JSON.stringify(
                    data,
                    null,
                    2
                );

            resultContainer.hidden =
                false;  */

            
            showResult(data);

        } catch (error) {

            showError(
                error.message
            );

        } finally {

            setLoading(false);
        }
    }
);

function setLoading(isLoading) {

    loading.hidden =
        !isLoading;

    sendButton.disabled =
        isLoading;

    sendButton.textContent =
        isLoading
            ? "Analizando..."
            : "Enviar para análisis";
}


function showError(message) {

    errorContainer.textContent =
        message;

    errorContainer.hidden =
        false;
}


function hideError() {

    errorContainer.textContent =
        "";

    errorContainer.hidden =
        true;
}

function escapeHtml(value) {

    const div = document.createElement("div");

    div.textContent = value;

    return div.innerHTML;
}

function showResult(data) {
    resultContainer.hidden = false;

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

    elementsContainer.innerHTML = "";

    jsonResult.textContent =
        JSON.stringify(
            data,
            null,
            2
        );
}

