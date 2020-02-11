$(document).ready(function(){
    $('#signup-submit').click(function(){
        var error = false;
        var user = document.getElementById("signup-user").value;
        var pwd = document.getElementById("signup-pwd").value;
        var pwdConf = document.getElementById("signup-pwd-conf").value;
        if (user == null || user == "")
            {
                document.getElementById("error-text").innerHTML = "Username Missing";
                error = true;
            }
        else if (pwd == null || pwd == "")
            {
                document.getElementById("error-text").innerHTML = "Password Missing";
                error = true;
            }
        else if (pwd.localeCompare(pwdConf))
            {
                document.getElementById("error-text").innerHTML = "Passwords don't match";
                error = true;
            }
        var endpoint = '?username=' + user + '&email=' + email + '&pwd=' + pwd;
        var url = 'https://groop.pw:3000/signup' + endpoint;
        console.log(url)
        let request = new XMLHttpRequest();
        request.open('POST', url, true);
        request.withCredentials = false;
        request.responseType = 'json';
        request.onload = function() {
            console.log(request.response);

            if (request.status == 200 && !error)
                {
                    window.location.replace("https://groop.pw/dashboard.html");
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
