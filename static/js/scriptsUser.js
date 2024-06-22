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


function createJanji(event) {
    event.preventDefault();

    const patientName = document.getElementById('patientName').value;
    const nurseName = document.getElementById('nurseName').value;
    const appointmentDate = document.getElementById('appointmentDate').value;
    const nurseId = document.getElementById('idNurse').value;

    fetchPatientId(patientName)
        .then(patientId => {
            // Proceed with creating the janji entry
            return fetch('http://localhost:59/janji', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    patient_name: patientName,
                    nurse_name: nurseName,
                    appointment_date: appointmentDate,
                    nurse_id: nurseId,
                    patient_id: patientId
                })
            });
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.message);
            }
            alert(data.message);
            loadJanji(); // Reload the janji table after successful addition
            document.getElementById('janji-form').reset(); // Reset the form
            // Automatically create a consultation when management_janji is added
            const managementJanjiId = data.management_janji_id;
            fetchPatientId(patientName).then(patientId => createConsultation(patientId, nurseId, managementJanjiId));
        })
        .catch(error => console.error('Error adding management_janji:', error));
}

function fetchPatientId(patientName) {
    return fetch(`http://localhost:59/get_patient_id?name=${encodeURIComponent(patientName)}`)
        .then(response => response.json())
        .then(data => {
            if (data && data.patient_id) {
                return data.patient_id;
            } else {
                throw new Error('Patient ID not found');
            }
        });
}

// Function to create a consultation automatically when a management_janji entry is added
function createConsultation(patientId, nurseId, managementJanjiId) {
    // Fetch patient name based on patientId
    fetch(`http://localhost:50/detail_user/${patientId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data && data.name) { // Check if data exists and has name property
                const patientName = data.name; // Get the patient name
                
                // Include patient name, nurse ID, and management_janji_id in the consultation data
                const consultationData = {
                    patient_id: patientId,
                    patient_name: patientName,
                    nurse_id: nurseId,
                    management_janji_id: managementJanjiId
                    // Include other consultation details here if needed
                };
                
                // Make POST request to create the consultation
                return fetch('http://localhost:55/konsultasi', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(consultationData)
                });
            } else {
                throw new Error('Patient details not found');
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.message);
            }
            console.log(data.message); // Log the message
            // You can perform additional actions after creating the consultation if needed
        })
        .catch(error => console.error('Error creating consultation:', error));
}


function deleteJanji(id) {
    fetch(`http://localhost:59/delete_janji?id=${id}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadJanji();
    })
    .catch(error => console.error('Error deleting janji:', error));
}

function editJanji(id) {
    fetch(`http://localhost:59/detail_janji/${id}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data) {
                document.getElementById('patientName').value = data.patient_name || '';
                document.getElementById('idNurseModal').value = data.nurse_id || '';
                document.getElementById('NurseNameModal').value = data.nurse_name || '';
                document.getElementById('appointmentDate').value = data.appointment_date || '';
                document.getElementById('editJanjiId').value = id; // Hidden field to store ID

                // Trigger Bootstrap modal manually
                const modal = new bootstrap.Modal(document.getElementById('editJanjiModal'));
                modal.show();
            } else {
                console.error('No janji data found');
            }
        })
        .catch(error => console.error('Error fetching janji details:', error));
}

function submitEditConsultation(event) {
    event.preventDefault(); // Prevent default form submission

    const id = document.getElementById('editConsultationId').value; // Get the consultation ID
    const patientAge = document.getElementById('editConsultationPatientAge').value;
    const resep = document.getElementById('editConsultationResep').value;
    const diseaseId = document.getElementById('editConsultationDiseaseId').value;
    const nurseId = document.getElementById('editConsultationNurseId').value;
    const patientId = document.getElementById('editConsultationPatientId').value;
    const patientName = document.getElementById('editConsultationPatientName').value; // Get the patient name

    fetch(`http://localhost:55/update_konsultasi/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            patient_age: patientAge,
            disease_id: diseaseId,
            nurse_id: nurseId,
            patient_id: patientId,
            resep_hasil_konsultasi: resep, 
            patient_name: patientName // Include patient name in the update
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to update consultation');
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
        new bootstrap.Modal(document.getElementById('editConsultationModal')).hide(); // Hide the modal after successful update
        loadConsultations(); // Reload the consultations table
    })
    .catch(error => console.error('Error updating consultation:', error));
}

function updateJanji() {
    const id = document.getElementById('editJanjiId').value;
    const data = {
        patient_name: document.getElementById('patientName').value,
        nurse_id: document.getElementById('idNurseModal').value,
        appointment_date: document.getElementById('appointmentDate').value,
    };

    fetch(`http://localhost:59/update_janji?id=${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(result => {
        console.log(result.message);
        // Close the modal after updating
        const modal = bootstrap.Modal.getInstance(document.getElementById('editJanjiModal'));
        modal.hide();

        // Optionally, refresh the page or update the UI to reflect changes
        location.reload();
    })
    .catch(error => console.error('Error updating janji:', error));
}

// Function to fetch nurse name based on nurse ID
function fetchNurseName() {
    const nurseId = document.getElementById('idNurse').value;
    fetch(`http://localhost:59/get_nurse_name?id=${nurseId}`)
        .then(response => response.json())
        .then(data => {
            if (data && data.nurse_name) {
                document.getElementById('nurseName').value = data.nurse_name;
            } else {
                document.getElementById('nurseName').value = '';
                alert('Nurse details not found');
            }
        })
        .catch(error => console.error('Error fetching nurse details:', error));
}


// Call the fetchNurseName function when nurse ID input changes
document.getElementById('idNurse').addEventListener('change', fetchNurseName);