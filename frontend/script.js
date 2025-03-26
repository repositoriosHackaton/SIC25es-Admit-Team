// Elementos del DOM
const inputElement = document.getElementById('user-input');
const chatMessages = document.getElementById('chat-messages');

// Función para enviar preguntas al chatbot
function enviarPregunta(customMessage = null) {
    // Determinar la pregunta (de input o del parámetro)
    const pregunta = customMessage || inputElement.value.trim();

    if (!pregunta) return; // Evita enviar preguntas vacías

    // Eliminar mensaje inicial y preguntas sugeridas si existen
    const initialMessage = chatMessages.querySelector('.initial-message');
    const suggestedQuestions = chatMessages.querySelector('.suggested-questions');
    if (initialMessage) initialMessage.remove();
    if (suggestedQuestions) suggestedQuestions.remove();

    // Agregar mensaje del usuario
    agregarMensajeAlChat(pregunta, 'user-message');
    
    // Limpiar input
    inputElement.value = '';

    // Simular respuesta del bot (reemplazar con lógica real de backend)
    setTimeout(() => {
        const respuestaSimulada = generarRespuestaSimulada(pregunta);
        agregarMensajeAlChat(respuestaSimulada, 'bot-message');
    }, 500);
}

// Función para agregar mensajes al chat
function agregarMensajeAlChat(texto, clase) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', clase);
    messageDiv.textContent = texto;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight; // Desplazar al fondo del chat
}

// Función para generar respuestas simuladas (reemplazar con backend real)
function generarRespuestaSimulada(pregunta) {
    const respuestas = {
        "¿Cómo puedo aplicar a universidades en EE.UU.?": "Para aplicar a universidades en EE.UU., necesitas: 1) Preparar tu expediente académico, 2) Tomar exámenes estandarizados como SAT o ACT, 3) Escribir ensayos de admisión, 4) Obtener cartas de recomendación.",
        "¿Qué carreras tienen mayor demanda en el futuro?": "Algunas carreras con alta demanda son: Tecnología (Ciencia de Datos, Inteligencia Artificial), Ingeniería de Software, Ciberseguridad, Enfermería, Sostenibilidad Ambiental.",
        "¿Cómo aprender a programar desde cero?": "Para aprender a programar: 1) Elige un lenguaje (Python es ideal para principiantes), 2) Toma cursos online gratuitos, 3) Practica con proyectos pequeños, 4) Únete a comunidades de programación.",
        "¿Cuáles son los beneficios de aprender inglés?": "Beneficios de aprender inglés: 1) Mejores oportunidades laborales, 2) Acceso a educación internacional, 3) Comunicación global, 4) Desarrollo personal y profesional."
    };

    return respuestas[pregunta] || "Lo siento, no tengo una respuesta específica para esa pregunta. ¿Podrías ser más específico?";
}

// Función para mostrar recomendaciones iniciales
function mostrarRecomendaciones() {
    const recomendaciones = [
        "¿Cómo puedo aplicar a universidades en EE.UU.?",
        "¿Qué carreras tienen mayor demanda en el futuro?",
        "¿Cómo aprender a programar desde cero?",
        "¿Cuáles son los beneficios de aprender inglés?"
    ];

    // Crear contenedor de preguntas sugeridas
    const suggestedQuestionsDiv = document.createElement('div');
    suggestedQuestionsDiv.classList.add('suggested-questions');

    recomendaciones.forEach(pregunta => {
        const questionDiv = document.createElement('div');
        questionDiv.classList.add('suggested-question');
        questionDiv.textContent = pregunta;
        questionDiv.addEventListener('click', () => enviarPregunta(pregunta));
        suggestedQuestionsDiv.appendChild(questionDiv);
    });

    chatMessages.appendChild(suggestedQuestionsDiv);
}

// Inicializar el chat al cargar la página
function inicializarChat() {
    chatMessages.innerHTML = '';
    mostrarRecomendaciones();
}

// Eventos
document.addEventListener('DOMContentLoaded', inicializarChat);
inputElement.addEventListener('keypress', e => { 
    if (e.key === 'Enter') enviarPregunta(); 
});

// Agregar evento a botón de enviar
const enviarButton = document.querySelector('.input-area button');
enviarButton.addEventListener('click', enviarPregunta);