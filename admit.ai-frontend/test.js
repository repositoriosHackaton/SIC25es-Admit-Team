document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const errorContainer = document.createElement('div');
    errorContainer.className = 'alert alert-danger mt-3 d-none';
    form.parentNode.insertBefore(errorContainer, form.nextSibling);

    // Configuración de validaciones
    const validations = {
        gre: {
            min: 0,
            max: 340,
            message: 'GRE debe estar entre 0 y 340'
        },
        toefl: {
            min: 0,
            max: 120,
            message: 'TOEFL debe estar entre 0 y 120'
        },
        gpa: {
            min: 0,
            max: 10.0,
            message: 'GPA debe estar entre 0.0 y 10.0'
        },
        recommendation: {
            min: 1,
            max: 5,
            message: 'Recomendación debe estar entre 1 y 5'
        },
        sop: {
            min: 1,
            max: 5,
            message: 'Statement of Purpose debe estar entre 1 y 5'
        }
    };

    const validateFormData = (data) => {
        const errors = [];
        
        // Validar campos numéricos
        Object.keys(validations).forEach(field => {
            if (data[field] < validations[field].min || data[field] > validations[field].max) {
                errors.push(validations[field].message);
            }
        });

        // Validar investigación seleccionada
        if (form.querySelector('[name="investigacion"]:checked') === null) {
            errors.push('Debes seleccionar si has realizado investigación');
        }

        // Validar decimales en GPA
        if (!/^\d+(\.\d{1,2})?$/.test(form.querySelector('[name="gpa"]').value)) {
            errors.push('GPA debe tener máximo 2 decimales');
        }

        return errors;
    };

    if(form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            errorContainer.classList.add('d-none');

            // Obtener valores del formulario
            const formValues = {
                greScore: parseInt(form.querySelector('[name="gre"]').value),
                toeflScore: parseInt(form.querySelector('[name="toefl"]').value),
                cgpa: parseFloat(form.querySelector('[name="gpa"]').value),
                lor: parseInt(form.querySelector('[name="recommendation"]').value),
                research: form.querySelector('[name="investigacion"]:checked')?.value === 'si' ? 1 : 0,
                sop: parseInt(form.querySelector('[name="sop"]').value)
            };

            // Validación de campos
            const errors = validateFormData(formValues);
            
            if(errors.length > 0) {
                errorContainer.innerHTML = `
                    <strong>Errores encontrados:</strong>
                    <ul class="mb-0">
                        ${errors.map(error => `<li>${error}</li>`).join('')}
                    </ul>
                `;
                errorContainer.classList.remove('d-none');
                window.scrollTo({ top: 0, behavior: 'smooth' });
                return;
            }

            try {
                const response = await fetch('http://127.0.0.1:8000/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formValues)
                });

                if(!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'Error en el servidor');
                }
                
                const result = await response.json();
                localStorage.setItem('predictionResults', JSON.stringify(result));
                window.location.href = 'resultados.html';
                
            } catch (error) {
                console.error('Error:', error);
                errorContainer.innerHTML = `
                    <strong>Error:</strong> ${error.message || 'Error al procesar la solicitud'}
                `;
                errorContainer.classList.remove('d-none');
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    }
});