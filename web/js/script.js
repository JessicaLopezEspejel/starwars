
let empire_params;
let boat_params;

// Function to read boat_params from the backend
async function readBoatParamsFromBackend() {
    try {
        const response = await fetch('./config/millennium-falcon.json'); // Adjust the endpoint as needed
        if (response.ok) {
            boat_params = await response.json();
            console.log('Boat Params from Backend:', boat_params);
        } else {
            console.error('Failed to fetch boat_params from backend:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching boat_params:', error);
    }
}

// Call the function to read boat_params when the page loads
window.addEventListener('load', readBoatParamsFromBackend);

function readFile(paramsType) {
    const input = document.getElementById('fileInput');
    const selectedFile = document.getElementById('selectedFile');
    const output = document.getElementById('output');

    const file = input.files[0];
    if (!file) {
        alert('Please select a file.');
        return;
    }

    const reader = new FileReader();
    // It is only to set style to the JSON format that will be display
    reader.onload = function(e) {
        try {
            if (paramsType === 'empire') {
                empire_params = JSON.parse(e.target.result);
                output.innerHTML = '<pre>' + syntaxHighlight(empire_params) + '</pre>';
            }else{
                alert('Invalid paramsType.');
            }
        } catch (error) {
            output.textContent = 'Error reading the file. Make sure it is a valid JSON file.';
        }
    };

    reader.readAsText(file);
}

// Add an event listener to the file input to update the selected file name
fileInput.addEventListener('change', function() {
    const fileName = this.files[0].name;
    selectedFile.textContent = fileName;
});


// Set style to the JSON file
function syntaxHighlight(json) {
    json = JSON.stringify(json, null, 4);
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)/g,
        function (match) {
            let cls = 'number';
            if (/^"/.test(match)) {
                if (/:$/.test(match)) {
                    cls = 'key';
                } else {
                    cls = 'string';
                }
            } else if (/true|false/.test(match)) {
                cls = 'boolean';
            } else if (/null/.test(match)) {
                cls = 'null';
            }
            return '<span class="' + cls + '">' + match + '</span>';
        });
}

function computeOdds() {
    const oddsOutput = document.getElementById('oddsOutput');
    // oddsOutput.textContent = 'Show odds';
    
    if (empire_params && boat_params) {
        const params = {
            boat_params: boat_params,
            empire_params: empire_params
    };

    // Make a POST request to the API endpoint
    fetch('http://127.0.0.1:5000/api/computeOdds', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
    })
    .then(response => response.json())
    .then(data => {
        // Update oddsOutput with the computed probability
        oddsOutput.textContent = 'Probability of success: ' + data.probability + " %";
    })
    .catch(error => {
        console.error('Error fetching odds:', error);
        oddsOutput.textContent = 'Error fetching odds.';
    });
    } else {
        alert('Please read both JSON files first.');
    }
}

function cleanContent() {
    // Clear oddsOutput content
    document.getElementById('oddsOutput').textContent = '';

    // Clear file-related elements
    const fileInput = document.getElementById('fileInput');
    fileInput.value = '';

    // Clear the content of the selectedFile span
    const selectedFile = document.getElementById('selectedFile');
    selectedFile.textContent = '';

    // Clear the content of the output div
    const outputDiv = document.getElementById('output');
    outputDiv.textContent = '';

    // Add an event listener to the file input to update the selected file name
    fileInput.addEventListener('change', function() {
        const fileName = this.files[0] ? this.files[0].name : '';
        selectedFile.textContent = fileName;
    });
}

