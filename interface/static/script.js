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
        if (data.image) {
            const img = document.getElementById("uploadPreview");
            img.src = `data:image/jpeg;base64,${data.image}`;
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
});

document.getElementById("file").addEventListener("change", function() {
    var fileName = this.files[0] ? this.files[0].name : "No file chosen";
    document.getElementById("file-name").innerText = fileName;
});