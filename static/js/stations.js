let latestRecommendation = null;
let markers = [];

async function loadStations(latitude, longitude, predictionTime = null) {

    console.log("Loading Stations...");

    const body = {

        latitude: latitude,
        longitude: longitude

    };

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

    markers = [];

    const stationList =
        document.getElementById("stationList");

    const recommendedStation =
        document.getElementById("recommendedStation");

    stationList.innerHTML = "";

    recommendedStation.innerHTML = "";

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

                const marker = L.marker([lat, lon])

            .addTo(stationLayer)

            .bindPopup(`

                <b>${name}</b><br>

                Brand : ${brand}<br>

                Crowd :

                <span style="color:${crowdColor};font-weight:bold;">

                ${crowd}

                </span><br>

                Waiting : ${waiting} min<br>

                Distance : ${distance.toFixed(2)} km<br><br>

                <a target="_blank"

                href="https://www.google.com/maps/dir/?api=1&destination=${lat},${lon}">

                Navigate

                </a>

            `);

        markers.push(marker);

        if (index === 0) {

            latestRecommendation = {

    station_name: name,

    brand: brand,

    latitude: lat,

    longitude: lon,

    prediction_time: predictionTime
        ? predictionTime
        : new Date().toISOString(),

    weather: "Unknown",

    predicted_waiting: waiting

};

            recommendedStation.innerHTML = `

            <div class="station-card recommended">

                

                <h3>${name}</h3>

                <p><b>Brand :</b> ${brand}</p>

                <p>${address}</p>

                <p>

                    <b>Distance :</b>

                    ${distance.toFixed(2)} km

                </p>

                <p>

    <b>Predicted Crowd :</b>

    <span style="color:${crowdColor};font-weight:bold;">

        ${crowd}

    </span>

</p>

                <p>

                    <b>Estimated Waiting :</b>

                    ${waiting} min

                </p>

                <p>

                    <b>Recommendation Score :</b>

                    ${score}/100

                </p>

                <p>

                    <b>Why Recommended?</b><br>

                    ✔ Lowest predicted waiting time<br>

                    ✔ Close to your location<br>

                    ✔ Best overall recommendation

                </p>

                <button
                    class="navigate-btn"
                    onclick="window.open('https://www.google.com/maps/dir/?api=1&destination=${lat},${lon}','_blank')">

                    🧭 Open in Google Maps

                </button>

            </div>

            `;

            setTimeout(showFeedbackPopup, 120000);

            return;

        }

        stationList.innerHTML += `

        <div class="station-card"

            onclick="focusStation(${index})">

            <h3>${name}</h3>

            <p><b>Brand :</b> ${brand}</p>

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

            <p>

                <b>Distance :</b>

                ${distance.toFixed(2)} km

            </p>

            <button
                class="navigate-btn"
                onclick="event.stopPropagation();window.open('https://www.google.com/maps/dir/?api=1&destination=${lat},${lon}','_blank')">

                Navigate

            </button>

        </div>

        `;

    });

}

function focusStation(index) {

    if (!markers[index])
        return;

    const marker = markers[index];

    map.setView(marker.getLatLng(), 16, {

        animate: true,
        duration: 1

    });

    marker.openPopup();

}


async function submitFeedback(rating) {

    if (!latestRecommendation)
        return;

    let actualWaiting = latestRecommendation.predicted_waiting;

    if (rating === 2) {

        const value = document.getElementById("actualWaiting").value;

        if (!value) {

            alert("Please enter the actual waiting time.");

            return;

        }

        actualWaiting = Number(value);

    }

    try {

        const response = await fetch("/feedback", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                station_name: latestRecommendation.station_name,

                brand: latestRecommendation.brand,

                latitude: latestRecommendation.latitude,

                longitude: latestRecommendation.longitude,

                prediction_time: latestRecommendation.prediction_time,

                weather: latestRecommendation.weather,

                predicted_waiting: latestRecommendation.predicted_waiting,

                actual_waiting: actualWaiting,

                rating: rating

            })

        });

        const result = await response.json();

        if (result.success) {

            document.getElementById("feedbackModal").style.display = "none";

            alert("Thank you! Your feedback has been saved.");

        } else {

            alert("Unable to save feedback.");

        }

    } catch (error) {

        console.error(error);

        alert("Server Error");

    }

}


function showFeedbackPopup() {

    const modal = document.getElementById("feedbackModal");

    if (modal) {

        modal.style.display = "flex";

    }

}


function showActualWaitingInput() {

    const container = document.getElementById("actualWaitingContainer");

    if (container) {

        container.style.display = "block";

    }

}
