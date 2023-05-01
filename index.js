var json_response = null;
var dataset_html = null;
// On DOM Load
jQuery(function() {
    event_handler()

    load_analysis()
})

function event_handler(){
    $(".master_content").find(".data_content").hide()
    $("#1_content").show()
    $(".content").find(".master_content").hide()
    $("#master_content_1").show()
    // on tab click
    $(".tab").on('click', function(){
        //unselect each tab
        $(this).parent().find(".tab").removeClass("selected")
        //select clicked tab
        var tab_id = $(this).attr('id')
        $(this).addClass('selected')

        var parent_class = $(this).parent().attr('class')

        if (parent_class == "master_tab_list") {
            //hide other analysis content
            $(".content").find(".master_content").hide()
            $("#master_content_" + tab_id).show()
        }
        else {
            //hide other analysis content
            $(".master_content").find(".data_content").hide()
            $("#" + tab_id + "_content").show()
        }
    })
}

function load_analysis() {
    console.log("Getting data...")
    get_data().then(function(response){
        json_response = response
        
        // Load all analyses
        load_max_speed(json_response.analyses.max_speed)
        load_play_length(json_response.analyses.play_length)
        load_field_type(json_response.analyses.field_type)
        load_table_samples(json_response.tables)
    })
}

function load_table_samples(tables) {
    const tables_json = tables

    dataset_html = ""
    for (var table in tables_json) {
        var html_table = `<b>${table} (${tables_json[table]['count']} records)</b><br>
        <table border=1><tr>`

        for (var col in tables_json[table]['data'][0]) {
            html_table += `<th>${col}`
        }

        for (var row in tables_json[table]['data']) {
            html_table += "<tr>"
            for (var col in tables_json[table]['data'][row]) {
                html_table += `<td>${tables_json[table]['data'][row][col]}`
            }
        }
        html_table += "</table><br><br><br>"
        dataset_html += html_table
    }

    $("div#dataset_info").html(dataset_html)
}

function load_max_speed(max_speed) {
    const analysis = max_speed
    console.log(analysis)

    // print image of chart
    var img_html = "<img src='charts/" + analysis.figure_name + "'>"
    $("div#1_content > .data_grid > .chart ").html(img_html)

    // print analysis of data
    var analysis_html = `
        <b>Figure 1:</b> Max speed of player during injury and non-injury causing plays<br><br>

        <b>X-axis:</b> Max speed<br>
        <b>Y-axis:</b> Number of plays<br><br>
        
        <b>Correlation Coefficient:</b> ${analysis.correlation_coefficient}<br>
        P-Value: ${analysis.p_value}<br><br>

        <b>Null hypothesis:</b> There is no correlation between max speed of a player during a play and rate of injury.<br><br>
       
        <b>Conclusion:</b> Because the p-value is less than the significance value of 0.05,
        we can accept the alternative hypothesis that there is a correlation between max speed
        and rate of injury.
    `
    $("div#1_content > .data_grid > .analysis").html(analysis_html)

}

function load_play_length(play_length) {
    const analysis = play_length
    console.log(analysis)

    // print image of chart
    var img_html = "<img src='charts/" + analysis.figure_name + "'>"
    $("div#2_content > .data_grid > .chart ").html(img_html)

    // print analysis of data
    var analysis_html = `
        <b>Figure 2:</b> Play length of injury and non-injury causing plays<br><br>

        <b>X-axis:</b> Injury or Non-injury play<br>
        <b>Y-Axis:</b> Play Length<br><br>
        
        <b>Median Injured Players:</b> ${analysis.median_injured.toFixed(2)}<br>
        <b>Median Non-Injured Players:</b> ${analysis.median_noninjured.toFixed(2)}<br><br>
    
    `
    $("div#2_content > .data_grid > .analysis").html(analysis_html)
}

function load_field_type(field_type) {
    const analysis = field_type
    console.log(analysis)

    // print image of chart
    var img_html = "<img src='charts/" + analysis.figure_name + "'>"
    $("div#3_content > .data_grid > .chart ").html(img_html)

    // print analysis of data
    var analysis_html = `
        <b>Figure 3:</b> Expected and observed distribution of field types for injury-causing plays<br><br>

        <b>X-axis:</b> Field Type<br>
        <b>Y-axis:</b> Number of plays<br><br>
        
        <b>Critical value:</b> ${analysis.critical_value}<br>
        <b>Chi-squared value:</b> 7.374364<br>
        <b>P-Value:</b> 0.00661602<br>${analysis.p_value}<br><br>
    
        <b>Null hypothesis:</b> There is no correlation between field type and rate of injury.<br><br>
        
        <b>Conclusion:</b> Because the p-value is less than the significance value of 0.05,
        we can accept the alternative hypothesis that there is a correlation between field type 
        and rate of injury.
    `
    $("div#3_content > .data_grid > .analysis").html(analysis_html)
}

function get_data() {
    return new Promise(function(resolve) {
        $.ajax({
            url: '../../cgi-bin/datamining_project/nfl_injury_stats.py',
            dataType: 'json',
            type: 'POST',
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