
//Here, we attempt to call a python3 script from node

var spawn = require("child_process").spawn;

var pProcess = spawn('python3',["./simple.py",,]);

var output = "";

//A process can have stream events attached to it (basic communication).
pProcess.stdout.on('data', function (data) {
  console.log(data.toString('utf8'));
  });
pProcess.on('close', function(stuff) {
    console.log("A");
    console.log(stuff);
  });
