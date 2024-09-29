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

// Evento para crear nuevas secciones
document.getElementById('create-div-btn').addEventListener('click', createNewSection);
// Evento para añadir atributos
document.getElementById('create-attribute-btn').addEventListener('click', createAttributeSection);

    /*  
document.addEventListener('DOMContentLoaded', function() {
    const createDivBtn = document.getElementById('create-div-btn');
    const dynamicSections = document.getElementById('dynamic-sections');

    // Obtener el token CSRF desde el input oculto en el HTML
    const csrfToken = document.getElementById('csrf_token').value;



    function createNewSection() {
        let sectionCounter = 0;

        sectionCounter++;
    
        // Crear un nuevo contenedor para la sección
        const container = document.createElement('div');
        container.classList.add('section-container');
    
        // Crear el textarea
        const textareaContainer = document.createElement('div');
        textareaContainer.classList.add('textarea-container');
    
        const textarea = document.createElement('textarea');
        textarea.name = 'inputText-' + sectionCounter;
        textarea.id = 'latex-input-' + sectionCounter;
        textarea.value = '\\( \\)'; // Agregar \( \)
        textarea.classList.add('textarea', 'form-control');
        textarea.setAttribute('placeholder', 'Escribe aquí el código LaTeX');
        textarea.cols = 80; // Establecer el número de columnas
        textarea.style.width = "100%"; // Hacer que el textarea ocupe todo el ancho disponible
        //textarea.style.resize = "none"; // Opcional: prevenir el cambio de tamaño por parte del usuario
    
        textareaContainer.appendChild(textarea);
        container.appendChild(textareaContainer);
    
        // Crear el contenedor de la vista previa
        const previewContainer = document.createElement('div');
        previewContainer.classList.add('preview-container', 'mi-clase');
        previewContainer.id = 'preview-' + sectionCounter;
        previewContainer.innerHTML = `<div></div>`;
        container.appendChild(previewContainer);
    
        // Insertar el nuevo contenedor al principio de dynamicSections
        dynamicSections.insertBefore(container, dynamicSections.firstChild);
    
        // Agregar el evento para actualizar la vista previa
        textarea.addEventListener('input', function() {
            updatePreview(textarea.id, previewContainer.id);
        });
    

    // Evento para crear una nueva sección
    createDivBtn.addEventListener('click', createNewSection);

});
*/


function toggleGreekLetters() {
    var lettersDiv = document.getElementById('greekLetters');
    if (lettersDiv.style.display === 'none') {
        lettersDiv.style.display = 'block';
    } else {
        lettersDiv.style.display = 'none';
    }
}

////////////////////////////////////// Propperties
