document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const messagesContainer = document.getElementById('messages');
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');

    // Scroll to the bottom of the messages container
    function scrollToBottom() {
        const container = document.getElementById('messages-container');
        container.scrollTop = container.scrollHeight;
    }
    scrollToBottom();

    // Handle form submission for new messages
    messageForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const messageBody = messageInput.value.trim();
        if (messageBody) {
            socket.emit('new_message', { 'body': messageBody });
            messageInput.value = '';
        }
    });

    // Listen for broadcasted messages
    socket.on('message_broadcast', (data) => {
        const messageDiv = document.createElement('div');
        messageDiv.innerHTML = data.html;
        messagesContainer.append(messageDiv.firstChild);
        scrollToBottom();
    });

    // Listen for edited messages
    socket.on('message_edited', (data) => {
        const messageElement = document.getElementById(`message-${data.id}`);
        if (messageElement) {
            messageElement.querySelector('.message-body').textContent = data.new_body;
            // Add or show an (edited) tag
            let editedTag = messageElement.querySelector('.edited-tag');
            if (!editedTag) {
                editedTag = document.createElement('span');
                editedTag.className = 'edited-tag';
                editedTag.textContent = ' (edited)';
                messageElement.querySelector('.message-body').after(editedTag);
            }
        }
    });

    // Listen for deleted messages
    socket.on('message_deleted', (data) => {
        const messageElement = document.getElementById(`message-${data.id}`);
        if (messageElement) {
            messageElement.remove();
        }
    });

    // Event delegation for edit and delete buttons
    messagesContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('edit-btn')) {
            const messageElement = e.target.closest('.message');
            const messageId = messageElement.dataset.id;
            const messageBody = messageElement.querySelector('.message-body');
            
            const newBody = prompt('Edit your message:', messageBody.textContent);
            if (newBody !== null && newBody.trim() !== '') {
                socket.emit('edit_message', { 'id': parseInt(messageId), 'new_body': newBody });
            }
        }

        if (e.target.classList.contains('delete-btn')) {
            if (confirm('Are you sure you want to delete this message?')) {
                const messageElement = e.target.closest('.message');
                const messageId = messageElement.dataset.id;
                socket.emit('delete_message', { 'id': parseInt(messageId) });
            }
        }
    });
});