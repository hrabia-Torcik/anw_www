

function clearCheckboxes() {
    // Metoda JS
    document.querySelectorAll('#sort_kursow input[type="checkbox"]').forEach(checkbox => {
        checkbox.checked = false;
    });
}
function setCheckboxes() {
    // Metoda JS
    document.querySelectorAll('#sort_kursow input[type="checkbox"]').forEach(checkbox => {
        checkbox.checked = true;
    });
}

function initTomSelect(selector) {

    const ankietaElements = document.querySelectorAll(selector);

    // if (!ankietaEl) return;
    ankietaElements.forEach(el => {

        const control = new TomSelect(el, {
            plugins: el.multiple ? ['remove_button'] : [],
            persist: false,
            create: false,
            allowEmptyOption: false,
            placeholder: el.getAttribute('placeholder') || "Wybierz...",

            // Magia dzieje się tutaj:
            // Nasze nowe stylowanie placeholdera
            onInitialize: function () {
                const input = this.control_input;
                if (input) {
                    input.classList.add('small', 'text-muted', 'fst-italic');
                }
            }
        });

        if (el.multiple) {
            // Reagujemy na zmiany od razu tutaj
            control.on('change', function () {
                // Wywołujemy funkcję budującą suwaki
                // przekazując 'control' jako argument
                renderujSuwaki(control);

                // Twoje czyszczenie okienka po wyborze
                this.setTextboxValue('');
                this.refreshOptions();
            });

            renderujSuwaki(control);
        }
    });
    
}

function renderujSuwaki(selector) {

        const selectedItems = selector.getValue(); // Pobiera ID wybranych instruktorów
        const container = document.getElementById('instruktorzy-oceny-container');

        if (!container) return;
        // Czyścimy kontener i budujemy go na nowo
        container.innerHTML = '';

        selectedItems.forEach(id => {
            // Pobieramy tekst (imię i nazwisko) dla danego ID
            const itemText = selector.options[id].text;

            // Tworzymy HTML dla dodatkowych pól (np. ocena 1-5)
            const row = `
                <div class="card col-md-10 offset-md-1 mb-3 p-3 bg-light shadow-sm">
                    <h5>Ocena dla: <strong>${itemText}</strong></h5>
                    <div class="mb-4">
                        <label>Punktualność:</label>
                        <select name="ocena_punktualnosc_${id}" class="form-select">
                            <option value="" disabled selected hidden>Wybierz ocenę...</option>
                            <option value="1">1 - ciągle czekaliśmy, zdażyło się, że długo</option>
                            <option value="2">2 - regularne spóźnienia, ale o niezauważalnej długości</option>
                            <option value="3">3 - w kratkę, raz tak, raz śmak</option>
                            <option value="4">4 - spóźnienie raz, może trzy razy</option>
                            <option value="5">5 - zawsze punktualnie</option>
                        </select>
                    </div>
                    <div class="mb-4">
                        <label>Wiedza merytoryczna:</label>
                        <div class="d-flex justify-content-between px-2 my-1">
                            <span class="small">1</span>
                            <span class="small">2</span>
                            <span class="small">3</span>
                            <span class="small">4</span>
                            <span class="small">5</span>
                        </div>
                        <input type="range" name="ocena_wiedza_${id}" class="form-range" min="1" max="5" step="1" value="3"">
                    <div class="d-flex justify-content-between px-1 mt-n1">
                        <small class="text-muted">Słabo</small>
                        <small class="text-muted">Super!</small>
                    </div>
                    </div>
                    <div class="mb-4">
                        <label>Umiejętność przekazywania wiedzy:</label>
                            <!-- Tutaj wklejasz swoje SVG lub ikony Bootstrapa -->
                            <div class="d-flex flex-wrap mt-2">
                                
                                ${[1, 2, 3, 4, 5].map(num => `
                            <div class="pe-3">
                                
                                <label class="d-flex align-items-center custom-star-label" style="cursor: pointer;">
                                <input type="radio" name="ocena_nauczania_${id}" value="${num}" class="me-2"}>
                                ${Array(num).fill('<i class="bi bi-star-fill text-warning"></i>').join('')}
                                </label>
                            </div>
                        `).join('')}
                            </div>
                    </div>
                    
                    <div class="mb-4">
                        <label>Sposób bycia:</label>
                        <select name="ocena_atmosfery_${id}" class="form-select">
                            <option value="" disabled selected hidden>Wybierz ocenę...</option>
                            <option value="1">1 - ciężko, nie mam ochoty doświadczać takiego zachowania</option>
                            <option value="2">2 - nieprzyjemnie, z deka nerwowo</option>
                            <option value="3">3 - w porządku, neutralnie</option>
                            <option value="4">4 - było fajnie</option>
                            <option value="5">5 - to był turboodlot</option>
                        </select>
                    </div>
                </div>
            `;
            container.insertAdjacentHTML('beforeend', row);
        });
}






