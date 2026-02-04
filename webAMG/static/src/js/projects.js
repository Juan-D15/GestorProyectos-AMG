// Funciones para la lista de proyectos

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
