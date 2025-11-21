// Configuración
const API_BASE = 'http://localhost:5000/api';
let fotoSeleccionada = null;
let historialLocal = [];

// Elementos del DOM
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const statusElement = document.getElementById('status');
const publishModal = document.getElementById('publishModal');
const suggestModal = document.getElementById('suggestModal');
const loadingSpinner = document.getElementById('loadingSpinner');

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
    console.log('✅ Aplicación iniciada');
    verificarConexion();
    cargarHistorial();
});

// CONEXIÓN API
async function verificarConexion() {
    try {
        const res = await fetch(`${API_BASE}/health`);
        if (res.ok) {
            actualizarStatus('connected', '✅ Conectado');
            addBotMessage('¡Conectado! Estoy listo para ayudarte. 🚀');
        }
    } catch (e) {
        actualizarStatus('disconnected', '❌ Sin conexión');
        addBotMessage('⚠️ No puedo conectarme al servidor. ¿Está ejecutándose?');
    }
}

function actualizarStatus(estado, texto) {
    statusElement.className = `status-${estado}`;
    statusElement.textContent = texto;
}

// CHAT
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function sendMessage() {
    const mensaje = userInput.value.trim();
    if (!mensaje) return;

    // Mostrar mensaje del usuario
    addUserMessage(mensaje);
    userInput.value = '';

    // Enviar a la IA
    chatConIA(mensaje);
}

function addUserMessage(texto) {
    const div = document.createElement('div');
    div.className = 'message user';
    div.innerHTML = `<div class="message-content">${escapeHtml(texto)}</div>`;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addBotMessage(texto) {
    const div = document.createElement('div');
    div.className = 'message bot';
    div.innerHTML = `<div class="message-content">${texto}</div>`;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function chatConIA(mensaje) {
    mostrarCargando(true);

    try {
        const res = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mensaje })
        });

        if (!res.ok) throw new Error('Error en la API');

        const data = await res.json();
        addBotMessage(data.respuesta);
    } catch (e) {
        addBotMessage('❌ Error: ' + e.message);
    } finally {
        mostrarCargando(false);
    }
}

// PUBLICAR
function openPublishModal() {
    publishModal.classList.add('active');
    document.getElementById('publishText').focus();
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

document.getElementById('publishText')?.addEventListener('input', (e) => {
    document.getElementById('charCount').textContent = e.target.value.length;
});

function previewPhoto(event) {
    const file = event.target.files[0];
    if (!file) return;

    fotoSeleccionada = file;
    const reader = new FileReader();
    reader.onload = (e) => {
        const preview = document.getElementById('photoPreview');
        preview.innerHTML = `
            <div style="position: relative; display: inline-block; margin-top: 10px;">
                <img src="${e.target.result}" style="max-width: 200px; border-radius: 8px;">
                <button onclick="fotoSeleccionada=null; this.parentElement.parentElement.innerHTML=''" 
                        style="position: absolute; top: -10px; right: -10px; width: 30px; height: 30px; border-radius: 50%; border: none; background: red; color: white; cursor: pointer;">
                    ✕
                </button>
            </div>
        `;
    };
    reader.readAsDataURL(file);
}

async function publicarPost() {
    const texto = document.getElementById('publishText').value.trim();
    if (!texto) {
        alert('Escribe algo primero');
        return;
    }

    mostrarCargando(true);

    try {
        let imagenUrl = null;

        // Subir foto si existe
        if (fotoSeleccionada) {
            const formData = new FormData();
            formData.append('file', fotoSeleccionada);

            const resFoto = await fetch(`${API_BASE}/subir-foto`, {
                method: 'POST',
                body: formData
            });

            if (resFoto.ok) {
                const dataFoto = await resFoto.json();
                imagenUrl = dataFoto.url;
            }
        }

        // Mejorar con IA si está checado
        let textoFinal = texto;
        if (document.getElementById('useAI').checked) {
            const resMejorar = await fetch(`${API_BASE}/mejorar`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ texto })
            });

            if (resMejorar.ok) {
                const dataMejorar = await resMejorar.json();
                textoFinal = dataMejorar.texto_mejorado;
            }
        }

        // Publicar
        const res = await fetch(`${API_BASE}/publicar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                texto: textoFinal,
                imagen_url: imagenUrl
            })
        });

        if (res.ok) {
            const data = await res.json();
            if (data.success) {
                addBotMessage('🎉 ¡Post publicado exitosamente en LinkedIn!');
                closeModal('publishModal');
                document.getElementById('publishText').value = '';
                document.getElementById('photoPreview').innerHTML = '';
                fotoSeleccionada = null;
                cargarHistorial();
                actualizarEstadisticas();
            }
        }
    } catch (e) {
        alert('Error: ' + e.message);
    } finally {
        mostrarCargando(false);
    }
}

// SUGERENCIAS
function openSuggestModal() {
    suggestModal.classList.add('active');
    document.getElementById('suggestTema').focus();
}

async function generarSugerencia() {
    const tema = document.getElementById('suggestTema').value.trim();
    const tono = document.getElementById('suggestTono').value;

    if (!tema) {
        alert('Escribe un tema');
        return;
    }

    mostrarCargando(true);

    try {
        const res = await fetch(`${API_BASE}/sugerir`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tema, tono })
        });

        if (res.ok) {
            const data = await res.json();
            document.getElementById('suggestResultText').textContent = data.sugerencia;
            document.getElementById('suggestResult').style.display = 'block';
        }
    } catch (e) {
        alert('Error: ' + e.message);
    } finally {
        mostrarCargando(false);
    }
}

// HISTORIAL
async function cargarHistorial() {
    try {
        const res = await fetch(`${API_BASE}/historial`);
        if (res.ok) {
            const data = await res.json();
            historialLocal = data.historial;
            actualizarEstadisticas();
        }
    } catch (e) {
        console.error('Error cargando historial:', e);
    }
}

function showHistorial() {
    if (historialLocal.length === 0) {
        addBotMessage('No hay posts aún. ¡Crea el primero! 🚀');
        return;
    }

    let html = '<div style="max-width: 500px;">';
    historialLocal.slice(-5).reverse().forEach(post => {
        const fecha = new Date(post.fecha).toLocaleDateString('es-ES');
        html += `<div style="padding: 10px; border: 1px solid #ccc; border-radius: 8px; margin-bottom: 10px;">
                    <small style="color: #666;">${fecha}</small>
                    <p style="margin: 5px 0;">${post.texto.substring(0, 100)}...</p>
                </div>`;
    });
    html += '</div>';
    addBotMessage('Últimos 5 posts:');
    chatMessages.lastChild.querySelector('.message-content').innerHTML = html;
}

function showFotos() {
    addBotMessage('Cargando fotos...');
    // TODO: Implementar listado de fotos
}

// ESTADÍSTICAS
function actualizarEstadisticas() {
    const total = historialLocal.length;
    const hoy = historialLocal.filter(p => {
        const fecha = new Date(p.fecha).toDateString();
        return fecha === new Date().toDateString();
    }).length;

    document.getElementById('totalPosts').textContent = total;
    document.getElementById('postsHoy').textContent = hoy;
}

// UTILIDADES
function mostrarCargando(mostrar) {
    loadingSpinner.style.display = mostrar ? 'flex' : 'none';
}

function escapeHtml(texto) {
    const div = document.createElement('div');
    div.textContent = texto;
    return div.innerHTML;
}
