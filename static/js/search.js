async function searchLocation() {

    const location = document.getElementById("locationInput").value;

    if (location.trim() === "") {

        alert("Please enter a location");

        return;

    }

    const response = await fetch("/search", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            location: location
        })

    });

    const data = await response.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    if (!data.results || data.results.length === 0) {

        alert("Location not found");

        return;

    }

    const latitude = data.results[0].lat;
    const longitude = data.results[0].lon;

    document.getElementById("result").innerHTML =

        `Latitude : ${latitude}<br>Longitude : ${longitude}`;

    createMap(latitude, longitude);

    // ----------------------------
    // Optional Prediction Time
    // ----------------------------

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

}