document.getElementById("uploadForm").addEventListener("submit", function(event) {
    event.preventDefault();

    let formData = new FormData(this);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error("Error:", error);
    });
});
