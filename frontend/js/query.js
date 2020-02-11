$(document).ready(function(){
    $("#plot-section").hide();
    $('#query-submit').click(function(){
        $("#plot-section").show();
        var word = document.getElementById("query-field").value;
        var raw = document.getElementById("raw-data").value;
        var endpoint = '?word=' + word + '&raw=' + raw;
        var url = 'https://groop.pw:3000/find' + endpoint;
        console.log(url)
        let request = new XMLHttpRequest();
        request.open('GET', url, true);
        request.withCredentials = false;
        request.responseType = 'json';
        request.onload = function() {
            console.log(request.response);
            if (request.status == 200)
                {
                    var pic = document.getElementById("plot-img");
                    var time = performance.now();
                    pic.src = "imgs/plot.png?" + time;
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
