// Mayúsculas en campo de patente y autofill de fecha/hora si existe
document.addEventListener('DOMContentLoaded', () => {
  const patente = document.querySelector("[name*='patente' i]");
  if (patente) {
    patente.addEventListener('input', () => { patente.value = patente.value.toUpperCase(); });
    patente.setAttribute('placeholder', 'Ej: AB-CD12');
    patente.setAttribute('maxlength', '8');
  }

  // setea ahora en datetime-local si existe algún campo de ese tipo
  const dt = document.querySelector("input[type='datetime-local']");
  if (dt && !dt.value) {
    const now = new Date();
    const pad = n => String(n).padStart(2, '0');
    dt.value = `${now.getFullYear()}-${pad(now.getMonth()+1)}-${pad(now.getDate())}T${pad(now.getHours())}:${pad(now.getMinutes())}`;
  }
});
