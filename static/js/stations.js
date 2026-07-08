async function loadStations(latitude, longitude, predictionTime = null) {

    console.log("Loading Stations...");

    const body = {
        latitude: latitude,
        longitude: longitude
    };

    // Optional Prediction Time
    if (predictionTime) {
        body.prediction_time = predictionTime;
    }

    const response = await fetch("/stations", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(body)

    });

    const data = await response.json();

    if (!data.features || data.features.length === 0) {

        alert("No Fuel Stations Found");

        return;

    }

    stationLayer.clearLayers();

    const stationList = document.getElementById("stationList");

    stationList.innerHTML = "";

    data.features.forEach((station, index) => {

        const lat = station.geometry.coordinates[1];
        const lon = station.geometry.coordinates[0];

        const props = station.properties;

        const name = props.name || "Fuel Station";

        const brand = props.brand || "Unknown";

        const address =
            props.formatted || "Address Not Available";

        const distance = station.distance;

        const crowd = station.predicted_crowd;

        const waiting = station.waiting_time;

        const score = station.prediction_score;

        let crowdColor = "green";

        if (crowd === "MEDIUM")
            crowdColor = "orange";

        else if (crowd === "HIGH")
            crowdColor = "#ff5722";

        else if (crowd === "VERY HIGH")
            crowdColor = "red";


        // -----------------------------
        // Marker
        // -----------------------------

        L.marker([lat, lon])

            .addTo(stationLayer)

            .bindPopup(`

                <b>${name}</b><br>

                Brand : ${brand}<br>

                Crowd :
                <span style="color:${crowdColor};font-weight:bold;">
                ${crowd}
                </span><br>

                Waiting :
                ${waiting} min<br>

                Distance :
                ${distance.toFixed(2)} km<br><br>

                <a target="_blank"
                href="https://www.google.com/maps/dir/?api=1&destination=${lat},${lon}">

                Navigate

                </a>

            `);


        // -----------------------------
        // Recommendation
        // -----------------------------

        if (index === 0) {

            stationList.innerHTML += `

            <div class="station-card recommended">

                <h2>⭐ Recommended Station</h2>

                <h3>${name}</h3>

                <p><b>Brand :</b> ${brand}</p>

                <p>${address}</p>

                <p><b>Distance :</b> ${distance.toFixed(2)} km</p>

                <p>

                <b>Predicted Crowd :</b>

                <span style="color:${crowdColor};font-weight:bold;">

                ${crowd}

                </span>

                </p>

                <p>

                <b>Estimated Waiting :</b>

                ${waiting} minutes

                </p>

                <p><b>Prediction Time :</b>
${predictionTime ? predictionTime.replace("T"," ") : "Current Time"}
</p>

                <p>

                <b>Prediction Score :</b>

                ${score}

                </p>

                <p>

<b>Reason :</b>

Lowest waiting time and nearest recommended station.

</p>

                <button
                class="navigate-btn"
                onclick="window.open('https://www.google.com/maps/dir/?api=1&destination=${lat},${lon}','_blank')">

                🧭 Open in Google Maps

                </button>

            </div>

            `;
        }


        // -----------------------------
        // Other Stations
        // -----------------------------

        stationList.innerHTML += `

        <div class="station-card">

            <h2>${index + 1}. ${name}</h2>

            <p><b>Brand :</b> ${brand}</p>

            <p>${address}</p>

            <p><b>Distance :</b> ${distance.toFixed(2)} km</p>

            <p>

            <b>Crowd :</b>

            <span style="color:${crowdColor};font-weight:bold;">

            ${crowd}

            </span>

            </p>

            <p>

            <b>Waiting :</b>

            ${waiting} min

            </p>

            <p><b>Prediction Time :</b>
${predictionTime ? predictionTime.replace("T"," ") : "Current Time"}
</p>

            <button
            class="navigate-btn"
            onclick="window.open('https://www.google.com/maps/dir/?api=1&destination=${lat},${lon}','_blank')">

            Navigate

            </button>

        </div>

        `;

    });

}