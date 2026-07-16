// static/orders/js/orders.js

// Function to get Django's CSRF Token for safe AJAX requests
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue
}

// 1. Fetch all orders (Get request)
async function loadOrders(params) {
    try {
        const response = await fetch(BASE_URL);
        if (!response.ok) throw new Error('Failed to fetch orders');
        const orders = await response.json();
        renderOrders(orders);
    } catch (error) {
        console.error(error);
        document.getElementById('orders-container').innerHTML = `
            <div class="col-span-full text-center py-12 text-red-500 font-semibold">
                Error loading orders. Please check your login session!
            </div>
        `;
    }
    
}