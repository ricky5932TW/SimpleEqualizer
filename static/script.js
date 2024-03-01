function updateImg_json() {
            var pic1 = document.getElementById('pic1');
            var pic2 = document.getElementById('pic2');
            // destroy the old image

            fetch('/img')
                .then(response => response.json())
                // forbidden cache on web browser
                .then(data => {
                    pic1.src = data.spectrum + '?' + new Date().getTime();
                    pic2.src = data.full + '?' + new Date().getTime();
                })
                /*
                .then(data => {
                    pic1.src = data.spectrum;
                    pic2.src = data.full;
                })
                */
                .catch(error => console.error('Error:', error));
            console.log("updateImg");
        }


function update_json_limited() {
            var pic1 = document.getElementById('pic1');
            var pic2 = document.getElementById('pic2');
            // destroy the old image

            fetch('/img')
                .then(response => response.json())
                // forbidden cache on web browser
                .then(data => {
                    pic1.src = data.spectrum + '?' + new Date().getTime();
                    pic2.src = data.full + '?' + new Date().getTime();
                })
                /*
                .then(data => {
                    pic1.src = data.spectrum;
                    pic2.src = data.full;
                })
                */
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

function shutdownServer() {
    fetch('/shutdown', {
        method: 'POST',
        headers: {
            'Authorization': 'gnhjr5og7wud'  // 使用实际的令牌
        }
    })
    .then(response => response.text())
    .then(data => console.log(data))
    .catch((error) => {
        console.error('Error:', error);
    });
    alert("Service is shutting down");
}



//setInterval(updateImg, 1000);
setInterval(updateImg_json, 1000);

setInterval(updateStatus, 500);




