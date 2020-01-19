const url = 'mongodb://127.0.0.1:27017/gc_data';

var mongoose = require('mongoose');
mongoose.connect(url, {useNewUrlParser: true});

var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function() {
	//
	var Message = mongoose.model('Message',
		new mongoose.Schema({"Date": Date, Author: String, Body: String}),
		'messages');

	const authorQuery = document.getElementById("authorField").value;
	const bodyQuery = document.getElementById("bodyField").value;
	var query = {};

	if (authorQuery != null  && bodyQuery != null){
		query = {Author: authorquery, Body: bodyQuery};
	}
	else if (bodyQuery != null) {
		query = {Body: bodyQuery};
	}
	else if (authorQuery != null) {
		query = {Author: authorquery};
	}
	else {
		console.log("Empty query")
	}

	Message.findOne(query, function(err, data) {
		if (data == null || data.length == 0) {
			console.log("no results");
		}
		else {
			console.log(err, data, data.length);
		}
	});
});


