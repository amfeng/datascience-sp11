$(document).ready(function(){
    currScrollLevel = 0;
    
    $("#toptagsn-iframe").hide();
    $("#normchooser a").toggle(toNorm, toUnNorm);

    function scrollFrame(left){
        console.log("scrolling" + left);
        //$("#toptags")animate({scrollTop: left}, 2000);
        $("#toptags")[0].contentWindow.scrollTo(left, 0);
        $("#toptagsn")[0].contentWindow.scrollTo(left, 0);
        currScrollLevel = left;
    }

    $(".yearscroll").click(function() {
        $(".yearscroll").removeClass("primary").removeClass("current");
        $(this).addClass("primary").addClass("current");

        year = $(this).attr("id");
        if(year == "ys2008"){
            scrollFrame(0);
        } else if (year == "ys2009") {
            scrollFrame(950);
        } else if (year == "ys2010") {
            scrollFrame(2000);
        }
        
    });

    function toNorm() {
        $("#toptags-iframe").hide();
        $("#toptagsn-iframe").show();
        $("#normchooser a span").addClass("check").addClass("icon");
    }

    function toUnNorm() {
        $("#toptagsn-iframe").hide();
        $("#toptags-iframe").show();
        $("#normchooser a span").removeClass("check").removeClass("icon");
    }

    
});

