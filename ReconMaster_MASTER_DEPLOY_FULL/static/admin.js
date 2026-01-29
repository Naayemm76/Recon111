
document.getElementById('loginForm').addEventListener('submit', function(event) {
  event.preventDefault();
  const user = document.getElementById('username').value;
  const pass = document.getElementById('password').value;
  if (user === 'admin' && pass === 'admin123') {
    alert('Access granted');
    window.location.href = 'dashboard.html';
  } else {
    alert('Invalid credentials');
  }
});
