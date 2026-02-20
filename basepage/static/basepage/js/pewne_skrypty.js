

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
        onItemAdd: function() { this.setTextboxValue(''); }, // Czyści szukanie po wyborze
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
                <div class="card mb-3 p-3 bg-light shadow-sm">
                    <h5>Ocena dla: <strong>${itemText}</strong></h5>
                    <div class="mb-4">
                        <label>Punktualność:</label>
                        <select name="ocena_punktualnosc_${id}" class="form-select">
                            <option value="5">5 - zawsze punktualnie</option>
                            <option value="4">4 - spóźnienie raz, może trzy razy</option>
                            <option value="3">3 - w kratkę, raz tak, raz śmak</option>
                            <option value="2">2 -regularne spóźnienia, ale o niezauważalnej długości</option>
                            <option value="1">1 -ciągle czekaliśmy, zdażyło się, że długo</option>
                        </select>
                    </div>
                    <div class="mb-4">
                        <label>Wiedza merytoryczna:</label>
                        <input type="range" name="ocena_wiedza_${id}" class="form-range" min="1" max="5">
                    </div>
                    <div class="mb-4">
                        <label>Umiejętność przekazywania wiedzy:</label>
                            <!-- Tutaj wklejasz swoje SVG lub ikony Bootstrapa -->
                            <div class="d-flex">
                                <div  class="pe-3"><input type="radio" name="ocena_nauczania${id}" value="5"> ★ ★ ★ ★ ★</div>
                                <div  class="pe-3"><input type="radio" name="ocena_nauczania${id}" value="4"> ★ ★ ★ ★</div>
                                <div  class="pe-3"><input type="radio" name="ocena_nauczania${id}" value="3"> ★ ★ ★ </div>
                                <div  class="pe-3"><input type="radio" name="ocena_nauczania${id}" value="2"> ★ ★ </div>
                                <div  class="pe-3"><input type="radio" name="ocena_nauczania${id}" value="1"> ★ </div>
                            </div>
                    </div>
                    
                    <div class="mb-4">
                        <label>Sposób bycia:</label>
                        <select name="ocena_atmosfery_${id}" class="form-select">
                            <option value="5">5 - to był turboodlot</option>
                            <option value="4">4 - było fajnie</option>
                            <option value="3">3 - w porządku, neutralnie</option>
                            <option value="2">2 - nieprzyjemnie, z deka nerwowo</option>
                            <option value="1">1 - ciężko, nie mam ochoty doświadczać takiego zachowania</option>
                        </select>
                    </div>
                </div>
            `;
            container.insertAdjacentHTML('beforeend', row);
        });
    });

}






