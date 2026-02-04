// Funciones para el modal de selección de beneficiarios en proyectos

// Variables globales
let selectedBeneficiaryIds = [];

function openBeneficiaryModal() {
    console.log('=== Abriendo modal de selección de beneficiarios ===');
    const modal = document.getElementById('beneficiaryModal');
    if (modal) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';

        // Obtener los IDs de beneficiarios ya seleccionados
        const beneficiariesInput = document.getElementById('beneficiariesInput');
        const existingBeneficiaries = beneficiariesInput.value ? beneficiariesInput.value.split(',').map(id => id.trim()).filter(id => id !== '') : [];
        selectedBeneficiaryIds = [...existingBeneficiaries];

        console.log('Beneficiarios ya seleccionados:', existingBeneficiaries);

        // Marcar los beneficiarios seleccionados
        const items = document.querySelectorAll('.beneficiary-item');
        items.forEach(item => {
            const id = item.dataset.id;
            const indicator = item.querySelector('.checkbox-indicator');
            const checkIcon = item.querySelector('.checkbox-indicator i');

            if (selectedBeneficiaryIds.includes(id)) {
                indicator.classList.remove('bg-gray-300');
                indicator.classList.add('bg-[#8a4534]', 'border-[#8a4534]');
                checkIcon.classList.remove('hidden');
            } else {
                indicator.classList.remove('bg-[#8a4534]', 'border-[#8a4534]');
                indicator.classList.add('bg-gray-300');
                checkIcon.classList.add('hidden');
            }
        });

        updateSelectedCount();
    }
}

function closeBeneficiaryModal() {
    console.log('Cerrando modal de selección de beneficiarios');
    const modal = document.getElementById('beneficiaryModal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = 'auto';
    }
}

function toggleBeneficiary(item) {
    const beneficiaryId = item.dataset.id;
    const indicator = item.querySelector('.checkbox-indicator');
    const checkIcon = item.querySelector('.checkbox-indicator i');

    if (selectedBeneficiaryIds.includes(beneficiaryId)) {
        selectedBeneficiaryIds = selectedBeneficiaryIds.filter(id => id !== beneficiaryId);
        indicator.classList.remove('bg-[#8a4534]', 'border-[#8a4534]');
        indicator.classList.add('bg-gray-300');
        checkIcon.classList.add('hidden');
    } else {
        selectedBeneficiaryIds.push(beneficiaryId);
        indicator.classList.remove('bg-gray-300');
        indicator.classList.add('bg-[#8a4534]', 'border-[#8a4534]');
        checkIcon.classList.remove('hidden');
    }

    updateSelectedCount();
}

function updateSelectedCount() {
    const countElement = document.getElementById('selectedCount');
    if (countElement) {
        countElement.textContent = selectedBeneficiaryIds.length;
    }
}

function addSelectedBeneficiaries() {
    console.log('Agregando beneficiarios seleccionados:', selectedBeneficiaryIds);

    const input = document.getElementById('beneficiariesInput');
    if (input) {
        input.value = selectedBeneficiaryIds.join(',');
    }

    const listElement = document.getElementById('selectedBeneficiariesList');
    if (listElement) {
        const selectedItems = document.querySelectorAll('.beneficiary-item');
        
        // Limpiar la lista actual
        listElement.innerHTML = '';

        selectedItems.forEach(item => {
            const beneficiaryId = item.dataset.id;
            if (selectedBeneficiaryIds.includes(beneficiaryId)) {
                const name = item.dataset.name;
                const dpi = item.dataset.dpi;
                const initials = name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();

                const newItem = document.createElement('div');
                newItem.className = 'beneficiary-selected flex items-center justify-between bg-gray-50 rounded-lg p-3';
                newItem.dataset.id = beneficiaryId;
                newItem.innerHTML = `
                    <div class="flex items-center space-x-3">
                        <div class="w-10 h-10 rounded-full bg-gradient-to-br from-[#8a4534] to-[#334e76] flex items-center justify-center text-white text-sm font-semibold">
                            <span>${initials}</span>
                        </div>
                        <div>
                            <p class="font-medium text-gray-900">${name}</p>
                            <p class="text-sm text-gray-500">${dpi ? 'DPI: ' + dpi : 'Sin DPI'}</p>
                        </div>
                    </div>
                    <button type="button" onclick="removeBeneficiary('${beneficiaryId}')" class="text-red-500 hover:text-red-700 transition-colors">
                        <i class="fas fa-times text-lg"></i>
                    </button>
                `;
                listElement.appendChild(newItem);
            }
        });

        // Si no hay beneficiarios seleccionados, mostrar mensaje
        if (selectedBeneficiaryIds.length === 0) {
            listElement.innerHTML = `
                <div class="text-center text-gray-500 py-8">
                    <i class="fas fa-users text-4xl mb-2"></i>
                    <p>No hay beneficiarios seleccionados</p>
                    <p class="text-sm">Haga clic en "Agregar Beneficiario" para seleccionar beneficiarios del sistema</p>
                </div>
            `;
        }
    }

    updateSelectedCount();
    closeBeneficiaryModal();
}

function removeBeneficiary(beneficiaryId) {
    const listElement = document.getElementById('selectedBeneficiariesList');
    const item = listElement.querySelector(`[data-id="${beneficiaryId}"]`);
    if (item) {
        item.remove();
    }

    selectedBeneficiaryIds = selectedBeneficiaryIds.filter(id => id !== beneficiaryId);

    const input = document.getElementById('beneficiariesInput');
    if (input) {
        const currentIds = input.value.split(',').filter(id => id.trim());
        const newIds = currentIds.filter(id => id !== beneficiaryId);
        input.value = newIds.join(',');
    }

    // Si no hay más beneficiarios, mostrar mensaje
    if (selectedBeneficiaryIds.length === 0) {
        listElement.innerHTML = `
            <div class="text-center text-gray-500 py-8">
                <i class="fas fa-users text-4xl mb-2"></i>
                <p>No hay beneficiarios seleccionados</p>
                <p class="text-sm">Haga clic en "Agregar Beneficiario" para seleccionar beneficiarios del sistema</p>
            </div>
        `;
    }

    updateSelectedCount();
}

function filterBeneficiaries() {
    const searchTerm = document.getElementById('beneficiarySearch').value.toLowerCase();
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

// Cerrar modal al hacer clic fuera
document.getElementById('beneficiaryModal')?.addEventListener('click', function(e) {
    if (e.target === this) closeBeneficiaryModal();
});

// Cerrar modal con Escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const modal = document.getElementById('beneficiaryModal');
        if (modal && !modal.classList.contains('hidden')) {
            closeBeneficiaryModal();
        }
    }
});

// Inicializar contador
document.addEventListener('DOMContentLoaded', function() {
    const countElement = document.getElementById('selectedCount');
    if (countElement) {
        const input = document.getElementById('beneficiariesInput');
        if (input && input.value) {
            selectedBeneficiaryIds = input.value.split(',').filter(id => id.trim());
            countElement.textContent = selectedBeneficiaryIds.length;
        }
    }
});
