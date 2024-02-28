function updateImg() {
            var pic1 = document.getElementById('pic1');
            var pic2 = document.getElementById('pic2');
            // destroy the old image
            pic1.src = "";
            pic2.src = "";
            pic1.src = "/static/temp_img/Spectrum.png" ;
            pic2.src = "/static/temp_img/full.png" ;
            console.log("updateImg");
        }

// update the image with json data
function updateImg_json() {
            var pic1 = document.getElementById('pic1');
            var pic2 = document.getElementById('pic2');
            // destroy the old image

            fetch('/img')
                .then(response => response.json())
                .then(data => {
                    pic1.src = data.spectrum;
                    pic2.src = data.full;
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


//setInterval(updateImg, 1000);
setInterval(updateImg_json, 1000);
setInterval(updateStatus, 1000);




