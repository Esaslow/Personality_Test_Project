var slider = document.getElementsByClassName("myRange");
var output = document.getElementsByClassName("slider_val");
var butt = document.getElementsByClassName("GetNextQuestion");
output.innerHTML = slider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
    output.innerHTML = this.value;
}
butt.oninput =  function() {
    console.log(this.value);
}

console.log('slider here');
