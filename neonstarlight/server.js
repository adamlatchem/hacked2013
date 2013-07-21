var fs = require('fs');
var buf = require('buffer').Buffer;
var freq = 880;
var frate = 44100;
var b = new Buffer(frate / 100);

var x = 0.25;
var y = 0.25;
var t = 0;

var http = require( "http" );
var url = require( "url" );
var queryString = require( "querystring" );

function strencode( data ) {
  return unescape( encodeURIComponent( JSON.stringify( data ) ) );
}
 
function strdecode( data ) {
  return JSON.parse( decodeURIComponent( escape ( data ) ) );
}

http.createServer(
    function (req, res) {
      try {

        // parses the request url
        var theUrl = url.parse( req.url );

        // gets the query part of the URL and parses it creating an object
        var queryObj = queryString.parse( theUrl.query );

        // queryObj will contain the data of the query as an object
        // and jsonData will be a property of it
        // so, using JSON.parse will parse the jsonData to create an object
        console.log(queryObj);

        x = queryObj.x;
        y = queryObj.y;
        res.end('<html><body>dude</body></html>');
      } catch (e) {
        console.log ( e );
      }
    }
).listen(80);

mkWave = function() {
  setTimeout(mkWave, 10);

  for(var i = 0; i < frate / 100; ++i)
  {
    var v = x * Math.sin(2*Math.PI*freq*y*(t/frate));
    t = t + 1;
    b[i] =  + (v * 120);
  }
  fs.appendFile('thermin.raw', b, function (err) {
    console.log(err);
  });
}

mkWave();

