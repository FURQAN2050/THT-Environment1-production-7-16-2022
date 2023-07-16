
// Answered questions that are yes

var questionsYes = 0;

// Create ring progess animation variables

const circle = document.querySelector('.ring__circle');
const radius = circle.r.baseVal.value;
const circumference = radius * 2 * Math.PI;
const DAYS_NUM = 5;
var dates = new Array();

var dayChart;
var pointsChartMe;
var numQuestions;

// API variables

var endpoint = '/board/api/data/'

// Get last 5 days for graph

for(i = 0; i < DAYS_NUM; i++) {
    
    //dates.unshift(new Date(date.setDate(date.getDate() - 1)).toLocaleDateString());
    dates.unshift(moment().subtract(i, 'days').format('MM/DD/YYYY'));

}

//var labels = ['Days', 'Points']

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

// Set progress for the ring and create animation

function setProgress(percent) {
    const offset = circumference - percent / 100 * circumference;
    circle.style.strokeDashoffset = offset;

    if(percent < 99) {
        circle.style.strokeWidth = 14;
    }

    if(percent >= 99) {
        circle.style.strokeWidth = 27;
    }
}

// Open tabs for the questions section

function openTab(evt, tab, tabSectionContent, tabSectionLinks) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class=tabSectionContent and hide them
    tabcontent = document.getElementsByClassName(tabSectionContent);
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }

    // Get all elements with class=tabSectionLinks and remove the class "active"
    tablinks = document.getElementsByClassName(tabSectionLinks);
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tab).style.display = "block";
    evt.currentTarget.parentNode.className += " active";
  }

// Create button questions functionality

function questionsButtonsListener(evt, question, date, answer) {

    // Update view

    questionUpdateView(evt);

    // Update questions

    questionUpdateDatabase(question, date, answer);

}


// Add styles to buttons when interacting with them

function questionUpdateView(evt) {

    var buttonDivs, button, i;

    buttonDivs = evt.currentTarget.parentNode.parentNode.getElementsByClassName("button-links");

    for(i = 0; i < buttonDivs.length; i++) {

        button = buttonDivs[i].getElementsByTagName("button")[0];

        if(button.classList.contains("questions-yes") && button.classList.contains("active")) {
            questionsYes -= 1;
            pointUpdate(-1);
        }

        button.className = button.className.replace(" active", "");
    }

    evt.currentTarget.className += " active";

    if(evt.currentTarget.classList.contains("questions-yes")) {
        questionsYes += 1;
        pointUpdate(1);
    }

    setProgress((100/numQuestions)*questionsYes);
}

// Create chart

function setBarChart(data, labels, id, color1, color2, minY, maxY) {

    // Bar chart
    var ctx = document.getElementById(id)
    var ctxc = ctx.getContext("2d");
    var gradientStroke = ctxc.createLinearGradient(0, 0, 0, 150);
    gradientStroke.addColorStop(1, color1);
    gradientStroke.addColorStop(0, color2);

    

    var dayChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: "Points",
                backgroundColor: gradientStroke,
                pointHoverRadius: 5,
                pointHitRadius: 50,
                pointBorderWidth: 2,
                data: data,
            }],
        },
        options: {
            scales: {
                xAxes: [{
                    time: {
                        unit: 'date'
                    },
                    gridLines: {
                        display: false
                    },
                    ticks: {
                        maxTicksLimit: 7,
                        display: false
                    }
                }],
                yAxes: [{
                    gridLines: {
                        display: false,
                    },
                    ticks: {
                        min: minY,
                        display: false,
                    }
                }],
            },
            legend: {
                display: false
            }
        }
    });

    return dayChart;
}

// Create line chart

function setLineChart(data, labels, id, color1, color2, minY, maxY) {

    // Line chart
    var ctx = document.getElementById(id)
    var ctxc = ctx.getContext("2d");
    var gradientStroke = ctxc.createLinearGradient(0, 0, 0, 150);
    gradientStroke.addColorStop(1, color1);
    gradientStroke.addColorStop(0, color2);

    var dayChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: "Points",
                backgroundColor: gradientStroke,
                borderColor: "rgba(12,84,96,1)",
                pointBackgroundColor: "rgba(2,117,216,1)",
                pointBorderColor: "rgba(255,255,255,0.8)",
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgba(2,117,216,1)",
                pointHitRadius: 50,
                pointBorderWidth: 2,
                data: data,
            }],
        },
        options: {
            scales: {
                xAxes: [{
                    time: {
                        unit: 'date'
                    },
                    gridLines: {
                        display: false
                    },
                    ticks: {
                        maxTicksLimit: 7,
                        display: false
                    }
                }],
                yAxes: [{
                    gridLines: {
                        display: false,
                    },
                    ticks: {
                        min: minY,
                        display: false,
                    }
                }],
            },
            legend: {
                display: false
            }
        }
    });

    return dayChart;
}

// Update points in view

function pointUpdate(amount) {

    var mePoints = parseInt($("#me").text(), 10);
    var teamPoints = parseInt($("#team").text(), 10);
    var districtPoints = parseInt($("#district").text(), 10);

    mePoints += amount;
    teamPoints += amount;
    districtPoints += amount;

    $("#me").text(mePoints);
    $("#team").text(teamPoints);
    $("#district").text(districtPoints);
}

// Update points in screen

function pointGetDatabase() {

    var csrftoken = getCookie('csrftoken');


    $.ajax({
        method:"POST",
        url: endpoint,
        data: {
            'action' : 'currentPoints',
            csrfmiddlewaretoken: csrftoken,
        },

        success: function(data) {
            $("#me").text(data.myPoints),
            $("#team").text(data.teamPoints),
            $("#district").text(data.districtPoints)
        },

        error: function(error_data) {
            console.log("error")
            console.log(error_data)
        },
    });

}

// Add questions to database

function questionUpdateDatabase(questionID, date, answer) {
    
    var csrftoken = getCookie('csrftoken');


    $.ajax({
        method:"POST",
        url: endpoint,
        data: {
            'action' : 'questionAction',
            'answer' : answer,
            'question' : questionID,
            'date' : date,
            csrfmiddlewaretoken: csrftoken,
        },

        success: function(data) {
            console.log("Success");
        },

        error: function(error_data) {
            console.log("error");
            console.log(error_data);
        },
    });
    

}

// Get question status

function getQuestionStatus(questionID) {
    
    var csrftoken = getCookie('csrftoken');

    console.log("Hey I am here")


    $.ajax({
        method:"POST",
        url: endpoint,
        data: {
            'action' : 'questionStatus',
            'question' : questionID,
            csrfmiddlewaretoken: csrftoken,
        },

        success: function(data) {
            
            $("#" + questionID).find("button").each(function(index) {
                if($(this).hasClass(data.answer)) {
                    $(this).addClass("active");
                    
                    if(data.today && data.answer == "yes") {
                        questionsYes += 1;
                        setProgress((100/numQuestions)*questionsYes);
                    }
                }
            });
        },

        error: function(error_data) {
            console.log("error");
            console.log(error_data);
        },
    });

}


// Update points

function getPointsDay(date) {

    return new Promise(function(resolve, reject) {

        var csrftoken = getCookie('csrftoken');

        var points;

        $.ajax({
            method:"POST",
            url: endpoint,
            data: {
                'action' : 'dayPoints',
                'date' : date,
                csrfmiddlewaretoken: csrftoken,
            },

            success: function(data) {
                
                points = data.points;
                resolve(points);
            },

            error: function(error_data) {
                reject(error_data);
            },
        });

    })

}

function getPointsMe(date) {

    return new Promise(function(resolve, reject) {

        var csrftoken = getCookie('csrftoken');

        var points;

        $.ajax({
            method:"POST",
            url: endpoint,
            data: {
                'action' : 'currentPoints',
                csrfmiddlewaretoken: csrftoken,
            },

            success: function(data) {
                
                points = data.myPoints;
                resolve(points);
            },

            error: function(error_data) {
                reject(error_data);
            },
        });

    })

}

// Update charts with data from server

function  updateChart(dayChart, pointsChartMe, dates) {

    var pointsArray = new Array();
    var accumulatedPoints = 0;

    // Clean graphs

    dayChart.reset();
    pointsChartMe.reset();

    // Get daily points for teacher

    var promise = new Promise(function(resolve) {

        // Get points for last 5 days

        var sequence = Promise.resolve();
        
        dates.forEach(function(date){
            
            sequence = sequence.then(function() {
                return getPointsDay(date);
            }).then(function(points) {

                dayChart.data.datasets.forEach((dataset) => {
                    dataset.data.push(points);
                });
                
                dayChart.update();

                pointsArray.push(points);

                if(pointsArray.length == 5) {
                    console.log(pointsArray);
                    resolve();
                    
                }

            });

        });

    });

    // Get line chart for teacher points

    promise.then(function() {
    
        getPointsMe().then(function(totalPoints) {

            accumulatedPoints = totalPoints;

        }).then(function() {

            // Update line chart for teacher

            // Update accumulated points

            for(i = pointsArray.length - 1; i >= 0 ; i--) {

                pointsChartMe.data.datasets.forEach((dataset) => {
                    dataset.data.unshift(accumulatedPoints);
                });
                pointsChartMe.update();

                accumulatedPoints = accumulatedPoints - pointsArray[i];
                console.log(accumulatedPoints)

            }

        });

    });
}



$(document).ready(function(){

    
    //document.getElementById("defaultOpen").click();
    document.getElementById("defaultOpenGraph").click();


    var data = new Array(); // Data for daily points

    // Get number of questions

    numQuestions = $("#Today").children().length;

    
    circle.style.strokeDasharray = `${circumference} ${circumference}`;
    circle.style.strokeDashoffset = `${circumference}`;
    circle.style.strokeWidth = 14;


    // Graph variables
    

    dayChart = setBarChart(data, dates, "dayChart", "#63C7FB", "#E280FF", 0, 3);
    pointsChartMe = setLineChart([], dates, "pointChart", "#63C7FB", "#E280FF", 0, 3);


    updateChart(dayChart, pointsChartMe, dates);


    // Get status and style question buttons

    $("#Today").children("div").each(function() {
        getQuestionStatus($(this).attr('id'))
    });

    if($(window).width() > 975) {
        $(".wrap").css("height", $("#Today").height() - $("#dayChart").height() * .8)
    }

    pointGetDatabase();
});