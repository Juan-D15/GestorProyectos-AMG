// Funciones para el modal de evidencias

// Variable global para almacenar las fotos seleccionadas
let selectedPhotos = [];

// Función para abrir el modal de selección de beneficiarios
function openBeneficiariesModal() {
    console.log('=== Abriendo modal de selección de beneficiarios para evidencia ===');
    
    const modal = document.getElementById('beneficiariesModal');
    if (modal) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';

        // Obtener los IDs de beneficiarios ya seleccionados
        const beneficiariesInput = document.getElementById('evidenceBeneficiariesInput');
        const existingBeneficiaries = beneficiariesInput.value ? beneficiariesInput.value.split(',').map(id => id.trim()).filter(id => id !== '') : [];
        selectedBeneficiaryIds = [...existingBeneficiaries];

        console.log('Beneficiarios ya seleccionados:', existingBeneficiaries);

        // Marcar los checkboxes según los beneficiarios seleccionados
        const items = document.querySelectorAll('.beneficiary-item');
        items.forEach(function(item) {
            const id = item.dataset.id;
            const checkbox = item.querySelector('input[type="checkbox"]');

            if (checkbox) {
                checkbox.checked = selectedBeneficiaryIds.includes(id);
            }
        });

        updateSelectedBeneficiariesCount();
    }
}

// Función para cerrar el modal de selección de beneficiarios
function closeBeneficiariesModal() {
    console.log('Cerrando modal de selección de beneficiarios para evidencia');
    const modal = document.getElementById('beneficiariesModal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = 'auto';
    }
}

// Función para actualizar el contador de beneficiarios seleccionados
function updateSelectedBeneficiariesCount() {
    const checkboxes = document.querySelectorAll('.beneficiary-item input[type="checkbox"]:checked');
    const count = checkboxes.length;
    const countElement = document.getElementById('selectedBeneficiariesCount');
    const badgeElement = document.getElementById('selectedBeneficiariesBadge');

    if (countElement) {
        countElement.textContent = count;
    }

    if (badgeElement) {
        if (count > 0) {
            badgeElement.textContent = count + ' seleccionados';
            badgeElement.classList.remove('hidden');
        } else {
            badgeElement.classList.add('hidden');
        }
    }
}

// Función para confirmar la selección de beneficiarios
function confirmBeneficiariesSelection() {
    console.log('=== Confirmando selección de beneficiarios para evidencia ===');

    const checkboxes = document.querySelectorAll('.beneficiary-item input[type="checkbox"]:checked');
    const selectedIds = Array.from(checkboxes).map(cb => cb.closest('.beneficiary-item').dataset.id);

    console.log('Beneficiarios seleccionados:', selectedIds);

    // Actualizar el input oculto con los IDs seleccionados
    const beneficiariesInput = document.getElementById('evidenceBeneficiariesInput');
    if (beneficiariesInput) {
        beneficiariesInput.value = selectedIds.join(',');
    }

    // Actualizar el badge en el botón
    const badgeElement = document.getElementById('selectedBeneficiariesBadge');
    if (badgeElement) {
        if (selectedIds.length > 0) {
            badgeElement.textContent = selectedIds.length + ' seleccionados';
            badgeElement.classList.remove('hidden');
        } else {
            badgeElement.classList.add('hidden');
        }
    }

    updateSelectedBeneficiariesCount();
    closeBeneficiariesModal();
}

// Función para filtrar beneficiarios (usa el input correcto según el contexto)
function filterBeneficiaries() {
    const searchInputProject = document.getElementById('beneficiarySearchInput');
    const searchInputPhase = document.getElementById('phaseEvidenceBeneficiariesSearch');
    
    if (searchInputProject) {
        filterBeneficiariesInList(searchInputProject, '.beneficiary-item');
    } else if (searchInputPhase) {
        filterBeneficiariesInList(searchInputPhase, '.phase-evidence-beneficiary-item');
    }
}

function filterBeneficiariesInList(searchInput, itemSelector) {
    const searchTerm = searchInput.value.toLowerCase();
    const items = document.querySelectorAll(itemSelector);

    items.forEach(item => {
        const name = item.dataset.name ? item.dataset.name.toLowerCase() : '';
        const dpi = item.dataset.dpi ? item.dataset.dpi.toLowerCase() : '';
        const community = item.dataset.community ? item.dataset.community.toLowerCase() : '';

        if (name.includes(searchTerm) || dpi.includes(searchTerm) || community.includes(searchTerm)) {
            item.style.display = 'flex';
        } else {
            item.style.display = 'none';
        }
    });
}

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
    
    // Limpiar el estado de beneficiarios
    const beneficiariesInput = document.getElementById('evidenceBeneficiariesInput');
    if (beneficiariesInput) {
        beneficiariesInput.value = '';
    }
    
    // Ocultar el badge de beneficiarios seleccionados
    const badgeElement = document.getElementById('selectedBeneficiariesBadge');
    if (badgeElement) {
        badgeElement.classList.add('hidden');
    }
    
    // Ocultar el contenedor de lista de beneficiarios seleccionados
    const container = document.getElementById('selectedBeneficiariesContainer');
    if (container) {
        container.classList.add('hidden');
    }
    
    // Limpiar la lista de beneficiarios seleccionados
    const list = document.getElementById('selectedBeneficiariesList');
    if (list) {
        list.innerHTML = '<p class="text-sm text-gray-500">No hay beneficiarios seleccionados</p>';
    }
    
    // Resetear la variable global de beneficiarios seleccionados
    if (typeof selectedBeneficiaryIds !== 'undefined') {
        selectedBeneficiaryIds = [];
    }
    
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
    
    // Cargar los beneficiarios existentes de la evidencia
    loadExistingBeneficiaries(evidenceId);
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
    
    // Limpiar el estado de beneficiarios
    const beneficiariesInput = document.getElementById('evidenceBeneficiariesInput');
    if (beneficiariesInput) {
        beneficiariesInput.value = '';
    }
    
    // Ocultar el badge de beneficiarios seleccionados
    const badgeElement = document.getElementById('selectedBeneficiariesBadge');
    if (badgeElement) {
        badgeElement.classList.add('hidden');
    }
    
    // Ocultar el contenedor de lista de beneficiarios seleccionados
    const container = document.getElementById('selectedBeneficiariesContainer');
    if (container) {
        container.classList.add('hidden');
    }
    
    // Limpiar la lista de beneficiarios seleccionados
    const list = document.getElementById('selectedBeneficiariesList');
    if (list) {
        list.innerHTML = '<p class="text-sm text-gray-500">No hay beneficiarios seleccionados</p>';
    }
    
    // Resetear la variable global de beneficiarios seleccionados
    if (typeof selectedBeneficiaryIds !== 'undefined') {
        selectedBeneficiaryIds = [];
    }
    
    console.log('Modal cerrado y estado limpiado');
}

// Función para abrir el modal de detalles de evidencia
function openEvidenceDetailsModal(button) {
    const evidenceId = button.getAttribute('data-evidence-id');
    const startDate = button.getAttribute('data-start-date');
    const endDate = button.getAttribute('data-end-date');
    const description = button.getAttribute('data-description');
    
    console.log(`Abriendo modal de detalles para evidencia ${evidenceId}`);
    
    // Llenar los datos básicos
    document.getElementById('evidenceDetailStartDate').textContent = formatEvidenceDate(startDate);
    document.getElementById('evidenceDetailEndDate').textContent = formatEvidenceDate(endDate);
    document.getElementById('evidenceDetailDescription').textContent = description;
    
    // Limpiar contenedores
    const photosContainer = document.getElementById('evidenceDetailPhotos');
    const beneficiariesContainer = document.getElementById('evidenceDetailBeneficiaries');
    photosContainer.innerHTML = '';
    beneficiariesContainer.innerHTML = '';
    
    // Cargar fotos de la evidencia
    loadEvidenceDetailsPhotos(evidenceId);
    
    // Cargar beneficiarios de la evidencia
    loadEvidenceDetailsBeneficiaries(evidenceId);
    
    // Mostrar el modal
    document.getElementById('evidenceDetailsModal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

// Función para cerrar el modal de detalles de evidencia
function closeEvidenceDetailsModal() {
    console.log('Cerrando modal de detalles de evidencia');
    document.getElementById('evidenceDetailsModal').classList.add('hidden');
    document.body.style.overflow = 'auto';
}

// Función para cargar las fotos de los detalles de evidencia
function loadEvidenceDetailsPhotos(evidenceId) {
    const projectId = document.getElementById('evidenceForm').action.match(/\/proyectos\/(\d+)\//)[1];
    const photosContainer = document.getElementById('evidenceDetailPhotos');
    const photosSection = document.getElementById('evidenceDetailPhotosContainer');
    
    console.log(`Cargando fotos para detalles de evidencia ${evidenceId}...`);
    
    fetch(`/dashboard/proyectos/${projectId}/evidencias/${evidenceId}/fotos/`)
        .then(response => response.json())
        .then(data => {
            if (data.photos && data.photos.length > 0) {
                photosSection.classList.remove('hidden');
                
                data.photos.forEach(photo => {
                    const photoDiv = document.createElement('div');
                    photoDiv.className = 'relative group';
                    
                    const img = document.createElement('img');
                    img.src = '/media/' + photo.photo_url;
                    img.className = 'w-full h-32 object-cover rounded-lg border border-gray-200 cursor-pointer hover:opacity-80 transition-opacity';
                    img.alt = photo.caption || 'Foto de evidencia';
                    img.onclick = function() {
                        document.getElementById('photoModalImage').src = '/media/' + photo.photo_url;
                        document.getElementById('photoModal').classList.remove('hidden');
                        document.body.style.overflow = 'hidden';
                    };
                    
                    photoDiv.appendChild(img);
                    photosContainer.appendChild(photoDiv);
                });
                
                console.log(`Se mostraron ${data.photos.length} fotos en los detalles`);
            } else {
                photosSection.classList.add('hidden');
            }
        })
        .catch(error => {
            console.error('Error al cargar fotos de detalles:', error);
            photosSection.classList.add('hidden');
        });
}

// Función para cargar los beneficiarios de los detalles de evidencia
function loadEvidenceDetailsBeneficiaries(evidenceId) {
    const projectId = document.getElementById('evidenceForm').action.match(/\/proyectos\/(\d+)\//)[1];
    const beneficiariesContainer = document.getElementById('evidenceDetailBeneficiaries');
    const beneficiariesSection = document.getElementById('evidenceDetailBeneficiariesContainer');
    
    console.log(`=== Cargando beneficiarios para detalles de evidencia ${evidenceId} ===`);
    console.log(`Project ID: ${projectId}`);
    console.log(`Evidence ID: ${evidenceId}`);
    console.log(`URL: /dashboard/proyectos/${projectId}/evidencias/${evidenceId}/beneficiarios/`);
    
    // Limpiar contenedor antes de cargar
    beneficiariesContainer.innerHTML = '';
    
    fetch(`/dashboard/proyectos/${projectId}/evidencias/${evidenceId}/beneficiarios/`)
        .then(response => {
            console.log(`Response status: ${response.status}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Datos recibidos:', data);
            
            if (data.beneficiaries && data.beneficiaries.length > 0) {
                console.log('Procesando beneficiarios para mostrar...');
                beneficiariesSection.classList.remove('hidden');
                
                data.beneficiaries.forEach((beneficiary, index) => {
                    console.log(`Procesando beneficiario ${index + 1}:`, beneficiary);
                    
                    const beneficiaryDiv = document.createElement('div');
                    beneficiaryDiv.className = 'flex items-center justify-between bg-white rounded-lg p-3 border border-gray-200';
                    
                    let initials = '';
                    if (beneficiary.first_name) {
                        initials += beneficiary.first_name[0];
                    }
                    if (beneficiary.last_name) {
                        initials += beneficiary.last_name[0];
                    }
                    
                    console.log(`Iniciales: ${initials}`);
                    
                    beneficiaryDiv.innerHTML = `
                        <div class="flex items-center space-x-3">
                            <div class="w-10 h-10 rounded-full bg-gradient-to-br from-[#8a4534] to-[#334e76] flex items-center justify-center text-white text-sm font-semibold">
                                <span>${initials}</span>
                            </div>
                            <div>
                                <p class="font-medium text-gray-900">${beneficiary.first_name} ${beneficiary.last_name}</p>
                                <p class="text-xs text-gray-500">
                                    ${beneficiary.cui_dpi ? 'DPI: ' + beneficiary.cui_dpi : 'Sin DPI'}
                                    ${beneficiary.community ? ' • ' + beneficiary.community : ''}
                                </p>
                            </div>
                        </div>
                    `;
                    
                    beneficiariesContainer.appendChild(beneficiaryDiv);
                });
                
                console.log(`Se mostraron ${data.beneficiaries.length} beneficiarios en los detalles`);
            } else {
                console.log('No hay beneficiarios asociados a esta evidencia');
                beneficiariesSection.classList.add('hidden');
            }
        })
        .catch(error => {
            console.error('Error al cargar beneficiarios de detalles:', error);
            beneficiariesSection.classList.add('hidden');
        });
}

// Cerrar modal de detalles al hacer clic fuera del contenido
document.getElementById('evidenceDetailsModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeEvidenceDetailsModal();
    }
});

// Cerrar modal de detalles con la tecla Escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeEvidenceDetailsModal();
    }
});

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

// Función para cargar los beneficiarios existentes de una evidencia
function loadExistingBeneficiaries(evidenceId) {
    // Hacer una petición AJAX para obtener los beneficiarios existentes
    const projectId = document.getElementById('evidenceForm').action.match(/\/proyectos\/(\d+)\//)[1];
    
    console.log(`=== Cargando beneficiarios existentes para evidencia ${evidenceId} ===`);
    console.log(`URL: /dashboard/proyectos/${projectId}/evidencias/${evidenceId}/beneficiarios/`);
    
    fetch(`/dashboard/proyectos/${projectId}/evidencias/${evidenceId}/beneficiarios/`)
        .then(response => {
            console.log('Response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Beneficiarios recibidos del servidor:', data.beneficiaries);
            
            if (data.beneficiaries && data.beneficiaries.length > 0) {
                // Actualizar el input oculto con los IDs de los beneficiarios
                const beneficiariesInput = document.getElementById('evidenceBeneficiariesInput');
                
                if (!beneficiariesInput) {
                    console.error('No se encontró el input de beneficiarios');
                    return;
                }
                
                const beneficiaryIds = data.beneficiaries.map(b => b.id);
                beneficiariesInput.value = beneficiaryIds.join(',');
                
                console.log(`Input de beneficiarios actualizado: ${beneficiariesInput.value}`);
                
                // Actualizar el badge en el botón
                const badgeElement = document.getElementById('selectedBeneficiariesBadge');
                if (badgeElement) {
                    badgeElement.textContent = `${beneficiaryIds.length} seleccionados`;
                    badgeElement.classList.remove('hidden');
                    console.log(`Badge actualizado: ${badgeElement.textContent}`);
                }
                
                // Actualizar la variable global de beneficiarios seleccionados
                if (typeof selectedBeneficiaryIds !== 'undefined') {
                    selectedBeneficiaryIds = [...beneficiaryIds];
                    console.log(`Variable global selectedBeneficiaryIds actualizada:`, selectedBeneficiaryIds);
                }
                
                // Actualizar la lista visual de beneficiarios seleccionados
                if (typeof updateSelectedBeneficiariesList === 'function') {
                    console.log('Llamando a updateSelectedBeneficiariesList()');
                    updateSelectedBeneficiariesList();
                } else {
                    console.error('La función updateSelectedBeneficiariesList no está definida');
                }
                
                console.log(`=== Beneficiarios cargados: ${beneficiaryIds.length} ===`);
            } else {
                console.log('No hay beneficiarios asignados a esta evidencia');
                // Limpiar el input y ocultar la lista
                const beneficiariesInput = document.getElementById('evidenceBeneficiariesInput');
                if (beneficiariesInput) {
                    beneficiariesInput.value = '';
                }
                
                const badgeElement = document.getElementById('selectedBeneficiariesBadge');
                if (badgeElement) {
                    badgeElement.classList.add('hidden');
                }
                
                const container = document.getElementById('selectedBeneficiariesContainer');
                if (container) {
                    container.classList.add('hidden');
                }
            }
        })
        .catch(error => {
            console.error('Error al cargar beneficiarios existentes:', error);
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
        // Verificar si estamos en el formulario de evidencia (modal)
        const evidenceForm = document.getElementById('evidenceForm');
        const previewContainer = document.getElementById('evidencePhotosPreview');
        
        // SOLO procesar si estamos en el modal de evidencia con ID 'evidenceForm'
        if (evidenceForm && evidenceForm.id === 'evidenceForm' && previewContainer) {
            // Si es una foto existente, agregar a la lista de fotos a eliminar
            // Crear un campo oculto para el ID de la foto a eliminar
            const deletePhotosInput = document.createElement('input');
            deletePhotosInput.type = 'hidden';
            deletePhotosInput.name = 'photos_to_delete'; // Corregido: usar el nombre correcto que espera el backend
            deletePhotosInput.value = photoId;
            evidenceForm.appendChild(deletePhotosInput);
            
            console.log(`Foto existente ${photoId} marcada para eliminar`);
            
            // Eliminar la foto del DOM
            photoElement.remove();
        } else {
            console.log('deleteEvidencePhoto ignorado: no estamos en el modal de evidencia correcto');
        }
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

// Manejar el envío del formulario de eliminación de evidencia
document.addEventListener('DOMContentLoaded', function() {
    const deleteEvidenceForm = document.getElementById('deleteEvidenceForm');
    if (deleteEvidenceForm) {
        deleteEvidenceForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const actionUrl = this.action;
            
            fetch(actionUrl, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    closeDeleteEvidenceModal();
                    location.reload();
                } else {
                    alert(data.message || 'Error al eliminar la evidencia');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al procesar la solicitud');
            });
        });
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
            
            // SOLO si es el formulario de evidencia con ID 'evidenceForm'
            // Si hay fotos nuevas en selectedPhotos, agregarlas al input antes de enviar
            if (evidenceForm.id === 'evidenceForm') {
                const photoInput = document.getElementById('evidencePhotosInput');
                if (selectedPhotos.length > 0 && photoInput) {
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

// Logs de depuración para el formulario de edición de evidencia
document.addEventListener('DOMContentLoaded', function() {
    console.log('=== Página de edición de evidencia cargada ===');
    
    const form = document.querySelector('form[action*="evidencias"][action*="editar"]');
    if (form) {
        console.log('Formulario encontrado:', form);
        console.log('Form ID:', form.id);
        
        // Monitorear cambios en el input de archivos
        const newPhotosInput = document.getElementById('newPhotosInput');
        if (newPhotosInput) {
            newPhotosInput.addEventListener('change', function() {
                console.log('=== Cambio en input de fotos ===');
                console.log('Archivos seleccionados:', this.files.length);
                Array.from(this.files).forEach((file, index) => {
                    console.log(`  ${index + 1}. ${file.name} (${file.size} bytes, ${file.type})`);
                });
            });
        }
        
        form.addEventListener('submit', function(e) {
            console.log('=== SUBMIT DEL FORMULARIO DE EDICIÓN ===');
            console.log('Form action:', form.action);
            console.log('Form method:', form.method);
            console.log('Form enctype:', form.enctype);
            
            // Verificar fotos a eliminar
            const photosToDelete = form.querySelectorAll('input[name="photos_to_delete"]');
            console.log('Fotos marcadas para eliminar (photos_to_delete):', photosToDelete.length);
            photosToDelete.forEach(input => {
                console.log(`  - Foto ID: ${input.value}, checked: ${input.checked}`);
            });
            
            // Verificar nuevas fotos
            const newPhotosInput = document.getElementById('newPhotosInput');
            console.log('Input de nuevas fotos encontrado:', !!newPhotosInput);
            if (newPhotosInput) {
                console.log('Nuevas fotos seleccionadas:', newPhotosInput.files.length);
                Array.from(newPhotosInput.files).forEach((file, index) => {
                    console.log(`  ${index + 1}. ${file.name} (${file.size} bytes, ${file.type})`);
                });
            }
            
            // Verificar beneficiarios
            const beneficiariesInputs = form.querySelectorAll('input[name="beneficiaries"]');
            console.log('Beneficiarios seleccionados:', beneficiariesInputs.length);
            beneficiariesInputs.forEach(input => {
                console.log(`  - Beneficiario ID: ${input.value}, checked: ${input.checked}`);
            });
            
            // Listar todos los inputs del formulario
            const allInputs = form.querySelectorAll('input');
            console.log('Total de inputs en el formulario:', allInputs.length);
            allInputs.forEach(input => {
                if (input.type !== 'submit' && input.type !== 'button') {
                    console.log(`  - type="${input.type}", name="${input.name}", value="${input.value}"`);
                }
            });
        });
    } else {
        console.log('ERROR: Formulario de edición no encontrado');
    }
});

function previewNewPhotos(input) {
    const previewContainer = document.getElementById('newPhotosPreview');
    previewContainer.innerHTML = '';
    
    if (input.files.length > 0) {
        previewContainer.classList.remove('hidden');
        console.log('=== Previsualizando fotos ===');
        console.log('Cantidad de fotos:', input.files.length);
        Array.from(input.files).forEach((file, index) => {
            console.log(`  Foto ${index + 1}: ${file.name} (${file.size} bytes)`);
            const reader = new FileReader();
            reader.onload = function(e) {
                const preview = document.createElement('div');
                preview.className = 'relative';
                
                const img = document.createElement('img');
                img.src = e.target.result;
                img.alt = 'Previsualización';
                img.className = 'w-full h-24 object-cover rounded-lg border border-gray-200';
                
                const label = document.createElement('label');
                label.htmlFor = `photo_delete_${index}`;
                label.className = 'absolute -top-2 -right-2 cursor-pointer w-6 h-6 bg-red-500 rounded-full flex items-center justify-center text-white opacity-0 hover:opacity-100 transition-opacity';
                label.innerHTML = '<i class="fas fa-times text-xs"></i>';
                
                preview.appendChild(img);
                preview.appendChild(label);
                previewContainer.appendChild(preview);
            };
             reader.readAsDataURL(file);
        });
    }
}

// Event listener para el input de búsqueda de beneficiarios (modal de proyectos)
document.getElementById('beneficiarySearchInput')?.addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const items = document.querySelectorAll('.beneficiary-item');

    items.forEach(item => {
        const name = item.dataset.name ? item.dataset.name.toLowerCase() : '';
        const dpi = item.dataset.dpi ? item.dataset.dpi.toLowerCase() : '';
        const community = item.dataset.community ? item.dataset.community.toLowerCase() : '';

        if (name.includes(searchTerm) || dpi.includes(searchTerm) || community.includes(searchTerm)) {
            item.style.display = 'flex';
        } else {
            item.style.display = 'none';
        }
    });
});

// Event listener para el input de búsqueda de beneficiarios (modal de fases)
document.getElementById('phaseEvidenceBeneficiariesSearch')?.addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const items = document.querySelectorAll('.phase-evidence-beneficiary-item');

    items.forEach(item => {
        const name = item.dataset.name ? item.dataset.name.toLowerCase() : '';
        const dpi = item.dataset.dpi ? item.dataset.dpi.toLowerCase() : '';
        const community = item.dataset.community ? item.dataset.community.toLowerCase() : '';

        if (name.includes(searchTerm) || dpi.includes(searchTerm) || community.includes(searchTerm)) {
            item.style.display = 'flex';
        } else {
            item.style.display = 'none';
        }
    });
});

// Event listeners para cerrar modales al hacer clic fuera
document.getElementById('beneficiariesModal')?.addEventListener('click', function(e) {
    if (e.target === this) closeBeneficiariesModal();
});

document.getElementById('phaseEvidenceBeneficiariesModal')?.addEventListener('click', function(e) {
    if (e.target === this) closePhaseEvidenceBeneficiariesModal();
});

// Cerrar modales con Escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeEvidenceModal();
        closePhotoModal();
        closeDeleteEvidenceModal();
        closeBeneficiariesModal();
        closePhaseEvidenceBeneficiariesModal();
    }
});

// =====================================================
// FUNCIONES PARA FILTRAR EVIDENCIAS DE PROYECTO
// =====================================================

// Event listener para limpiar caracteres no numéricos en el campo de año
document.addEventListener('DOMContentLoaded', function() {
    const yearInput = document.getElementById('projectEvidenceFilterYear');
    if (yearInput) {
        yearInput.addEventListener('input', function(e) {
            // Solo permitir números
            this.value = this.value.replace(/[^0-9]/g, '');
        });
    }
});

function applyProjectEvidenceFilters() {
    console.log('=== Aplicando filtros de evidencias de proyecto ===');

    const filterYear = document.getElementById('projectEvidenceFilterYear');
    const filterStartDate = document.getElementById('projectEvidenceFilterStartDate');
    const filterEndDate = document.getElementById('projectEvidenceFilterEndDate');

    if (!filterYear && !filterStartDate && !filterEndDate) {
        console.log('No hay filtros aplicados');
        return;
    }

    const year = filterYear ? filterYear.value : '';
    const startDate = filterStartDate ? filterStartDate.value : '';
    const endDate = filterEndDate ? filterEndDate.value : '';

    console.log('Filtros aplicados:', { year, startDate, endDate });

    const evidenceCards = document.querySelectorAll('.evidence-card');
    let visibleCount = 0;
    let totalCount = 0;

    evidenceCards.forEach(card => {
        totalCount++;

        const cardStartDate = card.dataset.startDate;
        const cardEndDate = card.dataset.endDate;
        const cardStartYear = card.dataset.startYear;
        const cardEndYear = card.dataset.endYear;

        let isVisible = true;

        if (year && isVisible) {
            if (cardStartYear !== year && cardEndYear !== year) {
                isVisible = false;
            }
        }

        if (isVisible && startDate) {
            if (cardEndDate < startDate) {
                isVisible = false;
            }
        }

        if (isVisible && endDate) {
            if (cardStartDate > endDate) {
                isVisible = false;
            }
        }

        if (isVisible) {
            card.style.display = 'block';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });

    console.log(`Evidencias visibles: ${visibleCount} de ${totalCount}`);

    const evidencesList = document.getElementById('projectEvidencesList');
    const noResultsMsg = document.getElementById('projectEvidenceNoResults');

    if (visibleCount === 0) {
        if (!noResultsMsg) {
            const messageDiv = document.createElement('div');
            messageDiv.id = 'projectEvidenceNoResults';
            messageDiv.className = 'text-center py-8';
            messageDiv.innerHTML = `
                <i class="fas fa-search text-4xl text-gray-300 mb-4"></i>
                <p class="text-gray-500">No se encontraron evidencias con los filtros seleccionados.</p>
            `;
            evidencesList.appendChild(messageDiv);
        }
    } else {
        if (noResultsMsg) {
            noResultsMsg.remove();
        }
    }
}

function clearProjectEvidenceFilters() {
    console.log('=== Limpiando filtros de evidencias de proyecto ===');

    const filterYear = document.getElementById('projectEvidenceFilterYear');
    const filterStartDate = document.getElementById('projectEvidenceFilterStartDate');
    const filterEndDate = document.getElementById('projectEvidenceFilterEndDate');

    if (filterYear) filterYear.value = '';
    if (filterStartDate) filterStartDate.value = '';
    if (filterEndDate) filterEndDate.value = '';

    const evidenceCards = document.querySelectorAll('.evidence-card');
    evidenceCards.forEach(card => {
        card.style.display = 'block';
    });

    const noResultsMsg = document.getElementById('projectEvidenceNoResults');
    if (noResultsMsg) {
        noResultsMsg.remove();
    }

    console.log('Filtros limpiados');
}

// =====================================================
// FUNIONES PARA MARCAR FOTOS PARA ELIMINAR (EDICIÓN)
// =====================================================

function togglePhotoDelete(checkbox) {
    const photoCard = checkbox.closest('.photo-card');
    const img = photoCard.querySelector('img');
    
    if (checkbox.checked) {
        // Marcar con borde rojo y opacidad reducida
        img.classList.remove('border-gray-200');
        img.classList.add('border-red-500', 'opacity-50');
        photoCard.classList.add('border-red-500', 'border-4');
    } else {
        // Restaurar estado original
        img.classList.remove('border-red-500', 'opacity-50');
        img.classList.add('border-gray-200');
        photoCard.classList.remove('border-red-500', 'border-4');
    }
}
