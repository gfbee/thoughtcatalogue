
//Here, we attempt to call a python3 script from node

var spawn = require("child_process").spawn;

var pProcess = spawn('python3',["../thoughtcat.py","-v"]);

var output = "";

//A process can have stream events attached to it (basic communication).
//The data we fetched is in a Buffer Object; we need to extract string.
pProcess.stdout.on('data', function (data) {
  output += data.toString('utf8'); //gather all of the data
  });
pProcess.on('close', function(stuff) {
    console.log(output);
  });

//Next, lets try to build a
