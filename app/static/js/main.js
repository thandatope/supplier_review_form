document.addEventListener('DOMContentLoaded', function () {
   var colors = ["rgba(125, 63, 151, 0.5)", "rgba(0, 166, 156, 0.5)", "rgba(244, 176, 35, 0.5)", "rgba(253, 124, 160, 0.5)", "rgba(48, 70, 194, 0.5)"];
   var cardHead = document.querySelectorAll(".card-header");
   var card = document.querySelectorAll('.card');
   for (i = 0; i < cardHead.length; i++) {
      var c = colors[Math.floor(Math.random() * colors.length)];
      cardHead[i].style.backgroundColor = c;
      card[i].style.boxShadow = "0 0 0.2em 0.2em " + c;
      card[i].style.backgroundColor = "rgba(243,240,238,0.75)"
   }
});
