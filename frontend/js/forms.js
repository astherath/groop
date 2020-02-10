$(document).ready(function(){
    $('#login-submit').click(function(){
        var error = false;
        var user = document.getElementById("login-user").value;
        if (user == null || user == "")
            {
                document.getElementById("error-text").innerHTML = "Username Missing";
                error = true;
            }
    	var pwd = document.getElementById("login-pwd").value;
        if (pwd == null || pwd == "")
            {
                document.getElementById("error-text").innerHTML = "Password Missing";
                error = true;
            }
        var url = 'https://felipearce.pw:3000/login?username=' + user + '&pwd=' + pwd;
        console.log(url)
        let request = new XMLHttpRequest();
        request.open('GET', url, true);
        request.withCredentials = false;
        request.responseType = 'json';
        request.onload = function() {
            console.log(request.response);
            if (request.status == 200 && !error)
                {
                    window.location.replace("https://felipearce.pw/dashboard.html");
                }
            else if (request.status == 404)
                {
                    document.getElementById("error-text").innerHTML = "User not found";
                }
            else if (request.status == 400)
                {
                    document.getElementById("error-text").innerHTML = "Incorrect Password";
                }
            else
                {
                    document.getElementById("error-text").innerHTML = "Error, please try again in a few minutes";
                }
        };
        request.send();
        return false;
    });
});
