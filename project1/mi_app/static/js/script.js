document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('paste-latex').addEventListener('click', function () {
        console.log("hiasdf");
        document.getElementById('paste-latex-textarea').style.display = 'block';
    });
});

  // Función para verificar si un elemento está en la vista
    function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    // Función para manejar el scroll
    function handleScroll() {
        const title = document.getElementById('main-title');
        if (isElementInViewport(title)) {
            title.classList.add('animate'); // Añade la clase de animación si está en la vista
            window.removeEventListener('scroll', handleScroll); // Remueve el listener para evitar múltiples llamadas
        }
    }

    // Agrega el event listener de scroll
    window.addEventListener('scroll', handleScroll);

    // Llama a la función al cargar la página por si el título ya está visible
    document.addEventListener('DOMContentLoaded', handleScroll);




let activeTextarea = null;

// Detectar el textarea activo cuando recibe el foco
document.addEventListener('focusin', function(event) {
    if (event.target.tagName === 'TEXTAREA') {
        activeTextarea = event.target; // Guardar el textarea que tiene el foco
    }
});

// Función para añadir el símbolo al textarea activo
function addSymbol(symbol) {
    console.log(activeTextarea);
    if (!activeTextarea) return; // Si no hay un textarea activo, salir

    const cursorPos = activeTextarea.selectionStart;  // Posición inicial del cursor
    const textBefore = activeTextarea.value.substring(0, cursorPos);  // Texto antes del cursor
    const textAfter = activeTextarea.value.substring(cursorPos);  // Texto después del cursor

    // Insertar el símbolo en la posición del cursor
    activeTextarea.value = textBefore + symbol + textAfter;

    // Mover el cursor a la posición justo después del símbolo insertado
    activeTextarea.selectionEnd = cursorPos + symbol.length;
    
    // Devolver el foco al textarea
    activeTextarea.focus();
}

// Función para actualizar la vista previa de MathJax
function updatePreview(textareaId, previewId) {
    const input = document.getElementById(textareaId);
    const preview = document.getElementById(previewId).querySelector('div');
    
    // Actualiza el contenido de la vista previa con el texto del textarea
    preview.innerHTML = input.value;

    // Renderiza el contenido de LaTeX con MathJax
    MathJax.typesetPromise([preview]);
}

// Selecciona todos los textareas cuyo id comienza con 'latex-input-'
const textareas = document.querySelectorAll('textarea[id^="latex-input-"]');

// Añade un evento 'input' a cada textarea seleccionado
textareas.forEach(function(textarea) {
    textarea.addEventListener('input', function() {
        const previewContainerId = 'preview-' + textarea.id.substring('latex-input-'.length); // Supone que el preview tiene un ID correspondiente
        updatePreview(textarea.id, previewContainerId);
    });
});

// Función para crear una nueva sección de LaTeX
let sectionCounter = 0; // Asignar el contador a nivel global para seguir incrementando
function createNewSection() {
    sectionCounter++;

    const container = document.createElement('div');
    container.classList.add('section-container', 'mb-3'); // Añadir espacio entre secciones

    const textareaContainer = document.createElement('div');
    textareaContainer.classList.add('textarea-container');

    const textarea = document.createElement('textarea');
    textarea.name = 'inputText-' + sectionCounter; // Asegurarse de que el nombre sea único
    textarea.id = 'latex-input-' + sectionCounter;
    textarea.value = '\\( \\)'; // Agregar \( \)
    textarea.classList.add('textarea', 'form-control');
    textarea.setAttribute('placeholder', 'Escribe aquí el código LaTeX');
    textarea.style.width = "100%"; // Hacer que el textarea ocupe todo el ancho disponible
    
    const previewContainer = document.createElement('div');
    previewContainer.classList.add('preview-container', 'mi-clase');
    previewContainer.id = 'preview-' + sectionCounter;
    previewContainer.innerHTML = `<div>Preview</div>`; // Mostrar el texto "Preview" al inicio

    // Añadir textarea y preview al contenedor principal
    textareaContainer.appendChild(textarea);
    container.appendChild(textareaContainer);
    container.appendChild(previewContainer);

    // Insertar el nuevo contenedor al final de dynamicSections
    document.getElementById('dynamic-sections').appendChild(container);

    // Añadir evento 'input' al textarea creado
    textarea.addEventListener('input', function() {
        updatePreview(textarea.id, previewContainer.id);
    });
}


    // Función para añadir un atributo a texto
    attributeCounter = 0;
    function createAttributeSection() {
        attributeCounter++;

        const container = document.createElement('div');
        container.classList.add('attribute-container', 'mb-2');

        const textInput = document.createElement('input');
        textInput.type = 'text';
        textInput.name = 'text_attribute-' + attributeCounter;
        textInput.classList.add('form-control', 'mb-1');
        textInput.placeholder = 'Texto';

        const colorInput = document.createElement('input');
        colorInput.type = 'color';
        colorInput.name = 'color_attribute-' + attributeCounter;
        colorInput.classList.add('form-control');

        container.appendChild(textInput);
        container.appendChild(colorInput);

        // Insertar el nuevo contenedor al final de dynamicAttributes
        document.getElementById('dynamic-attributes').appendChild(container);
    }
    function create_big_textarea() {
        // Crear el contenedor principal de la sección
        const container = document.createElement('div');
        container.classList.add('section-container', 'mb-3'); // Añadir espacio entre secciones
    
        // Crear el contenedor del textarea
        const textareaContainer = document.createElement('div');
        textareaContainer.classList.add('textarea-container');
    
        // Crear el textarea con un ID único
        const textarea = document.createElement('textarea');
        textarea.name = 'paste-latex-textarea'; // Asegurarse de que el nombre sea consistente
        textarea.id = 'paste-latex-textarea-' + document.getElementsByClassName('textarea').length; // ID único
        textarea.classList.add('textarea', 'form-control');
        textarea.setAttribute('placeholder', 'Paste your LaTeX document here...');
        textarea.style.width = "100%"; // Hacer que el textarea ocupe todo el ancho disponible
    
        // Añadir el textarea dentro de su contenedor
        textareaContainer.appendChild(textarea);
    
        // Añadir el contenedor del textarea al contenedor principal
        container.appendChild(textareaContainer);
    
        // Finalmente, agregar todo el contenedor a la sección deseada en el DOM
        document.getElementById('dynamic-textarea').appendChild(container);
    }
    
    // Añadir eventos a los botones
    document.getElementById('create-div-btn').addEventListener('click', createNewSection);
    document.getElementById('create-attribute-btn').addEventListener('click', createAttributeSection);
    document.getElementById('paste-latex').addEventListener('click', create_big_textarea);
    

function toggleGreekLetters() {
    var lettersDiv = document.getElementById('greekLetters');
    if (lettersDiv.style.display === 'none') {
        lettersDiv.style.display = 'block';
    } else {
        lettersDiv.style.display = 'none';
    }
}

