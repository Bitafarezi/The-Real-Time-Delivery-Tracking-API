// static/orders/js/orders.js

const BASE_URL = '/api/order/';

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

// 2. Render orders dynamically with Tailwind styling
function renderOrders(orders) {
    const container = document.getElementById('orders-container');
    container.innerHTML = '';

    if (orders.length === 0) {
        container.innerHTML = `
            <div class="col-span-full text-center py-12 text-gray-500 bg-white border rounded-xl p-8 shadow-sm">
                <p class="text-lg font-medium">No orders found.</p>
                <p class="text-sm text-gray-400 mt-1">There are no active orders for your account right now.</p>
            </div>
        `;
        return;
    }

    orders.forEach(order => {
        let statusColor = 'bg-yellow-100 text-yellow-800';
        if (order.status === 'Out for Delivery') statusColor = 'bg-blue-100 text-blue-800';
        if (order.status === 'Delivered') statusColor = 'bg-green-100 text-green-800';

        const card = document.createElement('div');
        card.className = "bg-white border border-gray-200 rounded-2xl shadow-sm p-6 hover:shadow-md transition-shadow flex flex-col justify-between";

        let actionButtons = '';
        if (order.status === 'Pending' || order.status === 'Preparing') {
            actionButtons = `
                <button onclick="updateOrderStatus(${order.id}, 'accept')" class="w-full mt-6 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2.5 px-4 rounded-xl transition-all shadow-sm shadow-indigo-100">
                    Accept Order
                </button>
            `;
        } else if (order.status === 'Out for Delivery') {
            actionButtons = `
                <button onclick="updateOrderStatus(${order.id}, 'deliver')" class="w-full mt-6 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold py-2.5 px-4 rounded-xl transition-all shadow-sm shadow-emerald-100">
                    Mark as Delivered
                </button>
            `;
        }

        card.innerHTML = `
            <div>
                <div class="flex justify-between items-start mb-4">
                    <span class="text-xs font-bold text-gray-400 uppercase">Order #${order.id}</span>
                    <span class="text-xs px-2.5 py-1 rounded-full font-semibold ${statusColor}">${order.status}</span>
                </div>
                <h3 class="text-lg font-bold text-gray-900 mb-1">${order.restaurant_name}</h3>
                <p class="text-sm text-gray-500 mb-4 flex items-start">
                    <svg class="w-4 h-4 mr-1 text-gray-400 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                    ${order.address}
                </p>
                <div class="border-t pt-4 space-y-2">
                    <div class="flex justify-between text-xs">
                        <span class="text-gray-400">Duration:</span>
                        <span class="font-semibold text-gray-700">${order.delivery_duration}</span>
                    </div>
                    ${order.customer_profile ? `
                    <div class="flex justify-between text-xs">
                        <span class="text-gray-400">Customer:</span>
                        <span class="font-semibold text-gray-700">${order.customer_profile.user.full_name} (${order.customer_profile.phone_number})</span>
                    </div>
                    ` : ''}
                </div>
            </div>
            ${actionButtons}
        `;

        container.appendChild(card);
    });
}


// 3. Update order status using AJAX (POST request to accept/deliver)
async function updateOrderStatus(orderId, action) {
    const url = `${BASE_URL}${orderId}/${action}/`;
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        const result = await response.json();

        if (response.ok) {
            alert(result.message);
            loadOrders(); // Real-time reload without refreshing the browser!
        } else {
            alert(`Error: ${result.error || 'Something went wrong'}`);
        }
    } catch (error) {
        console.error(error);
        alert('Network error, please try again.');
    }
}

// Initial load
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('username-display').innerText = "Active Session User";
    loadOrders();
});