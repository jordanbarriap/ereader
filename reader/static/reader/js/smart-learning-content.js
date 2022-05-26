
function fetchSmartContent(url_host,callback_f){
    var reader_info = new FormData();
    console.log("inside fetch smart content");
    reader_info.append("content_type","pcex_set");
    reader_info.append("provider_id","pcex");
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
    console.log("baton passed");
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
    
    $('#smart-learning-content').html("");

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
