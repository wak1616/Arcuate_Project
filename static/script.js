// Canvas setup and image loading (elements that are used globally)

const canvas = document.getElementById('my_canvas');
const ctx = canvas.getContext('2d');
const eye_img = new Image();

document.getElementById('patient_data').addEventListener('submit', function(e) {
    e.preventDefault();

    // Get values from the form
    let age = document.getElementById('age').value;
    let eye = document.querySelector('input[name="eye"]:checked').value;
    let corneal_astigmatism = document.getElementById('corneal_astigmatism').value;
    let steep_axis = document.getElementById('steep_axis').value;

    // Store form values in the dataset for use when the image loads (a good way to persist data)
    document.getElementById('patient_data').dataset.formValues = JSON.stringify({
        age: age, 
        eye: eye, 
        corneal_astigmatism: corneal_astigmatism, 
        steep_axis: steep_axis
    });

    // Dynamically set the image source based on the selected eye (which triggers reload)
    eye_img.src = eye === 'right' ? 'static/righteyetemplate.jpg' : 'static/lefteyetemplate.jpg';
});


//Send data to back-end, wait for data to come back, and then use it to produce image and arcuates info for the user
eye_img.onload = function() {
    let formValues = document.getElementById('patient_data').dataset.formValues;
    if (formValues) {
        formValues = JSON.parse(formValues);
        // Send the values to the Flask server for calculation
        fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formValues)   
        })
        .then(response => response.json())
        .then(data => {
            // Use the calculated value to render the image of the arcuate(s) on the eye
            renderImage(data, formValues.eye);
            // Use the calculated values to render the text underneath the canvas
            let arcuate1text = data.arcuate1text;
            let arcuate2text = data.arcuate2text;
            document.getElementById('arcuate1_display').textContent = arcuate1text;
            document.getElementById('arcuate2_display').textContent = arcuate2text;
        })
        .catch(error => console.error('Error:', error));
    }
};

// Function to draw arcs based on received data
function renderImage(data, eye) {
    // clear the canvas and redraw the background image for a fresh start
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // Reset transformations before applying new ones
    ctx.setTransform(1, 0, 0, 1, 0, 0); // Reset to the identity matrix
    ctx.scale(0.5, 0.5);

    ctx.drawImage(eye_img, 0, 0, canvas.width, canvas.height);

    //DRAWING ARC CODE
    let arc1start = data.arc1start;
    let arc1end = data.arc1end;
    let arc2start = data.arc2start;
    let arc2end = data.arc2end;
    if (eye == "left") {
        ctx.beginPath();
        ctx.arc(1454/3, 999/3, 751/3, arc1start, arc1end); // x, y, radius, startAngle, endAngle
        ctx.strokeStyle = '#FFFF00'; // Yellow Line color
        ctx.lineWidth = 10; // Line width
        ctx.stroke();
        if (data.arc2start != null) {
            ctx.beginPath();
            ctx.arc(1454/3, 999/3, 751/3, arc2start, arc2end); // x, y, radius, startAngle, endAngle
            ctx.strokeStyle = '#FFA500'; // Orange Line color
            ctx.lineWidth = 10; // Line width
            ctx.stroke();
        }
    } else if (eye === "right") {
        ctx.beginPath();
        ctx.arc(1312/3, 1024/3, 751/3, arc1start, arc1end);
        ctx.strokeStyle = '#FFFF00'; // Yellow Line color
        ctx.lineWidth = 10; // Line width
        ctx.stroke();
        if (data.arc2start != null) {
            ctx.beginPath();
            ctx.arc(1312/3, 1024/3, 751/3, arc2start, arc2end); // x, y, radius, startAngle, endAngle
            ctx.strokeStyle = '#FFA500'; // Orange Line color
            ctx.lineWidth = 10; // Line width
            ctx.stroke();
        }
    }
}


