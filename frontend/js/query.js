$(document).ready(function(){    
    $('#query-submit').click(function(){
        var plot = document.getElementById("plot-section")
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
                    // if hidden, display
                    if (plot.style["display"].localeCompare("none"))
                        {
                            plot.style["display"] = "contents";
                        }
                    // else do nothing
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