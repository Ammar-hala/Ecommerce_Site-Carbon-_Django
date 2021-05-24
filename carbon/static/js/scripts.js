$(document).ready(function(){
    $('#Men').click(function(){
      $('#Wom').removeClass("active");
      $('#Men').addClass("active");
});
  $('#Wom').click(function(){
    $('#Men').removeClass("active");
    $('#Wom').addClass("active");
});

$(".heart.fa").click(function() {
  $(this).toggleClass("fa-heart fa-heart-o");
});

});
