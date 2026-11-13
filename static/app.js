const form = document.querySelector('#upload-form');
const input = document.querySelector('#photos');
const selected = document.querySelector('#selected');
const previews = document.querySelector('#previews');
const submit = document.querySelector('#submit');
const feedback = document.querySelector('#feedback');
let urls = [];
input.addEventListener('change', () => {
  urls.forEach(URL.revokeObjectURL);
  urls = [];
  previews.replaceChildren();
  feedback.textContent = '';
  feedback.className = '';
  const photos = Array.from(input.files || []);
  selected.textContent = photos.length ? photos.length + ' foto(s) selecionada(s)' : 'Nenhuma foto selecionada';
  if (photos.length > 10) {
    feedback.textContent = 'Selecione no máximo 10 fotos por vez.';
    feedback.className = 'error';
  }
  for (const photo of photos.slice(0, 10)) {
    if (!photo.type.startsWith('image/')) continue;
    const url = URL.createObjectURL(photo);
    urls.push(url);
    const img = document.createElement('img');
    img.src = url;
    img.alt = 'Prévia da foto selecionada';
    previews.append(img);
  }
  submit.disabled = !photos.length || photos.length > 10;
});
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  if (submit.disabled) return;
  submit.disabled = true;
  submit.textContent = 'Enviando fotos...';
  feedback.textContent = 'Não feche esta página até terminar o envio.';
  feedback.className = '';
  try {
    const response = await fetch(form.action, {method:'POST',body:new FormData(form)});
    const result = await response.json();
    if (!response.ok) {
      const detail = result.enviados ? ' ' + result.enviados + ' foto(s) já foram salvas.' : '';
      throw new Error((result.error || 'Falha ao enviar.') + detail);
    }
    feedback.textContent = '♥ ' + result.enviados + ' foto(s) enviadas com sucesso! Obrigado por compartilhar.';
    feedback.className = 'success';
    form.reset();
    urls.forEach(URL.revokeObjectURL);
    urls = [];
    previews.replaceChildren();
    selected.textContent = 'Nenhuma foto selecionada';
  } catch (error) {
    feedback.textContent = error.message || 'Erro de conexão. Tente novamente.';
    feedback.className = 'error';
  } finally {
    submit.textContent = 'Enviar minhas fotos ↗';
    submit.disabled = !(input.files && input.files.length);
  }
});
