function renderCategoryChart(labels, values) {
    const ctx = document.getElementById("categoryChart");
    if (!ctx) return;

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Complaints",
                data: values,
                backgroundColor: "#0d6efd"
            }]
        }
    });
}
