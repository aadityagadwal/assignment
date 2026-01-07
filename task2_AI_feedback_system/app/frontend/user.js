const submitBtn = document.getElementById("submitBtn");
const responseBox = document.getElementById("response");

submitBtn.addEventListener("click", async () => {
    const rating = document.getElementById("rating").value;
    const review = document.getElementById("review").value;

    responseBox.style.display = "none";
    responseBox.innerHTML = "";
    responseBox.className = "response-box";

    // Validation: only rating is required
    if (!rating) {
        responseBox.innerHTML = `<div class="error"><strong>⚠️ Error:</strong> Please provide a rating.</div>`;
        responseBox.className = "response-box error-state";
        responseBox.style.display = "block";
        return;
    }

    submitBtn.disabled = true;
    responseBox.innerHTML = `<div class="loading">Processing your feedback...</div>`;
    responseBox.className = "response-box loading-state";
    responseBox.style.display = "block";

    try {
        const res = await fetch("/submit-review", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                rating: Number(rating),
                review: review || ""
            })
        });

        if (!res.ok) {
            throw new Error(`Server error: ${res.status}`);
        }

        const data = await res.json();

        // Success state with AI response
        responseBox.innerHTML = `
            <div class="success-container">
                <div class="success-header">✅ Thank You!</div>
                <div class="ai-response">
                    <p><strong>Our Response:</strong></p>
                    <p>${data.message}</p>
                </div>
                <div class="success-footer">Your feedback has been recorded and analyzed.</div>
            </div>
        `;
        responseBox.className = "response-box success-state";

        // Clear form
        document.getElementById("rating").value = "";
        document.getElementById("review").value = "";

    } catch (err) {
        console.error("Error:", err);
        responseBox.innerHTML = `
            <div class="error">
                <strong>❌ Error:</strong> ${err.message || "Something went wrong. Please try again."}
            </div>
        `;
        responseBox.className = "response-box error-state";
    } finally {
        submitBtn.disabled = false;
        responseBox.style.display = "block";
    }
});
