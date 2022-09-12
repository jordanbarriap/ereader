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
function fetchSmartContent(url_host,user_id,group_id,callback_f,content_id="parsons",provider_id="parsons"){

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
            callback_f(url_host,res,user_id,group_id);
        },
        error: function(res){
            console.log("display smart content  call failed",res);
        }
    });

    // displayCompletedActivities({},url_host,user_id,group_id);
    
    $(document).on('slideouttabopen', function(evt){
        console.log("tab open",evt.target.id);
        if (evt.target.id === 'completed_slc'){
            
            var read_wiki_url = `http://${url_host}/api/get_smart_content_completed?user_id=${user_id}&group_id=${group_id}`;

            $.ajax({
                url: read_wiki_url,
                type:"GET",
                processData: false,
                contentType: false,
                crossDomain: true,
                success:function(res){
                    displayCompletedActivities(url_host,res,user_id,group_id);
                },
                error: function(res, options, err){
                    console.log("display completed smart content completed call failed",res.status,err);
                }
            });
        }
    });

}

function displaySmartContent(url_host,content_provider_types,user_id,group_id){
    console.debug("baton passed to display smart content");
    console.log("inside display", content_provider_types);

    display_names = {
        "quizpet":"Questions",
        "parsons":"Parsons",
        "animatedexamples": "Animations",
        "pcex": "Annotated Examples",
        "pcrs": "Coding Problems"
    }


    $('.right-smart-content').remove();

    if($(".right-smart-content").length == 0){
        
        var start_bottom_loc = 620;
        
        var colorCount = 0;
        slc_count = 0;
        for (var id in content_provider_types){
            slc_count += 1;
            if (content_provider_types.hasOwnProperty(id) && display_names.hasOwnProperty(id)){ 
                
                if (true){
                    colorCount += 1; 
                    start_bottom_loc -= 150;

                    var bcolor = randomColor({ luminosity:"light", format:'rgb'});
                    var textcolor = randomColor({ hue:"monochrome",luminosity:"dark", format:'rgb'});

                    $('#reader-div').append(`<div id=${id} class="right-smart-content">
                    <a id="right-handle" class="handle ui-slideouttab-handle ui-slideouttab-handle-rounded" style="background-color:${bcolor}; border-color:${bcolor};color:${textcolor}">${display_names[id]} <i class="fas fa-book-reader"></i></a>
                        <div id="right-subpanel">
                        <div id=${id}-smart-learning-content></div>
                        </div>
                    </div>`);

                    $(`#${id}.right-smart-content`).tabSlideOut({
                    tabLocation: 'right',
                    offset: `${start_bottom_loc}px`,
                    offsetReverse: true, // position the panel from the bottom of the page, rather than the top
                    otherOffset: '40px', // force panel to be fixed height (required to get the scrollbars to appear in the sub-panel)
                    handleOffsetReverse: true, // position the tab from the bottom of the panel, rather than the top
                    onLoadSlideOut: false, // open by default
                    // don't close this tab if a button is clicked, or if the checkbox is set 
                    clickScreenToCloseFilters: [
                    'button', // ignore button clicks
                    function(event){ // custom filter
                        // filters need to return true to filter out the click passed in the parameter
                        return $('#keepTabOpen').is(':checked');
                    }
                    ]
                    });
                    
                    /// Add the list of smart content to content specific tabs
                    for(var slc_id in content_provider_types[id]){
                        var activity = content_provider_types[id][slc_id];
                        // console.log(activity);
                        if(activity.hasOwnProperty('display_name') &&
                            activity.display_name !== activity.content_name){
                            
                            var programming_activity_interface = $(
                                '<a id="'+slc_id+'" href="#" class="slc"><i class="fas fa-award"></i> '+ activity.display_name
                                +'</a><br/>');
                            $(`#${id}-smart-learning-content`).append(programming_activity_interface);
                        }
                
                    }
                }

            }
        }

        
        $(`.slc`).click(function(evt){
            evt.preventDefault();
            modal.style.display="block";
            var id = $(this).parent().parent().parent().attr('id');
            console.log(id);
            $(".modal-body").empty();
    
            $(".quiz-title").html(content_provider_types[id][this.id].display_name);
            
            var checked = ["","","",""];
            
            $(".modal-body").append(`
                <div style="width=50%; height=50%">
                    <iframe src=${content_provider_types[id][this.id].activity_url}&svc={{request.svc}}&grp={{request.grp}}&usr={{request.usr}}&sid={{sid}}&cid={{cid}} height="65%" width="100%" />
                    <div width="100%">
                        <span>Please, work on the smart content exercises to rate it</span> <br />
                        <span>
                            Is this recommended smart programming exercise relevant for the section you just read? <br />
                        
                            <img id="star1" src="${star1}" alt="0 star" height="20" width="20"><input type="radio" name="smart-content-relevance" value="0" ${checked[0]}> Not relevant at all<br> 
                            <img id="star2" src="${star2}" alt="1 star" height="20" width="20"><input type="radio" name="smart-content-relevance" value="1" ${checked[1]}> Relevant for the course but not for the current section<br>
                            <img id="star3" src="${star3}" alt="2 star" height="20" width="40"><input type="radio" name="smart-content-relevance" value="2" ${checked[2]}> Partly relevant for the current section<br>
                            <img id="star4" src="${star4}" alt="3 star" height="20" width="60"><input type="radio" name="smart-content-relevance" value="3" ${checked[3]}> Relevant for the current section<br>
                        
                        </span> <br />
                        <textarea id="slc-feedback" class='textual' rows='3' placeholder="Please explain why you gave this rating here..."/>
                    </div>
                </div>
                <span id="content-name" style="display:none;">${content_provider_types[id][this.id].content_name}</span>
                <span id="component-name" style="display:none;">${content_provider_types[id][this.id].component_name}</span>
                <span id="context-name" style="display:none;">${content_provider_types[id][this.id].context_name}</span>
            `).ready();

            $('input[name="smart-content-relevance"]').change(function(event){
                console.log("smart-content-relevance checked");
                smartContentFeedback(url_host, user_id, group_id,"smart_content_relevance_rating");
            });
        
            $('#slc-feedback').blur(function(event){
                console.log("slc feedback text changed");
                smartContentFeedback(url_host, user_id, group_id,"smart_content_relevance_text");
            })

        });


    }
    

    if (false){
        
        list_of_content_types = '<div>';
    
        for (var id in content_provider_types){
            if (content_provider_types.hasOwnProperty(id)){
                list_of_content_types += `</div><div><input type="checkbox" id="${content_provider_types[id].provider_id}" name="${content_provider_types[id].content_type}" checked><label for="${content_provider_types[id].content_type}">${content_provider_types[id].content_type}</label></div>`;
            }
        }

        $('#smart-learning-content').html(list_of_content_types);

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
    
}

function displayCompletedActivities(completed_activities,url_host,user_id,group_id){
    var bcolor = randomColor({ luminosity:"dark", format:'rgb'});
    if($("#completed_slc").length == 0){
        $('#reader-div').append(`<div id="completed_slc">
            <a id="right-handle" class="handle ui-slideouttab-handle ui-slideouttab-handle-rounded" style="background-color:${bcolor};width:100px;">Rated Content <i class="fas fa-book-open"></i></a>
            <div id="right-subpanel">
            <div id="completed-slc-link-list"></div>
            </div>
        </div>`);

        $('#completed_slc').tabSlideOut({
        tabLocation: 'right',
        offset: '600px',         // offset from bottom
        offsetReverse: true, // position the panel from the bottom of the page, rather than the top
        otherOffset: '40px', // force panel to be fixed height (required to get the scrollbars to appear in the sub-panel)
        handleOffsetReverse: true, // position the tab from the bottom of the panel, rather than the top
        onLoadSlideOut: false, // open by default
        // don't close this tab if a button is clicked, or if the checkbox is set 
        clickScreenToCloseFilters: [
        //'button', // ignore button clicks
        function(event){ // custom filter
            // filters need to return true to filter out the click passed in the parameter
            return $('#keepTabOpen').is(':checked');
        }
        ]
        });
    }

    $('#completed-slc-link-list').empty();
    
    for(var slc_id=0; slc_id < completed_activities.length; slc_id++){
        var programming_activity_interface = $(
            '<span id="'+slc_id+'" class="slc">' + completed_activities[slc_id].content_name 
            +'</span><br/>');
        $('#completed-slc-link-list').append(programming_activity_interface);
    }
}

function smartContentFeedback(url_host,user_id,group_id,action_type){
    var resource_id = last_page_read["resourceid"];
    var page_num = last_page_read["page"];
    
    var content_name = $('#content-name').html();
    var component_name = $('#component-name').html();
    var context_name = $('#context-name').html();
    var smart_content_rating =  $('input[name="smart-content-relevance"]:checked').val();
    var smart_content_feedback_text = $('textarea#slc-feedback').val();
    var feedback_url = "http://"+url_host+"/api/smart_content_feedback";
    var current_date = new Date();
    var feedback_date = current_date.toISOString();

    var feedback_data = new FormData();

    feedback_data.append("user_id",user_id);
    feedback_data.append("group_id",group_id);
    feedback_data.append("feedback_date",feedback_date);
    feedback_data.append("content_name", content_name);
    feedback_data.append("resource_id",`${resource_id}-${page_num}`);
    feedback_data.append("component_name",component_name);
    feedback_data.append("context_name",context_name);
    feedback_data.append("smart_content_rating",smart_content_rating);
    feedback_data.append("smart_content_feedback_text",smart_content_feedback_text);
    feedback_data.append("action_type",action_type);

    $.ajax({
        url: feedback_url,
        type:"POST",
        data: feedback_data,
        processData: false,
        contentType: false,
        crossDomain: true,
        success:function(res){
            console.log(res);
            loaderOff();
        },
        error: function(res, options, err){
            console.log("error sending feedback, failed!",res.status,err);
            loaderOff();
        }
    });

}

function submitActivityResponse(url_host,user_id,group_id){
    console.log("inside smart content response")
    
}
