$(document).ready(function(){
    $('#signup-submit').click(function(){
        var error = false;
        var user = document.getElementById("signup-user").value;
        if (user == null || user == "")
            {
                document.getElementById("error-text").innerHTML = "Username Missing";
                error = true;
            }
        var email = document.getElementById("signup-email").value;
        if (email == null || email == "")
            {
                document.getElementById("error-text").innerHTML = "Email Missing";
                error = true;
            }
    	var pwd = document.getElementById("signup-pwd").value;
        if (pwd == null || pwd == "")
            {
                document.getElementById("error-text").innerHTML = "Password Missing";
                error = true;
            }
        var pwdConf = document.getElementById("signup-pwd-conf").value;
        if (pwd.localeCompare(pwdConf))
            {
                document.getElementById("error-text").innerHTML = "Passwords don't match";
                error = true;
            }
        var endpoint = '?username=' + user + '&email=' + email + '&pwd=' + pwd;
        var url = 'https://felipearce.pw:3000/signup' + endpoint;
        console.log(url)
        let request = new XMLHttpRequest();
        request.open('POST', url, true);
        request.withCredentials = false;
        request.responseType = 'json';
        request.onload = function() {
            console.log(request.response);

            if (request.status == 200 && !error)
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
