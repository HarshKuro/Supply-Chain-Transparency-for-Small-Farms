// js/common.js

// Alert functions
export function showAlert(message, type = 'success') {
    let alertBox = document.getElementById('global-alert');
    if (!alertBox) {
        alertBox = document.createElement('div');
        alertBox.id = 'global-alert';
        alertBox.className = 'alert';
        // Add to top of body
        document.body.insertBefore(alertBox, document.body.firstChild);
        
        // Add some basic styling for global positioning if needed
        alertBox.style.position = 'fixed';
        alertBox.style.top = '10px';
        alertBox.style.left = '50%';
        alertBox.style.transform = 'translateX(-50%)';
        alertBox.style.zIndex = '9999';
        alertBox.style.width = '90%';
        alertBox.style.maxWidth = '600px';
        alertBox.style.textAlign = 'center';
    }
    
    alertBox.textContent = message;
    alertBox.className = `alert ${type}`;
    
    setTimeout(() => {
        alertBox.className = 'alert'; // hide
    }, 3000);
}

// Loader functions
export function showLoader() {
    let loader = document.getElementById('loader');
    if (!loader) {
        loader = document.createElement('div');
        loader.id = 'loader';
        loader.textContent = 'Loading...';
        document.body.appendChild(loader);
    }
    loader.style.display = 'flex';
}

export function hideLoader() {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.style.display = 'none';
    }
}

// Format currency
export function formatCurrency(amount) {
    return `₹${parseFloat(amount).toFixed(2)}`;
}
