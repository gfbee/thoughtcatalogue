
//Purpose: We have a singleton state object that iterates dynamic IDs;
//we call this, and then update it everytime a new object is made.
var dynamID = {
  currID:0,
  //Method: CurrID++
  //Method: reset currID property to zero.
}

//Signature: Void -> Intersect
//Purpose: Update dynamID by one, and return an ID to a generating function.
function idUpdate(){
  dynamID.currID = dynamID.currID + 1;
  return (dynamID.currID - 1);
}

function AddModeState() {
  this.numTextBlobs = 0;
  this.textBlobList = [];
  this.addTB = function (tbID) {this.textBlobList.push(tbID);}
}

//Purpose: For Display mode, this is our state object. Its values are updated
//As the user inputs information.
function DisplayModeState() {
  this.randOpt = false;
  this.allTags = false;
  this.intersectOp = false;
  this.unionOp = false;
  this.diffOp = false;
  this.tagSearchList = [];
  this.limit = -1;
}

//These functional constructors are used when we do a submit, or accept a request
//from the server. They are not used during the generation of things.

//Signature: String Int Boolean -> Tag object.
//Purpose: Our "Blueprint" Constructor for tags.
//Tags are not used in a mutable way. They can be deleted in entirety, though.
function Tag(label,id,created) {
  this.label = label;
  this.id = id;
  this.created = created;
}

//Signature: Int, Int(Date) List(Tag Objects) String -> TextBlob Objects.
//Purpose: This represents an actual textblob; these may be specified by the
//user, or generated from a Pull Request.

function TextBlob(id, gettime_date, taglist, textblob) {
  this.id = id;
  this.date = gettime_date;
  this.archive = false;
  this.taglist = taglist;
  this.tblob = textblob;
}

//Here, lets make our global state structures:

var addModeObj = new AddModeState();

//Below: We implement the GUI support for dyanmic textblobs. This is just the addtextblob.html consider
//refactored into our current interface code.

function processTagInput() {
  idIndex = idUpdate();
  var usertext = $(this).prop("value");
  $(this).hide();
  var spoint = jQuery("<span/>", {
      id: "s" + idIndex,
      class: "all",
      html: usertext,
  });
  $(this).parent().prepend(spoint);
}

function addTag() {
  idIndex = idUpdate();
  let tagpointId = "t" + idIndex;
  var tagpoint = jQuery("<div/>", {
    id: tagpointId,
    class: "all tagshared tagcont",
  });

  let inputId = "i" + idIndex;
  var inputpoint = jQuery("<input/>", {
    id: inputId,
    class: "all ibox",
    value: "...",
  });

  var buttonpoint = jQuery("<span/>", {
    id: "b" + idIndex,
    class: "all",
    html: "&otimes;",
  });

    $(this).parent().prepend(tagpoint);

    $("#" + tagpointId).append(inputpoint);
    $("#" + tagpointId).append(buttonpoint);
    $("#" + inputId).on("blur", processTagInput);
    $("#" + "b" + idIndex).
}

function generateTextBlob() {
  var idIndex = idUpdate();
  let tbId = "tb" + idIndex;
  //Generate Outer box: all, containshared outcontain
  var tblobbox = jQuery("<div/>", {
    id: tbId,
    class: "all tboxcontain",
  });

  var txtbox = jQuery("<textarea/>", {
    id: "ta" + idIndex,
    class: "all textbox",
    value: "An Input Textbox.",
  });

  let tagboxId = "tbout" + idIndex;
  var tagboxout = jQuery("<div/>", {
    id: tagboxId,
    class: "all tagshared parenttagcont",
    value: "",
  });

  var oplusId = "b" + idIndex;
  var buttonpoint = jQuery("<span/>", {
    id: oplusId,
    class: "all tagshared plusbutton",
    html: "&oplus;",
  });

  //We need to add tbId to our AddView DataStructure:
  addModeObj.addTB(tbId);

  $("body").append(tblobbox);
  $("#" + tbId).append(txtbox);
  $("#" + tbId).append(tagboxout);
  $("#" + tagboxId).append(buttonpoint);
  $("#" + oplusId).on("click", addTag);
  addMouseOver(("#" + oplusId));
}
