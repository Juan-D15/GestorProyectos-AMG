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
            // Si el elemento también tiene data-phase-id, no navegar (es una página de detalle de fase)
            if (this.hasAttribute('data-phase-id')) {
                return;
            }
            const projectId = this.getAttribute('data-project-id');
            window.location.href = `/dashboard/proyectos/${projectId}/`;
        });
    });

    // Verificar si hay parámetro para mostrar inactivos
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('show_inactive') === 'true') {
        setTimeout(loadInactiveProjects, 500);
    }
});

// Editar proyecto
function editProject(projectId) {
    window.location.href = `/dashboard/proyectos/${projectId}/editar/`;
}

// Eliminar proyecto (ahora es soft delete)
function deleteProject(projectId) {
    window.location.href = `/dashboard/proyectos/${projectId}/eliminar/`;
}

// ====================
// Funciones para Proyectos Inactivos
// ====================

let showingInactiveProjects = false;

function toggleInactiveProjects() {
    const activeSection = document.getElementById('activeProjectsSection');
    const inactiveSection = document.getElementById('inactiveProjectsSection');
    const showInactiveBtn = document.getElementById('showInactiveBtn');
    
    showingInactiveProjects = !showingInactiveProjects;
    
    if (showingInactiveProjects) {
        // Mostrar proyectos inactivos
        activeSection.classList.add('hidden');
        inactiveSection.classList.remove('hidden');
        showInactiveBtn.innerHTML = `
            <div class="w-12 h-12 rounded-lg bg-green-500/10 flex items-center justify-center">
                <i class="fas fa-list text-xl text-green-600"></i>
            </div>
            <div>
                <h3 class="text-lg font-semibold text-gray-900">Ver Activos</h3>
                <p class="text-sm text-gray-500">Volver a proyectos activos</p>
            </div>
        `;
        loadInactiveProjects();
    } else {
        // Mostrar proyectos activos
        inactiveSection.classList.add('hidden');
        activeSection.classList.remove('hidden');
        showInactiveBtn.innerHTML = `
            <div class="w-12 h-12 rounded-lg bg-gray-500/10 flex items-center justify-center">
                <i class="fas fa-archive text-xl text-gray-500"></i>
            </div>
            <div>
                <h3 class="text-lg font-semibold text-gray-900">Ver Inactivos</h3>
                <p class="text-sm text-gray-500">Proyectos desactivados</p>
            </div>
        `;
    }
}

function loadInactiveProjects() {
    const tableBody = document.getElementById('inactiveProjectsTableBody');
    
    if (!tableBody) return;
    
    // Mostrar loader
    tableBody.innerHTML = `
        <tr>
            <td colspan="6" class="text-center py-8">
                <div class="flex items-center justify-center">
                    <i class="fas fa-spinner fa-spin text-2xl text-gray-400 mr-3"></i>
                    <span class="text-gray-600">Cargando proyectos...</span>
                </div>
            </td>
        </tr>
    `;
    
    // Obtener parámetros de filtros actuales
    const urlParams = new URLSearchParams(window.location.search);
    
    // Llamada a API para obtener proyectos inactivos
    fetch(`/api/v1/projects/?show_inactive=true&${urlParams.toString()}`)
        .then(response => response.json())
        .then(data => {
            if (data.success && data.data.projects && data.data.projects.length > 0) {
                tableBody.innerHTML = data.data.projects.map(project => `
                    <tr class="border-b border-gray-200 bg-gray-50">
                        <td class="py-3 px-4">
                            <div class="flex items-center space-x-3">
                                <div class="w-10 h-10 rounded-lg bg-gray-300 flex items-center justify-center">
                                    <i class="fas fa-project-diagram text-gray-500"></i>
                                </div>
                                <div>
                                    <p class="font-medium text-gray-700">${project.project_name}</p>
                                    ${project.project_code ? `<p class="text-xs text-gray-400">${project.project_code}</p>` : ''}
                                </div>
                            </div>
                        </td>
                        <td class="py-3 px-4">
                            <p class="text-sm text-gray-600">
                                ${project.municipality || 'No especificado'}
                                ${project.department ? `<br><span class="text-xs">${project.department}</span>` : ''}
                            </p>
                        </td>
                        <td class="py-3 px-4">
                            <span class="px-2 py-1 rounded-full text-xs font-medium bg-gray-200 text-gray-600">
                                ${project.status === 'planificado' ? 'Planificado' : 
                                  project.status === 'en_progreso' ? 'En Progreso' :
                                  project.status === 'pausado' ? 'Pausado' :
                                  project.status === 'completado' ? 'Completado' :
                                  project.status === 'cancelado' ? 'Cancelado' : project.status}
                            </span>
                        </td>
                        <td class="py-3 px-4">
                            <p class="text-sm text-gray-600">${project.updated_at ? new Date(project.updated_at).toLocaleDateString('es-ES') : 'N/A'}</p>
                        </td>
                        <td class="py-3 px-4">
                            <div class="flex items-center justify-end space-x-2">
                                <a href="/dashboard/proyectos/${project.id}/reactivar/" class="px-3 py-2 text-sm font-medium text-green-600 hover:text-green-700 hover:bg-green-50 rounded-lg transition-colors" title="Reactivar">
                                    <i class="fas fa-undo"></i>
                                </a>
                            </div>
                        </td>
                    </tr>
                `).join('');
            } else {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="6" class="text-center py-12">
                            <i class="fas fa-folder-open text-4xl text-gray-300 mb-3"></i>
                            <h3 class="text-lg font-semibold text-gray-900 mb-2">No hay proyectos desactivados</h3>
                            <p class="text-gray-500">
                                <a href="/dashboard/proyectos/crear/" class="inline-flex items-center space-x-2 px-6 py-3 bg-[#8a4534] hover:bg-[#a05240] text-white font-medium rounded-lg transition-colors">
                                    <i class="fas fa-plus"></i>
                                    <span>Crear Proyecto</span>
                                </a>
                            </p>
                        </td>
                    </tr>
                `;
            }
        })
        .catch(error => {
            console.error('Error al cargar proyectos inactivos:', error);
            tableBody.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center py-8">
                        <i class="fas fa-exclamation-circle text-2xl text-red-400 mb-3"></i>
                        <p class="text-red-600">Error al cargar proyectos inactivos</p>
                    </td>
                </tr>
            `;
        });
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
