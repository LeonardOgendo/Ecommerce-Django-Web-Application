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

//Payment View redirect

function submitPaymentForm() {
    const paymentMethod = document.querySelector('input[name="payment_method"]:checked').value;
    if (paymentMethod === 'mpesa') {
        document.getElementById('checkout-form').action = "{% url 'Core:mpesa-payment' %}";
    } else if (paymentMethod === 'paypal') {
        document.getElementById('checkout-form').action = "{% url 'paypal_api_view' %}";
    }
    document.getElementById('checkout-form').submit();
}