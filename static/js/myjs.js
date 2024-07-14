let slideIndex = 1;
showSlides(slideIndex);function plusSlide(n) {
  showSlides(slideIndex += n);
}function showSlides(n) {
  let i;
  const slides = document.getElementsByClassName("slide");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  slides[slideIndex-1].style.display = "block";
}function prevSlide() {
  plusSlide(-1);
}function nextSlide() {
  plusSlide(1);
}

// document.addEventListener('DOMContentLoaded', function() {
//     // Save the scroll position before the page unloads
//     window.addEventListener('beforeunload', function() {
//         localStorage.setItem('scrollPosition', window.scrollY);
//     });

//     // Restore the scroll position when the page loads
//     var scrollPosition = localStorage.getItem('scrollPosition');
//     if (scrollPosition !== null) {
//         window.scrollTo(0, parseInt(scrollPosition));
//     }
// });


window.addEventListener('load', function() {
  var scrollPosition = localStorage.getItem('scrollPosition');
  if (scrollPosition !== null) {
      window.scrollTo(0, scrollPosition);
      localStorage.removeItem('scrollPosition'); // Clear the saved scroll position
  }
});
