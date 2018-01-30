
    var modestate = {
      curr: [0,0],
      diff: [0,0]
    };

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
            modestate.diff = [1,0];
          }
          else if (refName == "displaymode") {
            modestate.diff = [0,1];
          }
          //next, check state transition cases; we have simple arrays so stringify works here
          if (JSON.stringify(modestate.diff) == JSON.stringify(modestate.curr)) {
            modestate.curr = [0,0]; //same; cancel out settings.
          } else {
            modestate.curr = modestate.diff;
          }
          modestate.diff = [0,0]; //always reset!
          optionToggle("addmode", modestate.curr[0]);
          optionToggle("displaymode", modestate.curr[1]);
          return;
        });

      }

      $(document).ready(function(){
          addMouseOver("addmode");
          addMouseOver("displaymode");
          addMouseOver("randomopt");
          addMouseOver("intersectopt");
          addMouseOver("unionopt");
          addMouseOver("diffopt");
          addMouseOver("submitbutton");
          addMouseOver("textonlyopt");
          addClickMode("addmode");
          addClickMode("displaymode");

      });
