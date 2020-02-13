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
        else if (user.length < 6)
            {
                document.getElementById("error-text").innerHTML = "Username too short (6 characters minimum)";
                error = true;
            }
        else if (pwd == null || pwd == "")
            {
                document.getElementById("error-text").innerHTML = "Password Missing";
                error = true;
            }
        else if (pwd.length < 8)
            {
                document.getElementById("error-text").innerHTML = "Password too short (8 characters minimum)";
                error = true;
            }
        else if (pwd.localeCompare(pwdConf))
            {
                document.getElementById("error-text").innerHTML = "Passwords don't match";
                error = true;
            }
		pwd = btoa(pwd);
        var endpoint = '?username=' + user + '&pwd=' + pwd;
        var url = 'https://groop.pw:3000/signup' + endpoint;
        console.log(url)
        let request = new XMLHttpRequest();
        request.open('POST', url, true);
        request.withCredentials = false;
        request.responseType = 'json';
        request.onload = function() {
            let res = request.response;

            if (request.status == 200 && !error && res.created)
                {
                    window.location.replace("https://groop.pw/dashboard.html");
                }
            else if (request.status != 500)
                {
                    document.getElementById("error-text").innerHTML = res.error;
                }
            else
                {
                    document.getElementById("error-text").innerHTML = "Server error, please try again later";
                }
        };
        if (!error)
            {
                request.send();
            }

        return false;
    });


});
