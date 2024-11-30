// Set up the canvas and get the 2D drawing context (elements that are used globally)       
const canvas = document.getElementById('my_canvas');        
const ctx = canvas.getContext('2d');    

// Create a new image object for the eye
const eye_img = new Image();

// Add an event listener to the form submission
document.getElementById('patient_data').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the form from actually submitting and refreshing the page

    // Collect the form data
    let formValues = { //this is a javascript object (similar to a dictionary in python, but also has methods and properties)
        age: document.getElementById('age').value,
        eye: document.querySelector('input[name="eye"]:checked').value,
        sex: document.querySelector('input[name="sex"]:checked').value,
        cassini_corneal_astigmatism: document.getElementById('cassini_corneal_astigmatism').value,
        iolmaster700_corneal_astigmatism: document.getElementById('iolmaster700_corneal_astigmatism').value,
        steep_axis: document.getElementById('steep_axis').value,
        Mean_K: document.getElementById('Mean_K').value,
        WTW: document.getElementById('WTW').value
    };

    // Store form values in the html5 patient_data element for use when the image loads
    document.getElementById('patient_data').dataset.formValues = JSON.stringify(formValues);

    // Dynamically set the image source based on the selected eye (which triggers image load)
    eye_img.src = formValues.eye === 'OD' ? 'static/righteyetemplate.jpg' : 'static/lefteyetemplate.jpg';
});

// When the image loads, send form data to the server and render the image with arcuates
eye_img.onload = function() {
    let formValues = JSON.parse(document.getElementById('patient_data').dataset.formValues || '{}'); // the || prevents runtime error if the formValues are not yet set ( a common pattern in javascript to handle optional or missing data gracefully)
    if (Object.keys(formValues).length) {  // Object.keys() returns an array of a object's own property names, so we are checking if the formValues object has any properties / is not empty / has any "length"
        // Send the values to the server for calculation
        fetch('/calculate', {  // fetch is an ajax call to the server
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formValues)   
        })
        .then(response => response.json())
        .then(data => {
            console.log('Received calculated arcuate data:', data);

            // Render the eye image with the calculated arcuates
            renderImage(data, formValues.eye);

            // Display the calculated arcuate texts beneath the canvas
            document.getElementById('arcuate1_display').textContent = data.arcuate1text;
            document.getElementById('arcuate2_display').textContent = data.arcuate2text;
        })
        .catch(error => console.error('Error:', error));
    }
};

// Function to render the eye image and draw the arcuates
function renderImage(data, eye) {
    // Clear the canvas and reset any transformations
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.setTransform(1, 0, 0, 1, 0, 0); // Reset to the identity matrix
    ctx.scale(0.75, 0.75); // // Scale down the drawing context to 75% of its original size
    ctx.drawImage(eye_img, 0, 0, canvas.width, canvas.height);

    // Define common properties for the arcs
    const radius = 250.3334; 

    // Set the center coordinates of the arcuate at 3 o clock on the eye based on the selected eye
    let x, y;
    if (eye === 'OS') { // Left Eye
        x = 484.666; 
        y = 333.000;               
    } else {             // Right Eye (OD)
        x = 437.333;  
        y = 341.333;  
    }

    // Array containing arcuate data and styles
    const arcs = [
        {
            startAngle: data.arc1start,
            endAngle: data.arc1end,
            color: '#FFFF00' // Yellow line color
        },
        {
            startAngle: data.arc2start,
            endAngle: data.arc2end,
            color: '#FFA500' // Orange line color
        }
    ];

    // Draw each arcuate on the canvas
    arcs.forEach(arc => {
        ctx.beginPath();
        ctx.arc(x, y, radius, arc.startAngle, arc.endAngle);  // because initial coordinates of canvas plot start at 3 o clock and go clockwise, it makes sense to also draw arcs clockwise (so do not set "true" parameter which would draw in CCW direction)
        ctx.strokeStyle = arc.color;
        ctx.lineWidth = 10;
        ctx.stroke();
    });
}

