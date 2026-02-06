// Auto-dismiss para mensajes de Django

document.addEventListener('DOMContentLoaded', function() {
    dismissMessages();
});

document.addEventListener('messagesUpdated', function(e) {
    if (e.detail && e.detail.messages) {
        const messages = e.detail.messages;
        messages.forEach(function(message) {
            const dismissTime = parseInt(message.getAttribute('data-auto-dismiss'));
            dismissMessage(message, dismissTime);
        });
    }
});

function dismissMessages() {
    const allMessages = document.querySelectorAll('[data-auto-dismiss]');
    allMessages.forEach(function(message) {
        const dismissTime = parseInt(message.getAttribute('data-auto-dismiss'));
        dismissMessage(message, dismissTime);
    });
}

function dismissMessage(message, dismissTime) {
    setTimeout(function() {
        message.style.transition = 'opacity 0.3s ease';
        message.style.opacity = '0';
        setTimeout(function() {
            message.remove();
        }, 300);
    }, dismissTime);
}
