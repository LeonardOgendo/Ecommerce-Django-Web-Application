// message close function

function dismissMessage(button){
    //find the parent alert div of the clicked button
    const alertDiv = button.parentNode;

    //remove the parent alert div from the DOM
    alertDiv.parentNode.removeChild(alertDiv)
};

//Swiper
const swiper = new Swiper('.swiper', {
    autoplay: {
        delay: 3000,
        disableOnInteraction: false,
    },
loop: true,
pagination: {
    el: '.swiper-pagination',
    clickable:true,
},
    
navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
},
});

//Responsiveness
var navLinks = document.getElementById("navLinks");
function showMenu(){
    navLinks.style.right = "0";
}
function hideMenu(){
    navLinks.style.right = "-200px";
}