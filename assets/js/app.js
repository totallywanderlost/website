const map = L.map('map', {
    zoomControl: false,
});

map.setView([51.511040, -0.103510], 3);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoidG90YWxseXdhbmRlcmxvc3QiLCJhIjoiY2wwejdpcHZkMG5lZzNqbzF0eGYwYzg2ZyJ9.e_DZl8WK_sJqxMy5hCJeqw'
}).addTo(map);
