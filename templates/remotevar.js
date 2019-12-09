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

  var SESSION = '{{ data.session_id }}'; //A class variable

  var some_values = {}; //A class array
  {% if request.environ['SERVER_NAME'] == '192.168.1.112' %}
  var base_url = "http://192.168.1.112:5000";
  {% endif %}
  {% if request.environ['SERVER_NAME'] == 'lorenzopedrotti.pythonanywhere.com' %}
  var base_url = "http://lorenzopedrotti.pythonanywhere.com";
  {% endif %}

  ext.getvar = function(VAR, callback) {
    $.ajax({
      type: "GET",
      crossDomain: true,
      url: base_url + "/getvar/" + SESSION + "/" + VAR,
      success: function(data) {
        console.log(data)
        callback(data);
      },
      error: function(jqxhr, textStatus, error) {
        console.log("Error during get");
      }
    });
  }

  ext.putvar = function(VAR,VAL) {
    $.ajax({
      type: "GET",
      crossDomain: true,
      url: base_url + "/putvar/" + SESSION + "/" + VAR + "/" + VAL,
      success: function(data) {
        console.log(data)
      },
      error: function(jqxhr, textStatus, error) {
        console.log("Error during putval");
      }
    });

  }


  ext.delayedresult = function(A, B, callback) {
    $.ajax({
      type: "GET",
      //dataType: "json",
      crossDomain: true,
      url: base_url + "/testget/" + SESSION + "/" + A + "/" + B ,
      success: function(data) {
        callback(data);
      },
      error: function(jqxhr, textStatus, error) {
        console.log("Error during call");
      }
    });
  }

  ext.calculated = function(A, B) {
    //console.log(A);
    //console.log(B);
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
      //['h', 'when ISS passes over %s', 'whenISSPasses', 'Boston, MA'], // a starter block, event
      ['r', 'Sum of 2 numbers %s %s','calculated', 1, 2], // sync call
      ['R', 'Exp of numbers %s %s', 'delayedresult', 2, 4], // async call
      [' ', 'Save variable %s %s','putvar', 'varname', 'varvalue'], // sync command (w is for async)
      ['R', 'Get variable %s', 'getvar', 'variable']
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
