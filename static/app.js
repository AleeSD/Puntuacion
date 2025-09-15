// JS básico para mejoras menores
document.addEventListener('DOMContentLoaded', () => {
  // Cerrar mensajes al hacer clic
  document.querySelectorAll('.messages li').forEach(li => {
    li.addEventListener('click', () => li.remove());
  });
});

