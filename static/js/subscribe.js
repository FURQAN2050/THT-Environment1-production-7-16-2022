var endpoint = '/accounts/api/process_payment/'

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

function getPaypalForm() {

    var csrftoken = getCookie('csrftoken');
    var id = $('#id_order').find(":selected").val();

    console.log(id)
    

    $.ajax({

        method: "POST",
        url: endpoint,
        data: {
            csrfmiddlewaretoken: csrftoken,
            'OrderID': id,
        },

        success: function(data) {
            console.log(data.form);
            $('#pay').append(data.form);
        },

        error: function(error_data) {
            console.log("error")
            console.log(error_data)
        },

    })
}


$('#id_order').change(function(){

    $('#pay').empty()

    getPaypalForm();
})

$(document).ready(function(){

    getPaypalForm();

});