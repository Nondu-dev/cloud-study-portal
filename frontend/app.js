const API_URL = "https://q4mgnyvz5j.execute-api.eu-north-1.amazonaws.com";

const noteForm = document.getElementById("noteForm");
const notesList = document.getElementById("notesList");
const emptyMessage = document.getElementById("emptyMessage");
const apiStatus = document.getElementById("apiStatus");

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

checkApiHealth();
loadNotes();