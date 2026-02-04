// Auto-dismiss de mensajes flash

document.addEventListener('DOMContentLoaded', function() {
    // Buscar todos los mensajes con data-auto-dismiss
    const allMessages = document.querySelectorAll('[data-auto-dismiss]');
    allMessages.forEach(function(message) {
        const dismissTime = parseInt(message.getAttribute('data-auto-dismiss'));
        setTimeout(function() {
            message.style.transition = 'opacity 0';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, dismissTime);
    });
});
