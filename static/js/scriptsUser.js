document.addEventListener('DOMContentLoaded', function() {
    checkUserRoleAndId();
    loadJanji(); // Load janji data when the page is loaded
});

function getCookie(name) {
    const cookies = document.cookie.split(';').map(cookie => cookie.trim());
    for (const cookie of cookies) {
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}

function parseJwt(token) {
    try {
        return JSON.parse(atob(token.split('.')[1]));
    } catch (error) {
        console.error('Error parsing JWT token:', error);
        return null;
    }
}

function checkUserRoleAndId() {
    const token = getCookie('access_token');

    if (token) {
        const decodedToken = parseJwt(token);
        if (decodedToken) {
            window.userRole = decodedToken.role;
            window.userId = parseInt(decodedToken.user_id, 10);
            console.log('User Role:', window.userRole);
            console.log('User ID:', window.userId);
        } else {
            console.error('Invalid token format or decoding error.');
        }
    } else {
        console.error('No session token found.');
    }
}

async function loadJanji() {
    try {
        const response = await fetch('http://localhost:59/janji');
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        renderJanjiTable(data);
        console.log('Janji Data:', data);
        console.log('User Role (window):', window.userRole);
        console.log('User ID (window):', window.userId);
    } catch (error) {
        console.error('Error loading janji:', error);
    }
}

function renderJanjiTable(data) {
    const janjiTableBody = document.getElementById('janji-table-body');
    janjiTableBody.innerHTML = '';

    data.forEach((janji, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <th scope="row">${index + 1}</th>
            <td>${janji.patient_name}</td>
            <td>${janji.nurse_name}</td>
            <td>${janji.appointment_date}</td>
            <td>
                <button onclick="deleteJanji(${janji.id})" class="btn btn-danger btn-cancel" data-patient-id="${janji.patient_id}" data-nurse-id="${janji.nurse_id}">Cancel</button>
            </td>
        `;
        row.dataset.userId = window.userId; // Set user ID as a data attribute on the row
        janjiTableBody.appendChild(row);

        // Conditionally show or hide the button based on user ID comparison
        const cancelButton = row.querySelector('.btn-cancel');
        if (shouldShowButton(janji.patient_id)) {
            cancelButton.style.display = 'inline-block';
        } else {
            cancelButton.style.display = 'none';
        }
    });
}

function shouldShowButton(patientId) {
    console.log('Checking Button Visibility for Patient ID:', patientId, 'User ID:', window.userId);

    // Convert patientId to number (assuming both userId and patientId are integers)
    const parsedPatientId = parseInt(patientId, 10);

    return window.userId === parsedPatientId;
}

async function deleteJanji(id) {
    try {
        const response = await fetch(`http://localhost:59/delete_janji?id=${id}`, {
            method: 'DELETE'
        });
        const data = await response.json();
        alert(data.message);
        loadJanji();
    } catch (error) {
        console.error('Error deleting janji:', error);
    }
}
