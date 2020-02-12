$(document).ready(function(){
		$('#query-field').keydown(function(event){
			if(event.keyCode == 13) {
				event.preventDefault();
				return false;
			}
		});
	    $("#plot-section").hide();
		$('#query-submit').click(function(){
		$("#error-alert").hide();
        $("#plot-section").show();
		var error = false;
        var word = document.getElementById("query-field").value;
        var raw = document.getElementById("raw-data").value;
		if (word == "" || word == null)
			{
				error = true;
			}
        var endpoint = '?word=' + word + '&raw=' + raw;
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
                    pic.src = "imgs/plot.png?" + time;
                }
            else
                {
					$("#error-alert").show();
                }
        };
		if (!error)
			{
				request.send();
			}
        return false;
    });
});
