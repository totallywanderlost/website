---
layout: default
width: full
image_1: "/assets/img/home/bluelagoon.jpeg"
image_1_caption: "The Blue Lagoon, Malta - April 2018"
image_2: "/assets/img/home/monchique.jpeg"
image_2_caption: "Monchique, Portugal - September 2020"
image_3: "/assets/img/home/brighton.jpeg"
image_3_caption: "Brighton Beach, Australia - October 2019"
---

<!-- Slideshow container -->
<div>
  <!-- Full-width images with caption text -->
  <div class="mySlides fade" style="width:100vw; height:100vh;">
    <img class="photo" src="/assets/img/home/bluelagoon.jpeg" style="width:100%;height:100%">
    <div class="captiontext">{{ page.image_1_caption }}</div>
  </div>

  <div class="mySlides fade" style="width:100vw; height:100vh;">
    <img class="photo" src="/assets/img/home/monchique.jpeg" style="width:100%;height:100%">
    <div class="captiontext">{{ page.image_2_caption }}</div>
  </div>

  <div class="mySlides fade" style="width:100vw; height:100vh;">
    <img class="photo" src="/assets/img/home/brighton.jpeg" style="width:100%;height:100%">
    <div class="captiontext">{{ page.image_3_caption }}</div>
  </div>
</div>

<script>
let slideIndex = 0;
showSlides();

function showSlides() {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none"; 
  }
  slideIndex++;
  if (slideIndex > slides.length) {slideIndex = 1} 
  slides[slideIndex-1].style.display = "block"; 
  setTimeout(showSlides, 5000); // Change image every 5 seconds
}
</script>