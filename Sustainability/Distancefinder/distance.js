// To find distance between 2 location
function findDistance(location1, location2) {
    let geocoder;
    let request;
    geocoder = new google.maps.Geocoder();

    geocoder.geocode(request).then((result) => {
        const { results } = result;
        JSON.stringify(result, null, 2);
    }).catch((e) => {
        alert("Geocode was not successful for the following reason: " + e);
    })
}