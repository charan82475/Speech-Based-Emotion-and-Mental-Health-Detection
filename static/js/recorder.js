let mediaRecorder;
let audioChunks = [];
let stream;

function startRecording() {
    if (mediaRecorder && mediaRecorder.state === "recording") return;

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(s => {
            stream = s;
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.ondataavailable = e => {
                if (e.data.size > 0) audioChunks.push(e.data);
            };

            mediaRecorder.start();
            document.querySelector(".status").innerText = "🎙️ Recording... Speak now!";
        })
        .catch(err => {
            alert("Microphone access denied or not available.");
            console.error(err);
        });
}

function stopRecording() {
    if (!mediaRecorder || mediaRecorder.state !== "recording") return;

    mediaRecorder.stop();

    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }

    document.querySelector(".status").innerText = "⏳ Processing...";

    mediaRecorder.onstop = () => {
        const blob = new Blob(audioChunks, { type: "audio/webm" });
        const formData = new FormData();
        formData.append("audio", blob, "voice.webm");

        fetch("/voice", {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById("emotion").innerText =
                "Emotion: " + (data.emotion || "ERROR").toUpperCase();

            document.getElementById("confidence").innerText =
                "Confidence: " + (data.confidence || "0") + "%";

            // ✅ NEW: Drift display
            document.getElementById("drift").innerText =
                "Drift Score: " + (data.drift !== undefined ? data.drift : "---");

            // Explanation
            if (typeof updateExplanation === "function") {
                updateExplanation(data.emotion ? data.emotion.toUpperCase() : "ERROR");
            }

            document.querySelector(".status").innerText = "✅ Analysis complete";
        })
        .catch(err => {
            console.error(err);
            document.getElementById("emotion").innerText = "Emotion: ERROR";
            document.getElementById("confidence").innerText = "Confidence: ---";
            document.getElementById("drift").innerText = "Drift Score: ---";
            document.querySelector(".status").innerText = "❌ Error";
        });
    };
}