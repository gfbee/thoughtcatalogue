  var hidelists = {
    add: {"modeoptsinputs":0,"displaymodeopts":0,"addtextblobs":1},
    display: {"modeoptsinputs":1,"displaymodeopts":0,"addtextblobs":0},
    relation: {"modeoptsinputs":0,"displaymodeopts":0,"addtextblobs":0}
  };

    var modestate = {
      curr: [0,0,0],
      diff: [0,0,0]
    };

    var randstate = {
      curr: 0,
      diff: 0
    };

    var setoptstate = {
      curr: [0,0,0],
      diff: [0,0,0]
    };

    function hideToggle(hideArr) {
      for (key in hideArr) {
        if (hideArr[key] == 0) {
          $("#" + key).addClass("hide");
        } else {
          $("#" + key).removeClass("hide");
        }
      }
      return;
    }

    //Signature: Array -> String
    //Purpose: Stringify an array for quick comparison.
    function compArr(arrA, arrB) {
      return (JSON.stringify(arrA) == JSON.stringify(arrB));
    }

      //Signature: String Int -> Void
      //Purpose: Given an ID name and switch, toggle the UI option. Works for many different
      //Components
      function optionToggle(refName, isOn) {
        if(isOn == 1) {$("#" + refName).addClass("operateon");}
        else if (isOn == 0) {$("#" + refName).removeClass("operateon");}
        return;
      }

      // Purpose: When one of the two mode buttons is clicked,
      // we check to see if a valid state transition has occured,
      // update the data structure and then change the UI to reflect this.
      function addClickMode(refName) {
        $(("#" + refName)).click(function(ev) {
          if (refName == "addmode") {
            modestate.diff = [1,0,0];
            hideToggle(hidelists.add);
          }
          else if (refName == "displaymode") {
            modestate.diff = [0,1,0];
            hideToggle(hidelists.display);
          }
          else if (refName == "relationmode") {
            modestate.diff = [0,0,1];
            hideToggle(hidelists.relation);
          }
          //next, check state transition cases; we have simple arrays so stringify works here
          if (compArr(modestate.curr,modestate.diff)) {
            modestate.curr = [0,0,0]; //same; cancel out settings.
          } else {
            modestate.curr = modestate.diff;
          }
          modestate.diff = [0,0,0]; //always reset!
          optionToggle("addmode", modestate.curr[0]);
          optionToggle("displaymode", modestate.curr[1]);
          optionToggle("relationmode", modestate.curr[2]);
          return;
        });

      }

      function addClickSetOps(refName) {
        $(("#" + refName)).click(function(ev) {
          if (refName == "intersectopt") {
            setoptstate.diff = [1,0,0];
          }
          else if (refName == "unionopt") {
            setoptstate.diff = [0,1,0];
          }
          else if (refName == "diffopt") {
            setoptstate.diff = [0,0,1];
          }
          if (compArr(setoptstate.curr,setoptstate.diff)) {
            setoptstate.curr = [0,0,0]; //same; cancel out settings.
          } else {
            setoptstate.curr = setoptstate.diff;
          }
          setoptstate.diff = [0,0,0]; //always reset!
          optionToggle("intersectopt", setoptstate.curr[0]);
          optionToggle("unionopt", setoptstate.curr[1]);
          optionToggle("diffopt", setoptstate.curr[2]);
          ogeSetOpstoRand();
          return;
        });
      }

      function addClickRand(refName) {
        $(("#" + refName)).click(function(ev) {
          randstate.diff = 1;
          if (compArr(randstate.curr,randstate.diff)) {
            randstate.curr = 0; //same; cancel out settings.
          } else {
            randstate.curr = randstate.diff;
          }
          randstate.diff = 0; //always reset!
          optionToggle("randomopt", randstate.curr);
          ogeRandtoSetOps();
          return;
        });

      }

        //Signature: Void -> Void
        //Purpose: If Random button is toggled, the set ops buttons need to be turned off.
        //OGE stands for Other Group Effect; the set op buttons are in a separate "group"
        function ogeRandtoSetOps() {
          setoptstate.curr = [0,0,0];
          optionToggle("intersectopt", setoptstate.curr[0]);
          optionToggle("unionopt", setoptstate.curr[1]);
          optionToggle("diffopt", setoptstate.curr[2]);
          return
        }

        function ogeSetOpstoRand() {
          randstate.curr = 0;
          optionToggle("randomopt", randstate.curr);
        }


          var mouseadd = function() {
            $(this).addClass("pointer");
            if (!$(this).hasClass("operateon")) {
              $(this).addClass("hoverhighlight");
            }
          };

          var mouseremove = function() {
            $(this).removeClass("pointer");
            $(this).removeClass("hoverhighlight");
          };

            function addMouseOver(refName) {
              $(("#" + refName)).mouseenter(mouseadd);
              $(("#" + refName)).mouseleave(mouseremove);
            }


      $(document).ready(function(){
          addMouseOver("addmode");
          addMouseOver("displaymode");
          addMouseOver("relationmode");
          addMouseOver("randomopt");
          addMouseOver("intersectopt");
          addMouseOver("unionopt");
          addMouseOver("diffopt");
          addMouseOver("submitbutton");
          addMouseOver("textonlyopt");
          addClickMode("addmode");
          addClickMode("displaymode");
          addClickMode("relationmode");
          addClickSetOps("intersectopt");
          addClickSetOps("unionopt");
          addClickSetOps("diffopt");
          addClickRand("randomopt");
      });
