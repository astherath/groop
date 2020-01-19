var mongo = require('mongodb');

var url = "mongodb://localhost:27017/";

MongoClient.connect(url, function(err, db) {
	if (err) throw err;
	var dbo = db.db("gc_data");
	dbo.collection("messages").findOne({}, function(err, result) {
		if (err) throw err;
		console.log(result.name);
		db.close();
	});
});
