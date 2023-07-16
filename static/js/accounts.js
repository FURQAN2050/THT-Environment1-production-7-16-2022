// Create variables for data

var teams = []
var endpoint = '/accounts/api/data/'

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function(){

    var csrftoken = getCookie('csrftoken');
    

    $.ajax({

        method: "POST",
        url: endpoint,
        data: {
            csrfmiddlewaretoken: csrftoken,
            'action': 'availableTeams'
        },

        success: function(data) {
            teams  = data.teams
            console.log(teams)
        },

        error: function(error_data) {
            console.log("error")
            console.log(error_data)
        },

    })

});

// Grab teams and render them into local variables


// WORKON : Create API to render teams on the web