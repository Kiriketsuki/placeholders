function add_favourites(building_id) {
  fetch('/add_favourites', {
    method : "POST",
    body : JSON.stringify({building_id : building_id})
  }).then((_res) => {window.location.href = "#"})
}
