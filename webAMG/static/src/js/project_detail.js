// Funciones específicas para la página de detalles del proyecto

// Scroll suave hacia la sección de evidencias cuando haya filtros activos o hash
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const hash = window.location.hash;

    const hasEvidenceFilters = urlParams.has('filter_start_date') ||
                               urlParams.has('filter_end_date') ||
                               urlParams.has('filter_year') ||
                               hash === '#evidencias-section';

    if (hasEvidenceFilters) {
        setTimeout(function() {
            const evidenciasSection = document.getElementById('evidencias-section');
            if (evidenciasSection) {
                evidenciasSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }, 300);
    }

    // Scroll suave hacia la sección de fases cuando haya filtros activos o hash
    const hasPhaseFilters = urlParams.has('filter_phase_name') ||
                           urlParams.has('filter_phase_start') ||
                           urlParams.has('filter_phase_end') ||
                           urlParams.has('filter_phase_year') ||
                           hash === '#phases-section';

    if (hasPhaseFilters) {
        setTimeout(function() {
            const phasesSection = document.getElementById('phases-section');
            if (phasesSection) {
                phasesSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }, 300);
    }
});
