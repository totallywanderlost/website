const MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoidG90YWxseXdhbmRlcmxvc3QiLCJhIjoiY2wwejdpcHZkMG5lZzNqbzF0eGYwYzg2ZyJ9.e_DZl8WK_sJqxMy5hCJeqw';
const map = L.map('map', {
    zoomControl: false,
    layers: [
        L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            maxZoom: 18,
            id: 'mapbox/streets-v11',
            tileSize: 512,
            zoomOffset: -1,
            accessToken: MAPBOX_ACCESS_TOKEN
        })
    ]
});

fetch('assets/data/journey.json').then(function (response) {
    if (response.status !== 200) {
        return console.error(`Unable to fetch data, response status: ${response.status}`);
    }

    response.json().then(function (data) {
        const locations = data.pins.map(p => p.location);
        map.fitBounds(locations);

        for (const pin of data.pins) {
            L.marker(pin.location).addTo(map);
        }

        map.getContainer().classList.remove('hide');
    });
}).catch(function (e) {
    console.error(e);
})
