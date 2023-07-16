$(document).ready(function(){

    // Create content modal
    $("#terms").click(function(event) {

        $("#termsModal").show();

    });

    $("#privacy").click(function(event) {

        $("#privacyModal").show();

    });

    $("#termsClose").click(function(event) {

        $("#termsModal").hide();

    });

    $("#privacyClose").click(function(event) {

        $("#privacyModal").hide();

    });

});