// ==UserScript==
// @name           Stack Overflow Suggest
// @namespace     
// @description    Suggest tags and ways to make the response time faster on your Stack Overflow questions
// @include        *stackoverflow.com/questions/ask*
// @version        0.1
// @author         Amber Feng, Franklin Hu
// ==/UserScript==

/* Credits:
    - Eric Vold (http://erikvold.com/) for the script for adding JQuery to user scripts
 */

/* Loads jQuery and calls a callback function when jQuery has finished loading */
function addJQuery(callback) {
  var script = document.createElement("script");
  script.setAttribute("src", "http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js");
  script.addEventListener('load', function() {
    var script = document.createElement("script");
    script.textContent = "(" + callback.toString() + ")();";
    document.body.appendChild(script);
  }, false);
  document.body.appendChild(script);
}

/* Userscript */
function main() {
    var suggestButton = $("<input>").attr({"id" : "suggest-button", "type" : "submit", "value" : "Analyze"});
    $(suggestButton).click(function(e){
        e.preventDefault();
    });

    $(".form-submit").append(suggestButton);

   }

// load jQuery and execute the main function
addJQuery(main);
