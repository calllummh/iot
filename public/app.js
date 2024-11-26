/* jslint es6 */
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.8/firebase-app.js";
import { getDatabase, ref, query, onValue, orderByChild } from "https://www.gstatic.com/firebasejs/9.6.8/firebase-database.js";

// Firebase Configuration
const firebaseConfig = {
    apiKey: "AIzaSyDpE2uZyh7Pmk-nw0Mz3g3apr8UYQZ80mU",
    authDomain: "siotch-default-rtdb.firebaseapp.com",
    databaseURL: "https://siotch-default-rtdb.europe-west1.firebasedatabase.app/",
    projectId: "siotch",
    storageBucket: "siotch.appspot.com",
    messagingSenderId: "YOUR_SENDER_ID",
    appId: "YOUR_APP_ID"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const database = getDatabase(app);

// DOM Elements
const archSelect = document.getElementById("arch-select");
const chartsContainer = document.getElementById("charts");

archSelect.addEventListener("change", (event) => {
    const arch = event.target.value;
    if (arch) {
        loadCharts(arch);
    }
});

function loadCharts(arch) {
    const archRef = query(ref(database, "air_quality"), orderByChild("arch"), equalTo(arch));

    onValue(archRef, (snapshot) => {
        const data = snapshot.val();
        if (data) {
            // Populate charts
            console.log(data);
        } else {
            chartsContainer.innerHTML = "<p>No data available for this arch.</p>";
        }
    });
}
