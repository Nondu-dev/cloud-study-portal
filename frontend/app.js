const noteForm = document.getElementById("noteForm");
const notesList = document.getElementById("notesList");
const emptyMessage = document.getElementById("emptyMessage");

let notes = JSON.parse(localStorage.getItem("cloudStudyNotes")) || [];

function saveNotes() {
    localStorage.setItem("cloudStudyNotes", JSON.stringify(notes));
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

        deleteButton.addEventListener("click", function () {
            notes = notes.filter(function (item) {
                return item.id !== note.id;
            });

            saveNotes();
            displayNotes();
        });

        card.append(subjectHeading, noteTitle, noteContent, deleteButton);
        notesList.appendChild(card);
    });
}

noteForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const subject = document.getElementById("subject").value.trim();
    const title = document.getElementById("title").value.trim();
    const content = document.getElementById("content").value.trim();

    if (!subject || !title || !content) {
        return;
    }

    const note = {
        id: crypto.randomUUID(),
        subject: subject,
        title: title,
        content: content
    };

    notes.push(note);
    saveNotes();
    displayNotes();
    noteForm.reset();
});

displayNotes();


const API_URL = "https://q4mgnyvz5j.execute-api.eu-north-1.amazonaws.com";


async function checkApiHealth() {
    const apiStatus = document.getElementById("apiStatus");

    try {
        const response = await fetch(API_URL + "/health");

        if (!response.ok) {
            throw new Error("API request failed");
        }

        const data = await response.json();

        apiStatus.textContent = "Cloud connection: " + data.status;
    } catch (error) {
        apiStatus.textContent = "Cloud connection unavailable. Please try again.";
        console.error("API health check failed:", error);
    }
}

checkApiHealth();


