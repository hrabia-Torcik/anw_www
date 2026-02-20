

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

    if (ankietaEl) {
        new TomSelect(ankietaEl, {
            plugins: ['remove_button'],
            placeholder: "Wskaż osobę/osoby",
            maxItems: 5, // Możesz ograniczyć wybór
        });


    }

}






