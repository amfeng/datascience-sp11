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
    var analyzeButton = $("<input>").attr({"id" : "analyze-button", "type" : "submit", "value" : "Analyze"});
    $(analyzeButton).click(function(e){
        e.preventDefault();
        
        $("#analysis").remove();

        analyzeBar = $("<div></div>").attr("id", "analysis").addClass("form-item");
        analyzeBar.append($("<label></label>").html("Analysis"));
        suggestedTags = $("<div></div>").attr("id", "suggested-tags");
        suggestions = $("<ul></ul>").attr("id", "suggestions").css({"margin-top": "5px"});

        analyzeBar.css({"background-color": "#FFFCE0", "border": "1px solid #F2ECAA", "padding": "1em", "margin-bottom": "10px"});
        
        body = $("#wmd-input").val();
        tagnames = $("#tagnames").val();
        
        /* Make an ajax call */
        $.get("http://stackingdata.appspot.com/analyze", {"body": body, "tagnames": tagnames },
            function(data){
                tags = data["tags"];
                suggest = data["suggest"];
                respTime = data["respTime"];
                for (var i in tags){
                    newTag = $("<span></span>").html(tags[i]).addClass("post-tag").css({"padding-right": "5px"});
                    suggestedTags.append(newTag);
                }
                for (var i in suggest){
                    console.log(suggest);
                    newSuggest = $("<li></li>").html(suggest[i]);
                    suggestions.append(newSuggest);
                }
                analyzeBar.append($("<span></span>").css({"display": "block", "margin-top": "1em", "font-weight": "bold"}).html("Did you forget these tags?"));
                analyzeBar.append(suggestedTags);
                analyzeBar.append($("<h6></h6>").css({"display": "block", "margin-top": "1em"}).html("Suggestions"));
                analyzeBar.append(suggestions);
                analyzeBar.append($("<span></span>").css({"display": "block", "margin-top": "1em", "font-weight": "bold", "font-size": "130%"}).html("Predicted Response Time: " + respTime + " minutes."));

                $("#notify-options").before(analyzeBar);
                $("#analyze-button").attr("value", "Reanalyze");
            }, 
            "jsonp"
        );
    });

    $(".form-submit").append(analyzeButton);

   }

// load jQuery and execute the main function
addJQuery(main);
