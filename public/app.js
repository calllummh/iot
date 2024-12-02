"use strict";

// Firebase Configuration
var firebaseConfig = {
    apiKey: "AIzaSyDpE2uZyh7Pmk-nw0Mz3g3apr8UYQZ80mU",
    authDomain: "https://siotch.web.app",
    databaseURL: "https://siotch-default-rtdb.europe-west1.firebasedatabase.app/",
    projectId: "siotch"}

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
var database = firebase.database();

// DOM Elements
var archSelect = document.getElementById("arch-select");
var pm25ChartElem = document.getElementById("pm25-chart");
var temperatureChartElem = document.getElementById("temperature-chart");
var humidityChartElem = document.getElementById("humidity-chart");

// Initialize Charts
function initChart(label, yAxisLabel) {
    return new Chart(document.getElementById(label), {
        type: "line",
        data: {
            labels: [], // Timestamps
            datasets: [{
                label: yAxisLabel,
                data: [],
                borderColor: "rgba(75, 192, 192, 1)",
                backgroundColor: "rgba(75, 192, 192, 0.2)",
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: "Timestamp" } },
                y: { title: { display: true, text: yAxisLabel } }
            }
        }
    });
}

var pm25Chart = initChart("pm25-chart", "PM2.5 (µg/m³)");
var