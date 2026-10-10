const noteForm = document.getElementById("noteForm");
const notesList = document.getElementById("notesList");
const emptyMessage = document.getElementById("emptyMessage");

noteForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const subject = document.getElementById("subject").value.trim();
    const title = document.getElementById("title").value.trim();
    const content = document.getElementById("content").value.trim();

    if (!subject || !title || !content) {
        return;
    }

    const card = document.createElement("article");
    card.className = "note-card";

    const subjectHeading = document.createElement("p");
    subjectHeading.textContent = "Subject: " + subject;

    const noteTitle = document.createElement("h3");
    noteTitle.textContent = title;

    const noteContent = document.createElement("p");
    noteContent.textContent = content;

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete Note";
    deleteButton.className = "delete-button";

    deleteButton.addEventListener("click", function () {
        card.remove();
        emptyMessage.hidden = notesList.children.length > 0;
    });

    card.append(subjectHeading, noteTitle, noteContent, deleteButton);
    notesList.prepend(card);

    emptyMessage.hidden = true;
    noteForm.reset();
});
