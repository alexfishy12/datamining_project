// On DOM Load
jQuery(function() {
    event_handler()

    load_analysis(1)
})

function event_handler(){
    // on tab click
    $(".tab").on('click', function(){
        //unselect each tab
        $(".content").find(".tab").removeClass("selected")
        //select clicked tab
        var tab_id = $(this).attr('id')
        $(this).addClass('selected')

        load_analysis(tab_id)
    })
}

function load_analysis(analysis) {
    //hide other analysis content
    $(".inner_content").find(".data_content").hide()
    $("#" + analysis + "_content").show()

    console.log("Loading analysis " + analysis)
    get_data(analysis).then(function(response){
        if (response.contains("error")) {
            console.log("ERROR: " + response)
        }
        else {
            console.log(response)

        }
    })
}

function get_data(analysis) {
    return new Promise(function(resolve) {
        $.ajax({
            url: '../../nfl_injury_stats.py',
            dataType: 'text',
            type: 'POST',
            data: {email_id: email_id},
            success: function (response, status) {
                console.log('AJAX Success.');
                resolve(response);
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                console.log('AJAX Error:' + textStatus);
                resolve("Error " . textStatus);
            }
        })
    });
}