// script.js

function toggleMarketHours() {
    const dropdown = document.getElementById('market-hours-dropdown');
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}

function toggleStockOptions() {
    const dropdown = document.getElementById('stock-options-dropdown');
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}

// Toggle functions for add/edit/remove options
function toggleAddStock() {
    const addDropdown = document.getElementById('add-stock-dropdown');
    const editDropdown = document.getElementById('edit-stock-dropdown');
    const removeDropdown = document.getElementById('remove-stock-dropdown');

    // Show or hide the add stock dropdown and hide others
    addDropdown.style.display = addDropdown.style.display === 'block' ? 'none' : 'block';
    editDropdown.style.display = 'none';
    removeDropdown.style.display = 'none';
}

function toggleEditStock() {
    const addDropdown = document.getElementById('add-stock-dropdown');
    const editDropdown = document.getElementById('edit-stock-dropdown');
    const removeDropdown = document.getElementById('remove-stock-dropdown');

    // Show or hide the edit stock dropdown and hide others
    editDropdown.style.display = editDropdown.style.display === 'block' ? 'none' : 'block';
    addDropdown.style.display = 'none';
    removeDropdown.style.display = 'none';
}

function toggleRemoveStock() {
    const addDropdown = document.getElementById('add-stock-dropdown');
    const editDropdown = document.getElementById('edit-stock-dropdown');
    const removeDropdown = document.getElementById('remove-stock-dropdown');

    // Show or hide the remove stock dropdown and hide others
    removeDropdown.style.display = removeDropdown.style.display === 'block' ? 'none' : 'block';
    addDropdown.style.display = 'none';
    editDropdown.style.display = 'none';
}

// Simulating stock data for demonstration
const stockData = {
    'AAPL': {
        stockName: 'Apple Inc.',
        startingValue: 150,
        marketCap: 2500000000000,
        description: 'Apple Inc. is a multinational technology company that designs, develops, and sells consumer electronics...'
    },
    'GOOGL': {
        stockName: 'Alphabet Inc.',
        startingValue: 2800,
        marketCap: 1800000000000,
        description: 'Alphabet Inc. is the parent company of Google and several other businesses...'
    },
    // Add more stocks as needed
};

// Confirm the ticker input and populate fields
function confirmTickerEdit() {
    const ticker = document.getElementById('edit-ticker').value.trim().toUpperCase();
    const stock = stockData[ticker]; // Simulate fetching stock data

    if (stock) {
        document.getElementById('edit-stock-name').value = stock.stockName;
        document.getElementById('edit-starting-value').value = stock.startingValue;
        document.getElementById('edit-market-cap').value = stock.marketCap;
        document.getElementById('edit-description').value = stock.description;
        document.getElementById('edit-fields').style.display = 'block'; // Show fields after confirming ticker
    } else {
        // Reset fields if ticker is not found
        document.getElementById('edit-stock-name').value = '';
        document.getElementById('edit-starting-value').value = '';
        document.getElementById('edit-market-cap').value = '';
        document.getElementById('edit-description').value = '';
        document.getElementById('edit-fields').style.display = 'none'; // Hide fields if not found
        alert('Stock not found!');
    }
}

function confirmAdd() {
    // Here you would typically send the data to your server
    alert('Stock added successfully!');
    toggleAddStock(); // Hide the add stock dropdown
}

function confirmEdit() {
    // Here you would typically send the updated data to your server
    alert('Stock edited successfully!');
    toggleEditStock(); // Hide the edit stock dropdown
}

function confirmRemove() {
    // Here you would typically send the removal request to your server
    alert('Stock removed successfully!');
    toggleRemoveStock(); // Hide the remove stock dropdown
}

function confirmHours() {
    // Here you would typically send the market hours to your server
    const openingHours = document.getElementById('opening-hours').value;
    const closingHours = document.getElementById('closing-hours').value;
    alert(`Market hours set: ${openingHours} - ${closingHours}`);
    toggleMarketHours(); // Hide the market
}