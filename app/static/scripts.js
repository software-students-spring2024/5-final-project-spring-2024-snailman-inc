function redirectToSelected(dropdownId) {
    var dropdown = document.getElementById(dropdownId);
    var selectedOption = dropdown.options[dropdown.selectedIndex].value;
    if (selectedOption !== "") {
        window.location.href = selectedOption;
    }
}