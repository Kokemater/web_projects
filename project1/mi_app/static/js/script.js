document.addEventListener("DOMContentLoaded", function () {
    /////////////////////////////////////
    ////////////////////////////////////
    //  SORTING ALGORITHMS ////////////

    const sorting_alg_insertCodeBtn = document.getElementById("insert-code-btn");
    const sortingTextarea = document.getElementById("sorting-algorytm");

    // Código de Selection Sort en formato de string
    const selectionSortCode = `def selection_sort(list_of_numbers):
    # Recorre toda la lista
    for i in range(len(list_of_numbers)):
    # Encuentra el índice del elemento mínimo en el resto de la lista desordenada
    min_index = i
    for j in range(i + 1, len(list_of_numbers)):
        if list_of_numbers[j] < list_of_numbers[min_index]:
            min_index = j

    # Intercambia el elemento mínimo con el primer elemento de la sublista desordenada
    list_of_numbers[i], list_of_numbers[min_index] = list_of_numbers[min_index], list_of_numbers[i]
`;

    // Añade el código al textarea cuando se hace clic en el botón
    if (sorting_alg_insertCodeBtn) {
        sorting_alg_insertCodeBtn.addEventListener("click", () => {
            sortingTextarea.value = selectionSortCode;
        });
    }
    
    let activeTextarea = null;

    // Detectar el textarea activo cuando recibe el foco
    document.addEventListener('focusin', function(event) {
        if (event.target.tagName === 'TEXTAREA') {
            activeTextarea = event.target; // Guardar el textarea que tiene el foco
        }
    });

    // Función para añadir el símbolo al textarea activo
    function addSymbol(symbol) {
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

    // Función para crear una nueva sección de LaTeX
    let sectionCounter = 0; // Asignar el contador a nivel global para seguir incrementando
    function createNewSection() {
        sectionCounter++;

        const container = document.createElement('div');
        container.classList.add('section-container', 'mb-3'); // Añadir espacio entre secciones

        const textareaContainer = document.createElement('div');
        textareaContainer.classList.add('textarea-container');

        // Crear el elemento numérico para 'duration'
        const durationLabel = document.createElement('label');
        durationLabel.textContent = 'Duration';
        durationLabel.setAttribute('for', 'duration-' + sectionCounter);
        durationLabel.style.fontSize = 'small'; // Hacer que el texto sea pequeño
        durationLabel.style.marginRight = '5px'; // Espacio entre el label y el input

        const durationInput = document.createElement('input');
        durationInput.type = 'number';
        durationInput.name = 'duration-' + sectionCounter; // Asegurarse de que el nombre sea único
        durationInput.id = 'duration-' + sectionCounter;
        durationInput.value = 2; // Inicializar a 2
        durationInput.style.width = '60px'; // Ajustar el ancho si es necesario

        // Añadir label y input de duration al contenedor
        const durationContainer = document.createElement('div');
        durationContainer.appendChild(durationLabel);
        durationContainer.appendChild(durationInput);

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

        // Añadir duration y textarea al contenedor principal
        textareaContainer.appendChild(durationContainer); // Añadir el contenedor de duration
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

    const createDivBtn = document.getElementById("create-div-btn");
    const pasteLatexBtn = document.getElementById("paste-latex");
    const dynamicSections = document.getElementById("dynamic-sections");
    const pasteLatexTextarea = document.getElementById("paste-latex-textarea");
    const attributeBtn = document.getElementById('create-attribute-btn');

    // Verifica que los elementos no sean nulos antes de agregar eventos
    if (createDivBtn) {
        createDivBtn.addEventListener('click', createNewSection);
    }

    if (pasteLatexBtn) {
        pasteLatexBtn.addEventListener("click", function () {
            pasteLatexTextarea.style.display = "block";
            dynamicSections.style.display = "none";
        });
    }

    if (attributeBtn) {
        attributeBtn.addEventListener('click', createAttributeSection);
    }
});
