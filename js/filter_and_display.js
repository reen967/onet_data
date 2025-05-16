
// filter_and_display.js
const applyFilters = () => {
    const occupationCode = document.getElementById("occupation").value;
    const importance = document.getElementById("importance").value;
    const level = document.getElementById("level").value;
    const context = document.getElementById("context").value;

    fetchData().then(data => {
        const filteredData = data.filter(item => {
            return item['O*NET-SOC Code'].includes(occupationCode) &&
                item['Importance'] >= importance &&
                item['Level'] >= level &&
                item['Work Context'] === context;
        });

        displayResults(filteredData);
    });
};

const displayResults = (filteredData) => {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';
    
    filteredData.forEach(item => {
        const div = document.createElement('div');
        div.className = 'result-item';
        div.innerHTML = `
            <h3>${item['Title']}</h3>
            <p>${item['Description']}</p>
        `;
        resultsDiv.appendChild(div);
    });
};
