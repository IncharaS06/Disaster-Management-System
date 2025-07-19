document.getElementById('alertForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;

    const response = await fetch("http://localhost:5000/api/alerts/flood", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
    });

    document.getElementById('alertMessage').textContent = response.ok ? "Flood alert sent!" : "Failed to send alert.";
});

// ✅ Community Reporting
document.getElementById('reportForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const name = document.getElementById('name').value;
    const location = document.getElementById('location').value;
    const description = document.getElementById('description').value;

    const response = await fetch("http://localhost:5000/api/report", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, location, description }),
    });

    document.getElementById('reportMessage').textContent = response.ok ? "Report submitted!" : "Failed to submit report.";
});

// ✅ Emergency Contacts
async function getEmergencyContacts() {
    const response = await fetch("http://localhost:5000/api/emergency-contacts");
    const contacts = await response.json();
    document.getElementById('contactList').innerHTML = contacts.map(c => `<li>${c.name} (${c.type}) - ${c.phone}</li>`).join('');
}
