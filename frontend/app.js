const API_URL = "https://q4mgnyvz5j.execute-api.eu-north-1.amazonaws.com";

const noteForm = document.getElementById("noteForm");
const notesList = document.getElementById("notesList");
const emptyMessage = document.getElementById("emptyMessage");
const apiStatus = document.getElementById("apiStatus");

const documentForm = document.getElementById("documentForm");
const studyDocument = document.getElementById("studyDocument");
const uploadStatus = document.getElementById("uploadStatus");

let notes = [];

async function checkApiHealth() {
    try {
        const response = await fetch(API_URL + "/health");

        if (!response.ok) {
            throw new Error("Health check failed");
        }

        const data = await response.json();
        apiStatus.textContent = "Cloud connection: " + data.status;
    } catch (error) {
        apiStatus.textContent = "Cloud connection unavailable. Please try again.";
        console.error("API health check failed:", error);
    }
}

function displayNotes() {
    notesList.replaceChildren();
    emptyMessage.hidden = notes.length > 0;

    notes.forEach(function (note) {
        const card = document.createElement("article");
        card.className = "note-card";

        const subjectHeading = document.createElement("p");
        subjectHeading.textContent = "Subject: " + note.subject;

        const noteTitle = document.createElement("h3");
        noteTitle.textContent = note.title;

        const noteContent = document.createElement("p");
        noteContent.textContent = note.content;

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete Note";
        deleteButton.className = "delete-button";

        deleteButton.addEventListener("click", async function () {
            deleteButton.disabled = true;

            try {
                const response = await fetch(
                    API_URL + "/notes/" + encodeURIComponent(note.noteId),
                    { method: "DELETE" }
                );

                if (!response.ok) {
                    throw new Error("Could not delete note");
                }

                await loadNotes();
            } catch (error) {
                alert("Could not delete the note. Please try again.");
                console.error("Delete note failed:", error);
                deleteButton.disabled = false;
            }
        });

        card.append(subjectHeading, noteTitle, noteContent, deleteButton);
        notesList.appendChild(card);
    });
}

async function loadNotes() {
    try {
        const response = await fetch(API_URL + "/notes");

        if (!response.ok) {
            throw new Error("Could not load notes");
        }

        const data = await response.json();
        notes = data.notes || [];
        displayNotes();
    } catch (error) {
        emptyMessage.hidden = false;
        emptyMessage.textContent = "Could not load notes. Please refresh the page.";
        console.error("Load notes failed:", error);
    }
}

noteForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const subject = document.getElementById("subject").value.trim();
    const title = document.getElementById("title").value.trim();
    const content = document.getElementById("content").value.trim();

    if (!subject || !title || !content) {
        return;
    }

    const submitButton = noteForm.querySelector("button[type='submit']");
    submitButton.disabled = true;

    try {
        const response = await fetch(API_URL + "/notes", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                subject: subject,
                title: title,
                content: content
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Could not save note");
        }

        noteForm.reset();
        await loadNotes();
    } catch (error) {
        alert("Could not save the note. Please try again.");
        console.error("Save note failed:", error);
    } finally {
        submitButton.disabled = false;
    }
});

documentForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const file = studyDocument.files[0];

    if (!file) {
        uploadStatus.textContent = "Please choose a document.";
        return;
    }

    const allowedTypes = {
        pdf: "application/pdf",
        txt: "text/plain",
        docx: "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    };

    const extension = file.name.split(".").pop().toLowerCase();
    const expectedType = allowedTypes[extension];

    if (!expectedType || file.type !== expectedType) {
        uploadStatus.textContent = "Choose a PDF, TXT or DOCX file with a matching file type.";
        return;
    }

    if (file.size === 0 || file.size > 3 * 1024 * 1024) {
        uploadStatus.textContent = "Choose a file larger than 0 bytes and no bigger than 3 MB.";
        return;
    }

    const uploadButton = documentForm.querySelector("button[type='submit']");
    uploadButton.disabled = true;
    uploadStatus.textContent = "Uploading document...";

    try {
        const fileContent = await readFileAsBase64(file);

        const response = await fetch(API_URL + "/documents", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                fileName: file.name,
                contentType: expectedType,
                fileContent: fileContent
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Upload failed");
        }

        uploadStatus.textContent = "Document uploaded successfully: " + data.fileName;
        documentForm.reset();
    } catch (error) {
        uploadStatus.textContent = "Could not upload the document. Please try again.";
        console.error("Document upload failed:", error);
    } finally {
        uploadButton.disabled = false;
    }
});

function readFileAsBase64(file) {
    return new Promise(function (resolve, reject) {
        const reader = new FileReader();

        reader.onload = function () {
            const result = reader.result;
            resolve(result.split(",")[1]);
        };

        reader.onerror = function () {
            reject(new Error("Could not read the selected file"));
        };

        reader.readAsDataURL(file);
    });
}

checkApiHealth();
loadNotes();
