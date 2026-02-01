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
}
