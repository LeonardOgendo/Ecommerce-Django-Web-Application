// message close function

function dismissMessage(button){
    //find the parent alert div of the clicked button
    const alertDiv = button.parentNode;

    //remove the parent alert div from the DOM
    alertDiv.parentNode.removeChild(alertDiv)
}