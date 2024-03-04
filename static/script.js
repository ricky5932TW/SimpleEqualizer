function updateImg_json() {
            var pic1 = document.getElementById('pic1');
            var pic2 = document.getElementById('pic2');

            fetch('/img')
                .then(response => response.json())

                .then(data => {
                    pic1.src = data.spectrum + '?' + new Date().getTime();
                    pic2.src = data.full + '?' + new Date().getTime();
                })
                .catch(error => console.error('Error:', error));
            console.log("updateImg");
        }


function update_json_limited() {
            var pic3 = document.getElementById('pic3');

            // destroy the old image

            fetch('/img_limited')
                .then(response => response.json())
                // forbidden cache on web browser
                .then(data => {
                    pic3.src = data.full + '?' + new Date().getTime();
                })

                .catch(error => console.error('Error:', error));
            console.log("updateImg");
        }



function updateStatus() {
            var statusElement = document.getElementById('status');
            fetch('/status')
                .then(response => response.json())
                .then(data => {
                    statusElement.innerText = data.status;
                })
                .catch(error => console.error('Error:', error));
            console.log("updateStatus");
        }

function updateInstruction() {
            var statusElement = document.getElementById('instruction');
            fetch('/instruction')
                .then(response => response.json())
                .then(data => {
                    statusElement.innerText = data.instruction;
                })
                .catch(error => console.error('Error:', error));
            console.log("updateStatus");
        }

function shutdownServer() {
    fetch('/shutdown', {
        method: 'POST',

    })
    .then(response => response.text())
    .then(data => console.log(data))
    .catch((error) => {
        console.error('Error:', error);
    });
    alert("Service is shutting down");
}











