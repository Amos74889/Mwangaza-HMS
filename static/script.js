async function fetchPredictions() {
    const res = await fetch("/predict");
    const data = await res.json();
    return data.next_7_days_predictions;
}

async function renderDashboard() {
    const predictions = await fetchPredictions();

    // Update Prediction Card
    const predList = document.getElementById("prediction-list");
    predList.innerHTML = "";
    predictions.forEach(p => {
        const li = document.createElement("li");
        li.textContent = `Day ${p.day}: ${p.predicted_admissions.toFixed(0)} admissions`;
        li.style.color = p.predicted_admissions > 100 ? "red" : "green";
        predList.appendChild(li);
    });

    // Update Confidence Card
    const confList = document.getElementById("confidence-list");
    confList.innerHTML = "";
    predictions.forEach(p => {
        const li = document.createElement("li");
        li.textContent = `Day ${p.day}: ${(p.confidence*100).toFixed(0)}%`;
        confList.appendChild(li);
    });

    // Update Chart
    const days = predictions.map(p => "Day " + p.day);
    const values = predictions.map(p => p.predicted_admissions);
    const colors = values.map(v => v > 100 ? 'red' : 'orange');

    const trace = {
        x: days,
        y: values,
        type: 'bar',
        marker: {color: colors},
        text: values.map(v => Math.round(v)),
        textposition: 'auto'
    };

    const layout = {
        title: "Next 7 Days Hospital Admissions",
        xaxis: {title: "Day"},
        yaxis: {title: "Predicted Admissions"},
        margin: { t: 50 }
    };

    Plotly.newPlot('chart', [trace], layout, {responsive: true});

    // Last updated timestamp
    const timestamp = new Date().toLocaleString();
    document.getElementById("last-updated").textContent = `Last updated: ${timestamp}`;
}

function refreshDashboard() {
    renderDashboard();
}

// Initial render
renderDashboard();
