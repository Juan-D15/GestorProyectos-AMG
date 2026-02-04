// Funciones para la lista de proyectos

// Manejar clic en fila de proyecto para ir al detalle
document.addEventListener('DOMContentLoaded', function() {
    const projectRows = document.querySelectorAll('[data-project-id]');
    projectRows.forEach(function(row) {
        row.addEventListener('click', function(e) {
            // Si el clic es en un botón de acción, no navegar al detalle
            if (e.target.closest('button')) {
                e.stopPropagation();
                return;
            }
            const projectId = this.getAttribute('data-project-id');
            window.location.href = `/dashboard/proyectos/${projectId}/`;
        });
    });

    // Validación del formulario de proyectos
    const form = document.querySelector('form');
    const errorMessagesDiv = document.getElementById('formErrorMessages');
    
    if (form && errorMessagesDiv) {
        form.addEventListener('submit', function(e) {
            // Limpiar errores anteriores
            errorMessagesDiv.innerHTML = '';
            
            const project_name = form.querySelector('input[name="project_name"]')?.value.trim();
            const project_code = form.querySelector('input[name="project_code"]')?.value.trim();
            
            let errors = [];
            
            // Validar nombre del proyecto
            if (!project_name) {
                errors.push('El nombre del proyecto es obligatorio');
            }
            
            // Validar código del proyecto si se ingresó
            if (project_code && !/^[a-zA-Z0-9-]+$/.test(project_code)) {
                errors.push('El código solo puede contener letras, números y guiones');
            }
            
            // Mostrar errores si los hay
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
                
                // Scroll al inicio del formulario
                form.scrollIntoView({ behavior: 'smooth' });
                
                // Disparar evento personalizado para el script de auto-dismiss
                const customEvent = new CustomEvent('messagesUpdated', { detail: { messages: document.querySelectorAll('[data-auto-dismiss]') } });
                document.dispatchEvent(customEvent);
            }
        });
    }
});

// Editar proyecto
function editProject(projectId) {
    window.location.href = `/dashboard/proyectos/${projectId}/editar/`;
}

// Eliminar proyecto
function deleteProject(projectId) {
    window.location.href = `/dashboard/proyectos/${projectId}/eliminar/`;
}

// Funciones para manejo de imagen de portada
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById('imagePreview');
            const container = document.getElementById('imagePreviewContainer');
            
            preview.src = e.target.result;
            container.classList.remove('hidden');
            inputContainer.classList.add('hidden');
            
            // Asegurar que la imagen se cargue completamente antes de ajustar
            preview.onload = function() {
                // Ajustar altura del contenedor a la altura natural de la imagen
                const naturalHeight = preview.naturalHeight;
                const naturalWidth = preview.naturalWidth;
                const containerHeight = Math.min(naturalHeight, 400); // Altura máxima de 400px
                
                // Ajustar el estilo de la imagen para que llene el contenedor
                preview.style.height = 'auto';
                preview.style.maxHeight = containerHeight + 'px';
                preview.style.maxWidth = '100%';
            };
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function removeCoverImage() {
    const input = document.getElementById('coverImageInput');
    const preview = document.getElementById('imagePreview');
    const container = document.getElementById('imagePreviewContainer');
    const inputContainer = input.closest('.flex-1');
    
    input.value = '';
    preview.src = '';
    container.classList.add('hidden');
    inputContainer.classList.remove('hidden');
    
    // Resetear estilos
    preview.style.height = '';
    preview.style.maxHeight = '';
    preview.style.maxWidth = '';
}

// Eliminar proyecto
function deleteProject(projectId) {
    window.location.href = `/dashboard/proyectos/${projectId}/eliminar/`;
}

// Funciones para manejo de imagen de portada
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById('imagePreview');
            const container = document.getElementById('imagePreviewContainer');
            const inputContainer = input.closest('.flex-1');
            
            preview.src = e.target.result;
            container.classList.remove('hidden');
            inputContainer.classList.add('hidden');
            
            // Asegurar que la imagen se cargue completamente antes de ajustar
            preview.onload = function() {
                // Ajustar altura del contenedor a la altura natural de la imagen
                const naturalHeight = preview.naturalHeight;
                const naturalWidth = preview.naturalWidth;
                const containerHeight = Math.min(naturalHeight, 400); // Altura máxima de 400px
                
                // Ajustar el estilo de la imagen para que llene el contenedor
                preview.style.height = 'auto';
                preview.style.maxHeight = containerHeight + 'px';
                preview.style.maxWidth = '100%';
            };
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function removeCoverImage() {
    const input = document.getElementById('coverImageInput');
    const preview = document.getElementById('imagePreview');
    const container = document.getElementById('imagePreviewContainer');
    const inputContainer = input.closest('.flex-1');
    
    input.value = '';
    preview.src = '';
    container.classList.add('hidden');
    inputContainer.classList.remove('hidden');
    
    // Resetear estilos
    preview.style.height = '';
    preview.style.maxHeight = '';
    preview.style.maxWidth = '';
}
