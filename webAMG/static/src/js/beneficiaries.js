// Beneficiarios seleccionados
let selectedBeneficiaries = [];

// Debug: Verificar que el script se cargó
console.log('beneficiaries.js cargado correctamente');

// Abrir modal de beneficiarios
function openBeneficiaryModal() {
    console.log('Abriendo modal de beneficiarios...');
    const modal = document.getElementById('beneficiaryModal');
    console.log('Modal encontrado:', modal);
    
    if (modal) {
        modal.classList.remove('hidden');
    }
    
    // Limpiar el campo de búsqueda
    const searchInput = document.getElementById('beneficiarySearch');
    if (searchInput) {
        searchInput.value = '';
    }
    
    // Mostrar todos los beneficiarios
    const beneficiariesList = document.getElementById('beneficiariesList');
    console.log('beneficiariesList encontrado:', beneficiariesList);
    console.log('Contenido de beneficiariesList:', beneficiariesList ? beneficiariesList.innerHTML : 'null');
    
    const items = document.querySelectorAll('#beneficiariesList .beneficiary-item');
    console.log('Items de beneficiarios encontrados:', items.length);
    items.forEach(item => item.classList.remove('hidden'));
    
    // Marcar los beneficiarios que ya están seleccionados en el formulario
    const selectedList = document.getElementById('selectedBeneficiariesList');
    const selectedElements = selectedList ? selectedList.querySelectorAll('.beneficiary-selected') : [];
    console.log('Beneficiarios ya seleccionados:', selectedElements.length);
    
    // Limpiar selección actual en el modal
    selectedBeneficiaries = [];
    const checkboxes = document.querySelectorAll('#beneficiariesList .checkbox-indicator');
    const checkIcons = document.querySelectorAll('#beneficiariesList .fa-check');
    checkboxes.forEach(cb => {
        cb.classList.remove('bg-[#8a4534]', 'border-[#8a4534]');
        cb.classList.add('border-gray-300');
    });
    checkIcons.forEach(icon => icon.classList.add('hidden'));
    
    // Marcar los que ya están en el formulario
    selectedElements.forEach(el => {
        const id = el.getAttribute('data-id');
        const modalItem = document.querySelector(`#beneficiariesList .beneficiary-item[data-id="${id}"]`);
        if (modalItem) {
            const name = modalItem.getAttribute('data-name');
            const dpi = modalItem.getAttribute('data-dpi');
            const initials = modalItem.querySelector('.rounded-full span').textContent;
            const checkbox = modalItem.querySelector('.checkbox-indicator');
            const checkIcon = checkbox.querySelector('.fa-check');
            
            selectedBeneficiaries.push({ id, name, dpi, initials });
            checkbox.classList.add('bg-[#8a4534]', 'border-[#8a4534]');
            checkbox.classList.remove('border-gray-300');
            checkIcon.classList.remove('hidden');
        }
    });
    
    const selectedCount = document.getElementById('selectedCount');
    if (selectedCount) {
        selectedCount.textContent = selectedBeneficiaries.length;
    }
    console.log('Beneficiarios seleccionados después de abrir modal:', selectedBeneficiaries.length);
}

// Cerrar modal de beneficiarios
function closeBeneficiaryModal() {
    console.log('Cerrando modal de beneficiarios...');
    const modal = document.getElementById('beneficiaryModal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

// Toggle selección de beneficiario
function toggleBeneficiary(element) {
    const id = element.getAttribute('data-id');
    const name = element.getAttribute('data-name');
    const dpi = element.getAttribute('data-dpi');
    const initials = element.querySelector('.rounded-full span').textContent;
    
    const checkbox = element.querySelector('.checkbox-indicator');
    const checkIcon = checkbox.querySelector('.fa-check');
    
    const existingBeneficiary = selectedBeneficiaries.find(b => b.id === id);
    
    if (existingBeneficiary) {
        // Deseleccionar
        selectedBeneficiaries = selectedBeneficiaries.filter(b => b.id !== id);
        checkbox.classList.remove('bg-[#8a4534]', 'border-[#8a4534]');
        checkbox.classList.add('border-gray-300');
        checkIcon.classList.add('hidden');
    } else {
        // Seleccionar
        selectedBeneficiaries.push({ id, name, dpi, initials });
        checkbox.classList.add('bg-[#8a4534]', 'border-[#8a4534]');
        checkbox.classList.remove('border-gray-300');
        checkIcon.classList.remove('hidden');
    }
    
    const selectedCount = document.getElementById('selectedCount');
    if (selectedCount) {
        selectedCount.textContent = selectedBeneficiaries.length;
    }
    console.log('Beneficiario seleccionado/deseleccionado:', id, 'Total:', selectedBeneficiaries.length);
}

// Filtrar beneficiarios
function filterBeneficiaries() {
    const searchTerm = document.getElementById('beneficiarySearch').value.toLowerCase().trim();
    const items = document.querySelectorAll('#beneficiariesList .beneficiary-item');
    
    console.log('Filtrando beneficiarios con término:', searchTerm);
    
    // Si el término de búsqueda está vacío, mostrar todos
    if (searchTerm === '') {
        items.forEach(item => item.classList.remove('hidden'));
        return;
    }
    
    items.forEach(item => {
        const name = item.getAttribute('data-name').toLowerCase();
        const dpi = item.getAttribute('data-dpi').toLowerCase();
        const community = item.getAttribute('data-community').toLowerCase();
        
        // Filtrar por nombre, DPI o comunidad
        if (name.includes(searchTerm) || 
            (dpi && dpi.includes(searchTerm)) || 
            (community && community.includes(searchTerm))) {
            item.classList.remove('hidden');
        } else {
            item.classList.add('hidden');
        }
    });
}

// Agregar beneficiarios seleccionados
function addSelectedBeneficiaries() {
    console.log('Agregando beneficiarios seleccionados...');
    const list = document.getElementById('selectedBeneficiariesList');
    
    if (selectedBeneficiaries.length === 0) {
        console.log('No hay beneficiarios seleccionados');
        return;
    }
    
    console.log('Beneficiarios a agregar:', selectedBeneficiaries);
    
    // Eliminar el mensaje de "No hay beneficiarios seleccionados" si existe
    const emptyMessage = list.querySelector('.text-center');
    if (emptyMessage) {
        emptyMessage.remove();
    }
    
    // Agregar cada beneficiario seleccionado
    selectedBeneficiaries.forEach(b => {
        // Verificar si el beneficiario ya está en la lista (ambas clases posibles)
        const existingElement = list.querySelector(`.beneficiary-selected[data-id="${b.id}"]`) ||
                           list.querySelector(`.selected-beneficiary[data-id="${b.id}"]`);
        if (existingElement) {
            console.log('Beneficiario ya existe en la lista:', b.id);
            return; // Ya existe, no agregar de nuevo
        }
        
        const beneficiaryHtml = `
            <div class="beneficiary-selected flex items-center justify-between bg-gray-50 rounded-lg p-3" data-id="${b.id}">
                <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 rounded-full bg-gradient-to-br from-[#8a4534] to-[#334e76] flex items-center justify-center text-white text-sm font-semibold">
                        <span>${b.initials}</span>
                    </div>
                    <div>
                        <p class="font-medium text-gray-900">${b.name}</p>
                        <p class="text-sm text-gray-500">${b.dpi ? 'DPI: ' + b.dpi : 'Sin DPI'}</p>
                    </div>
                </div>
                <button type="button" onclick="removeBeneficiary('${b.id}')" class="text-red-500 hover:text-red-700 transition-colors">
                    <i class="fas fa-times text-lg"></i>
                </button>
            </div>
        `;
        list.insertAdjacentHTML('beforeend', beneficiaryHtml);
        console.log('Beneficiario agregado al formulario:', b.id);
    });
    
    // Actualizar el input hidden principal con todos los IDs de beneficiarios
    const beneficiariesInput = document.getElementById('beneficiariesInput');
    if (beneficiariesInput && selectedBeneficiaries.length > 0) {
        const beneficiaryIds = selectedBeneficiaries.map(b => b.id);
        beneficiariesInput.value = beneficiaryIds.join(',');
        console.log('IDs de beneficiarios enviados al formulario:', beneficiaryIds);
    }
    
    closeBeneficiaryModal();
}

// Eliminar beneficiario de la lista
function removeBeneficiary(id) {
    console.log('Eliminando beneficiario:', id);
    selectedBeneficiaries = selectedBeneficiaries.filter(b => b.id !== id);
    
    // Buscar el elemento con ambas clases posibles
    const element = document.querySelector(`.beneficiary-selected[data-id="${id}"]`) ||
                   document.querySelector(`.selected-beneficiary[data-id="${id}"]`);
    if (element) {
        element.remove();
    }
    
    // Si no hay beneficiarios, mostrar mensaje
    if (selectedBeneficiaries.length === 0) {
        document.getElementById('selectedBeneficiariesList').innerHTML = `
            <div class="text-center text-gray-500 py-8">
                <i class="fas fa-users text-4xl mb-2"></i>
                <p>No hay beneficiarios seleccionados</p>
                <p class="text-sm">Haga clic en "Agregar Beneficiario" para seleccionar beneficiarios del sistema</p>
            </div>
        `;
    }
    
    // Actualizar el input hidden con los IDs restantes
    const beneficiariesInput = document.getElementById('beneficiariesInput');
    if (beneficiariesInput) {
        if (selectedBeneficiaries.length > 0) {
            const beneficiaryIds = selectedBeneficiaries.map(b => b.id);
            beneficiariesInput.value = beneficiaryIds.join(',');
            console.log('IDs de beneficiarios actualizados:', beneficiaryIds);
        } else {
            beneficiariesInput.value = '';
            console.log('Input de beneficiarios vaciado');
        }
    }
    
    console.log('Beneficiarios restantes:', selectedBeneficiaries.length);
}
