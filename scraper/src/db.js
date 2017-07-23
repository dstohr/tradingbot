var MongoClient = require( 'mongodb' ).MongoClient;

var url = `mongodb://${process.env.MONGODB_HOST}/poloniex`
var _db;

module.exports = {

  connect: function( callback ) {
    MongoClient.connect(url, function( err, db ) {
      
      if(err) console.log(err)
      else{
          console.log('mongodb connected to ' + url)
          _db = db;
      }
    } );
  },

  db: _db,
  url: url
};