const SHEET_ID = '1VDhmvE0dUElPv05FZKqXK43hMF7TkRIaRSLwAIc65aQ';
const SHEET_NAME = 'Sheet1'; // Adjust to the actual sheet name if different

async function fetchData() {
    const response = await fetch(`https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?tqx=out:json&sheet=${SHEET_NAME}`);
    const text = await response.text();
    const json = JSON.parse(text.substring(47, text.length - 2));
    return json.table.rows.map(row => row.c.map(cell => cell ? cell.v : ''));
}

function createTable(data) {
    const headerRow = document.getElementById('header-row');
    const dataRows = document.getElementById('data-rows');

    // Create the table header for 'Name' and 'Time-Out'
    ['Adm No', 'Answer'].forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        headerRow.appendChild(th);
    });

    // Populate the table with data from the sheet
    data.forEach(row => {
        const tr = document.createElement('tr');
        row.slice(0, 2).forEach((cell, index) => {
            const td = document.createElement('td');


            
            // Check if the cell is a date string and format it
            
            if (index === 1 && typeof cell === 'string' && cell.startsWith('Date')) {

                if (parseInt(cell.slice(15,17))>11) {
                    add = ' PM'
                } else {
                    add = ' AM'
                }
                
                var parts = cell.replace('Date(2024,7,19,','');
                var parts = parts.replace('Date(2024,7,20,','');
                var parts = parts.replace('Date(2024,7,21,','');
                var parts = parts.replace('Date(2024,7,22,','');
                var parts = parts.replace(')','');
                var parts = parts.replace(',',':');
                var parts = parts.replace(',',':');
                td.textContent = parts.concat(add);
                
                //const date = new Date(eval(cell)); // Convert serialized date string to Date object
                //td.textContent = date.toLocaleString(); // Format the date as 'MM/DD/YYYY, HH:MM:SS AM/PM'
            } else {
                td.textContent = cell;
            }
            

            //cell = new Date(cell)

            //td.textContent = cell;
            


            td.setAttribute('data-label', ['Name', 'Time-Out'][index]);
            tr.appendChild(td);
        });
        dataRows.appendChild(tr);
    });
}

// Add event listener to download button
document.getElementById('downloadBtn').addEventListener('click', function() {
    const url = `https://docs.google.com/spreadsheets/d/${SHEET_ID}/export?format=xlsx&id=${SHEET_ID}`;
    const link = document.createElement('a');
    link.href = url;
    link.download = 'Student_Report.xlsx';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});

fetchData().then(data => {
    createTable(data);
}).catch(error => {
    console.error('Error fetching data:', error);
});
