

function testFunc() {
    var button = document.getElementById('myButton');
    button.addEventListener('click', function(e) {
        var authorQuery = document.getElementById("authorField").value;
        var bodyQuery = document.getElementById("bodyField").value;
        console.log("author query: ", authorQuery);
        console.log("body query: ", bodyQuery);
        let request = new XMLHttpRequest();
        request.open('GET', url);
        request.responseType = 'text';
        request.onload = function() {
            queryDisplay.textContent = request.response;
        };
        request.send();
        
    });
};

window.addEventListener('load', testFunc, false);
