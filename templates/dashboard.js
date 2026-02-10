fetch("/api/predictions")
  .then(res => res.json())
  .then(data => {
    document.getElementById("confidence").innerText =
      "BIC Score: " + data.confidence;

    const ctx = document.getElementById("chart");

    new Chart(ctx, {
      type: 'line',
      data: {
        labels: ["T-6","T-5","T-4","T-3","T-2","T-1","Now","+1","+2","+3","+4","+5","+6","+7"],
        datasets: [
          {
            label: "Historical Admissions",
            data: data.historical,
            borderColor: "blue",
            fill: false
          },
          {
            label: "Predicted Admissions",
            data: new Array(7).fill(null).concat(data.predicted),
            borderColor: "green",
            borderDash: [5,5],
            fill: false
          }
        ]
      }
    });
  });
