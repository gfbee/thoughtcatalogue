//This small script attempts to open a Read and Write Stream, Form a file to
//input into thoughtcat.py, and then prints out the response of thoughtcat.py into
//our console

//1: We need to open a readablestream with the FS module, and add data and end events.
//We can't assume the chunks will be congruent with valid JSON chunks, so we read everything
//in. on "END", we parse the full JSON text.

const fs = require("fs");
var storage = "";
var jsonData = "";
fs.readFile("./input.json",'utf8', function (err,data) {
  if (err) throw err;

  storage += data;
  jsonData = JSON.parse(data); //now in object form.

  for (var key in jsonData)
  {
    console.log(JSON.stringify(jsonData[key]));
  }
});
