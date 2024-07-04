document.addEventListener('DOMContentLoaded', function () {
    // Custom code here
    console.log('Custom JS loaded');
    
    // Example: Show an alert when a button is clicked
    const button = document.querySelector('.btn-alert');
    if (button) {
        button.addEventListener('click', function () {
            alert('Button clicked!');
        });
    }
});