// Funciones para el modal de selección de beneficiarios en evidencias

// Variables globales
let selectedBeneficiaryIds = [];
let allBeneficiaryIds = [];

// Abrir modal de beneficiarios
function openBeneficiariesModal() {
    console.log('=== Abriendo modal de selección de beneficiarios ===');
    
    // Obtener todos los elementos del modal
    const items = document.querySelectorAll('.beneficiary-item');
    
    // Obtener los IDs de beneficiarios ya seleccionados
    const beneficiariesInput = document.getElementById('evidenceBeneficiariesInput');
    const existingBeneficiaries = beneficiariesInput.value ? beneficiariesInput.value.split(',').map(id => id.trim()).filter(id => id !== '') : [];
    
    console.log('Beneficiarios ya seleccionados:', existingBeneficiaries);
    console.log('Items de beneficiarios encontrados:', items.length);
    
    // Guardar todos los IDs de beneficiarios disponibles y marcar los seleccionados
    allBeneficiaryIds = [];
    selectedBeneficiaryIds = [...existingBeneficiaries];
    
    items.forEach(function(item) {
        const id = item.dataset.id;
        allBeneficiaryIds.push(id);
        
        // Verificar si este beneficiario está seleccionado
        const isSelected = existingBeneficiaries.includes(id);
        const checkbox = item.querySelector('input[type="checkbox"]');
        
        if (checkbox) {
            checkbox.checked = isSelected;
        }
    });
    
    console.log('Total de beneficiarios disponibles:', allBeneficiaryIds.length);
    console.log('Total de beneficiarios seleccionados:', selectedBeneficiaryIds.length);
    
    // Actualizar contador de seleccionados
    updateSelectedCount();
    
    // Mostrar el modal
    document.getElementById('beneficiariesModal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    
    // Limpiar el campo de búsqueda
    const searchInput = document.getElementById('beneficiarySearchInput');
    if (searchInput) {
        searchInput.value = '';
        searchInput.focus();
    }
    
    console.log('=== Modal de beneficiarios abierto ===');
}

// Cerrar modal de beneficiarios
function closeBeneficiariesModal() {
    console.log('Cerrando modal de selección de beneficiarios');
    document.getElementById('beneficiariesModal').classList.add('hidden');
    document.body.style.overflow = 'auto';
}

// Actualizar contador de seleccionados
function updateSelectedCount() {
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

// Confirmar selección de beneficiarios
function confirmBeneficiariesSelection() {
    const checkboxes = document.querySelectorAll('.beneficiary-item input[type="checkbox"]:checked');
    const selectedIds = Array.from(checkboxes).map(cb => cb.closest('.beneficiary-item').dataset.id);
    
    console.log('Confirmando selección de beneficiarios:', selectedIds);
    
    // Actualizar el input oculto con los IDs seleccionados
    document.getElementById('evidenceBeneficiariesInput').value = selectedIds.join(',');
    updateSelectedCount();
    closeBeneficiariesModal();
    
    // Mostrar mensaje de confirmación
    if (selectedIds.length > 0) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50';
        messageDiv.textContent = `${selectedIds.length} beneficiario(s) seleccionado(s)`;
        document.body.appendChild(messageDiv);
        
        setTimeout(function() {
            messageDiv.remove();
        }, 3000);
    }
}

// Filtrar beneficiarios
function filterBeneficiaries() {
    const searchTerm = document.getElementById('beneficiarySearchInput').value.toLowerCase();
    const items = document.querySelectorAll('.beneficiary-item');
    
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
}

// Event listeners
document.getElementById('beneficiariesModal')?.addEventListener('click', function(e) {
    if (e.target === this) {
        closeBeneficiariesModal();
    }
});

document.getElementById('beneficiarySearchInput')?.addEventListener('input', filterBeneficiaries);

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeBeneficiariesModal();
    }
});
