const GITHUB_RAW = 'https://raw.githubusercontent.com/reen967/onet_data/main/';
const OCCUPATIONS_CSV = GITHUB_RAW + 'occupation_data.csv';
const ABILITIES_CSV = GITHUB_RAW + 'abilities.csv';

let occupations = [];
let abilities = [];

window.onload = () => {
  loadCSVs().then(() => {
    document.getElementById('searchBox').addEventListener('input', displayResults);
    displayResults();
  });
};

async function loadCSVs() {
  const occData = await fetchCSV(OCCUPATIONS_CSV);
  const abilData = await fetchCSV(ABILITIES_CSV);
  occupations = occData;
  abilities = abilData.filter(row => row['Scale ID'] === 'IM'); // only show Importance values
}

function fetchCSV(url) {
  return fetch(url)
    .then(r => r.text())
    .then(t => Papa.parse(t, { header: true }).data);
}

function displayResults() {
  const q = document.getElementById('searchBox').value.toLowerCase();
  const results = occupations.filter(o => o['Title'].toLowerCase().includes(q)).slice(0, 10);

  const container = document.getElementById('results');
  container.innerHTML = '';

  for (const occ of results) {
    const code = occ['O*NET-SOC Code'];
    const relatedAbilities = abilities
      .filter(a => a['O*NET-SOC Code'] === code)
      .map(a => `<li>${a['Abilities Element Name']} (Importance: ${a['Data Value']})</li>`)
      .join('');

    container.innerHTML += `
      <div class="occupation">
        <h2>${occ['Title']}</h2>
        <p><strong>Description:</strong> ${occ['Description']}</p>
        <p><strong>Abilities:</strong></p>
        <ul>${relatedAbilities || '<li>No data available</li>'}</ul>
      </div>
    `;
  }
}
