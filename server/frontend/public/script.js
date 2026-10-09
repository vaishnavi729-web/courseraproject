document.addEventListener('DOMContentLoaded', () => {
    const button = document.getElementById('action-btn');
    const outputMsg = document.getElementById('output-msg');

    button.addEventListener('click', () => {
        outputMsg.textContent = 'Task completed successfully! Interactive action triggered.';
    });
});