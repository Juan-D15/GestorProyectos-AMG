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
    const editPhaseEvidenceForm = document.getElementById('editPhaseEvidenceForm');
    if (editPhaseEvidenceForm) {
        editPhaseEvidenceForm.addEventListener('submit', function(e) {
            e.preventDefault();
            e.stopPropagation();

            const formData = new FormData(this);
            const actionUrl = this.action;

            console.log('Enviando formulario de edición de evidencia de fase a:', actionUrl);
            console.log('FormData - photos_to_delete:', formData.getAll('photos_to_delete'));

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
// Modal para detalles de evidencia de fase
function openPhaseEvidenceDetailsModal(button) {
    const evidenceId = button.dataset.evidenceId;
    const startDate = button.dataset.startDate;
    const endDate = button.dataset.endDate;
    const description = button.dataset.description;
    const projectId = document.querySelector('[data-project-id]').dataset.projectId;
    const phaseId = document.querySelector('[data-phase-id]').dataset.phaseId;

    const modal = document.getElementById('phaseEvidenceDetailsModal');
    if (!modal) {
        console.error('Modal de detalles de evidencia no encontrado');
        return;
    }

    const startDateEl = document.getElementById('evidenceDetailStartDate');
    const endDateEl = document.getElementById('evidenceDetailEndDate');
    const descriptionEl = document.getElementById('evidenceDetailDescription');

    if (startDateEl) startDateEl.textContent = formatEvidenceDate(startDate);
    if (endDateEl) endDateEl.textContent = formatEvidenceDate(endDate);
    if (descriptionEl) descriptionEl.textContent = description;

    // Cargar fotos de la evidencia
    loadPhaseEvidenceDetailsPhotos(evidenceId, projectId, phaseId);

    // Cargar beneficiarios de la evidencia
    loadPhaseEvidenceDetailsBeneficiaries(evidenceId, projectId, phaseId);

    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

// Función para formatear fechas de evidencia (YYYY-MM-DD a DD/MM/YYYY)
function formatEvidenceDate(dateString) {
    if (!dateString) return '';
    
    // Si la fecha ya está en formato YYYY-MM-DD, formatearla
    if (dateString.includes('-')) {
        const parts = dateString.split('-');
        if (parts.length === 3) {
            return `${parts[2]}/${parts[1]}/${parts[0]}`;
        }
    }
    
    return dateString;
}

// Función para cargar las fotos en los detalles de evidencia de fase
function loadPhaseEvidenceDetailsPhotos(evidenceId, projectId, phaseId) {
    const photosContainer = document.getElementById('evidenceDetailPhotos');
    const photosSection = document.getElementById('evidenceDetailPhotosSection');
    
    console.log(`Cargando fotos para detalles de evidencia de fase ${evidenceId}...`);
    
    fetch(`/dashboard/proyectos/${projectId}/fases/${phaseId}/evidencias/${evidenceId}/fotos/`)
        .then(response => response.json())
        .then(data => {
            photosContainer.innerHTML = '';
            
            if (data.photos && data.photos.length > 0) {
                photosSection.classList.remove('hidden');
                
                data.photos.forEach(photo => {
                    const photoDiv = document.createElement('div');
                    photoDiv.className = 'relative group';
                    
                    const img = document.createElement('img');
                    img.src = '/media/' + photo.photo_url;
                    img.className = 'w-full h-32 object-cover rounded-lg border border-gray-200 cursor-pointer hover:opacity-80 transition-opacity';
                    img.alt = 'Foto de evidencia';
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

// Función para cargar los beneficiarios en los detalles de evidencia de fase
function loadPhaseEvidenceDetailsBeneficiaries(evidenceId, projectId, phaseId) {
    const beneficiariesContainer = document.getElementById('evidenceDetailBeneficiaries');
    const beneficiariesSection = document.getElementById('evidenceDetailBeneficiariesSection');
    
    console.log(`=== Cargando beneficiarios para detalles de evidencia de fase ${evidenceId} ===`);
    console.log(`URL: /dashboard/proyectos/${projectId}/fases/${phaseId}/evidencias/${evidenceId}/beneficiarios/`);
    
    // Limpiar contenedor antes de cargar
    beneficiariesContainer.innerHTML = '';
    
    fetch(`/dashboard/proyectos/${projectId}/fases/${phaseId}/evidencias/${evidenceId}/beneficiarios/`)
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

function closePhaseEvidenceDetailsModal() {
    const modal = document.getElementById('phaseEvidenceDetailsModal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = 'auto';
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
    // Verificar si estamos en modo edición o creación
    const editModal = document.getElementById('editPhaseEvidenceModal');
    const createModal = document.getElementById('phaseEvidenceModal');
    const isEditMode = editModal && !editModal.classList.contains('hidden');
    const isCreateMode = createModal && !createModal.classList.contains('hidden');

    // Seleccionar el input correcto según el modo
    let beneficiariesInput;
    if (isEditMode) {
        beneficiariesInput = document.getElementById('editPhaseEvidenceBeneficiariesInput');
        console.log('Modo: EDICIÓN');
    } else if (isCreateMode) {
        beneficiariesInput = document.getElementById('createPhaseEvidenceBeneficiariesInput');
        console.log('Modo: CREACIÓN');
    } else {
        console.error('No se pudo determinar el modo (ni edición ni creación)');
        return;
    }

    if (!beneficiariesInput) {
        console.error('No se encontró el input de beneficiarios');
        return;
    }

    const currentIds = beneficiariesInput.value.split(',').filter(id => id.trim() !== '');

    console.log('IDs actuales en input:', currentIds);
    console.log('Tipo de datos en input:', currentIds.map(id => typeof id));

    // Marcar checkboxes basados en los IDs del input
    document.querySelectorAll('.phase-evidence-beneficiary-item input[type="checkbox"]').forEach(checkbox => {
        const beneficiaryId = checkbox.closest('.phase-evidence-beneficiary-item').dataset.id;
        const isChecked = currentIds.includes(beneficiaryId);
        checkbox.checked = isChecked;
        console.log(`Checkbox ID ${beneficiaryId}: ${isChecked}`);
    });

    updatePhaseEvidenceBeneficiariesCount();
    document.getElementById('phaseEvidenceBeneficiariesModal').classList.remove('hidden');
}

function closePhaseEvidenceBeneficiariesModal() {
    console.log('=== Cerrando modal de beneficiarios ===');
    
    // Verificar valor del input antes de cerrar
    const editModal = document.getElementById('editPhaseEvidenceModal');
    const createModal = document.getElementById('phaseEvidenceModal');
    const isEditMode = editModal && !editModal.classList.contains('hidden');
    const isCreateMode = createModal && !createModal.classList.contains('hidden');
    
    let beneficiariesInput;
    if (isEditMode) {
        beneficiariesInput = document.getElementById('editPhaseEvidenceBeneficiariesInput');
    } else if (isCreateMode) {
        beneficiariesInput = document.getElementById('createPhaseEvidenceBeneficiariesInput');
    }
    
    if (beneficiariesInput) {
        console.log('Valor del input de beneficiarios antes de cerrar modal:', beneficiariesInput.value);
        console.log('Longitud:', beneficiariesInput.value.length);
    }
    
    document.getElementById('phaseEvidenceBeneficiariesModal').classList.add('hidden');
    console.log('=== Fin de cierre del modal de beneficiarios ===');
}

// Event listener para actualizar el contador cuando cambian los checkboxes en el modal
document.addEventListener('DOMContentLoaded', function() {
    const checkboxesContainer = document.getElementById('phaseEvidenceBeneficiariesList');
    if (checkboxesContainer) {
        checkboxesContainer.addEventListener('change', function(e) {
            if (e.target.type === 'checkbox') {
                updatePhaseEvidenceBeneficiariesCount();
            }
        });
    }
});

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
    
    console.log('=== Confirmando selección de beneficiarios ===');
    console.log('Checkboxes seleccionados:', checkboxes.length);
    console.log('Checkboxes encontrados:', document.querySelectorAll('.phase-evidence-beneficiary-item input[type="checkbox"]').length);
    
    // Usar el valor del checkbox directamente
    const selectedIds = Array.from(checkboxes).map(cb => {
        console.log(`  Checkbox seleccionado - value: ${cb.value}, type: ${typeof cb.value}`);
        return cb.value;
    });
    
    console.log('IDs seleccionados (del value):', selectedIds);
    console.log('Tipo de datos:', selectedIds.map(id => typeof id));

    // Verificar si estamos en modo edición o creación
    const editModal = document.getElementById('editPhaseEvidenceModal');
    const createModal = document.getElementById('phaseEvidenceModal');
    const isEditMode = editModal && !editModal.classList.contains('hidden');
    const isCreateMode = createModal && !createModal.classList.contains('hidden');

    console.log('Modo edición:', isEditMode);
    console.log('Modo creación:', isCreateMode);

    // Seleccionar el input correcto según el modo
    let beneficiariesInput;
    if (isEditMode) {
        beneficiariesInput = document.getElementById('editPhaseEvidenceBeneficiariesInput');
        console.log('Guardando en input de EDICIÓN');
    } else if (isCreateMode) {
        beneficiariesInput = document.getElementById('createPhaseEvidenceBeneficiariesInput');
        console.log('Guardando en input de CREACIÓN');
    } else {
        console.error('No se pudo determinar el modo (ni edición ni creación)');
        return;
    }

    if (beneficiariesInput) {
        beneficiariesInput.value = selectedIds.join(',');
        console.log('Valor asignado al input:', beneficiariesInput.value);
        console.log('Nombre del input:', beneficiariesInput.name);
        console.log('ID del input:', beneficiariesInput.id);
        console.log('Beneficiarios confirmados:', selectedIds);
    } else {
        console.error('No se encontró el input de beneficiarios');
    }

    // Solo actualizar el badge, no la lista visual
    updatePhaseEvidenceBeneficiariesCount();
    closePhaseEvidenceBeneficiariesModal();
    
    // Verificar que el valor se guardó
    if (beneficiariesInput) {
        setTimeout(() => {
            console.log('=== Valor del input DESPUÉS de cerrar modal ===');
            console.log('Valor:', beneficiariesInput.value);
            console.log('Longitud:', beneficiariesInput.value.length);
            console.log('=== Fin de verificación ===');
        }, 100);
    }
    
    console.log('=== Fin de confirmación de beneficiarios ===');
}

function updateSelectedBeneficiariesList(selectedIds) {
    const listElement = document.getElementById('selectedPhaseEvidenceBeneficiariesList');
    const container = document.getElementById('selectedPhaseEvidenceBeneficiariesContainer');
    const countElement = document.getElementById('selectedPhaseEvidenceBeneficiariesCount');

    if (!listElement || !container) return;

    if (selectedIds.length === 0) {
        listElement.innerHTML = '<p class="text-sm text-gray-500">No hay beneficiarios seleccionados</p>';
        container.classList.add('hidden');
        if (countElement) countElement.textContent = '0';
        return;
    }

    // El contenedor debe mantenerse oculto siempre en el formulario
    // Solo actualizamos el badge con el contador

    // Obtener información de los beneficiarios seleccionados (para uso interno)
    const selectedBeneficiaries = [];
    document.querySelectorAll('.phase-evidence-beneficiary-item').forEach(item => {
        const beneficiaryId = parseInt(item.dataset.id);
        if (selectedIds.includes(beneficiaryId)) {
            selectedBeneficiaries.push({
                id: item.dataset.id,
                name: item.dataset.name,
                dpi: item.dataset.dpi,
                community: item.dataset.community
            });
        }
    });

    listElement.innerHTML = '';
    selectedBeneficiaries.forEach(beneficiary => {
        const item = document.createElement('div');
        item.className = 'flex items-center justify-between p-2 bg-white rounded-lg border border-gray-200';
        item.innerHTML = `
            <p class="text-sm font-medium text-gray-900">${beneficiary.name}</p>
            <button type="button" class="text-red-500 hover:text-red-700 transition-colors" onclick="removeSelectedBeneficiary(${beneficiary.id})">
                <i class="fas fa-times"></i>
            </button>
        `;
        listElement.appendChild(item);
    });

    // MANTENER OCULTO el contenedor de la lista de beneficiarios
    container.classList.add('hidden');

    if (countElement) countElement.textContent = selectedIds.length;
}

function removeSelectedBeneficiary(id) {
    const beneficiariesInput = document.getElementById('phaseEvidenceBeneficiariesInput');
    const currentIds = beneficiariesInput.value.split(',').filter(id => id.trim() !== '');

    const newIds = currentIds.filter(bId => bId !== id.toString());
    beneficiariesInput.value = newIds.join(',');

    // Actualizar badge y contador
    updatePhaseEvidenceBeneficiariesCount();

    // Actualizar checkbox en el modal
    const checkbox = document.querySelector(`.phase-evidence-beneficiary-item[data-id="${id}"] input[type="checkbox"]`);
    if (checkbox) {
        checkbox.checked = false;
    }
}

// Previsualización de fotos de evidencia de fase
function previewPhaseEvidencePhotos(input) {
    const previewContainer = document.getElementById('phaseEvidencePhotosPreview');

    // Inicializar el array de fotos si no existe
    if (!window.selectedPhaseEvidencePhotos) {
        window.selectedPhaseEvidencePhotos = [];
        console.log('Array inicializado');
    }

    console.log('=== Agregando fotos nuevas ===');
    console.log('Fotos actuales en array antes de agregar:', window.selectedPhaseEvidencePhotos.length);
    console.log('Nuevas fotos seleccionadas:', input.files.length);

    // Agregar archivos al array (evitando duplicados)
    Array.from(input.files).forEach(file => {
        const isDuplicate = window.selectedPhaseEvidencePhotos.some(existing =>
            existing.name === file.name && existing.size === file.size
        );

        if (!isDuplicate) {
            window.selectedPhaseEvidencePhotos.push(file);
            console.log(`✓ Foto agregada: ${file.name}`);
        } else {
            console.log(`✗ Foto duplicada omitida: ${file.name}`);
        }
    });

    console.log('Total de fotos en array después de agregar:', window.selectedPhaseEvidencePhotos.length);

    // Mostrar el contenedor
    previewContainer.classList.remove('hidden');

    // Limpiar el contenedor
    previewContainer.innerHTML = '';

    // Renderizar TODAS las fotos seleccionadas (incluyendo las anteriores)
    console.log('Renderizando', window.selectedPhaseEvidencePhotos.length, 'fotos en el DOM');
    window.selectedPhaseEvidencePhotos.forEach((file, index) => {
        const photoId = `new-photo-${Date.now()}-${index}`;
        const reader = new FileReader();
        reader.onload = function(e) {
            const previewDiv = document.createElement('div');
            previewDiv.className = 'relative group';
            previewDiv.dataset.photoId = photoId;
            previewDiv.dataset.fileIndex = index;
            previewDiv.innerHTML = `
                <img src="${e.target.result}" alt="Previsualización" class="w-full h-32 object-cover rounded-lg border border-gray-200">
                <button type="button" class="absolute -top-2 -right-2 w-8 h-8 bg-red-500 hover:bg-red-600 text-white rounded-full shadow-lg transition-colors flex items-center justify-center z-10" onclick="deletePreviewedPhaseEvidencePhoto(this, ${index})">
                    <i class="fas fa-times text-sm"></i>
                </button>
            `;
            previewContainer.appendChild(previewDiv);
        };
        reader.readAsDataURL(file);
    });
    console.log('Total de fotos renderizadas en DOM:', window.selectedPhaseEvidencePhotos.length);

    // Limpiar el input
    input.value = '';
}

function deletePreviewedPhaseEvidencePhoto(button, fileIndex) {
    console.log('=== Eliminando foto ===');
    console.log('Índice de foto a eliminar:', fileIndex);
    console.log('Fotos antes de eliminar:', window.selectedPhaseEvidencePhotos.length);

    // Eliminar la foto del array
    if (window.selectedPhaseEvidencePhotos) {
        const deletedFile = window.selectedPhaseEvidencePhotos[fileIndex];
        console.log('Foto eliminada:', deletedFile.name);
        window.selectedPhaseEvidencePhotos.splice(fileIndex, 1);
    }

    console.log('Fotos restantes en array:', window.selectedPhaseEvidencePhotos.length);

    // Eliminar el elemento del DOM directamente sin recrear todo
    button.parentElement.remove();

    // Actualizar los índices de los elementos restantes
    const previewContainer = document.getElementById('phaseEvidencePhotosPreview');
    Array.from(previewContainer.children).forEach((element, newIndex) => {
        const removeBtn = element.querySelector('button');
        if (removeBtn) {
            removeBtn.onclick = function() {
                deletePreviewedPhaseEvidencePhoto(this, newIndex);
            };
        }
    });

    // Ocultar el contenedor si no hay fotos
    if (window.selectedPhaseEvidencePhotos.length === 0) {
        previewContainer.innerHTML = '';
        previewContainer.classList.add('hidden');
    }
}
// Variable global para fotos seleccionadas en edición de evidencia de fase
let selectedEditPhasePhotos = [];

// Función para previsualizar nuevas fotos en edición de evidencia de fase
function previewEditPhaseEvidencePhotos(input) {
    const previewContainer = document.getElementById('editPhaseEvidencePhotosPreview');

    if (input.files.length > 0) {
        previewContainer.classList.remove('hidden');
        console.log('Nuevas fotos seleccionadas para editar evidencia:', input.files.length);

        // Agregar fotos al array global para persistencia al reabrir el modal
        Array.from(input.files).forEach(file => {
            // Verificar duplicados por nombre y tamaño
            const isDuplicate = selectedEditPhasePhotos.some(existing =>
                existing.name === file.name && existing.size === file.size
            );

            if (!isDuplicate) {
                selectedEditPhasePhotos.push(file);
                console.log(`Foto agregada a array de edición: ${file.name}`);
            }
        });

        // Limpiar y volver a renderizar TODAS las fotos para mantener el orden correcto
        previewContainer.innerHTML = '';

        selectedEditPhasePhotos.forEach((file, index) => {
            const reader = new FileReader();
            reader.onload = function(e) {
                const preview = document.createElement('div');
                preview.className = 'relative group';
                preview.dataset.fileName = file.name;
                preview.dataset.fileSize = file.size;
                preview.dataset.fileIndex = index;
                preview.innerHTML = `
                    <img src="${e.target.result}" alt="Previsualización" class="w-full h-32 object-cover rounded-lg border border-gray-200">
                    <span class="absolute bottom-2 right-2 bg-[#8a4534] text-white text-xs px-2 py-1 rounded">Nueva</span>
                    <button type="button" class="absolute -top-2 -right-2 w-8 h-8 bg-red-500 hover:bg-red-600 text-white rounded-full shadow-lg transition-colors flex items-center justify-center z-10" onclick="removeEditPhasePhoto(this, ${index})">
                        <i class="fas fa-times text-sm"></i>
                    </button>
                `;
                previewContainer.appendChild(preview);
            };
            reader.readAsDataURL(file);
        });

        // Limpiar el input
        input.value = '';
    }
}

// Función para eliminar una foto nueva del preview de edición
function removeEditPhasePhoto(button, fileIndex) {
    console.log('=== Eliminando foto nueva de edición ===');
    console.log('Índice de foto a eliminar:', fileIndex);
    console.log('Fotos antes de eliminar:', selectedEditPhasePhotos.length);

    // Eliminar la foto del array
    const deletedFile = selectedEditPhasePhotos[fileIndex];
    console.log('Foto eliminada:', deletedFile.name);
    selectedEditPhasePhotos.splice(fileIndex, 1);

    console.log('Fotos restantes en array:', selectedEditPhasePhotos.length);

    // Eliminar el elemento del DOM directamente sin recrear todo
    button.parentElement.remove();

    // Actualizar los índices de los elementos restantes
    const previewContainer = document.getElementById('editPhaseEvidencePhotosPreview');
    Array.from(previewContainer.children).forEach((element, newIndex) => {
        const removeBtn = element.querySelector('button');
        if (removeBtn) {
            removeBtn.onclick = function() {
                removeEditPhasePhoto(this, newIndex);
            };
        }
    });

    // Ocultar el contenedor si no hay fotos
    if (selectedEditPhasePhotos.length === 0) {
        previewContainer.innerHTML = '';
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
    const editEvidenceForm = document.getElementById('editPhaseEvidenceForm');
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

            // Si hay fotos nuevas en el array, agregarlas al input antes de enviar
            if (selectedEditPhasePhotos.length > 0 && newPhotos) {
                console.log(`Agregando ${selectedEditPhasePhotos.length} fotos nuevas al input antes de enviar:`);
                selectedEditPhasePhotos.forEach((file, index) => {
                    console.log(`  ${index + 1}. ${file.name} (${file.size} bytes)`);
                });

                // Crear un nuevo FileList con todas las fotos seleccionadas
                const dt = new DataTransfer();
                selectedEditPhasePhotos.forEach(function(file) {
                    dt.items.add(file);
                });
                newPhotos.files = dt.files;
                console.log(`Fotos en el input después de asignar: ${newPhotos.files.length}`);
            } else {
                console.log('No hay fotos nuevas para enviar');
            }

             // Verificar beneficiarios
             const beneficiariesInput = this.querySelector('#editPhaseEvidenceBeneficiariesInput');
             console.log('Beneficiarios seleccionados (edición):', beneficiariesInput ? beneficiariesInput.value : 'No encontrado');
             console.log('Tipo de valor:', beneficiariesInput ? typeof beneficiariesInput.value : 'N/A');
             console.log('Longitud del valor:', beneficiariesInput ? beneficiariesInput.value.length : 'N/A');
             
             // Imprimir todos los datos del formulario
             const formData = new FormData(this);
             console.log('=== Datos del FormData (edición) ===');
             for (let [key, value] of formData.entries()) {
                 console.log(`  ${key}: ${value}`);
             }
             console.log('=== Fin del FormData (edición) ===');
 
             // Limpiar el array de fotos nuevas al enviar exitosamente
             selectedEditPhasePhotos = [];

            // Permitir envío normal
        });
    }

    // Event listener para el formulario de creación de evidencia
    const createEvidenceForm = document.getElementById('phaseEvidenceForm');
    if (createEvidenceForm) {
        createEvidenceForm.addEventListener('submit', function(e) {
            console.log('=== Formulario de creación enviado ===');
            e.preventDefault(); // Prevenir envío automático
            e.stopPropagation();
            
            // Verificar beneficiarios ANTES de crear el FormData
            const beneficiariesInput = document.getElementById('createPhaseEvidenceBeneficiariesInput');
            if (beneficiariesInput) {
                console.log('Beneficiarios en input ANTES de FormData:', beneficiariesInput.value);
                console.log('Tipo de valor:', typeof beneficiariesInput.value);
                console.log('Longitud del valor:', beneficiariesInput.value.length);
            } else {
                console.error('ERROR: No se encontró el input createPhaseEvidenceBeneficiariesInput');
            }
            
            // Ahora enviar el formulario
            const form = this;
            const formDataToSend = new FormData(form);
            
            // Verificar beneficiarios DESPUÉS de crear el FormData
            const beneficiariesValue = formDataToSend.get('beneficiaries');
            console.log('Beneficiarios en FormData DESPUÉS de crear:', beneficiariesValue);
            
            // Agregar fotos del array al FormData
            if (window.selectedPhaseEvidencePhotos && window.selectedPhaseEvidencePhotos.length > 0) {
                console.log(`Agregando ${window.selectedPhaseEvidencePhotos.length} fotos al FormData:`);
                window.selectedPhaseEvidencePhotos.forEach((file, index) => {
                    console.log(`  ${index + 1}. ${file.name} (${file.size} bytes)`);
                    // Agregar la foto con el nombre 'photos' como lo espera Django
                    formDataToSend.append('photos', file);
                });
                console.log('Fotos agregadas al FormData');
            } else {
                console.log('No hay fotos seleccionadas en el array window.selectedPhaseEvidencePhotos');
            }
            
            // Imprimir todos los datos del FormData (después de agregar las fotos)
            console.log('=== Datos del FormData ===');
            for (let [key, value] of formDataToSend.entries()) {
                if (value instanceof File) {
                    console.log(`  ${key}: ${value.name} (${value.size} bytes)`);
                } else {
                    console.log(`  ${key}: ${value}`);
                }
            }
            console.log('=== Fin del FormData ===');
            
            fetch(form.action, {
                method: form.method,
                body: formDataToSend,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formDataToSend.get('csrfmiddlewaretoken')
                },
                credentials: 'same-origin'
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => {
                        throw new Error(err.message || 'Error en la respuesta del servidor');
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert(data.message || 'Error al agregar la evidencia');
                }
            })
            .catch(error => {
                console.error('Error al enviar formulario:', error);
                alert('Error de red al agregar la evidencia');
            });
            
            return false;
        });
    }
});

// Función para abrir el modal para crear evidencia de fase
function openPhaseEvidenceModal() {
    console.log('=== Abriendo modal para CREAR nueva evidencia de fase ===');

    const modal = document.getElementById('phaseEvidenceModal');
    if (modal) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }

    // Cambiar título a "Agregar Evidencia a la Fase"
    const titleElement = document.getElementById('phaseEvidenceModalTitle');
    if (titleElement) {
        titleElement.textContent = 'Agregar Evidencia a la Fase';
    }

    // Limpiar completamente el formulario
    const form = document.getElementById('phaseEvidenceForm');
    if (form) {
        form.reset();
    }

    const evidenceIdInput = document.getElementById('phaseEvidenceIdInput');
    if (evidenceIdInput) {
        evidenceIdInput.value = '';
    }

    // Limpiar el input de fotos y el array de fotos
    const photoInput = document.getElementById('phaseEvidencePhotosInput');
    if (photoInput) {
        photoInput.value = '';
    }
    window.selectedPhaseEvidencePhotos = []; // Array para rastrear fotos seleccionadas
    console.log('✓ Array de fotos limpiado al abrir modal');

    // Limpiar y ocultar el preview
    const previewContainer = document.getElementById('phaseEvidencePhotosPreview');
    if (previewContainer) {
        previewContainer.innerHTML = '';
        previewContainer.classList.add('hidden');
    }

    // Limpiar fotos marcadas para eliminar
    const deletePhotosInputs = document.querySelectorAll('#phaseEvidenceForm input[name="photos_to_delete"]');
    deletePhotosInputs.forEach(input => input.remove());

    // Limpiar beneficiarios
    const beneficiariesInput = document.getElementById('createPhaseEvidenceBeneficiariesInput');
    if (beneficiariesInput) {
        beneficiariesInput.value = '';
    }

    // Limpiar lista de beneficiarios seleccionados
    const selectedBeneficiariesContainer = document.getElementById('selectedPhaseEvidenceBeneficiariesContainer');
    if (selectedBeneficiariesContainer) {
        selectedBeneficiariesContainer.classList.add('hidden');
    }

    const selectedBeneficiariesList = document.getElementById('selectedPhaseEvidenceBeneficiariesList');
    if (selectedBeneficiariesList) {
        selectedBeneficiariesList.innerHTML = '<p class="text-sm text-gray-500">No hay beneficiarios seleccionados</p>';
    }

    const selectedBeneficiariesBadge = document.getElementById('selectedPhaseEvidenceBeneficiariesBadge');
    if (selectedBeneficiariesBadge) {
        selectedBeneficiariesBadge.classList.add('hidden');
    }

    const selectedBeneficiariesCount = document.getElementById('selectedPhaseEvidenceBeneficiariesCount');
    if (selectedBeneficiariesCount) {
        selectedBeneficiariesCount.textContent = '0';
    }

    // Limpiar checkboxes de beneficiarios en el modal
    document.querySelectorAll('.phase-evidence-beneficiary-item input[type="checkbox"]').forEach(checkbox => {
        checkbox.checked = false;
    });

    console.log('Estado limpiado para nueva evidencia de fase');
}

// Función para cerrar el modal de evidencia de fase
function closePhaseEvidenceModal() {
    console.log('=== Cerrando modal para crear evidencia de fase ===');

    const modal = document.getElementById('phaseEvidenceModal');
    if (modal) {
        modal.classList.add('hidden');
    }

    document.body.style.overflow = 'auto';

    const form = document.getElementById('phaseEvidenceForm');
    if (form) {
        form.reset();
    }

    const evidenceIdInput = document.getElementById('phaseEvidenceIdInput');
    if (evidenceIdInput) {
        evidenceIdInput.value = '';
    }

    // Limpiar el input de fotos
    const photoInput = document.getElementById('phaseEvidencePhotosInput');
    if (photoInput) {
        photoInput.value = '';
    }

    // Limpiar y ocultar el preview
    const previewContainer = document.getElementById('phaseEvidencePhotosPreview');
    if (previewContainer) {
        previewContainer.innerHTML = '';
        previewContainer.classList.add('hidden');
    }

    // Limpiar fotos marcadas para eliminar
    const deletePhotosInputs = document.querySelectorAll('#phaseEvidenceForm input[name="photos_to_delete"]');
    deletePhotosInputs.forEach(input => input.remove());

    // Limpiar la lista de fotos seleccionadas
    if (typeof selectedPhasePhotos !== 'undefined') {
        selectedPhasePhotos = [];
    }

    // Limpiar el estado de beneficiarios
    const beneficiariesInput = document.getElementById('createPhaseEvidenceBeneficiariesInput');
    if (beneficiariesInput) {
        beneficiariesInput.value = '';
    }

    // Ocultar el badge de beneficiarios seleccionados
    const badgeElement = document.getElementById('selectedPhaseEvidenceBeneficiariesBadge');
    if (badgeElement) {
        badgeElement.classList.add('hidden');
    }

    // Ocultar el contenedor de lista de beneficiarios seleccionados
    const container = document.getElementById('selectedPhaseEvidenceBeneficiariesContainer');
    if (container) {
        container.classList.add('hidden');
    }

    // Limpiar la lista de beneficiarios seleccionados
    const list = document.getElementById('selectedPhaseEvidenceBeneficiariesList');
    if (list) {
        list.innerHTML = '<p class="text-sm text-gray-500">No hay beneficiarios seleccionados</p>';
    }

    // Resetear la variable global de beneficiarios seleccionados
    if (typeof selectedPhaseEvidenceBeneficiaryIds !== 'undefined') {
        selectedPhaseEvidenceBeneficiaryIds = [];
    }
}

// Función para editar evidencia de fase
function openPhaseEditEvidenceModal(button) {
    const evidenceId = button.dataset.evidenceId;
    const projectId = document.querySelector('[data-project-id]').dataset.projectId;
    const phaseId = document.querySelector('[data-phase-id]').dataset.phaseId;

    const modal = document.getElementById('editPhaseEvidenceModal');
    const form = document.getElementById('editPhaseEvidenceForm');
    const titleElement = document.getElementById('editPhaseEvidenceModalTitle');

    if (!modal || !form) {
        console.error('Formulario o modal de edición no encontrado');
        return;
    }

    document.getElementById('editEvidenceId').value = evidenceId;
    document.getElementById('editStartDate').value = button.dataset.startDate;
    document.getElementById('editEndDate').value = button.dataset.endDate;
    document.getElementById('editDescription').value = button.dataset.description;

    // Cambiar título
    titleElement.textContent = 'Editar Evidencia de la Fase';

    // Establecer action del formulario inmediatamente
    const actionUrl = `/dashboard/proyectos/${projectId}/fases/${phaseId}/evidencias/${evidenceId}/editar/`;
    form.action = actionUrl;
    console.log('Action del formulario establecido:', actionUrl);

    // Limpiar completamente el estado anterior
    selectedEditPhasePhotos = [];

    // Limpiar campos ocultos de fotos a eliminar
    const deletePhotosInputs = document.querySelectorAll('#editPhaseEvidenceForm input[name="photos_to_delete"]');
    deletePhotosInputs.forEach(input => input.remove());

    // Limpiar el input de fotos
    const photoInput = document.getElementById('editPhaseEvidencePhotosInput');
    if (photoInput) {
        photoInput.value = '';
    }

    // Limpiar y ocultar previsualización
    const previewContainer = document.getElementById('editPhaseEvidencePhotosPreview');
    if (previewContainer) {
        previewContainer.innerHTML = '';
        previewContainer.classList.add('hidden');
    }

    console.log('Estado limpiado antes de cargar fotos existentes');

    // Cargar las fotos existentes de la evidencia
    loadPhaseEvidencePhotos(evidenceId);

    // Cargar los beneficiarios existentes de la evidencia
    loadPhaseEvidenceBeneficiaries(evidenceId);

    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
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

// Función para cargar las fotos existentes de una evidencia de fase
function loadPhaseEvidencePhotos(evidenceId) {
    const projectId = document.querySelector('[data-project-id]').dataset.projectId;
    const phaseId = document.querySelector('[data-phase-id]').dataset.phaseId;

    console.log(`Cargando fotos existentes para evidencia de fase ${evidenceId}...`);

    fetch(`/dashboard/proyectos/${projectId}/fases/${phaseId}/evidencias/${evidenceId}/fotos/`)
        .then(response => {
            console.log('Response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Fotos recibidas del servidor:', data.photos);
            const previewContainer = document.getElementById('editEvidencePhotosContainer');
            if (!previewContainer) {
                console.error('Contenedor de fotos no encontrado');
                return;
            }

            previewContainer.innerHTML = '';

            if (data.photos && data.photos.length > 0) {
                console.log(`Mostrando ${data.photos.length} fotos existentes en el modal`);

                data.photos.forEach((photo, index) => {
                    const wrapperDiv = document.createElement('div');
                    wrapperDiv.className = 'relative group';
                    wrapperDiv.dataset.photoId = photo.id;

                    const img = document.createElement('img');
                    img.src = '/media/' + photo.photo_url;
                    img.className = 'w-full h-24 object-cover rounded-lg border border-gray-200 cursor-pointer hover:opacity-80 transition-opacity';
                    img.onclick = function() {
                        document.getElementById('photoModalImage').src = '/media/' + photo.photo_url;
                        document.getElementById('photoModal').classList.remove('hidden');
                        document.body.style.overflow = 'hidden';
                    };

                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.name = 'photos_to_delete';
                    checkbox.value = photo.id;
                    checkbox.className = 'hidden';
                    checkbox.id = `photo_delete_${photo.id}`;

                    const removeBtn = document.createElement('button');
                    removeBtn.type = 'button';
                    removeBtn.className = 'absolute -top-2 -right-2 w-8 h-8 bg-red-500 hover:bg-red-600 text-white rounded-full shadow-lg transition-colors flex items-center justify-center z-10';
                    removeBtn.innerHTML = '<i class="fas fa-times text-sm"></i>';
                    removeBtn.onclick = function() {
                        const checkboxEl = document.getElementById(`photo_delete_${photo.id}`);
                        checkboxEl.checked = !checkboxEl.checked;
                        console.log(`Foto ${photo.id} marcada para ${checkboxEl.checked ? 'eliminar' : 'conservar'}`);

                        if (checkboxEl.checked) {
                            wrapperDiv.classList.add('border-4', 'border-red-500', 'opacity-60');
                            removeBtn.classList.remove('bg-red-500', 'hover:bg-red-600');
                            removeBtn.classList.add('bg-green-500', 'hover:bg-green-600');
                            removeBtn.innerHTML = '<i class="fas fa-undo text-sm"></i>';
                        } else {
                            wrapperDiv.classList.remove('border-4', 'border-red-500', 'opacity-60');
                            removeBtn.classList.remove('bg-green-500', 'hover:bg-green-600');
                            removeBtn.classList.add('bg-red-500', 'hover:bg-red-600');
                            removeBtn.innerHTML = '<i class="fas fa-times text-sm"></i>';
                        }
                    };

                    wrapperDiv.appendChild(checkbox);
                    wrapperDiv.appendChild(img);
                    wrapperDiv.appendChild(removeBtn);
                    previewContainer.appendChild(wrapperDiv);
                    console.log(`Foto existente agregada al preview: ID=${photo.id}`);
                });

                console.log(`Total de elementos en preview después de cargar fotos existentes: ${previewContainer.children.length}`);
            } else {
                previewContainer.innerHTML = '<p class="text-sm text-gray-500 col-span-full">No hay fotos asociadas</p>';
            }
        })
        .catch(error => {
            console.error('Error al cargar fotos existentes:', error);
            const previewContainer = document.getElementById('editEvidencePhotosContainer');
            if (previewContainer) {
                previewContainer.innerHTML = '<p class="text-sm text-red-500 col-span-full">Error al cargar fotos</p>';
            }
        });
}

// Función para cargar los beneficiarios existentes de una evidencia de fase
function loadPhaseEvidenceBeneficiaries(evidenceId) {
    const projectId = document.querySelector('[data-project-id]').dataset.projectId;
    const phaseId = document.querySelector('[data-phase-id]').dataset.phaseId;

    console.log(`=== Cargando beneficiarios existentes para evidencia de fase ${evidenceId} ===`);
    console.log(`Project ID: ${projectId}, Phase ID: ${phaseId}`);
    console.log(`URL: /dashboard/proyectos/${projectId}/fases/${phaseId}/evidencias/${evidenceId}/beneficiarios/`);

    fetch(`/dashboard/proyectos/${projectId}/fases/${phaseId}/evidencias/${evidenceId}/beneficiarios/`)
        .then(response => {
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Beneficiarios recibidos del servidor:', data.beneficiaries);

            // Limpiar estado anterior
            selectedPhaseEvidenceBeneficiaryIds = [];

            // Actualizar el input oculto con los IDs (usar el input de edición)
            const beneficiariesInput = document.getElementById('editPhaseEvidenceBeneficiariesInput');
            if (beneficiariesInput) {
                const ids = data.beneficiaries ? data.beneficiaries.map(b => b.id.toString()) : [];
                beneficiariesInput.value = ids.join(',');

                console.log('Beneficiarios cargados:', ids);
                console.log('Tipo de datos:', ids.map(id => typeof id));
                console.log('Valor del input:', beneficiariesInput.value);
                console.log('Longitud de ids:', ids.length);

                // Actualizar el badge
                const badgeElement = document.getElementById('selectedPhaseEvidenceBeneficiariesBadge');
                const countElement = document.getElementById('selectedPhaseEvidenceBeneficiariesCount');

                if (badgeElement) {
                    if (ids.length > 0) {
                        badgeElement.textContent = ids.length + ' seleccionados';
                        badgeElement.classList.remove('hidden');
                        console.log('Badge mostrado:', badgeElement.textContent);
                    } else {
                        badgeElement.classList.add('hidden');
                        console.log('Badge oculto (no hay beneficiarios)');
                    }
                }

                if (countElement) {
                    countElement.textContent = ids.length;
                }

                // Marcar los checkboxes en el modal de selección
                const checkboxes = document.querySelectorAll('.phase-evidence-beneficiary-item input[type="checkbox"]');
                console.log('Encontrados', checkboxes.length, 'checkboxes en el modal de selección');
                
                checkboxes.forEach(checkbox => {
                    const beneficiaryId = checkbox.closest('.phase-evidence-beneficiary-item').dataset.id;
                    const isChecked = ids.includes(beneficiaryId);
                    checkbox.checked = isChecked;
                    console.log(`Checkbox ID ${beneficiaryId} (${typeof beneficiaryId}): ${isChecked}`);
                });

                selectedPhaseEvidenceBeneficiaryIds = ids.map(id => parseInt(id));
            } else {
                console.error('ERROR: No se encontró el input editPhaseEvidenceBeneficiariesInput');
            }
        })
        .catch(error => {
            console.error('Error al cargar beneficiarios:', error);
        });
}

// Función para quitar un beneficiario seleccionado del modal de edición
function removePhaseEvidenceBeneficiary(id) {
    const beneficiariesInput = document.getElementById('phaseEvidenceBeneficiariesInput');
    const currentIds = beneficiariesInput.value.split(',').filter(bId => bId.trim() !== '');

    const newIds = currentIds.filter(bId => bId !== id.toString());

    // Actualizar el input
    beneficiariesInput.value = newIds.join(',');

    // Actualizar lista visual
    const selectedIds = newIds.map(id => parseInt(id));
    updateSelectedBeneficiariesList(selectedIds);

    // Actualizar variable global si existe
    if (typeof selectedPhaseEvidenceBeneficiaryIds !== 'undefined') {
        selectedPhaseEvidenceBeneficiaryIds = selectedIds;
    }

    // Marcar checkbox como no seleccionado
    const checkbox = document.querySelector(`.phase-evidence-beneficiary-item[data-id="${id}"] input[type="checkbox"]`);
    if (checkbox) {
        checkbox.checked = false;
    }

    updatePhaseEvidenceBeneficiariesCount();
}

// Función para eliminar foto en el modal de edición de evidencia de fase
function deletePhaseEvidencePhoto(button) {
    const photoId = button.dataset.photoId;
    const checkbox = document.getElementById(`photo_delete_${photoId}`);

    if (checkbox) {
        checkbox.checked = !checkbox.checked;
        console.log(`Foto ${photoId} marcada para ${checkbox.checked ? 'eliminar' : 'conservar'}`);
    }
}

// Modal para eliminar evidencia de fase
function confirmPhaseDeleteEvidence(button) {
    const evidenceId = button.dataset.evidenceId;
    const projectId = document.querySelector('[data-project-id]').dataset.projectId;
    const phaseId = document.querySelector('[data-phase-id]').dataset.phaseId;

    const form = document.getElementById('deletePhaseEvidenceFormAction');
    form.action = `/dashboard/proyectos/${projectId}/fases/${phaseId}/evidencias/${evidenceId}/eliminar/`;

    document.getElementById('deletePhaseEvidenceId').value = evidenceId;

    document.getElementById('deletePhaseEvidenceModal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeDeletePhaseEvidenceModal() {
    document.getElementById('deletePhaseEvidenceModal').classList.add('hidden');
    document.body.style.overflow = 'auto';
    const form = document.getElementById('deletePhaseEvidenceFormAction');
    form.reset();
}

// Funciones para modal de beneficiarios de fase (phase_edit.html)
function openBeneficiariesModalForPhase() {
    document.getElementById('beneficiariesModalForPhase').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

// Agregar nuevos beneficiarios seleccionados a la lista
function addSelectedBeneficiaryPhase(item) {
    const container = document.getElementById('selectedBeneficiariesListPhase');
    const id = item.dataset.id;

    const beneficiaryItem = item.cloneNode(true);
    beneficiaryItem.onclick = function() { removeSelectedBeneficiaryPhase(id); };
    beneficiaryItem.innerHTML = `
        <div class="flex items-center justify-between p-2 bg-white rounded-lg border border-gray-200">
            <p class="text-sm font-medium text-gray-900">${item.dataset.name}</p>
            <button type="button" class="text-red-500 hover:text-red-700 transition-colors">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    container.appendChild(beneficiaryItem);
}

function removeSelectedBeneficiaryPhase(id) {
    const container = document.getElementById('selectedBeneficiariesListPhase');
    const items = container.querySelectorAll('[data-id="' + id + '"]');
    items.forEach(item => item.remove());

    updateBeneficiariesCountPhase();

    // Desmarcar el checkbox correspondiente en la lista original
    const checkbox = document.querySelector('.beneficiary-item-for-phase[data-id="' + id + '"] input[type="checkbox"]');
    if (checkbox) {
        checkbox.checked = false;
    }
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
    console.log('=== Inicializando fotos de evidencias de fase ===');
    setTimeout(function() {
        const containers = document.querySelectorAll('[id^="phase-evidence-photos-"]');
        console.log(`Encontrados ${containers.length} contenedores de fotos`);

        if (containers.length === 0) {
            console.log('No se encontraron contenedores de fotos de fase');
            return;
        }

        containers.forEach(function(container) {
            const photos = container.querySelectorAll('.evidence-photo');
            const totalPhotos = photos.length;

            console.log(`Configurando evidencia de fase ${container.id.replace('phase-evidence-photos-', '')} con ${totalPhotos} fotos`);

            // Solo manejar navegación si hay más de 6 fotos
            const parent = container.parentElement;
            const navButtons = parent.querySelectorAll('button');
            console.log(`  - Botones de navegación encontrados: ${navButtons.length}`);

            if (totalPhotos > 6) {
                console.log('  - Más de 6 fotos, inicializando navegación');
                // Inicializar la página actual en 0
                container.setAttribute('data-current-page', '0');

                // Asegurar que se muestren solo las primeras 6 fotos
                const photosPerPage = 6;
                photos.forEach(function(photo, index) {
                    if (index < photosPerPage) {
                        photo.style.display = 'block';
                    } else {
                        photo.style.display = 'none';
                    }
                });
                console.log(`  - Mostrando fotos 0-5 de ${totalPhotos}`);
            } else {
                console.log('  - 6 fotos o menos, todas visibles');
                // Asegurar que todas las fotos sean visibles
                photos.forEach(function(photo) {
                    photo.style.display = 'block';
                });
            }
        });
    }, 200);
});
