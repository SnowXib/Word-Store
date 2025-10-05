document.addEventListener("DOMContentLoaded", async() => {
    const output = document.getElementById("output");
    const settingsModal = document.getElementById("settingsModal");
    const testingModal = document.getElementById("testingModal");
    const submitBtn = document.getElementById("submit");
    const settingsBtn = document.querySelector("button.button:first-child");
    const testingBtn = document.getElementById("testingBtn");

    const api_key_input = document.getElementById("api_key_input");
    const base_url_input = document.getElementById("base_url_input");
    const model_input = document.getElementById("model_input");
    const language_input = document.getElementById("language_input");

    const closeBtn = settingsModal.querySelector(".close");

    submitBtn.disabled = true;

    try {
        const response = await fetch('http://127.0.0.1:8000/api/get-settings', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const settings = await response.json();
        api_key_input.value = settings['api_key']
        model_input.value = settings['model']
        base_url_input.value = settings['base_url']
        language_input.value = settings['language']


    } catch (e) {
        console.error('Error', e);
        output.textContent = 'Error';
    }

    function validateInputs() {
        if (
            api_key_input.value.trim() === "" ||
            base_url_input.value.trim() === "" ||
            model_input.value.trim() === "" ||
            language_input.value.trim() === ""
        ) {
            submitBtn.disabled = true;
            if (!output.querySelector('table')) {
                output.textContent = "Все поля должны быть заполнены!";
            }
        } else {
            submitBtn.disabled = false;
            if (!output.querySelector('table')) {
                output.textContent = "";
            }
        }
    }

    [api_key_input, base_url_input, model_input, language_input].forEach(input => {
        input.addEventListener("input", validateInputs);
    });

    submitBtn.addEventListener("click", async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/api/set-settings", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    api_key: api_key_input.value.trim(),
                    base_url: base_url_input.value.trim(),
                    model: model_input.value.trim(),
                    language: language_input.value.trim()
                })
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        } catch (e) {
            console.error("Error:", e);
            output.textContent = "Error";
        }
    });

    testingBtn.addEventListener("click", () => {
        testingModal.style.display = "flex"
    })

    settingsBtn.addEventListener("click", () => {
        settingsModal.style.display = "flex";
    });

    closeBtn.addEventListener("click", () => {
        settingsModal.style.display = "none";
    });

    settingsModal.addEventListener("click", (e) => {
        if (e.target === settingsModal) {
            settingsModal.style.display = "none";
        }
    });

    try {
        const response = await fetch('http://127.0.0.1:8000/api/get-most-frequent-words?count=10', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const frequentWords = await response.json();
        createTable(frequentWords);

    } catch (e) {
        console.error('Error', e);
        output.textContent = 'Error';
    }

    testingBtn.addEventListener("click", async() => {
        try {
        const response = await fetch('http://127.0.0.1:8000/api/get-testing?count=10', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const testItems = await response.json();
        createTesting(testItems)

    } catch (e) {
        console.error('Error', e);
        output.textContent = 'Error';
    }
    })

    function createTesting(testItems){
        
    }

    function createTable(wordsData) {
        output.innerHTML = '';

        const table = document.createElement('table');
        table.style.opacity = '0';
        table.style.transition = 'opacity 0.5s ease';

        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');

        ['Word', 'Count', 'Translate'].forEach(text => {
            const th = document.createElement('th');
            th.textContent = text;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);

        const tbody = document.createElement('tbody');
        wordsData.forEach(item => {
            const row = document.createElement('tr');
            ['word', 'count', 'translate'].forEach(key => {
                const td = document.createElement('td');
                td.textContent = item[key];
                if (key !== 'word') td.style.textAlign = 'center';
                row.appendChild(td);
            });
            tbody.appendChild(row);
        });
        table.appendChild(tbody);
        output.appendChild(table);

        setTimeout(() => table.style.opacity = '1', 50);
    }
});