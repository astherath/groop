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
		pwd = btoa(pwd);
		console.log(pwd);
        var url = 'https://groop.pw:3000/login?username=' + user + '&pwd=' + pwd;
        console.log(url);
        let request = new XMLHttpRequest();
        request.open('GET', url, true);
        request.withCredentials = false;
        request.responseType = 'json';
        request.onload = function() {
            let res = request.response;

            if (request.status == 200 && !error && res.success)
                {
                    let id = res.id;
                    window.location.replace("https://groop.pw/dashboard.html?" + id);
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
