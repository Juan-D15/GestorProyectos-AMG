// Funciones para gestión de fases y evidencias de fases

// Variables globales
let selectedPhaseBeneficiaries = [];

// =====================================================
// FUNCIONES PARA GESTIÓN DE FASES
// =====================================================

// Modal para crear fase
function openPhaseModal() {
    console.log('Abriendo modal para crear fase');
    document.getElementById('phaseModal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closePhaseModal() {
    console.log('Cerrando modal para crear fase');
    document.getElementById('phaseModal').classList.add('hidden');
    document.body.style.overflow = 'auto';
    document.getElementById('phaseForm').reset();
    document.getElementById('phaseBeneficiariesInput').value = '';
    document.getElementById('selectedPhaseBeneficiariesBadge').classList.add('hidden');
    selectedPhaseBeneficiaries = [];
}

// Modal para editar fase
function openEditPhaseModal(button) {
    const phaseId = button.dataset.phaseId;
    const phaseName = button.dataset.phaseName;
    const description = button.dataset.description;
    const startDate = button.dataset.startDate;
    const endDate = button.dataset.endDate;
    const status = button.dataset.status;
    const beneficiaries = button.dataset.beneficiaries;

    console.log('Abriendo modal para editar fase:', {
        phaseId,
        phaseName,
        beneficiaries,
        beneficiariesType: typeof beneficiaries
    });

    document.getElementById('editPhaseId').value = phaseId;
    document.getElementById('editPhaseName').value = phaseName;
    document.getElementById('editPhaseDescription').value = description;
    document.getElementById('editPhaseStartDate').value = startDate;
    document.getElementById('editPhaseEndDate').value = endDate;
    document.getElementById('editPhaseStatus').value = status;

    const projectId = button.dataset.projectId;
    document.getElementById('editPhaseForm').action = `/dashboard/proyectos/${projectId}/fases/${phaseId}/editar/`;

    // Guardar los beneficiarios seleccionados
    selectedPhaseBeneficiaries = beneficiaries ? beneficiaries.split(',') : [];
    
    // Actualizar el input oculto y el badge para edición
    const beneficiariesInputEdit = document.getElementById('phaseBeneficiariesInputEdit');
    if (beneficiariesInputEdit) {
        beneficiariesInputEdit.value = selectedPhaseBeneficiaries.join(',');
    }
    
    // Actualizar el badge con el número de beneficiarios
    const badgeElement = document.getElementById('selectedPhaseBeneficiariesBadgeEdit');
    if (badgeElement) {
        if (selectedPhaseBeneficiaries.length > 0) {
            badgeElement.textContent = selectedPhaseBeneficiaries.length + ' seleccionados';
            badgeElement.classList.remove('hidden');
        } else {
            badgeElement.classList.add('hidden');
        }
    }
    
    console.log('Beneficiarios cargados para editar:', selectedPhaseBeneficiaries);

    document.getElementById('editPhaseModal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeEditPhaseModal() {
    console.log('Cerrando modal para editar fase');
    document.getElementById('editPhaseModal').classList.add('hidden');
    document.body.style.overflow = 'auto';
    document.getElementById('editPhaseForm').reset();
    
    const beneficiariesInputEdit = document.getElementById('phaseBeneficiariesInputEdit');
    if (beneficiariesInputEdit) {
        beneficiariesInputEdit.value = '';
    }
    
    const badgeElement = document.getElementById('selectedPhaseBeneficiariesBadgeEdit');
    if (badgeElement) {
        badgeElement.classList.add('hidden');
    }
    
    selectedPhaseBeneficiaries = [];
}

// Modal de beneficiarios para fase (crear y editar)
function openPhaseBeneficiariesModal() {
    console.log('Abriendo modal de beneficiarios para fase');
    
    // Detectar si estamos en modo edición o creación ANTES de hacer cambios
    const editModal = document.getElementById('editPhaseModal');
    const createModal = document.getElementById('phaseModal');
    const isEditMode = editModal && !editModal.classList.contains('hidden');
    const isCreateMode = createModal && !createModal.classList.contains('hidden');
    
    console.log('Modo:', isEditMode ? 'EDICIÓN' : (isCreateMode ? 'CREACIÓN' : 'DESCONOCIDO'));
    console.log('selectedPhaseBeneficiaries:', selectedPhaseBeneficiaries);
    
    document.getElementById('phaseBeneficiariesModal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    
    // Marcar los checkboxes según el modo actual
    const checkboxes = document.querySelectorAll('.phase-beneficiary-item input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        const beneficiaryId = checkbox.closest('.phase-beneficiary-item').dataset.id;
        
        if (isEditMode) {
            // Modo edición: usar selectedPhaseBeneficiaries
            console.log(`Checkbox ${beneficiaryId}: ${selectedPhaseBeneficiaries.includes(beneficiaryId) ? 'marcado' : 'desmarcado'} (modo edición)`);
            checkbox.checked = selectedPhaseBeneficiaries.includes(beneficiaryId);
        } else if (isCreateMode) {
            // Modo creación: usar el valor del input de creación
            const currentValue = document.getElementById('phaseBeneficiariesInput').value;
            const currentIds = currentValue ? currentValue.split(',') : [];
            checkbox.checked = currentIds.includes(beneficiaryId);
        }
    });

    updatePhaseBeneficiariesCount();
}

function closePhaseBeneficiariesModal() {
    console.log('Cerrando modal de beneficiarios para fase');
    document.getElementById('phaseBeneficiariesModal').classList.add('hidden');
    document.body.style.overflow = 'auto';
}

function updatePhaseBeneficiariesCount() {
    const checkboxes = document.querySelectorAll('.phase-beneficiary-item input[type="checkbox"]:checked');
    const count = checkboxes.length;
    const countElement = document.getElementById('selectedPhaseBeneficiariesCount');
    
    // Detectar si estamos en modo edición o creación
    const editModal = document.getElementById('editPhaseModal');
    const isEditMode = editModal && !editModal.classList.contains('hidden');
    
    if (countElement) {
        countElement.textContent = count;
    }
    
    if (isEditMode) {
        // Modo edición: actualizar badge de edición
        const badgeElement = document.getElementById('selectedPhaseBeneficiariesBadgeEdit');
        if (badgeElement) {
            if (count > 0) {
                badgeElement.textContent = count + ' seleccionados';
                badgeElement.classList.remove('hidden');
            } else {
                badgeElement.classList.add('hidden');
            }
        }
    } else {
        // Modo creación: actualizar badge de creación
        const badgeElement = document.getElementById('selectedPhaseBeneficiariesBadge');
        if (badgeElement) {
            if (count > 0) {
                badgeElement.textContent = count + ' seleccionados';
                badgeElement.classList.remove('hidden');
            } else {
                badgeElement.classList.add('hidden');
            }
        }
    }
}

function confirmPhaseBeneficiariesSelection() {
    const checkboxes = document.querySelectorAll('.phase-beneficiary-item input[type="checkbox"]:checked');
    const selectedIds = Array.from(checkboxes).map(cb => cb.closest('.phase-beneficiary-item').dataset.id);

    console.log('Guardando beneficiarios seleccionados para fase:', selectedIds);

    // Detectar si estamos en modo edición o creación
    const editModal = document.getElementById('editPhaseModal');
    const createModal = document.getElementById('phaseModal');
    const isEditMode = editModal && !editModal.classList.contains('hidden');
    const isCreateMode = createModal && !createModal.classList.contains('hidden');

    // Actualizar la variable global
    selectedPhaseBeneficiaries = selectedIds;

    if (isEditMode) {
        // Modo edición: guardar en phaseBeneficiariesInputEdit
        const inputEdit = document.getElementById('phaseBeneficiariesInputEdit');
        if (inputEdit) {
            inputEdit.value = selectedIds.join(',');
        }
        
        const badgeElement = document.getElementById('selectedPhaseBeneficiariesBadgeEdit');
        if (badgeElement) {
            if (selectedIds.length > 0) {
                badgeElement.textContent = selectedIds.length + ' seleccionados';
                badgeElement.classList.remove('hidden');
            } else {
                badgeElement.classList.add('hidden');
            }
        }
    } else if (isCreateMode) {
        // Modo creación: guardar en phaseBeneficiariesInput
        const inputCreate = document.getElementById('phaseBeneficiariesInput');
        if (inputCreate) {
            inputCreate.value = selectedIds.join(',');
        }
        
        const badgeElement = document.getElementById('selectedPhaseBeneficiariesBadge');
        if (badgeElement) {
            if (selectedIds.length > 0) {
                badgeElement.textContent = selectedIds.length + ' seleccionados';
                badgeElement.classList.remove('hidden');
            } else {
                badgeElement.classList.add('hidden');
            }
        }
    }

    updatePhaseBeneficiariesCount();
    closePhaseBeneficiariesModal();
}

function openPhaseBeneficiariesModalForEdit() {
    console.log('Abriendo modal de beneficiarios para editar fase');
    
    // Marcar los checkboxes de beneficiarios seleccionados
    const checkboxes = document.querySelectorAll('.phase-beneficiary-item input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        const beneficiaryId = checkbox.closest('.phase-beneficiary-item').dataset.id;
        checkbox.checked = selectedPhaseBeneficiaries.includes(beneficiaryId);
    });

    updatePhaseBeneficiariesCount();
    document.getElementById('phaseBeneficiariesModal').classList.remove('hidden');
}

// Modal para eliminar fase
function confirmDeletePhase(phaseId, phaseName) {
    const projectId = document.querySelector('[data-project-id]')?.dataset.projectId;
    
    document.getElementById('deletePhaseId').value = phaseId;
    document.getElementById('deletePhaseName').textContent = phaseName;
    document.getElementById('deletePhaseForm').action = `/dashboard/proyectos/${projectId}/fases/${phaseId}/eliminar/`;
    document.getElementById('deletePhaseModal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeDeletePhaseModal() {
    document.getElementById('deletePhaseModal').classList.add('hidden');
    document.body.style.overflow = 'auto';
    document.getElementById('deletePhaseForm').reset();
}

// Manejar el envío del formulario de edición de fase
document.addEventListener('DOMContentLoaded', function() {
    const editPhaseForm = document.getElementById('editPhaseForm');
    if (editPhaseForm) {
        editPhaseForm.addEventListener('submit', function(e) {
            e.preventDefault();
            e.stopPropagation();

            const formData = new FormData(this);
            const actionUrl = this.action;

            console.log('Enviando formulario de edición de fase a:', actionUrl);

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
                    closeEditPhaseModal();
                    location.reload();
                } else {
                    alert(data.message || 'Error al actualizar la fase');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al procesar la solicitud');
            });
        });
    }
});

// Manejar el envío del formulario de edición de evidencia de fase
document.addEventListener('DOMContentLoaded', function() {
    const editPhaseEvidenceForm = document.getElementById('phaseEditEvidenceForm');
    if (editPhaseEvidenceForm) {
        editPhaseEvidenceForm.addEventListener('submit', function(e) {
            e.preventDefault();
            e.stopPropagation();

            const formData = new FormData(this);
            const actionUrl = this.action;

            console.log('Enviando formulario de edición de evidencia de fase a:', actionUrl);

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
                    closePhaseEditEvidenceModal();
                    location.reload();
                } else {
                    alert(data.message || 'Error al actualizar la evidencia');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al procesar la solicitud');
            });
        });
    }
});

// Manejar el envío del formulario de eliminación de evidencia de fase
document.addEventListener('DOMContentLoaded', function() {
    const deletePhaseEvidenceForm = document.getElementById('deletePhaseEvidenceFormAction');
    if (deletePhaseEvidenceForm) {
        deletePhaseEvidenceForm.addEventListener('submit', function(e) {
            e.preventDefault();
            e.stopPropagation();

            const formData = new FormData(this);
            const actionUrl = this.action;

            console.log('Enviando formulario de eliminación de evidencia de fase a:', actionUrl);

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
                    closeDeletePhaseEvidenceModal();
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

// Manejar el envío del formulario de eliminación de fase
document.addEventListener('DOMContentLoaded', function() {
    const deletePhaseForm = document.getElementById('deletePhaseForm');
    if (deletePhaseForm) {
        deletePhaseForm.addEventListener('submit', function(e) {
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
                    closeDeletePhaseModal();
                    location.reload();
                } else {
                    alert(data.message || 'Error al eliminar la fase');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al procesar la solicitud');
            });
        });
    }
});

// Búsqueda de beneficiarios para fase
document.getElementById('phaseBeneficiariesSearch')?.addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const items = document.querySelectorAll('.phase-beneficiary-item');

    items.forEach(item => {
        const name = item.dataset.name.toLowerCase();
        const dpi = item.dataset.dpi.toLowerCase();
        const community = item.dataset.community.toLowerCase();

        if (name.includes(searchTerm) || dpi.includes(searchTerm) || community.includes(searchTerm)) {
            item.style.display = 'flex';
        } else {
            item.style.display = 'none';
        }
    });
});

// =====================================================
// FUNCIONES PARA EVIDENCIAS DE FASES
// =====================================================

// Modal para crear evidencia de fase
function openPhaseEvidenceModal() {
    console.log('Abriendo modal para crear evidencia de fase');
    document.getElementById('phaseEvidenceModal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closePhaseEvidenceModal() {
    console.log('Cerrando modal para crear evidencia de fase');
    document.getElementById('phaseEvidenceModal').classList.add('hidden');
    document.body.style.overflow = 'auto';
    document.getElementById('phaseEvidenceForm').reset();
    document.getElementById('phaseEvidenceBeneficiariesInput').value = '';
    document.getElementById('selectedPhaseEvidenceBeneficiariesBadge').classList.add('hidden');
    document.getElementById('phaseEvidencePhotosPreview').classList.add('hidden');
    document.getElementById('phaseEvidencePhotosPreview').innerHTML = '';
    
    // Limpiar el Set de fotos a eliminar
    if (window.photosToDelete) {
        window.photosToDelete.clear();
    }
}

// Modal para detalles de evidencia de fase
function openPhaseEvidenceDetailsModal(button) {
    const evidenceId = button.dataset.evidenceId;
    const startDate = button.dataset.startDate;
    const endDate = button.dataset.endDate;
    const description = button.dataset.description;
    const createdBy = button.dataset.createdBy;
    const createdAt = button.dataset.createdAt;
    const updatedAt = button.dataset.updatedAt;

    const modal = document.getElementById('phaseEvidenceDetailsModal');
    if (!modal) {
        console.error('Modal de detalles de evidencia no encontrado');
        return;
    }

    const startDateEl = document.getElementById('evidenceDetailStartDate');
    const endDateEl = document.getElementById('evidenceDetailEndDate');
    const descriptionEl = document.getElementById('evidenceDetailDescription');
    const createdByEl = document.getElementById('evidenceDetailCreatedBy');
    const updatedAtEl = document.getElementById('evidenceDetailUpdatedAt');

    if (startDateEl) startDateEl.textContent = formatDate(startDate);
    if (endDateEl) endDateEl.textContent = formatDate(endDate);
    if (descriptionEl) descriptionEl.textContent = description;
    if (createdByEl) createdByEl.textContent = createdBy;
    if (updatedAtEl) updatedAtEl.textContent = updatedAt;

    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closePhaseEvidenceDetailsModal() {
    const modal = document.getElementById('phaseEvidenceDetailsModal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = 'auto';
    }
}

// Modal para editar evidencia de fase
function openPhaseEditEvidenceModal(button) {
    const evidenceId = button.dataset.evidenceId;
    const projectId = document.querySelector('[data-project-id]').dataset.projectId;
    const phaseId = document.querySelector('[data-phase-id]').dataset.phaseId;

    const form = document.getElementById('editPhaseEvidenceForm');
    const modal = document.getElementById('editPhaseEvidenceModal');

    if (!form || !modal) {
        console.error('Formulario o modal de edición no encontrado');
        return;
    }

    document.getElementById('editEvidenceId').value = evidenceId;
    document.getElementById('editStartDate').value = button.dataset.startDate;
    document.getElementById('editEndDate').value = button.dataset.endDate;
    document.getElementById('editDescription').value = button.dataset.description;

    // Establecer action del formulario inmediatamente
    const actionUrl = `/dashboard/proyectos/${projectId}/fases/${phaseId}/evidencias/${evidenceId}/editar/`;
    form.action = actionUrl;
    console.log('Action del formulario establecido:', actionUrl);

    // Cargar fotos existentes
    fetch(`/dashboard/proyectos/${projectId}/fases/${phaseId}/evidencias/${evidenceId}/fotos/`)
        .then(response => response.json())
        .then(data => {
            const photosContainer = document.getElementById('editEvidencePhotosContainer');
            photosContainer.innerHTML = '';
            
            if (data.photos && data.photos.length > 0) {
                data.photos.forEach(photo => {
                    const photoDiv = document.createElement('div');
                    photoDiv.className = 'relative group';
                    
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.name = 'photos_to_delete';
                    checkbox.value = photo.id;
                    checkbox.className = 'hidden';
                    checkbox.id = `photo_delete_${photo.id}`;
                    
                    const label = document.createElement('label');
                    label.htmlFor = `photo_delete_${photo.id}`;
                    label.className = 'absolute top-2 right-2 cursor-pointer w-8 h-8 bg-red-500 rounded-full flex items-center justify-center text-white opacity-0 hover:opacity-100 transition-opacity';
                    label.innerHTML = '<i class="fas fa-trash text-sm"></i>';
                    
                    const img = document.createElement('img');
                    img.src = `/media/${photo.photo_url}`;
                    img.alt = 'Foto de evidencia';
                    img.className = 'w-full h-32 object-cover rounded-lg border border-gray-200';
                    
                    const orderLabel = document.createElement('div');
                    orderLabel.className = 'absolute bottom-2 left-2 bg-black/50 text-white text-xs px-2 py-1 rounded';
                    orderLabel.textContent = `#${photo.photo_order}`;
                    
                    photoDiv.appendChild(img);
                    photoDiv.appendChild(checkbox);
                    photoDiv.appendChild(label);
                    photoDiv.appendChild(orderLabel);
                    
                    photosContainer.appendChild(photoDiv);
                });
            } else {
                photosContainer.innerHTML = '<p class="text-sm text-gray-500 col-span-full">No hay fotos asociadas</p>';
            }
            console.log('Fotos cargadas:', data.photos);
        })
        .catch(error => {
            console.error('Error al cargar fotos:', error);
        });

    // Cargar beneficiarios actuales
    fetch(`/dashboard/proyectos/${projectId}/fases/${phaseId}/evidencias/${evidenceId}/beneficiarios/`)
        .then(response => response.json())
        .then(data => {
            const beneficiaries = data.beneficiaries || [];
            const selectedIds = beneficiaries.map(b => b.id.toString());
            const beneficiariesInput = document.getElementById('phaseEvidenceBeneficiariesInput');
            beneficiariesInput.value = selectedIds.join(',');
            
            const badgeElement = document.getElementById('selectedPhaseEvidenceBeneficiariesBadge');
            if (badgeElement) {
                if (selectedIds.length > 0) {
                    badgeElement.textContent = selectedIds.length + ' seleccionados';
                    badgeElement.classList.remove('hidden');
                } else {
                    badgeElement.classList.add('hidden');
                }
            }
            console.log('Beneficiarios cargados:', selectedIds);
        })
        .catch(error => {
            console.error('Error al cargar beneficiarios:', error);
        });

    // Limpiar previsualización de nuevas fotos
    const previewContainer = document.getElementById('editPhaseEvidencePhotosPreview');
    if (previewContainer) {
        previewContainer.innerHTML = '';
        previewContainer.classList.add('hidden');
    }
    const photoInput = document.getElementById('editPhaseEvidencePhotosInput');
    if (photoInput) {
        photoInput.value = '';
    }

    if (modal) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }
}

function closePhaseEditEvidenceModal() {
    const modal = document.getElementById('editPhaseEvidenceModal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = 'auto';
    }

    // Limpiar badge de beneficiarios
    const badgeElement = document.getElementById('selectedPhaseEvidenceBeneficiariesBadge');
    if (badgeElement) {
        badgeElement.classList.add('hidden');
    }
}

// Modal para eliminar evidencia de fase
function confirmPhaseDeleteEvidence(button) {
    const evidenceId = button.dataset.evidenceId;
    const projectId = document.querySelector('[data-project-id]').dataset.projectId;
    const phaseId = document.querySelector('[data-phase-id]').dataset.phaseId;

    document.getElementById('deletePhaseEvidenceId').value = evidenceId;
    const form = document.getElementById('deletePhaseEvidenceFormAction');
    form.action = `/dashboard/proyectos/${projectId}/fases/${phaseId}/evidencias/${evidenceId}/eliminar/`;

    document.getElementById('deletePhaseEvidenceModal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeDeletePhaseEvidenceModal() {
    document.getElementById('deletePhaseEvidenceModal').classList.add('hidden');
    document.body.style.overflow = 'auto';
    const form = document.getElementById('deletePhaseEvidenceFormAction');
    form.reset();
}

// Modal de beneficiarios para evidencia de fase
function openPhaseEvidenceBeneficiariesModal() {
    const projectId = document.querySelector('[data-project-id]').dataset.projectId;
    const phaseId = document.querySelector('[data-phase-id]').dataset.phaseId;
    
    // Verificar si estamos en modo edición
    const editModal = document.getElementById('phaseEditEvidenceModal');
    const isEditMode = editModal && !editModal.classList.contains('hidden');
    
    if (isEditMode) {
        // Modo edición: cargar beneficiarios de la evidencia existente
        const evidenceId = document.getElementById('editEvidenceId').value;
        console.log('Modo edición, cargando beneficiarios de evidencia:', evidenceId);
        
        fetch(`/dashboard/proyectos/${projectId}/fases/${phaseId}/evidencias/${evidenceId}/beneficiarios/`)
            .then(response => response.json())
            .then(data => {
                const beneficiaries = data.beneficiaries || [];
                const selectedIds = beneficiaries.map(b => b.id.toString());
                console.log('Beneficiarios cargados:', selectedIds);

                document.querySelectorAll('.phase-evidence-beneficiary-item input[type="checkbox"]').forEach(checkbox => {
                    const beneficiaryId = checkbox.closest('.phase-evidence-beneficiary-item').dataset.id;
                    checkbox.checked = selectedIds.includes(beneficiaryId);
                });

                updatePhaseEvidenceBeneficiariesCount();
                document.getElementById('phaseEvidenceBeneficiariesModal').classList.remove('hidden');
            })
            .catch(error => {
                console.error('Error al cargar beneficiarios:', error);
            });
    } else {
        // Modo creación: limpiar selección
        console.log('Modo creación, limpiando selección de beneficiarios');
        document.querySelectorAll('.phase-evidence-beneficiary-item input[type="checkbox"]').forEach(checkbox => {
            checkbox.checked = false;
        });
        updatePhaseEvidenceBeneficiariesCount();
        document.getElementById('phaseEvidenceBeneficiariesModal').classList.remove('hidden');
    }
}

function closePhaseEvidenceBeneficiariesModal() {
    document.getElementById('phaseEvidenceBeneficiariesModal').classList.add('hidden');
}

function togglePhaseEvidenceBeneficiarySelection(item) {
    const checkbox = item.querySelector('input[type="checkbox"]');
    checkbox.checked = !checkbox.checked;
    updatePhaseEvidenceBeneficiariesCount();
}

function updatePhaseEvidenceBeneficiariesCount() {
    const checkboxes = document.querySelectorAll('.phase-evidence-beneficiary-item input[type="checkbox"]:checked');
    const count = checkboxes.length;
    const countElement = document.getElementById('selectedPhaseEvidenceBeneficiariesCount');
    const badgeElement = document.getElementById('selectedPhaseEvidenceBeneficiariesBadge');

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

function confirmPhaseEvidenceBeneficiariesSelection() {
    const checkboxes = document.querySelectorAll('.phase-evidence-beneficiary-item input[type="checkbox"]:checked');
    const selectedIds = Array.from(checkboxes).map(cb => cb.closest('.phase-evidence-beneficiary-item').dataset.id);

    const beneficiariesInput = document.getElementById('phaseEvidenceBeneficiariesInput');
    beneficiariesInput.value = selectedIds.join(',');
    
    console.log('Beneficiarios confirmados:', selectedIds);
    console.log('Valor del input hidden:', beneficiariesInput.value);
    
    updatePhaseEvidenceBeneficiariesCount();
    closePhaseEvidenceBeneficiariesModal();
}

// Previsualización de fotos de evidencia de fase
function previewPhaseEvidencePhotos(input) {
    const previewContainer = document.getElementById('phaseEvidencePhotosPreview');
    previewContainer.innerHTML = '';
    previewContainer.classList.remove('hidden');

    // Crear un Set para rastrear las fotos que se deben eliminar
    if (!window.photosToDelete) {
        window.photosToDelete = new Set();
    }

    Array.from(input.files).forEach((file, index) => {
        const photoId = `new-photo-${Date.now()}-${index}`;
        const reader = new FileReader();
        reader.onload = function(e) {
            const previewDiv = document.createElement('div');
            previewDiv.className = 'relative group';
            previewDiv.dataset.photoId = photoId;
            previewDiv.innerHTML = `
                <img src="${e.target.result}" alt="Previsualización" class="w-full h-32 object-cover rounded-lg border border-gray-200">
                <button type="button" class="absolute -top-2 -right-2 w-8 h-8 bg-red-500 hover:bg-red-600 text-white rounded-full shadow-lg transition-colors flex items-center justify-center" onclick="deletePreviewedPhaseEvidencePhoto(this, '${photoId}')">
                    <i class="fas fa-times text-sm"></i>
                </button>
                <span class="absolute bottom-2 right-2 bg-black/50 text-white text-xs px-2 py-1 rounded">${index + 1}</span>
            `;
            previewContainer.appendChild(previewDiv);
        };
        reader.readAsDataURL(file);
    });
}

function deletePreviewedPhaseEvidencePhoto(button, photoId) {
    const previewDiv = button.parentElement;
    previewDiv.remove();
    
    // Agregar el ID de la foto al Set de fotos a eliminar
    if (!window.photosToDelete) {
        window.photosToDelete = new Set();
    }
    window.photosToDelete.add(photoId);
    
    // Ocultar el contenedor si no hay más fotos
    const previewContainer = document.getElementById('phaseEvidencePhotosPreview');
    if (previewContainer.children.length === 0) {
        previewContainer.classList.add('hidden');
    }
}

// Previsualización de nuevas fotos al editar evidencia de fase
function previewEditPhaseEvidencePhotos(input) {
    const previewContainer = document.getElementById('editPhaseEvidencePhotosPreview');
    previewContainer.innerHTML = '';
    
    if (input.files.length > 0) {
        previewContainer.classList.remove('hidden');
        console.log('Nuevas fotos seleccionadas:', input.files.length);
        Array.from(input.files).forEach((file, index) => {
            const reader = new FileReader();
            reader.onload = function(e) {
                const preview = document.createElement('div');
                preview.className = 'relative';
                preview.innerHTML = `
                    <img src="${e.target.result}" alt="Previsualización" class="w-full h-32 object-cover rounded-lg border border-gray-200">
                    <span class="absolute bottom-2 right-2 bg-[#8a4534] text-white text-xs px-2 py-1 rounded">Nueva</span>
                `;
                previewContainer.appendChild(preview);
            };
            reader.readAsDataURL(file);
        });
    } else {
        previewContainer.classList.add('hidden');
    }
}

// Formatear fecha
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric' });
}

// Búsqueda de beneficiarios para evidencia de fase
document.getElementById('phaseEvidenceBeneficiariesSearch')?.addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const items = document.querySelectorAll('.phase-evidence-beneficiary-item');

    items.forEach(item => {
        const name = item.dataset.name.toLowerCase();
        const dpi = item.dataset.dpi.toLowerCase();
        const community = item.dataset.community.toLowerCase();

        if (name.includes(searchTerm) || dpi.includes(searchTerm) || community.includes(searchTerm)) {
            item.style.display = 'flex';
        } else {
            item.style.display = 'none';
        }
    });
});

// Event listener para el formulario de edición de evidencia
document.addEventListener('DOMContentLoaded', function() {
    const editEvidenceForm = document.getElementById('phaseEditEvidenceForm');
    if (editEvidenceForm) {
        editEvidenceForm.addEventListener('submit', function(e) {
            console.log('Formulario de edición enviado');
            console.log('Action:', this.action);
            console.log('Method:', this.method);

            // Verificar fotos marcadas para eliminar
            const photosToDelete = this.querySelectorAll('input[name="photos_to_delete"]:checked');
            console.log('Fotos marcadas para eliminar:', photosToDelete.length);
            photosToDelete.forEach((checkbox, index) => {
                console.log(`  - Foto ${index + 1}: ID ${checkbox.value}`);
            });

            // Verificar nuevas fotos
            const newPhotos = this.querySelector('#editPhaseEvidencePhotosInput');
            console.log('Nuevas fotos a subir:', newPhotos.files.length);

            // Verificar beneficiarios
            const beneficiariesInput = this.querySelector('#phaseEvidenceBeneficiariesInput');
            console.log('Beneficiarios seleccionados:', beneficiariesInput.value);

            // Permitir envío normal
        });
    }
});

// Funciones para modal de beneficiarios de fase (phase_edit.html)
function openBeneficiariesModalForPhase() {
    document.getElementById('beneficiariesModalForPhase').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeBeneficiariesModalForPhase() {
    document.getElementById('beneficiariesModalForPhase').classList.add('hidden');
    document.body.style.overflow = 'auto';
}

function updateBeneficiariesCountPhase() {
    const checkboxes = document.querySelectorAll('.beneficiary-item-for-phase input[type="checkbox"]:checked');
    const count = checkboxes.length;
    const countElement = document.getElementById('selectedBeneficiariesCountPhase');
    const badgeElement = document.getElementById('selectedBeneficiariesBadgePhase');
    
    countElement.textContent = count;
    if (count > 0) {
        badgeElement.textContent = count + ' seleccionados';
        badgeElement.classList.remove('hidden');
    } else {
        badgeElement.classList.add('hidden');
    }
}

function confirmBeneficiariesSelectionPhase() {
    const checkboxes = document.querySelectorAll('.beneficiary-item-for-phase input[type="checkbox"]:checked');
    const selectedIds = Array.from(checkboxes).map(cb => cb.closest('.beneficiary-item-for-phase').dataset.id);
    
    document.getElementById('beneficiariesInputPhase').value = selectedIds.join(',');
    updateBeneficiariesCountPhase();
    closeBeneficiariesModalForPhase();
}

// Búsqueda de beneficiarios
document.getElementById('beneficiariesSearchPhase')?.addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const items = document.querySelectorAll('.beneficiary-item-for-phase');
    
    items.forEach(item => {
        const name = item.dataset.name.toLowerCase();
        const dpi = item.dataset.dpi.toLowerCase();
        const community = item.dataset.community.toLowerCase();
        
        if (name.includes(searchTerm) || dpi.includes(searchTerm) || community.includes(searchTerm)) {
            item.style.display = 'flex';
        } else {
            item.style.display = 'none';
        }
    });
});

// Cerrar modales al hacer clic fuera
document.getElementById('beneficiariesModalForPhase').addEventListener('click', function(e) {
    if (e.target === this) closeBeneficiariesModalForPhase();
});

// Cerrar modales con Escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeBeneficiariesModalForPhase();
    }
});

// Inicializar contador
updateBeneficiariesCountPhase();

// =====================================================
// EVENT LISTENERS - CERRAR MODALES
// =====================================================

// Modales de fases
document.getElementById('phaseModal')?.addEventListener('click', function(e) {
    if (e.target === this) closePhaseModal();
});

document.getElementById('editPhaseModal')?.addEventListener('click', function(e) {
    if (e.target === this) closeEditPhaseModal();
});

document.getElementById('phaseBeneficiariesModal')?.addEventListener('click', function(e) {
    if (e.target === this) closePhaseBeneficiariesModal();
});

document.getElementById('deletePhaseModal')?.addEventListener('click', function(e) {
    if (e.target === this) closeDeletePhaseModal();
});

// Modales de evidencias de fases
document.getElementById('phaseEvidenceModal')?.addEventListener('click', function(e) {
    if (e.target === this) closePhaseEvidenceModal();
});

document.getElementById('phaseEvidenceDetailsModal')?.addEventListener('click', function(e) {
    if (e.target === this) closePhaseEvidenceDetailsModal();
});

document.getElementById('editPhaseEvidenceModal')?.addEventListener('click', function(e) {
    if (e.target === this) closePhaseEditEvidenceModal();
});
document.getElementById('deletePhaseEvidenceModal')?.addEventListener('click', function(e) {
    if (e.target === this) closeDeletePhaseEvidenceModal();
});
document.getElementById('phaseEvidenceBeneficiariesModal')?.addEventListener('click', function(e) {
    if (e.target === this) closePhaseEvidenceBeneficiariesModal();
});

document.getElementById('deletePhaseEvidenceModal')?.addEventListener('click', function(e) {
    if (e.target === this) closeDeletePhaseEvidenceModal();
});

document.getElementById('phaseEvidenceBeneficiariesModal')?.addEventListener('click', function(e) {
    if (e.target === this) closePhaseEvidenceBeneficiariesModal();
});

// Cerrar modales con Escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closePhaseModal();
        closeEditPhaseModal();
        closePhaseBeneficiariesModal();
        closeDeletePhaseModal();
        closePhaseEvidenceModal();
        closePhaseEvidenceDetailsModal();
        closePhaseEditEvidenceModal();
        closeDeletePhaseEvidenceModal();
        closePhaseEvidenceBeneficiariesModal();
        closePhotoModal();
    }
});

// Cerrar modal de foto al hacer clic fuera
document.getElementById('photoModal')?.addEventListener('click', function(e) {
    if (e.target === this) closePhotoModal();
});

// Función para navegar entre las fotos de una evidencia de fase
function navigatePhaseEvidencePhotos(evidenceId, direction) {
    const container = document.getElementById(`phase-evidence-photos-${evidenceId}`);
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

// Inicializar las fotos de evidencias de fases al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    // Para cada evidencia de fase, configurar el grid de fotos dinámicamente
    document.querySelectorAll('[id^="phase-evidence-photos-"]').forEach(function(container) {
        const photos = container.querySelectorAll('.evidence-photo');
        const totalPhotos = photos.length;
        
        console.log(`Configurando evidencia de fase ${container.id.replace('phase-evidence-photos-', '')} con ${totalPhotos} fotos`);
        
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
