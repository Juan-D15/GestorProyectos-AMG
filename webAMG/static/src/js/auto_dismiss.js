// Auto-dismiss para mensajes de Django

(function() {
    function dismissMessage(message, dismissTime) {
        console.log('Desapareciendo mensaje en', dismissTime, 'ms');
        setTimeout(function() {
            message.style.transition = 'opacity 0.3s ease';
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
                console.log('Mensaje eliminado');
            }, 300);
        }, dismissTime);
    }

    function dismissMessages() {
        const allMessages = document.querySelectorAll('[data-auto-dismiss]');
        console.log('Mensajes encontrados:', allMessages.length);
        allMessages.forEach(function(message) {
            const dismissTime = parseInt(message.getAttribute('data-auto-dismiss'));
            console.log('Dismiss time:', dismissTime);
            dismissMessage(message, dismissTime);
        });
    }

    // Ejecutar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', dismissMessages);
    } else {
        dismissMessages();
    }

    // Escuchar eventos personalizados de mensajes actualizados
    document.addEventListener('messagesUpdated', function(e) {
        if (e.detail && e.detail.messages) {
            const messages = e.detail.messages;
            messages.forEach(function(message) {
                const dismissTime = parseInt(message.getAttribute('data-auto-dismiss'));
                dismissMessage(message, dismissTime);
            });
        }
    });
})();
