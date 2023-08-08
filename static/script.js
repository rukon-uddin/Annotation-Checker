let slideIndex = 1;
current_image = ""
current_div = ""
let dots = document.getElementsByClassName("dot");
showSlides(slideIndex);

function plusSlides(n) {
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    
    if (n > slides.length) { slideIndex = 1 }
    if (n < 1) { slideIndex = slides.length }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex - 1].style.display = "block";
    current_div = slides[slideIndex - 1]
    var imgSrc = current_div.querySelector("img").getAttribute("src");
    current_image_src = imgSrc
    console.log("Cant get the class name")
}

function del_img(){
    var server_data = [
        {"Current Image": current_image_src},
        {"prolonged": "Hello"}
      ];

    fetch("/delete_img", {
      method: "POST",
       
      body: JSON.stringify(server_data),
      headers: {
          "Content-type": "application/json; charset=UTF-8"
      }
    })
    // current_div.parentNode.removeChild(current_div);
    plusSlides(slideIndex)
}