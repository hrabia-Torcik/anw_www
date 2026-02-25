

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

    // --- 1. TWOJA NOWA ANKIETA (TomSelect) ---
    // Upewnij się, że masz klasę "ankieta-select" w swoim HTML
    const ankietaEl = document.querySelector(selector);

    if (!ankietaEl) return;

    const control = new TomSelect(ankietaEl, {
        plugins: ['remove_button'],
        persist: false,
        placeholder: ankietaEl.getAttribute('placeholder') || "Wybierz...",

        // Twoje czyszczenie okienka po wyborze (zostaje!)
        onItemAdd: function() {
            this.setTextboxValue('');
            this.refreshOptions();
        },

        // Magia dzieje się tutaj:
        // Nasze nowe stylowanie placeholdera
        onInitialize: function() {
            const input = this.control_input;
            if (input) {
                input.classList.add('small', 'text-muted', 'fst-italic');
            }
        }
        });


    // Nasłuchiwanie na zmiany
    control.on('change', function() {
        const selectedItems = control.getValue(); // Pobiera ID wybranych instruktorów
        const container = document.getElementById('instruktorzy-oceny-container');

        // Czyścimy kontener i budujemy go na nowo
        container.innerHTML = '';

        selectedItems.forEach(id => {
            // Pobieramy tekst (imię i nazwisko) dla danego ID
            const itemText = control.options[id].text;

            // Tworzymy HTML dla dodatkowych pól (np. ocena 1-5)
            const row = `
                <div class="card col-md-10 offset-md-1 mb-3 p-3 bg-light shadow-sm">
                    <h5>Ocena dla: <strong>${itemText}</strong></h5>
                    <div class="mb-4">
                        <label>Punktualność:</label>
                        <select name="ocena_punktualnosc_${id}" class="form-select">
                            <option value="1">1 -ciągle czekaliśmy, zdażyło się, że długo</option>
                            <option value="2">2 -regularne spóźnienia, ale o niezauważalnej długości</option>
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
                            <div class="d-flex mt-2">
                                
                                <div class="pe-5"><input type="radio" name="ocena_nauczania_${id}" value="1"> <i class="bi bi-star-fill"></i> </div>
                                
                                <div class="pe-5"><input type="radio" name="ocena_nauczania_${id}" value="2"> <i class="bi bi-star-fill"></i> 
                                                                                                              <i class="bi bi-star-fill"></i> </div>
                               
                                <div class="pe-5"><input type="radio" name="ocena_nauczania_${id}" value="3"> <i class="bi bi-star-fill"></i>
                                                                                                              <i class="bi bi-star-fill"></i>
                                                                                                              <i class="bi bi-star-fill"></i> </div>
                                
                                <div class="pe-5"><input type="radio" name="ocena_nauczania_${id}" value="3"> <i class="bi bi-star-fill"></i>
                                                                                                              <i class="bi bi-star-fill"></i>
                                                                                                              <i class="bi bi-star-fill"></i>
                                                                                                              <i class="bi bi-star-fill"></i> </div>
                                                                                                              
                                <div class="pe-5"><input type="radio" name="ocena_nauczania_${id}" value="3"> <i class="bi bi-star-fill"></i>
                                                                                                              <i class="bi bi-star-fill"></i>
                                                                                                              <i class="bi bi-star-fill"></i>
                                                                                                              <i class="bi bi-star-fill"></i>
                                                                                                              <i class="bi bi-star-fill"></i> </div>                                                                              

                            </div>
                    </div>
                    
                    <div class="mb-4">
                        <label>Sposób bycia:</label>
                        <select name="ocena_atmosfery_${id}" class="form-select">
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
    });
    // NOWOŚĆ: Funkcja budująca suwaki wyciągnięta do osobnej nazwy
    const buildRatings = () => {
        const selectedItems = control.getValue();
        const container = document.getElementById('instruktorzy-oceny-container');

        // Tutaj logika budowania suwaków (ta sama co wcześniej w 'change')
        // Ale dodaj mały trik: spróbujemy odzyskać wartość z POST jeśli istnieje
        // (Wymaga to małego wsparcia od Django w punkcie 3)
    };

    // Odpal budowanie przy każdej zmianie...
    control.on('change', buildRatings);

    // ...oraz NATYCHMIAST przy załadowaniu (jeśli są już wybrani instruktorzy)
    buildRatings();
}






