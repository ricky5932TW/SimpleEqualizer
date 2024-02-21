function updateContent() {
    fetch('/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ /* data if needed */ })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('instruction').textContent = data.instruction;
        document.getElementById('status').textContent = data.status;
        document.getElementById('pic1').src = data.pic1;
        document.getElementById('pic2').src = data.pic2;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}