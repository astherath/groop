$(document).ready(function(){
    let doc = document.getElementById("file-upload").files[0];  // file from input
    var url = 'https://groop.pw:3000/files/upload';
    console.log(url);
    let request = new XMLHttpRequest();
    let formData = new FormData();
    formData.append("file", doc);
    request.open('POST', url, true);
    request.withCredentials = false;
    request.responseType = 'json';
    request.onload = function() {
        let res = request.response;

        if (request.status == 200 && res.success)
            {
//                    window.location.replace("https://groop.pw/dashboard.html");
                console.log('all good');
            }
        else if (request.status != 500)
            {
//                document.getElementById("error-text").innerHTML = res.error;
                console.log("500 error");
            }
        else
            {
//                document.getElementById("error-text").innerHTML = "Server error, please try again later";
                console.log("Server error, please try again later");
            }
    };
//    if (!error)
//        {
//            request.send(formData);
//        }
    request.send(formData);
    return false;
});




