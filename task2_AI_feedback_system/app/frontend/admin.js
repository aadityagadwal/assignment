const submissionsDiv = document.getElementById("submissions");
const statusDiv = document.getElementById("status");
const filterSelect = document.getElementById("filterRating");
const refreshBtn = document.getElementById("refreshBtn");

let allSubmissions = [];

function getStarRating(rating) {
    return "⭐".repeat(rating);
}

function updateAnalytics() {
    const totalCount = allSubmissions.length;
    const avgRating = totalCount > 0 
        ? (allSubmissions.reduce((sum, item) => sum + item.user_rating, 0) / totalCount).toFixed(1)
        : 0;
    
    // Update stat cards
    document.getElementById("totalCount").textContent = totalCount;
    document.getElementById("avgRating").textContent = avgRating;
    
    const now = new Date();
    document.getElementById("lastUpdate").textContent = now.toLocaleTimeString();

    // Calculate rating distribution
    const distribution = { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 };
    allSubmissions.forEach(item => {
        distribution[item.user_rating]++;
    });

    const distributionDiv = document.getElementById("distribution");
    distributionDiv.innerHTML = "";
    for (let i = 5; i >= 1; i--) {
        const count = distribution[i];
        const percentage = totalCount > 0 ? ((count / totalCount) * 100).toFixed(0) : 0;
        const barWidth = percentage;
        
        distributionDiv.innerHTML += `
            <div class="dist-row">
                <span class="dist-label">${getStarRating(i)}</span>
                <div class="dist-bar-container">
                    <div class="dist-bar" style="width: ${barWidth}%"></div>
                </div>
                <span class="dist-count">${count} (${percentage}%)</span>
            </div>
        `;
    }
}

function renderSubmissions(filter = "") {
    const filtered = filter 
        ? allSubmissions.filter(item => item.user_rating === Number(filter))
        : allSubmissions;

    submissionsDiv.innerHTML = "";

    if (filtered.length === 0) {
        statusDiv.textContent = "No submissions found.";
        return;
    }

    statusDiv.textContent = `Showing ${filtered.length} of ${allSubmissions.length} submissions`;

    filtered.forEach((item, index) => {
        const div = document.createElement("div");
        div.className = "submission-card";
        div.innerHTML = `
            <div class="submission-header">
                <div class="rating-badge">${getStarRating(item.user_rating)}</div>
                <div class="submission-time">${new Date(item.created_at).toLocaleString()}</div>
            </div>
            
            <div class="submission-body">
                <div class="section">
                    <strong>User Review:</strong>
                    <p>${item.user_review || '<em>(No review provided)</em>'}</p>
                </div>

                <div class="section">
                    <strong>AI Summary:</strong>
                    <p>${item.ai_summary}</p>
                </div>

                <div class="section">
                    <strong>Recommended Action:</strong>
                    <p class="action-text">${item.ai_action}</p>
                </div>
            </div>
        `;
        submissionsDiv.appendChild(div);
    });
}

async function loadSubmissions() {
    try {
        const res = await fetch("/submissions");

        if (!res.ok) {
            throw new Error("Failed to fetch submissions");
        }

        allSubmissions = await res.json();
        updateAnalytics();
        renderSubmissions(filterSelect.value);

    } catch (error) {
        console.error("Error loading submissions:", error);
        statusDiv.textContent = "Error loading submissions.";
    }
}

// Event listeners
filterSelect.addEventListener("change", (e) => {
    renderSubmissions(e.target.value);
});

refreshBtn.addEventListener("click", () => {
    refreshBtn.textContent = "🔄 Refreshing...";
    loadSubmissions();
    setTimeout(() => {
        refreshBtn.textContent = "🔄 Refresh Now";
    }, 500);
});

// Initial load
loadSubmissions();

// Auto-refresh every 5 seconds
setInterval(loadSubmissions, 5000);

