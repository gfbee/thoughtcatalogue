//In this script, we make a server that accepts a GET,HEAD or METHOD
//HTTP request, and returns a response. HEAD and METHOD are hard coded,
//Get just echos back whatever the front end requester sent.

//This will incrementally be built up, so that proper piping, and error
//handling is done.

const http = require('http');

http.createServer((request, response) => {
  const { headers, method, url } = request;
  let body = [];
  request.on('error', (err) => {
    console.error(err);
  }).on('data', (chunk) => { //This is necessary!
    //body.push(chunk);
  }).on('end', () => { //Once we get everything, check METHOD
    response.statusCode = 200;
    if (method == "GET") {
      body = "Token Response; This is what you GET.";
    } else if (method == "HEAD") {
      body = "";
    } else if (method == "OPTION") {
      body = "Methods Available: GET, HEAD, OPTION ONLY.";
    } else  {
      response.statusCode = 405;
      body = "Method " + method + " not allowed.";
    }
    response.on('error', (err) => {
      console.error(err);
    });

    response.setHeader('Content-Type', 'application/json');

    const responseBody = { headers, method, url, body };

    response.write(JSON.stringify(responseBody));
    response.end();
  });
}).listen(8081);
