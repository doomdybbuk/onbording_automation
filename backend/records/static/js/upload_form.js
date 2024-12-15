document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        alert("Form submitted! Files are being uploaded.");
        // Add your AJAX or fetch logic here if needed
    });
});
