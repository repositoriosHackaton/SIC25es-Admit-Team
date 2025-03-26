document.addEventListener('DOMContentLoaded', function() {
    const results = JSON.parse(localStorage.getItem('predictionResults'));
    
    if(!results) {
        alert('No se encontraron resultados. Por favor completa el cuestionario primero.');
        window.location.href = 'cuestionario.html';
        return;
    }

    // Función para actualizar cada tarjeta
    const updateCard = (selector, data) => {
        const card = document.querySelector(selector);
        if(!card) return;

        card.querySelector('.probability-percent').textContent = `${data.probability}%`;
        
        // Actualizar estrellas basadas en rating (entero)
        const starsContainer = card.querySelector('.stars');
        starsContainer.innerHTML = Array(5).fill()
            .map((_, i) => `<i class="fas fa-star ${i < data.rating ? 'text-warning' : ''}"></i>`)
            .join('');
        
        // Actualizar recomendaciones
        const recommendationsList = card.querySelector('.recommendations ul');
        recommendationsList.innerHTML = data.recommendations
            .map(uni => `<li><i class="fas fa-check me-2"></i>${uni}</li>`)
            .join('');
    };

    // Actualizar todas las tarjetas
    updateCard('.safe-school', {
        probability: results.safeSchool.probability,
        rating: results.safeSchool.rating,  // Usa 'rating' en lugar de 'ranking'
        recommendations: results.safeSchool.recommendations
    });

    updateCard('.target-school', {
        probability: results.targetSchool.probability,
        rating: results.targetSchool.rating,  // Usa 'rating' en lugar de 'ranking'
        recommendations: results.targetSchool.recommendations
    });

    updateCard('.reach-school', {
        probability: results.reachSchool.probability,
        rating: results.reachSchool.rating,  // Usa 'rating' en lugar de 'ranking'
        recommendations: results.reachSchool.recommendations
    });
});