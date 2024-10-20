// Function to get URL parameters
function getUrlParams() {
    const params = new URLSearchParams(window.location.search);
    return {
        ticker: params.get('ticker'),
        action: params.get('action')
    };
}

// Function to set initial values on page load
function setInitialValues() {
    const params = getUrlParams();

    // Set the stock ticker field
    if (params.ticker) {
        document.getElementById('ticker').value = params.ticker;
    }

    // Select the appropriate radio button
    if (params.action === 'buy') {
        document.getElementById('buy').checked = true;
    } else if (params.action === 'sell') {
        document.getElementById('sell').checked = true;
    }
}

// Call setInitialValues when the page loads
window.onload = setInitialValues;

// Confirmation and Popup Functions
function confirmTrade() {
    const action = document.querySelector('input[name="trade_action"]:checked').value;
    const ticker = document.getElementById('ticker').value.trim();
    const quantity = document.getElementById('quantity').value;
    const totalValue = document.getElementById('total_value').value;

    let message = `You are about to ${action} ${ticker} `;
    if (quantity) {
        message += `${quantity} shares.`;
    } else if (totalValue) {
        message += `worth $${totalValue}.`;
    } else {
        message += `but no shares or value entered.`;
    }

    document.getElementById('confirmationMessage').innerText = message;
    document.getElementById('popup').style.display = 'block';
}

function closePopup() {
    document.getElementById('popup').style.display = 'none';
}

function proceedWithTrade() {
    alert('Trade has been confirmed!');
    closePopup();
}
