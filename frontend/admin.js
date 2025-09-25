// admin.js - Live admin dashboard integration

document.addEventListener('DOMContentLoaded', function () {
    fetchAllComplaints();
});

function fetchAllComplaints() {
    fetch('http://localhost:5000/api/admin/complaints')
        .then(res => res.json())
        .then(complaints => {
            updateStatsLive(complaints);
            updateRecentDisputesTable(complaints);
            updateAllDisputesTable(complaints);
        })
        .catch(err => {
            console.error('Error fetching complaints:', err);
        });
}

function updateStatsLive(complaints) {
    // Update stat cards with real data
    const total = complaints.length;
    const resolved = complaints.filter(c => c.status && c.status.toLowerCase() === 'resolved').length;
    const pending = complaints.filter(c => c.status && c.status.toLowerCase() === 'pending').length;
    const active = complaints.filter(c => c.status && c.status.toLowerCase() === 'active').length;
    const resolutionRate = total ? ((resolved / total) * 100).toFixed(1) : '0.0';
    // Example: update stat numbers (adjust selectors as needed)
    document.querySelectorAll('.stat-number')[0].textContent = total;
    document.querySelectorAll('.stat-number')[1].textContent = active + pending;
    document.querySelectorAll('.stat-number')[2].textContent = resolutionRate + '%';
    // Avg. days to resolve (dummy for now)
    document.querySelectorAll('.stat-number')[3].textContent = '2.4';
}

function updateRecentDisputesTable(complaints) {
    // Fill the "Recent Disputes" table with the latest 5 complaints
    const table = document.querySelector('.dispute-table tbody');
    if (!table) return;
    table.innerHTML = complaints.slice(0, 5).map(c => `
        <tr>
            <td>#${c.id}</td>
            <td>${c.subject || '(No Subject)'}</td>
            <td>${c.type || '-'}</td>
            <td><span class="status-badge status-${(c.status || 'pending').toLowerCase()}">${c.status || 'Pending'}</span></td>
            <td>${c.ai_response ? 'AI' : '-'}</td>
            <td>${c.created_at ? c.created_at.split('T')[0] : '-'}</td>
        </tr>
    `).join('');
}

function updateAllDisputesTable(complaints) {
    // Fill the "All Disputes" table with all complaints
    const table = document.querySelector('.data-table tbody');
    if (!table) return;
    table.innerHTML = complaints.map(c => `
        <tr>
            <td>#${c.id}</td>
            <td>${c.subject || '(No Subject)'}</td>
            <td>${c.email || '-'}</td>
            <td>${c.type || '-'}</td>
            <td><span class="status-badge status-${(c.status || 'pending').toLowerCase()}">${c.status || 'Pending'}</span></td>
            <td>${c.created_at ? c.created_at.split('T')[0] : '-'}</td>
            <td>
                <button class="btn btn-primary" style="padding: 0.3rem 0.6rem; font-size: 0.8rem;" onclick="openRespondModal(${c.id})">
                    <i class="fas fa-eye"></i> View
                </button>
            </td>
        </tr>
    `).join('');
}

function openRespondModal(complaintId) {
    // Find the complaint data
    fetch('http://localhost:5000/api/admin/complaints')
        .then(res => res.json())
        .then(complaints => {
            const complaint = complaints.find(c => c.id === complaintId);
            if (!complaint) return alert('Complaint not found.');
            // Call AI analytics API
                fetch('http://localhost:5000/api/ai/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ description: complaint.description })
                })
                .then(async res => {
                    let data;
                    try {
                        data = await res.json();
                    } catch (e) {
                        alert('Error parsing AI response.');
                        return;
                    }
                    if (res.ok && data.analysis) {
                        alert('AI Analysis:\n' + data.analysis);
                    } else if (data.error) {
                        alert('AI Error: ' + data.error);
                    } else {
                        alert('No AI suggestion available.');
                    }
                })
                .catch(err => {
                    alert('Error analyzing complaint.');
                    console.error(err);
                });
        });
}
