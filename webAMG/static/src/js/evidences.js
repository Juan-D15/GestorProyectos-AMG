// Funciones para el modal de evidencias

// Variable global para almacenar las fotos seleccionadas
let selectedPhotos = [];

function openEvidenceModal() {
    console.log('=== Abriendo modal para CREAR nueva evidencia ===');
    
    document.getElementById('evidenceModal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    
    // Cambiar título a "Agregar Evidencia"
    document.getElementById('evidenceModalTitle').textContent = 'Agregar Evidencia';
    
    // Cambiar acción del formulario a agregar
    const projectId = document.getElementById('evidenceForm').action.match(/\/proyectos\/(\d+)\//)[1];
    document.getElementById('evidenceForm').action = `/dashboard/proyectos/${projectId}/evidencias/agregar/`;
    
    // Limpiar completamente el formulario
    document.getElementById('evidenceForm').reset();
    document.getElementById('evidenceIdInput').value = '';
    
    // Limpiar el input de fotos
    const photoInput = document.getElementById('evidencePhotosInput');
    if (photoInput) {
        photoInput.value = '';
    }
    
    // Limpiar y ocultar el preview
    const previewContainer = document.getElementById('evidencePhotosPreview');
    previewContainer.innerHTML = '';
    previewContainer.classList.add('hidden');
    
    // Limpiar fotos marcadas para eliminar
    const deletePhotosInputs = document.querySelectorAll('#evidenceForm input[name="delete_photos"]');
    deletePhotosInputs.forEach(input => input.remove());
    
    // Limpiar la lista de fotos seleccionadas
    selectedPhotos = [];
    
    console.log('Estado limpiado para nueva evidencia');
    console.log('selectedPhotos:', selectedPhotos.length);
    
    // Hacer que la fecha de fin sea opcional
    document.querySelector('input[name="end_date"]').removeAttribute('required');
}

function openEditEvidenceModal(button) {
    const evidenceId = button.getAttribute('data-evidence-id');
    const startDate = button.getAttribute('data-start-date');
    const endDate = button.getAttribute('data-end-date');
    const description = button.getAttribute('data-description');
    
    console.log(`Abriendo modal de edición para evidencia ${evidenceId}`);
    
    // Abrir el modal
    document.getElementById('evidenceModal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    
    // Cambiar título a "Editar Evidencia"
    document.getElementById('evidenceModalTitle').textContent = 'Editar Evidencia';
    
    // Cambiar acción del formulario a editar
    const projectId = document.getElementById('evidenceForm').action.match(/\/proyectos\/(\d+)\//)[1];
    document.getElementById('evidenceForm').action = `/dashboard/proyectos/${projectId}/evidencias/${evidenceId}/editar/`;
    
    // Llenar el formulario con los datos de la evidencia
    document.getElementById('evidenceIdInput').value = evidenceId;
    document.querySelector('input[name="start_date"]').value = startDate;
    document.querySelector('input[name="end_date"]').value = endDate;
    document.querySelector('textarea[name="description"]').value = description;
    
    // Limpiar completamente el estado anterior
    // Limpiar fotos nuevas seleccionadas
    selectedPhotos = [];
    
    // Limpiar campos ocultos de fotos a eliminar
    const deletePhotosInputs = document.querySelectorAll('#evidenceForm input[name="delete_photos"]');
    deletePhotosInputs.forEach(input => input.remove());
    
    // Limpiar el input de fotos
    const photoInput = document.getElementById('evidencePhotosInput');
    if (photoInput) {
        photoInput.value = '';
    }
    
    // Limpiar y ocultar previsualización
    const previewContainer = document.getElementById('evidencePhotosPreview');
    previewContainer.innerHTML = '';
    previewContainer.classList.add('hidden');
    
    console.log('Estado limpiado antes de cargar fotos existentes');
    
    // Cargar las fotos existentes de la evidencia
    loadExistingPhotos(evidenceId);
}

function closeEvidenceModal() {
    console.log('=== Cerrando modal de evidencia ===');
    
    document.getElementById('evidenceModal').classList.add('hidden');
    document.body.style.overflow = 'auto';
    
    // Limpiar completamente el formulario
    document.getElementById('evidenceForm').reset();
    document.getElementById('evidenceIdInput').value = '';
    
    // Limpiar el input de fotos
    const photoInput = document.getElementById('evidencePhotosInput');
    if (photoInput) {
        photoInput.value = '';
    }
    
    // Limpiar y ocultar el preview
    const previewContainer = document.getElementById('evidencePhotosPreview');
    previewContainer.innerHTML = '';
    previewContainer.classList.add('hidden');
    
    // Limpiar fotos marcadas para eliminar
    const deletePhotosInputs = document.querySelectorAll('#evidenceForm input[name="delete_photos"]');
    deletePhotosInputs.forEach(input => input.remove());
    
    // Limpiar la lista de fotos seleccionadas
    selectedPhotos = [];
    
    console.log('Modal cerrado y estado limpiado');
}

// Función para cargar las fotos existentes de una evidencia
function loadExistingPhotos(evidenceId) {
    // Hacer una petición AJAX para obtener las fotos existentes
    const projectId = document.getElementById('evidenceForm').action.match(/\/proyectos\/(\d+)\//)[1];
    
    console.log(`Cargando fotos existentes para evidencia ${evidenceId}...`);
    
    fetch(`/dashboard/proyectos/${projectId}/evidencias/${evidenceId}/fotos/`)
        .then(response => response.json())
        .then(data => {
            console.log('Fotos recibidas del servidor:', data.photos);
            if (data.photos && data.photos.length > 0) {
                const previewContainer = document.getElementById('evidencePhotosPreview');
                // NO limpiar el contenido, ya que puede haber fotos nuevas previamente seleccionadas
                // previewContainer.innerHTML = '';
                previewContainer.classList.remove('hidden');
                
                console.log(`Mostrando ${data.photos.length} fotos existentes en el modal`);
                
                data.photos.forEach((photo, index) => {
                    // Verificar que ya no exista una foto con este ID (para evitar duplicados)
                    const existingPhoto = previewContainer.querySelector(`button[data-photo-id="${photo.id}"]`);
                    if (existingPhoto) {
                        console.log(`Foto con ID ${photo.id} ya existe en el preview, omitiendo`);
                        return;
                    }
                    
                    const previewDiv = document.createElement('div');
                    previewDiv.className = 'relative group';
                    previewDiv.classList.add('existing-photo'); // Marcar como foto existente
                    
                    const img = document.createElement('img');
                    img.src = '/media/' + photo.photo_url;
                    img.className = 'w-full h-24 object-cover rounded-lg border border-gray-200 cursor-pointer hover:opacity-80 transition-opacity';
                    img.alt = photo.caption || 'Foto de evidencia';
                    // Agregar evento click para ver foto en tamaño completo
                    img.onclick = function() {
                        document.getElementById('photoModalImage').src = '/media/' + photo.photo_url;
                        document.getElementById('photoModal').classList.remove('hidden');
                        document.body.style.overflow = 'hidden';
                    };
                    
                    const removeBtn = document.createElement('button');
                    removeBtn.type = 'button';
                    removeBtn.className = 'absolute -top-2 -right-2 w-8 h-8 bg-red-500 hover:bg-red-600 text-white rounded-full shadow-lg transition-colors flex items-center justify-center';
                    removeBtn.innerHTML = '<i class="fas fa-times text-sm"></i>';
                    removeBtn.setAttribute('data-photo-id', photo.id);
                    removeBtn.setAttribute('title', 'Eliminar esta foto');
                    removeBtn.onclick = function(e) {
                        e.stopPropagation();
                        console.log(`Marcando foto ID ${photo.id} para eliminar`);
                        deleteEvidencePhoto(this);
                    };
                    
                    previewDiv.appendChild(img);
                    previewDiv.appendChild(removeBtn);
                    previewContainer.appendChild(previewDiv);
                    console.log(`Foto existente agregada al preview: ID=${photo.id}`);
                });
                
                console.log(`Total de elementos en preview después de cargar fotos existentes: ${previewContainer.children.length}`);
            }
        })
        .catch(error => {
            console.error('Error al cargar fotos existentes:', error);
        });
}

function previewEvidencePhotos(input) {
    const previewContainer = document.getElementById('evidencePhotosPreview');
    
    if (input.files && input.files.length > 0) {
        previewContainer.classList.remove('hidden');
        
        console.log(`previewEvidencePhotos llamado: ${input.files.length} fotos recibidas`);
        console.log('Fotos actuales en selectedPhotos:', selectedPhotos.length);
        
        // Agregar solo las NUEVAS fotos a la lista de fotos seleccionadas
        // Verificar duplicados por nombre y tamaño
        const newFiles = Array.from(input.files).filter(newFile => {
            return !selectedPhotos.some(existingFile => 
                existingFile.name === newFile.name && 
                existingFile.size === newFile.size
            );
        });
        
        console.log(`Fotos nuevas (sin duplicados): ${newFiles.length}`);
        
        // Agregar las nuevas fotos a selectedPhotos
        newFiles.forEach(file => {
            selectedPhotos.push(file);
            console.log(`Foto agregada: ${file.name} (${file.size} bytes)`);
        });
        
        console.log(`Total de fotos después de agregar: ${selectedPhotos.length}`);
        
        // Mostrar solo las nuevas fotos en el preview
        const startIndex = selectedPhotos.length - newFiles.length;
        newFiles.forEach((file, index) => {
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    const previewDiv = document.createElement('div');
                    previewDiv.className = 'relative group new-photo';
                    
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.className = 'w-full h-24 object-cover rounded-lg border border-gray-200';
                    img.alt = file.name;
                    
                    const removeBtn = document.createElement('button');
                    removeBtn.type = 'button';
                    removeBtn.className = 'absolute -top-2 -right-2 w-8 h-8 bg-red-500 hover:bg-red-600 text-white rounded-full shadow-lg transition-colors flex items-center justify-center';
                    removeBtn.innerHTML = '<i class="fas fa-times text-sm"></i>';
                    removeBtn.onclick = function() {
                        const photoIndex = startIndex + index;
                        console.log(`Eliminando foto en índice ${photoIndex}: ${file.name}`);
                        previewDiv.remove();
                        selectedPhotos.splice(photoIndex, 1);
                        console.log(`Total de fotos restantes: ${selectedPhotos.length}`);
                        
                        // Si no hay más fotos nuevas y no hay fotos existentes, ocultar el contenedor
                        const existingPhotos = previewContainer.querySelectorAll(':not(.new-photo)');
                        const newPhotos = previewContainer.querySelectorAll('.new-photo');
                        if (newPhotos.length === 0 && existingPhotos.length === 0) {
                            previewContainer.classList.add('hidden');
                        }
                    };
                    
                    previewDiv.appendChild(img);
                    previewDiv.appendChild(removeBtn);
                    previewContainer.appendChild(previewDiv);
                    console.log(`Preview creado para: ${file.name}`);
                };
                
                reader.readAsDataURL(file);
            }
        });
        
        // Limpiar el input para que pueda seleccionar más fotos
        input.value = '';
    }
}

// Función para abrir el modal de foto en tamaño completo
function openPhotoModal(button) {
    const photoUrl = button.getAttribute('data-photo-url');
    const photoCaption = button.getAttribute('data-photo-caption');
    
    document.getElementById('photoModalImage').src = '/media/' + photoUrl;
    document.getElementById('photoModal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closePhotoModal() {
    document.getElementById('photoModal').classList.add('hidden');
    document.getElementById('photoModalImage').src = '';
    document.body.style.overflow = 'auto';
}

// Función para eliminar una foto individual
function deleteEvidencePhoto(button) {
    const photoId = button.getAttribute('data-photo-id');
    const photoElement = button.parentElement;
    const isNewPhoto = photoElement.classList.contains('new-photo');
    
    console.log(`deleteEvidencePhoto llamado - photoId: ${photoId}, isNewPhoto: ${isNewPhoto}`);
    
    if (isNewPhoto) {
        // Si es una foto nueva, simplemente eliminar del DOM y del array
        photoElement.remove();
    } else {
        // Si es una foto existente, agregar a la lista de fotos a eliminar
        // Crear un campo oculto para el ID de la foto a eliminar
        const deletePhotosInput = document.createElement('input');
        deletePhotosInput.type = 'hidden';
        deletePhotosInput.name = 'delete_photos';
        deletePhotosInput.value = photoId;
        document.getElementById('evidenceForm').appendChild(deletePhotosInput);
        
        console.log(`Foto existente ${photoId} marcada para eliminar`);
        
        // Eliminar la foto del DOM
        photoElement.remove();
    }
}

// Función para navegar entre las fotos de una evidencia
function navigateEvidencePhotos(evidenceId, direction) {
    const container = document.getElementById(`evidence-photos-${evidenceId}`);
    if (!container) return;
    
    const photos = container.querySelectorAll('.evidence-photo');
    const totalPhotos = photos.length;
    const photosPerPage = 6;
    
    // Obtener la página actual del contenedor
    let currentPage = parseInt(container.getAttribute('data-current-page') || '0');
    
    // Calcular el número total de páginas
    const totalPages = Math.ceil(totalPhotos / photosPerPage);
    
    // Calcular la nueva página
    let newPage = currentPage + direction;
    newPage = Math.max(0, Math.min(newPage, totalPages - 1));
    
    // Actualizar la página actual en el contenedor
    container.setAttribute('data-current-page', newPage.toString());
    
    // Calcular el índice de inicio y fin
    const startIndex = newPage * photosPerPage;
    const endIndex = Math.min(startIndex + photosPerPage, totalPhotos);
    
    // Ocultar todas las fotos
    photos.forEach(function(photo, index) {
        if (index >= startIndex && index < endIndex) {
            photo.style.display = 'block';
        } else {
            photo.style.display = 'none';
        }
    });
    
    // Prevenir comportamiento por defecto de los botones
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
}

// Cerrar modal al hacer clic fuera del contenido
document.getElementById('evidenceModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeEvidenceModal();
    }
});

// Cerrar modal al hacer clic fuera del contenido
document.getElementById('photoModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closePhotoModal();
    }
});

// Función para abrir el modal de confirmación de eliminación de evidencia
function confirmDeleteEvidence(button) {
    const evidenceId = button.getAttribute('data-evidence-id');
    const projectId = document.getElementById('evidenceForm').action.match(/\/proyectos\/(\d+)\//)[1];
    
    // Configurar la acción del formulario de eliminación
    document.getElementById('deleteEvidenceForm').action = `/dashboard/proyectos/${projectId}/evidencias/${evidenceId}/eliminar/`;
    
    // Mostrar el modal
    document.getElementById('deleteEvidenceModal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

// Función para cerrar el modal de confirmación de eliminación de evidencia
function closeDeleteEvidenceModal() {
    document.getElementById('deleteEvidenceModal').classList.add('hidden');
    document.body.style.overflow = 'auto';
}

// Cerrar modal al hacer clic fuera del contenido
document.getElementById('evidenceModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeEvidenceModal();
    }
});

// Cerrar modal al hacer clic fuera del contenido
document.getElementById('photoModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closePhotoModal();
    }
});

// Cerrar modal al hacer clic fuera del contenido
document.getElementById('deleteEvidenceModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeDeleteEvidenceModal();
    }
});

// Cerrar modal con la tecla Escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeEvidenceModal();
        closePhotoModal();
        closeDeleteEvidenceModal();
    }
});

// Agregar depuración al submit del formulario de evidencia
document.addEventListener('DOMContentLoaded', function() {
    const evidenceForm = document.getElementById('evidenceForm');
    if (evidenceForm) {
        evidenceForm.addEventListener('submit', function(e) {
            console.log('=== SUBMIT DEL FORMULARIO DE EVIDENCIA ===');
            console.log('selectedPhotos.length:', selectedPhotos.length);
            
            // Verificar si es una creación o edición
            const evidenceId = document.getElementById('evidenceIdInput').value;
            const isEditing = !!evidenceId;
            console.log('Modo:', isEditing ? 'EDICIÓN' : 'CREACIÓN');
            console.log('Evidence ID:', evidenceId || '(nueva evidencia)');
            
            // Verificar las fotos en el preview
            const previewContainer = document.getElementById('evidencePhotosPreview');
            if (previewContainer) {
                const existingPhotos = previewContainer.querySelectorAll(':not(.new-photo)');
                const newPhotos = previewContainer.querySelectorAll('.new-photo');
                console.log('Fotos en el preview - Existentes:', existingPhotos.length, ', Nuevas:', newPhotos.length);
            }
            
            // Verificar las fotos marcadas para eliminar
            const deletePhotos = evidenceForm.querySelectorAll('input[name="delete_photos"]');
            console.log('Fotos marcadas para eliminar:', deletePhotos.length);
            deletePhotos.forEach(input => {
                console.log(`  - Foto ID: ${input.value}`);
            });
            
            // Si hay fotos nuevas en selectedPhotos, agregarlas al input antes de enviar
            const photoInput = document.getElementById('evidencePhotosInput');
            if (selectedPhotos.length > 0) {
                console.log(`Agregando ${selectedPhotos.length} fotos al input file antes de enviar:`);
                selectedPhotos.forEach((file, index) => {
                    console.log(`  ${index + 1}. ${file.name} (${file.size} bytes)`);
                });
                
                // Crear un nuevo FileList con todas las fotos seleccionadas
                const dt = new DataTransfer();
                selectedPhotos.forEach(function(file) {
                    dt.items.add(file);
                });
                photoInput.files = dt.files;
                console.log(`Fotos en el input después de asignar: ${photoInput.files.length}`);
            } else {
                console.log('No hay fotos nuevas para enviar');
            }
            
            console.log('=============================================');
        });
    }
});

// Inicializar las fotos de evidencias al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    // Para cada evidencia, configurar el grid de fotos dinámicamente
    document.querySelectorAll('[id^="evidence-photos-"]').forEach(function(container) {
        const photos = container.querySelectorAll('.evidence-photo');
        const totalPhotos = photos.length;
        
        console.log(`Configurando evidencia ${container.id.replace('evidence-photos-', '')} con ${totalPhotos} fotos`);
        
        // Calcular el número óptimo de columnas basado en la cantidad de fotos
        let columns = 1;
        if (totalPhotos === 1) {
            columns = 1;
        } else if (totalPhotos === 2) {
            columns = 2;
        } else if (totalPhotos >= 3 && totalPhotos <= 4) {
            columns = 2;
        } else if (totalPhotos >= 5) {
            columns = 3;
        }
        
        // Aplicar las columnas al grid
        container.classList.remove('grid-cols-1', 'grid-cols-2', 'grid-cols-3', 'md:grid-cols-1', 'md:grid-cols-2', 'md:grid-cols-3');
        container.classList.add('grid-cols-' + columns, 'md:grid-cols-' + columns);
        
        // Ocultar botones de navegación si hay menos de 7 fotos
        const parent = container.parentElement;
        const navButtons = parent.querySelectorAll('button');
        if (totalPhotos < 7) {
            navButtons.forEach(function(btn) {
                btn.style.display = 'none';
            });
        } else {
            navButtons.forEach(function(btn) {
                btn.style.display = 'flex';
            });
            
            // Inicializar la página actual en 0
            container.setAttribute('data-current-page', '0');
            
            // Mostrar solo las primeras 6 fotos
            const photosPerPage = 6;
            photos.forEach(function(photo, index) {
                if (index < photosPerPage) {
                    photo.style.display = 'block';
                } else {
                    photo.style.display = 'none';
                }
            });
        }
        
        console.log(`  - Columnas: ${columns}`);
        console.log(`  - Botones navegación: ${navButtons.length > 0 ? 'mostrados' : 'ocultos'}`);
    });
});
