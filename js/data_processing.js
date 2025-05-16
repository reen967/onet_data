// data_processing.js
const fetchData = async () => {
    const response = await fetch('data/merged_data.json');
    const data = await response.json();
    return data;
};
