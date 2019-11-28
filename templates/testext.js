/*
Original taken here
https://github.com/khanning/scratch-isstracker-extension/edit/gh-pages/iss_extension.js
Some lesson about make an extension
https://www.slideshare.net/DarrenAdkinson/understanding-scratchx-extensions-with-javascript

Create scratch extensions for the raspberry
https://mryslab.github.io/s2-pi/

The official documentation about extensions
https://github.com/LLK/scratchx/wiki#contents

 */
(function(ext) {

  var SOME_GLOB = 10; //A class variable

  var some_values = {}; //A class array

  ext.delayedresult = function(A, B, callback) {
    $.ajax({
      type: "GET",
      //dataType: "json",
      url: "http://{{ request.environ['SERVER_NAME'] }}/testget/" + A + "/" + B",
      success: function(data) {
        callback(data);
      },
      error: function(jqxhr, textStatus, error) {
        console.log("Error during call");
      }
    });
  }


  ext.calculated = function(A, B) {
    console.log(A);
    console.log(B);
    return (parseInt(A)+parseInt(B)).toString();
  };

  ext._getStatus = function() {
    return { status:2, msg:'Ready' };
  };

  ext._shutdown = function() {
      /*
    if (poller) {
      clearInterval(poller);
      poller = null;
    }
    */
  };

  var descriptor = {
    blocks: [
      //['h', 'when ISS passes over %s', 'whenISSPasses', 'Boston, MA'],
      ['r', 'Sum of 2 numbers %s %s','calculated', 1, 2], // sync call
      ['R', 'Exp of numbers %s %s', 'delayedresult', 2, 4] // async call
    ],
    /*
    menus: {
      loc: ['longitude', 'latitude', 'altitude', 'velocity'],
      measurements: ['kilometers', 'miles']
    },
    */
    url: 'http://lorenzopedrotti.pythonanywhere.com'
  };

  //things to do during first run
  ScratchExtensions.register('Test ext', descriptor, ext);

  //updateISSLocation();
  //poller useful for Raspberry gizmos
  //var poller = setInterval(updateISSLocation, 2000);

})({});
