// Validación de formularios de proyectos (crear y editar)

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const errorMessagesDiv = document.getElementById('formErrorMessages');

    if (form && errorMessagesDiv) {
        form.addEventListener('submit', function(e) {
            errorMessagesDiv.innerHTML = '';

            const project_name = form.querySelector('input[name="project_name"]').value.trim();
            const project_code = form.querySelector('input[name="project_code"]').value.trim();

            let errors = [];

            if (!project_name) {
                errors.push('El nombre del proyecto es obligatorio');
            }

            if (project_code && !/^[a-zA-Z0-9-]+$/.test(project_code)) {
                errors.push('El código solo puede contener letras, números y guiones');
            }

            if (errors.length > 0) {
                e.preventDefault();

                errorMessagesDiv.innerHTML = `
                    <div class="mb-6 p-4 rounded-lg bg-red-100 border-red-200 text-red-700" data-auto-dismiss="5000">
                        <div class="mb-3">
                            <div class="flex items-center">
                                <i class="fas fa-exclamation-circle mr-2"></i>
                                <p class="font-medium">Por favor corrija los siguientes errores:</p>
                            </div>
                        </div>
                        <ul class="list-disc list-inside space-y-1 text-sm">
                            ${errors.map(error => `<li>${error}</li>`).join('')}
                        </ul>
                    </div>
                `;

                form.scrollIntoView({ behavior: 'smooth' });

                const customEvent = new CustomEvent('messagesUpdated', { detail: { messages: document.querySelectorAll('[data-auto-dismiss]') } });
                document.dispatchEvent(customEvent);
            }
        });
    }
});
