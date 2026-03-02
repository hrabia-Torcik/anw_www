

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

// --- 1. GŁÓWNA FUNKCJA INICJUJĄCA TOMSELECT ---
function initTomSelect(selector) {
    document.querySelectorAll(selector).forEach(el => {
        const control = new TomSelect(el, {
            plugins: el.multiple ? ['remove_button'] : [],
            // ... reszta Twojej konfiguracji ...
        });

        control.on('change', function() {
            // Gdy użytkownik coś wybierze, usuwamy błąd TYLKO z tego bloku
            const block = el.closest('.ocena-blok');
            if (this.getValue().length > 0 || this.getValue() !== "") {
                block?.classList.remove('was-validated');
            }

            if (el.multiple) renderujSuwaki(control);
        });
    });
}

// --- Obsługa wysyłki ---
document.addEventListener('submit', function(event) {
    const form = event.target;
    if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();

        // Znajdź wszystkie bloki, które mają w środku błąd
        form.querySelectorAll('.ocena-blok').forEach(block => {
            const input = block.querySelector(':invalid');
            if (input) {
                block.classList.add('was-validated');
            } else {
                block.classList.remove('was-validated');
            }
        });

        // Przewiń do pierwszego błędu (zewnętrznego lub w karcie)
        form.querySelector('.was-validated')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}, false);

// --- 2. GENEROWANIE KART OCEN ---
function renderujSuwaki(control) {
    const selectedItems = control.getValue();
    const container = document.getElementById('instruktorzy-oceny-container');
    if (!container) return;

    // Zapisujemy aktualne wartości
    const savedValues = {};
    container.querySelectorAll('input, select').forEach(field => {
        if (field.type === 'radio') {
            if (field.checked) savedValues[field.name] = field.value;
        } else {
            savedValues[field.name] = field.value;
        }
    });

    container.innerHTML = '';

    selectedItems.forEach(id => {
        const itemText = control.options[id]?.text || "Instruktor";

        const row = `
            <div class="card col-md-10 offset-md-1 mb-4 p-3 bg-light shadow-sm border-0 border-start border-primary border-4 new-card">
                <h5 class="mb-3">Ocena dla: <strong class="text-primary">${itemText}</strong></h5>
                
                <div class="ocena-blok mb-4">
                    <label class="form-label fw-bold">Punktualność:</label>
                    <select name="ocena_punktualnosc_${id}" class="form-select" required>
                        <option value="" disabled selected hidden>Wybierz ocenę...</option>
                        <option value="1">1 - ciągle czekaliśmy</option>
                        <option value="2">2 - regularne spóźnienia, ale o niezauważalnej długości</option>
                        <option value="3">3 - w kratkę, raz tak, raz śmak</option>
                        <option value="4">4 - spóźnienie raz, może trzy razy</option>
                        <option value="5">5 - zawsze punktualnie</option>
                    </select>
                    <div class="invalid-feedback">Proszę wybrać ocenę punktualności.</div>
                </div>

                <div class="ocena-blok mb-4">
                    <label class="form-label fw-bold">Wiedza merytoryczna:</label>
                    <input type="range" name="ocena_wiedza_${id}" class="form-range" min="1" max="5" step="1" value="${savedValues[`ocena_wiedza_${id}`] || 3}">
                    <div class="d-flex justify-content-between px-1 text-muted small">
                        <span>Słabo</span><span>Super!</span>
                    </div>
                </div>

                <div class="ocena-blok mb-4">
                    <label class="form-label fw-bold d-block">Umiejętność przekazywania wiedzy:</label>
                    <div class="strefa-gwiazdek p-2 pe-4 ms-3 rounded"> 
                        <div class="d-flex flex-wrap gap-2 my-2">
                            ${[1, 2, 3, 4, 5].map(num => `
                                <div class="form-check form-check-inline m-0 custom-check-row">
                                    <label class="custom-star-label p-2 border rounded border-white shadow-sm bg-white" style="cursor: pointer;">
                                        <input type="radio" name="ocena_nauczania_${id}" value="${num}" class="form-check-input me-2" required 
                                        ${savedValues[`ocena_nauczania_${id}`] == num ? 'checked' : ''}>
                                        ${Array(num).fill('<i class="bi bi-star-fill"></i>').join('')}
                                    </label>
                                </div>
                            `).join('')}
                        </div>
                        
                        <i class="bi bi-exclamation-circle text-danger wykrzyknik-ankieta"></i>
                    </div>
                    <div class="invalid-feedback">Proszę wybrać ocenę nauczania.</div>
                </div>
                
                <div class="ocena-blok mb-2">
                    <label class="form-label fw-bold">Sposób bycia:</label>
                    <select name="ocena_atmosfery_${id}" class="form-select" required>
                        <option value="" disabled selected hidden>Wybierz ocenę...</option>
                        <option value="1">1 - ciężko</option>
                        <option value="2">2 - nieprzyjemnie, z deka nerwowo</option>
                        <option value="3">3 - w porządku, neutralnie</option>
                        <option value="4">4 - było fajnie</option>
                        <option value="5">5 - turboodlot</option>
                    </select>
                    <div class="invalid-feedback">Proszę wybrać ocenę sposobu bycia.</div>
                </div>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', row);

        // Przywracanie selectów
        if (savedValues[`ocena_punktualnosc_${id}`]) container.querySelector(`[name="ocena_punktualnosc_${id}"]`).value = savedValues[`ocena_punktualnosc_${id}`];
        if (savedValues[`ocena_atmosfery_${id}`]) container.querySelector(`[name="ocena_atmosfery_${id}"]`).value = savedValues[`ocena_atmosfery_${id}`];
    });

    // --- 3. Globalny nasłuchiwacz ZMIAN (czyści błędy punktowo) ---
    document.addEventListener('change', function(e) {
        if (e.target.checkValidity()) {
            e.target.closest('.ocena-blok')?.classList.remove('was-validated');
        }
    });

    // --- 4. Obsługa WYSYŁKI ---
    document.addEventListener('submit', function(event) {
        const form = event.target;
        if (!form.hasAttribute('novalidate')) return;

        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();

            // Zapalamy błędy TYLKO tam, gdzie są puste pola
            form.querySelectorAll('.ocena-blok').forEach(blok => {
                if (blok.querySelector(':invalid')) {
                    blok.classList.add('was-validated');
                }
            });

            form.querySelector(':invalid')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }, false);
}






