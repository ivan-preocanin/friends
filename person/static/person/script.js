function showDetails() {
    var e = document.getElementById("persons_drop");
    var selectedPerson = e.options[e.selectedIndex].value;
    if (selectedPerson != -1) {
        window.location.href = 'http://localhost:8000/person/' + selectedPerson;
        e.selectedIndex = 1;
    }    
}