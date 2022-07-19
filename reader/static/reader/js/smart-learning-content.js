/**
 * 
 * @param {string} url_host 
 * @param {function} callback_f 
 * @param {string} default_content_id, default: "parsons"
 * @param {string} default_provider_id, default: "parsons"
 * 
 * fetches contents of type --
 * 
 */
function fetchSmartContent(url_host,callback_f,content_id="parsons",provider_id="parsons"){

    var section_id = last_page_read["id"];
    var section_name = last_page_read["name"];
    var resource_id = last_page_read["resourceid"];
    var page_num = last_page_read["page"];

    var reader_info = new FormData();
    console.log("inside fetch smart content");
    reader_info.append("content_type",content_id); 
    reader_info.append("provider_id",provider_id);
    reader_info.append("section_id",section_id);
    reader_info.append("section_name",section_name);
    reader_info.append("resource_id",resource_id);
    reader_info.append("page_id",page_num);
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
            callback_f(url_host,res);
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
    
    list_of_content_types = '<div>';
    
    content_provider_types = activityurls["content_providers"];

    for (var id in content_provider_types){
        if (content_provider_types.hasOwnProperty(id)){
            list_of_content_types += `</div><div><input type="checkbox" id="${content_provider_types[id].provider_id}" name="${content_provider_types[id].content_type}" checked><label for="${content_provider_types[id].content_type}">${content_provider_types[id].content_type}</label></div>`;
        }
    }

    $('#smart-learning-content').html(list_of_content_types);

    for(var slc_id in activityurls){
        if(activityurls.hasOwnProperty(slc_id) &&
           activityurls[slc_id].hasOwnProperty('display_name')){
            var programming_activity_interface = $(
                '<a id="'+slc_id+'" href="#" class="slc">'+ activityurls[slc_id].display_name
                +'</a><br/>');
            $('#smart-learning-content').append(programming_activity_interface);
        }
    }

    $(".slc").click(function(evt){
        evt.preventDefault();
        modal.style.display="block";

        $(".modal-body").empty();

        $(".quiz-title").html(activityurls[this.id].display_name);
        $(".modal-footer").empty();
        $(".modal-body").append('<iframe src="'+ activityurls[this.id].activity_url 
        +'&svc={{request.svc}}&grp={{request.grp}}&usr={{request.usr}}&sid={{sid}}&cid={{cid}}'+
        ' height="100%" width="100%"></div>').ready();
    });


    var checkboxes = document.querySelectorAll("input[type=checkbox]");

    for (id =0; id < checkboxes.length; id++){
        checkboxes[id].addEventListener('change', function() {
            if (this.checked) {
            console.log(`${this.id} is checked`);
            } else {
            console.log(`${this.id} is not checked`);
            }
        });
    }
    
}
