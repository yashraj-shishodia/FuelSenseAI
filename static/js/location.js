function getLocation() {

    if (navigator.geolocation) {

        navigator.geolocation.getCurrentPosition(

            success,

            error

        );

    }

    else {

        alert("Geolocation is not supported.");

    }

}

function success(position) {

    const latitude = position.coords.latitude;

    const longitude = position.coords.longitude;

    document.getElementById("result").innerHTML =

        `
        Latitude : ${latitude}<br>
        Longitude: ${longitude}
        `;

    fetch("/location", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            latitude: latitude,

            longitude: longitude

        })

    })

    .then(response => response.json())

    .then(data => {

        console.log(data);

    });

}

function error() {

    alert("Location permission denied.");

}