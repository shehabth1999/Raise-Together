spans = document.querySelectorAll('span');
for (var j = 0; j < spans.length; j++) {
    spans[j].classList.add('d-block');
}


labels = document.querySelectorAll('label');

for (var i = 0; i < labels.length; i++) {
    labels[i].classList.add('form-label');
    labels[i].classList.add('mt-3')
}

inputs = document.querySelectorAll('input');
for (var i = 0; i < inputs.length; i++) {
    inputs[i].classList.add('form-control');
    inputs[i].removeAttribute('required');
    
}
// document.addEventListener('DOMContentLoaded', function () {
//     var inputs = document.querySelectorAll('input');
    
//     inputs.forEach(function(input) {
//         input.classList.add('form-control');
//         input.removeAttribute('required');
//         input.style.backgroundColor = '#d1e7dd';
//     });
// });

divs = document.getElementsByClassName("form_element")
for (var d =0; d < divs.length; d++){
    divs[d].classList.add('mb-3')
}

checkboxex=document.querySelectorAll('input[type="checkbox"]')
for (var d =0; d < checkboxex.length; d++){
    checkboxex[d].classList.remove('form-control')
}

errors = document.querySelectorAll('ul.errorlist')
for (var m=0 ; m < errors.length; m++){
    errors[m].classList.add('text-danger','mb-0', 'p-0')
    errors[m].querySelector('li').classList.add('list-group-item')
}

var inputs = document.querySelectorAll('input.form-control');
for (var i = 0; i < inputs.length; i++) {
  var input = inputs[i];
  var errorList = input.previousElementSibling;
  if (errorList && errorList.classList.contains('errorlist')) {
    input.parentNode.insertBefore(errorList, input.nextSibling);
  }
}

var helpText = document.querySelectorAll('span.helptext');
console.log(helpText)
for (var i = 0; i < helpText.length; i++) {
    helpText[i].classList.add('text-danger');
    var helpLsit = helpText[i].querySelector("ul");
    if (helpLsit) {
       helpLsit.classList.add('list-group-item')
       helpLsitLis = helpLsit.querySelectorAll('li')
       console.log(helpLsitLis)
       for(var j = 0; j < helpLsitLis.length; j++) {
        console.log(helpLsitLis[j])
            helpLsitLis[j].classList.add('list-group-item')
       }
    }  
}