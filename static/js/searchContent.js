// API Variable

var endpointSearch = '/content/api/search/';

function ListElement(name, tags, id, thumbnail, ulID) {
    this.name = name;
    this.tags = tags;
    this.thumbnail = thumbnail;
    this.id = id;
    this.ulID = ulID;

    this.createElement = function() {

        var tagText = "";

        for (var i = 0; i < this.tags.length; i++) {
            tagText += this.tags[i] + " ";
        }

        var html = `
        <li class="px-2 my-0 py-1 searchItem" id="` + this.id + `">` 
        + this.name +
        `<br><p class="small">` + tagText + `</p>
        </li>`;

        $("#" + this.ulID).append(html);

        $("#" + this.id).click(function(){

            $("#myModal").toggle();

            getElementOpen(this.id).then(function(data) {

                var contentOpen = new ContentOpen(data.name, data.description, data.videosThumbnail, data.imagesThumbnail, data.videos, data.images);

                contentOpen.createContent();

                
                $("#aClose").click(function() {

                    $("#myModal").toggle();
                    $("#myModal").empty();
                });
            });
        });
    }
}

// Get cookie function

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

function getContent(value) {

    return new Promise(function(resolve, reject){

        var csrftoken = getCookie('csrftoken');

        $.ajax({
            method: "GET",
            url: endpointSearch,
            data: {
                'action' : 'filterContent',
                'query' : $("#myInput").val(),
            },

            success: function(info) {
                resolve(info);
                console.log(info.name);
            },
            
            error: function(error) {
                reject(error);
            },
        });

    });
}

function searchContent() {

    getContent($("#myInput").val()).then(function(info){
        $("#myDropdown").empty();
        console.log(info);
        for(var i = 0; i < info.name.length; i++) {
            var element = new ListElement(info.name[i], info.tags[i], info.id[i], "", "myDropdown");
            element.createElement();
            console.log(info.name[i]);
        }
    });
}

$(document).ready(function(){

    searchContent();

    $(document).click(function(){
        
        $("#myInput").width(0);
        $("#myDropdown").hide();
        
    });

    $("#myInput").keyup(function(){
        searchContent();
    })

    $("#searchContainer").click(function(){

        $("#myInput").width(240);
        $("#myInput").css({
            "border": "solid 1px #eaecf4",
        })
        $("#myDropdown").show();
        event.stopPropagation();
    });

    $("#myDropdown").hide();

});