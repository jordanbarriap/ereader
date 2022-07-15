/**
 * 
 * @param {string} url_host 
 * @param {function} callback_f 
 * @param {string} default_content_id, default: "parsons"
 * @param {string} default_provider_id, default: "parsons"
 * 
 * fetches contents of type --
        +------------------+------------------+
        | content_type     | provider_id      |
        +------------------+------------------+
        | parsons          | parsons          | -- doesn't load; initialization failed -- 404 http://adapt2.sis.pitt.edu/acos/pitt/jsparsons/jsparsons-python/ps?example-id=ps_python_calculate_function
        | animatedexamples | animatedexamples | -- doesn't load; initialization failed -- 404 	http://acos.cs.hut.fi/pitt/jsvee/jsvee-python/ae?example-id=ae_adl_swap
        | educvideos       | educvideos (not needed)    | -- doesn't load; timeout; http://columbus.exp.sis.pitt.edu/educvideos/loadVideo.html?videoid=vd_video0013&sub=1 
        | example          | webex            | -- loads; but after selection -- 403 forbidden; http://adapt2.sis.pitt.edu/web_ex_NV0FGdaHzy/Dissection2
        | question         | quizpet          | -- works without errors
        | pcrs             | pcrs             | -- doesn't load; response 500 url - https://pcrs.utm.utoronto.ca/mgrids/problems/python/179/embed?act=PCRS&sub=py_sum_product
        | pcex_set         | pcex             | -- loads without errors
        | question         | ctat             | -- no entries in the table (not needed)
        | pcex_challenge   | pcex_ch          | -- works without errors (count as pcex_set)
        | question         | codeocean        | -- no entries in the table (not needed)
        | question         | parsons          | -- doesn't load; intialization failed; 404 http://adapt2.sis.pitt.edu/acos/pitt/jsparsons/jsparsons-python/ps?example-id=ps_python_freq_of_char2 (not needed)
        | readingmirror    | readingmirror    | -- Doesn't load; 500 error can't open page http://adapt2.sis.pitt.edu/ereader/reader/7/pfe-3-1/ (not needed)
        +------------------+------------------+
 */
function fetchSmartContent(url_host,callback_f,content_id="parsons",provider_id="parsons"){
    var reader_info = new FormData();
    console.log("inside fetch smart content");
    reader_info.append("content_type",content_id); 
    reader_info.append("provider_id",provider_id);
    reader_info.append("privacy","public");

    $.ajax({
        url: "http://"+url_host+"/api/smart_learning_content/programming",
        type:"POST",
        data: reader_info,
        processData: false,
        contentType: false,
        crossDomain: true,
        success:function(res){
            // console.log("response from programming api",res.activity_url);
            callback_f(url_host,res.activity_url);
        },
        error: function(res){
            console.log("display smart content  call failed",res);
        }
    });
}

function displaySmartContent(url_host,activityurls){
    console.debug("baton passed to display smart content");
    console.log("inside display", activityurls);

    if($("#right-smart-content").length == 0){
        $('#reader-div').append('<div id="right-smart-content">' +
        '<a id="right-handle" class="handle ui-slideouttab-handle ui-slideouttab-handle-rounded">Smart Content <i class="far fa-play-circle fa-lg"></i></a>' +
        '      <div id="right-subpanel">' +
        '      <div id="smart-learning-content"></div>' +
        '      </div>' +
        '</div>');

        $('#right-smart-content').tabSlideOut({
        tabLocation: 'right',
        offsetReverse: true, // position the panel from the bottom of the page, rather than the top
        otherOffset: '40px', // force panel to be fixed height (required to get the scrollbars to appear in the sub-panel)
        handleOffsetReverse: true, // position the tab from the bottom of the panel, rather than the top
        onLoadSlideOut: true, // open by default
        // don't close this tab if a button is clicked, or if the checkbox is set 
        clickScreenToCloseFilters: [
        'button', // ignore button clicks
        function(event){ // custom filter
            // filters need to return true to filter out the click passed in the parameter
            return $('#keepTabOpen').is(':checked');
        }
        ]
        });
    }
    
    $('#smart-learning-content').html('<div>' +
                                        '<input type="checkbox" id="parsons" name="parsons" checked>' +
                                        '<label for="Parsons">Parsons</label>' +
                                        '</div><div>' + 
                                        '<input type="checkbox" id="pcex" name="pcex" checked>' +
                                        '<label for="pcex">PCEX_set</label>' + 
                                        '</div><div>' +
                                        '<input type="checkbox" id="pcrs" name="pcrs" checked>' +
                                        '<label for="pcrs">PCRS</label>' + 
                                        '</div><div>' +
                                        '<input type="checkbox" name="animatedexamples" checked>'+
                                        '<label for="animatedexamples">animatedexamples</label>' +
                                        '</div><div>' +
                                        '<input type="checkbox" name="webex" checked>'+
                                        '<label for="webex">webex</label>' +
                                        '</div><div>'+
                                        '<input type="checkbox" name="quizpet" checked>'+
                                        '<label for="quizpet">quizpet</label>' +
                                        '</div><div>'+
                                        '<input type="checkbox" name="pcex_ch" checked>'+
                                        '<label for="pcex_h">pcex challenge</label>' +
                                        '</div>'
                                    );

    for(var slc_id=0; slc_id<activityurls.length;slc_id++){
        var programming_activity_interface = $(
            '<a id="'+slc_id+'" href="#" class="slc">smart_learning_content ' + slc_id 
            +'</a><br/>');
        $('#smart-learning-content').append(programming_activity_interface);
    }

    $(".slc").click(function(evt){
        evt.preventDefault();
        modal.style.display="block";

        $(".modal-body").empty();

        $(".quiz-title").html("Smart Content " + this.id);
        $(".modal-footer").empty();
        $(".modal-body").append('<iframe src="'+ activityurls[this.id] +'" height="100%" width="100%"></div>').ready();
    });
    
}
