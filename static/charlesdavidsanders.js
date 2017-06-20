$(document).ready(function() {

  // External links open in new tabs
  $("a[href^='http://']")
    .not("[href^='http://"+window.location.hostname+"']")
    .attr("target","_blank");
  $("a[href^='https://']")
    .not("[href^='https://"+window.location.hostname+"']")
    .attr("target","_blank");

});
