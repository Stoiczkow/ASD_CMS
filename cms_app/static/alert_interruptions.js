setInterval(function() {
  $.get('/current_interruptions/');
  console.log("poszlo ze static");
}, 1000 * 60 * 1);