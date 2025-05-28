// Theme Management
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Update icon
    const icon = document.querySelector('.theme-toggle i');
    icon.className = newTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
}

// History Management
function toggleHistory() {
    const panel = document.querySelector('.history-panel');
    panel.classList.toggle('active');
}

function addToHistory(operation, result) {
    const historyList = document.getElementById('history-list');
    const historyItem = document.createElement('div');
    historyItem.className = 'history-item';
    historyItem.innerHTML = `
        <div class="operation">${operation}</div>
        <div class="result">${result}</div>
        <div class="history-actions">
            <button class="favorite-btn" onclick="toggleFavorite(this, '${operation.id}')">
                <i class="far fa-star"></i>
            </button>
            <button class="note-btn" onclick="showNoteInput(this, '${operation.id}')">
                <i class="fas fa-sticky-note"></i>
            </button>
        </div>
    `;
    historyList.insertBefore(historyItem, historyList.firstChild);
}

// Favorites Management
function toggleFavorite(button, operationId) {
    button.classList.toggle('active');
    const icon = button.querySelector('i');
    icon.className = button.classList.contains('active') ? 'fas fa-star' : 'far fa-star';
    
    fetch('/favorites', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ operation_id: operationId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.is_favorite) {
            showNotification('Añadido a favoritos');
        } else {
            showNotification('Eliminado de favoritos');
        }
    });
}

// Notes Management
function showNoteInput(button, operationId) {
    const noteInput = document.createElement('textarea');
    noteInput.className = 'note-input';
    noteInput.placeholder = 'Añade una nota...';
    
    const saveButton = document.createElement('button');
    saveButton.className = 'save-note-btn';
    saveButton.textContent = 'Guardar';
    saveButton.onclick = () => saveNote(operationId, noteInput.value);
    
    const noteContainer = document.createElement('div');
    noteContainer.className = 'note-container';
    noteContainer.appendChild(noteInput);
    noteContainer.appendChild(saveButton);
    
    button.parentElement.appendChild(noteContainer);
}

function saveNote(operationId, note) {
    fetch('/notes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ operation_id: operationId, note: note })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Nota guardada');
        }
    });
}

// Examples Management
function loadExample(type, func1, func2 = null) {
    switch(type) {
        case 'derivada':
            document.getElementById('funcion_derivada').value = func1;
            break;
        case 'integral':
            document.getElementById('funcion_integral').value = func1;
            break;
        case 'area':
            document.getElementById('funcion1_area').value = func1;
            document.getElementById('funcion2').value = func2;
            break;
    }
}

// Tutorial Management
function showTutorial() {
    const overlay = document.querySelector('.tutorial-overlay');
    overlay.classList.add('active');
}

function closeTutorial() {
    const overlay = document.querySelector('.tutorial-overlay');
    overlay.classList.remove('active');
}

// Notifications
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Form Submission
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        const operationType = form.getAttribute('data-operation');
        formData.append('type', operationType);
        
        try {
            const response = await fetch('/calculate', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                const resultElement = form.querySelector('.result p');
                resultElement.innerHTML = data.result;
                
                // Add to history
                addToHistory(data.history_item, data.result);
                
                // Show success notification
                showNotification('Cálculo realizado con éxito');
            } else {
                showNotification('Error: ' + data.error);
            }
        } catch (error) {
            showNotification('Error al procesar la solicitud');
        }
    });
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    const themeIcon = document.querySelector('.theme-toggle i');
    themeIcon.className = savedTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    
    // Show tutorial on first visit
    if (!localStorage.getItem('tutorialShown')) {
        showTutorial();
        localStorage.setItem('tutorialShown', 'true');
    }
    
    // Load history
    fetch('/history')
        .then(response => response.json())
        .then(history => {
            history.forEach(item => {
                addToHistory(item, item.result);
            });
        });
}); 