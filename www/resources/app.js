const express = require('express')
const app = express()
const port = 3000

var bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({ extended: false }));

app.get('/query', function(req, res) {

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

		var authorQuery = req.body.author;
		var bodyQuery = req.body.body;
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
				res.status(404).send("no results");
			}
			else {
				console.log(err, data, data.length);
				res.status(200).send(data);
			}
		});
	});
});

var server = app.listen(port, function () {
    console.log('Node server is running..');
});
