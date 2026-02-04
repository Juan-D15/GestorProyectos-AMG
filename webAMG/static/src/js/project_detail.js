// Funciones específicas para la página de detalles del proyecto

// Scroll suave hacia la sección de evidencias cuando haya filtros activos
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const hasFilters = urlParams.has('filter_start_date') ||
                      urlParams.has('filter_end_date') ||
                      urlParams.has('filter_year') ||
                      window.location.hash === '#evidencias-section';

    if (hasFilters) {
        setTimeout(function() {
            const evidenciasSection = document.getElementById('evidencias-section');
            if (evidenciasSection) {
                evidenciasSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }, 300);
    }
});
