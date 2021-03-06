$(document).ready(function(){
    var docUrl = document.location.href;
    var userId = docUrl.split('?').pop();
    console.log('userid is: ' , userId);
    console.log('equal?: ' , (userId == docUrl));
    if (userId == "" || userId == docUrl)
        {
            let redirect = window.location.replace("https://groop.pw/login.html");
        }

	let query = function(){
		$("#error-alert").hide();
		var error = false;
        var word = document.getElementById("query-field").value;
        var raw = document.getElementById("raw-data").value;
		if (word == "" || word == null)
			{
				error = true;
			}
        var endpoint = '?word=' + word + '&raw=' + raw + '&id=' + userId;
        var url = 'https://groop.pw:3000/find' + endpoint;
        console.log(url)
        let request = new XMLHttpRequest();
        request.open('GET', url, true);
        request.withCredentials = false;
        request.responseType = 'json';
        request.onload = function() {
            console.log(request.response);
            if (request.status == 200 && !error)
                {
                    var pic = document.getElementById("plot-img");
                    var time = performance.now();
                    pic.src = "imgs/" + userId + ".png?" + time;
        			$("#plot-section").show();
                }
            else
                {
					// var err = document.getElementById("error-alert");
					// err.style = "display: content";
					$("#plot-section").hide();
					$("#error-alert").show();
                }
        	};
		if (!error)
			{
				request.send();
			}
        return false;
	};

	$('#query-field').keydown(function(event){
		if(event.keyCode == 13) {
			event.preventDefault();
			query();
			return false;
		}
	});

	$("#plot-section").hide();
	$('#query-submit').click(query);
});
