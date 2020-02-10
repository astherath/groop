$(document).ready(function(){
    $('#login-submit').click(function(){
        var user = document.getElementById("login-user").value;
    	var pwd = document.getElementById("login-pwd").value;
        var url = 'https://felipearce.pw:3000/login?username=' + user + '&pwd=' + pwd;
        console.log(url)
        let request = new XMLHttpRequest();
        request.open('GET', url, true);
        request.withCredentials = false;
        request.responseType = 'json';
        request.onload = function() {
            console.log(request.response);
            if (request.status == 200)
                {
                    window.location.replace("https://felipearce.pw/dashboard.html");
                }
            else
                {
                    console.log("Error: " + request.status);
                }
        };
        request.send();
        return false;
    });
});
