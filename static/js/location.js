let map;

function getLocation() {

    if (navigator.geolocation) {

        navigator.geolocation.getCurrentPosition(success, error);

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

    Longitude : ${longitude}

    `;

    fetch("/location",{

        method:"POST",

        headers:{

            "Content-Type":"application/json"

        },

        body:JSON.stringify({

            latitude:latitude,

            longitude:longitude

        })

    });

    createMap(latitude,longitude);

}

function createMap(latitude,longitude){

    if(map){

        map.remove();

    }

    map=L.map('map').setView([latitude,longitude],15);

    L.tileLayer(

        'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',

        {

            attribution:'© OpenStreetMap contributors'

        }

    ).addTo(map);

    L.marker([latitude,longitude])

        .addTo(map)

        .bindPopup("📍 You are here")

        .openPopup();

}

function error(){

    alert("Location permission denied.");

}