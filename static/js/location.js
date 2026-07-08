let map;
let stationLayer;

function createMap(latitude, longitude) {

    if (!map) {

        map = L.map("map").setView([latitude, longitude], 14);

        L.tileLayer(
            "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            {
                attribution: "&copy; OpenStreetMap Contributors"
            }
        ).addTo(map);

        stationLayer = L.layerGroup().addTo(map);

    } else {

        map.setView([latitude, longitude], 14);

        stationLayer.clearLayers();

    }

    L.marker([latitude, longitude])
        .addTo(map)
        .bindPopup("Your Location")
        .openPopup();

}


function getDistance(lat1, lon1, lat2, lon2) {

    const R = 6371;

    const dLat = (lat2 - lat1) * Math.PI / 180;

    const dLon = (lon2 - lon1) * Math.PI / 180;

    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * Math.PI / 180) *
        Math.cos(lat2 * Math.PI / 180) *
        Math.sin(dLon / 2) *
        Math.sin(dLon / 2);

    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return R * c;

}


function getCurrentLocation() {

    if (!navigator.geolocation) {

        alert("Geolocation not supported");

        return;

    }

    navigator.geolocation.getCurrentPosition(

        function(position) {

            const latitude = position.coords.latitude;

            const longitude = position.coords.longitude;

            document.getElementById("result").innerHTML =
                `Latitude : ${latitude}<br>Longitude : ${longitude}`;

            createMap(latitude, longitude);

            const date =
                document.getElementById("predictionDate").value;

            const time =
                document.getElementById("predictionTime").value;

            let predictionTime = null;

            if (date !== "" && time !== "") {

                predictionTime = `${date}T${time}`;

            }

            loadStations(

                latitude,

                longitude,

                predictionTime

            );

        },

        function() {

            alert("Unable to fetch location");

        }

    );

}