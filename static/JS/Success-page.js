document.addEventListener('DOMContentLoaded', function() {
  const successMessage = document.getElementById('success-message');

  if (successMessage) {
    console.log('Success message found'); // Check if this logs
    successMessage.style.display = 'block'; // Ensure element is displayed
    successMessage.classList.add('show');

    setTimeout(() => {
      successMessage.classList.remove('show');
      successMessage.classList.add('hide');

      setTimeout(() => {
        successMessage.style.display = 'none';
      }, 500); // Match this duration with the CSS transition duration
    }, 2500); // Duration for how long the message should be visible
  }
});
