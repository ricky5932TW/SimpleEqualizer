function updateImg() {
            var pic1 = document.getElementById('pic1');
            var pic2 = document.getElementById('pic2');
            pic1.src = "/static/temp_img/Spectrum.png" ;
            pic2.src = "/static/temp_img/full.png" ;
            console.log("updateImg");
        }

function fetchTextAndUpdate() {
            fetch('/get-text')
                .then(response => response.text())
                .then(text => {
                    document.getElementById('text-container').innerText = text;
                })
                .catch(error => console.error('Error:', error));
        }

setInterval(updateImg, 1000);
setInterval(fetchTextAndUpdate, 5000);



