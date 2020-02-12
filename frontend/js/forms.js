$(document).ready(function(){
    $('#login-submit').click(function(){
        var error = false;
        var user = document.getElementById("login-user").value;
    	var pwd = document.getElementById("login-pwd").value;
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
        var url = 'https://groop.pw:3000/login?username=' + user + '&pwd=' + pwd;
        console.log(url)
        let request = new XMLHttpRequest();
        request.open('GET', url, true);
        request.withCredentials = false;
        request.responseType = 'json';
        request.onload = function() {
            let res = request.response;
            
            if (request.status == 200 && !error && res.success)
                {
                    window.location.replace("https://groop.pw/dashboard.html");
                }
            else if (request.status == 404 && !error)
                {
                    document.getElementById("error-text").innerHTML = "User not found";
                }
            else if (request.status == 400 && !error)
                {
                    document.getElementById("error-text").innerHTML = "Incorrect Password";
                }
            else if (request.status == 500 && !error)
                {
                    document.getElementById("error-text").innerHTML = "Error, please try again in a few minutes";
                }
        };
        if (!error)
            {
                request.send();
            }
        return false;
    });
});
