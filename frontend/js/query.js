$(document).ready(function(){    
    $("#plot-section").hide();
    $('#query-submit').click(function(){
        var word = document.getElementById("query-field").value;
        var raw = document.getElementById("raw-data").value;
        var endpoint = '?word=' + word + '&raw=' + raw;
        var url = 'https://felipearce.pw:3000/find' + endpoint;
        console.log(url)
        let request = new XMLHttpRequest();
        request.open('GET', url, true);
        request.withCredentials = false;
        request.responseType = 'json';
        request.onload = function() {
            console.log(request.response);
            if (request.status == 200)
                {
                    $("#plot-section").show();
                }
            else 
                {
                    console.log("error:" + request.status);
                }
        };
        request.send();
        return false;
    });
});