// app.js - Código común
document.addEventListener('DOMContentLoaded', function() {
    // Navegación entre páginas
    const navigateTo = (page) => {
        window.location.href = page;
    };

    // Botón de inicio en página principal
    const startBtn = document.getElementById('startTest');
    if(startBtn) {
        startBtn.addEventListener('click', () => navigateTo('test.html'));
    }

    const startBtn2 = document.getElementById('comenzar');
    if(startBtn2) {
        startBtn2.addEventListener('click', () => navigateTo('test.html'));
    }

    // Botón de regreso
    const backBtn = document.getElementById('backButton');
    if(backBtn) {
        backBtn.addEventListener('click', () => navigateTo('index.html'));
    }
});