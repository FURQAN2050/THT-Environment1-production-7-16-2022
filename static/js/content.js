// API Variable

var endpointContent = '/content/api/data/';
var lastElement = [];
var datesSent = [];

// Object constructors


function Document(name, url, id) {

    this.name = name;
    this.url = url;
    this.id = id;

    console.log(this.name, this.url, this.id);

    this.createElement = function () {

        var html = `
            <div class="mx-3"><a href=`+ this.url + ` target="_blank">` + this.name + `</a></div>
        `

        return html;
    }
}

function ContentElement(name, tags, id, thumbnail, datePosted) {

    this.name = name;
    this.tags = tags;
    this.id = id;
    this.thumbnail = thumbnail;
    this.datePosted = datePosted;

    this.createElement = function () {


        var tagsText = "";
        var maxLength = 5;
        var numTags = 0;

        numTags = tags.length > maxLength ? maxLength : tags.length;

        for (x = 0; x < numTags; x++) {
            tagsText += '<div class="tag mx-2 small text-right">' + this.tags[x].slice(0, 12) + '</div>';
        }

        var html = `<div class="content col-sm-5 col-md-5 col-xl-3 px-0 mx-4 my-3" id="content_` + this.id + `">
            <div class="parentThumbnail">
                <div class="thumbnail"></div>
            </div>
            <div class="text-area pb-3 px-2">
                <div class="name h5 py-2 px-2 text-center">` + this.name.slice(0, 30) + `</div>
                <div class="tags row justify-content-end mx-2">
                    ` + (tags.length > 0 ? `<span class="fa fa-tag"></span>` : ' ')
            + tagsText +
            `</div>
            </div>
        </div>`;

        return html;
    }

    this.addThumbnail = function () {

        var css;

        css = {
            "background-image": "url(" + this.thumbnail + ")",
            "background-size": "cover",
            "height": "100%",
        }

        return css;
    }

    this.getDate = function () {
        return this.datePosted;
    }
}

function ContentOpen(name, description, imagesThumbnail, videos, images, docs, docsNames, imagesNames, videosNames) {

    this.name = name;
    this.description = description;
    this.videosNames = videosNames;
    this.imagesThumbnail = imagesThumbnail;
    this.imagesNames = imagesNames;
    this.videos = videos;
    this.images = images;
    this.docs = docs;
    this.docsNames = docsNames;


    this.createContent = function () {

        var html;
        var videosList = new Array;
        var imagesList = new Array;
        var docsList = ' ';
        var imagesTitle = ' ';
        var videosTitle = ' ';
        var docsTitle = ' ';

        for (i = 0; i < this.docs.length; i++) {

            var document = new Document(this.docsNames[i], this.docs[i], i);

            docsList += document.createElement();

        }

        for (i = 0; i < this.videos.length; i++) {

            videosList.push(`
            <div id="video_`+ i + `">
                <div>
                    <iframe height="200" width="300"  
                    src=`+ this.videos[i] + `> 
                    </iframe>
                </div>
                <p class="mx-auto text-center my-1">` + this.videosNames[i] + `</p>
            </div>`)
        }

        for (i = 0; i < this.imagesThumbnail.length; i++) {

            imagesList.push(`
            <div id="image_`+ i + `">
                <div class="parentThumbnail">
                    <div class="thumbnail"></div>
                </div>
                <p class="mx-auto text-center my-1">` + this.imagesNames[i] + `</p>
            </div>`)
        }

        if (this.imagesThumbnail.length > 0) {
            imagesTitle = 'Images'
        }

        if (this.videos.length > 0) {
            videosTitle = 'Videos'
        }

        if (this.docs.length > 0) {
            docsTitle = 'Documents'
        }



        html = `
        <div class="modal-content">
            <div id="aClose" class="close align-self-end">&times;</div>
            <div class="elementContainer">

                <h5 class="mx-3">` + imagesTitle + `</h5>
                <hr>

                <div id="imageContainer"></div>
            
                <h5 class="mx-3">` + videosTitle + `</h5>
                <hr>
                
                <div id="videoContainer"></div>

                <h5 class="mx-3 mt-3">` + docsTitle + `</h5>
                <div>
                    ` + docsList + `
                </div>

                <h5 class="mx-3 mt-3">Description</h5>
                <hr>
                <div class="mx-3 my-3"><p>` + this.description + `</p></div>
            </div>
        </div>`;

        $("#myModal").append(html);

        if (imagesList.length > 0) {

            this.createSliderHTML(imagesList, "contentImage", "imageContainer");

            for (i = 0; i < this.imagesThumbnail.length; i++) {
                $("#image_" + i + " .thumbnail").css({
                    "background-image": "url(" + this.imagesThumbnail[i] + ")",
                    "background-size": "cover",
                    "height": "100%",
                })
            }

            this.createSlider("contentImage");
        }

        if (videosList.length > 0) {

            this.createSliderHTML(videosList, "contentVideo", "videoContainer");

            // for(i = 0; i < this.videos.length; i++) {

            //     $("#video_" + i + " .thumbnail").css({
            //         "background-image" : "url(" + this.videos[i] + ")",
            //         "background-size" : "cover",
            //         "height" : "100%",
            //     })
            // }

            this.createSlider("contentVideo");
        }

        return html;
    }

    this.createSliderHTML = function (elementsHTML, idSlider, idParent) {

        li = "";
        bullets = "";
        var elements = idSlider == "contentImage" ? this.images : this.videos

        for (i = 0; i < elementsHTML.length; i++) {
            li += '<li id=' + idSlider + '_' + i + ' class="glide__slide">' + elementsHTML[i] + '</li>';
            bullets += `<button class="glide__bullet" data-glide-dir="=` + i + `"></button>`;
        }

        HTML = `
        <div id="` + idSlider + `">
            <div data-glide-el="track" class="glide__track">
                <ul class="glide__slides">
                    ` + li + `
                </ul>
            </div>

            <div class="glide__arrows" data-glide-el="controls">
                <button class="glide__arrow glide__arrow--left" data-glide-dir="<"><i class="fa fa-angle-left"></i></button>
                <button class="glide__arrow glide__arrow--right" data-glide-dir=">"><i class="fa fa-angle-right"></i></button>
            </div>

            <div class="glide__bullets" data-glide-el="controls[nav]">
                ` + bullets + `
            </div>
        </div>`

        $("#" + idParent).append(HTML);

        // for(i = 0; i < elementsHTML.length; i++) {
        //     this.addClickFunctionality(idSlider + "_" + i, elements[i]);
        // }

        return HTML;
    }

    this.createSlider = function (id) {

        var glide = new Glide('#' + id, {
            type: 'slider',
            gap: 30,
            startAt: 0,
            perView: 4,
            perTouch: 1,
            focusAt: 'center',
            breakpoints: {
                2048: {
                    perView: 3,
                    startAt: 1,
                },
                1400: {
                    perView: 2,
                    startAt: 1,
                },
                720: {
                    perView: 1,
                    startAt: 0,
                },
            },
        })

        glide.mount()

    }

    this.addClickFunctionality = function (id, linkOpen) {
        $("#" + id).click(function (event) {
            if (id.substring(0, 12) == "contentImage") {
                var image = new ImageOpen(linkOpen, "myModalMedia");
            }
            else {
                var video = new VideoOpen(linkOpen, "myModalMedia");
            }
        });
    }
}

function ImageOpen(url, id) {

    this.url = url;
    this.id = id

    $("#" + this.id).show();

    this.createContent = function () {

        var html = `
                <div id="imageContent" class="modal-content">
                    <div id="aClose_media" class="close align-self-end">&times;</div>
                    <img src="` + this.url + `" width="100%">
                </div>`

        $("#" + this.id).append(html);

    }

    this.createContent()

    $("#aClose_media").click(function () {

        $("#myModalMedia").hide();
        $("#myModalMedia").empty();
    });

}

function VideoOpen(url, id) {

    this.url = url;
    this.id = id

    $("#" + this.id).show();

    this.createContent = function () {

        var html = `
                <div id="videoContent" class="modal-content">
                    <div id="aClose_media" class="close align-self-end">&times;</div>
                </div>`

        $("#" + this.id).append(html);

        $("#videoContent").append($("<video controls='controls' controlsList='nodownload' class='col video' />"));
        $("#videoContent .video").attr('src', this.url);

    }

    this.createContent()

    $("#aClose_media").click(function () {

        $("#myModalMedia").hide();
        $("#myModalMedia").empty();
    });

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


function getElement(date, length, tags) {

    return new Promise(function (resolve, reject) {

        var csrftoken = getCookie('csrftoken');

        $.ajax({
            method: "POST",
            url: endpointContent,
            data: {
                'action': 'getContent',
                'tags': tags,
                'startDate': date,
                'length': length,
                csrfmiddlewaretoken: csrftoken,
            },

            success: function (data) {
                resolve(data);
            },

            error: function (error_data) {
                reject(error_data);
            },
        });
    });
}

function getElementOpen(id) {

    return new Promise(function (resolve, reject) {

        var csrftoken = getCookie('csrftoken');

        $.ajax({
            method: "POST",
            url: endpointContent,
            data: {
                'action': 'getContentOpen',
                'id': id,
                csrfmiddlewaretoken: csrftoken,
            },

            success: function (data) {
                resolve(data);
            },

            error: function (error_data) {
                reject(error_data);
            },
        });
    });
}

// $(window).scroll(function() {


//     if($(window).scrollTop() >= $(document).height() - $(window).height()) {


//         getElement(lastElement[lastElement.length -1].getDate(), 6, 'Tag1').then(function(data) { 

//             for(i = 0; i < data.names.length; i++) {

//                 // Sometimes browser will send request multiple times and receive multiple responses with the 
//                 // same element. This line disregards those requests.


//                 if(lastElement.map(a => a.id).includes(data.id[i])) {
//                     continue;
//                 }

//                 var contentElement = new ContentElement(data.names[i], data.tags[i], data.id[i], data.thumbnail[i], data.datesPosted[i]);
//                 lastElement.push(contentElement);
//                 lastElement.sort((a,b) => b.getDate() - a.getDate())

//                 $("#content-area").append(
//                     contentElement.createElement()
//                 );

//                 if(data.thumbnail[i] != "None") {

//                     $("#content_" + data.id[i] + " .thumbnail").css(
//                         contentElement.addThumbnail()
//                     );
//                 }

//                 else {

//                     $("#content_" + data.id[i] + " .thumbnail").css({
//                         "height" : "100%",
//                         "padding" : "3rem",
//                     });

//                     $("#content_" + data.id[i] + " .thumbnail").append(
//                         data.description[i].slice(0,100) + "..."
//                     )
//                 }

//                 // Create content modal
//                 $("#content_"+ data.id[i]).click(function(event) {

//                     $("#myModal").toggle();

//                     getElementOpen($(this).attr('id').split("_").pop()).then(function(data) {

//                         var contentOpen = new ContentOpen(data.name, data.description, data.imagesThumbnail, data.videos, data.images, data.docs, data.docsNames, data.imagesNames, data.videosNames);

//                         contentOpen.createContent();


//                         $("#aClose").click(function() {

//                             $("#myModal").toggle();
//                             $("#myModal").empty();
//                         });
//                     });
//                 });
//             }
//         });
//     }
// });

$(document).ready(function () {

    getElement("now", 40, 'Tag1').then(function (data) {
        console.log(data);
    }, function (error_data) {
        console.log(error_data);
    });

    getElement("now", 40, 'Tag1').then(function (data) {

        for (i = 0; i < data.names.length; i++) {

            var contentElement = new ContentElement(data.names[i], data.tags[i], data.id[i], data.thumbnail[i], data.datesPosted[i]);

            lastElement.push(contentElement);
            lastElement.sort((a, b) => b.getDate() - a.getDate())
            datesSent.push(contentElement.getDate());
            datesSent.sort();

            $("#content-area").append(
                contentElement.createElement()
            );


            if (data.thumbnail[i] != "None") {

                $("#content_" + data.id[i] + " .thumbnail").css(
                    contentElement.addThumbnail()
                );

            }

            else {

                $("#content_" + data.id[i] + " .thumbnail").css({
                    "height": "100%",
                    "padding": "3rem",
                });

                $("#content_" + data.id[i] + " .thumbnail").append(
                    data.description[i].slice(0, 100)
                )

            }

            // Create content modal
            $("#content_" + data.id[i]).click(function (event) {

                $("#myModal").toggle();

                getElementOpen($(this).attr('id').split("_").pop()).then(function (data) {

                    var contentOpen = new ContentOpen(data.name, data.description, data.imagesThumbnail, data.videos, data.images, data.docs, data.docsNames, data.imagesNames, data.videosNames);

                    contentOpen.createContent();


                    $("#aClose").click(function () {

                        $("#myModal").toggle();
                        $("#myModal").empty();
                    });
                });
            });
        }
    });
});