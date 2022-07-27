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

function displaySmartContent(url_host,content_provider_types){
    console.debug("baton passed to display smart content");
    console.log("inside display", content_provider_types);

    display_names = {
        "quizpet":"Questions",
        "parsons":"Parsons Problems",
        "animatedexamples": "Animated Examples",
        "pcex": "Annotated Examples"
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
            $(".modal-footer").empty();
            $(".modal-body").append(`<iframe src=${content_provider_types[id][this.id].activity_url}&svc={{request.svc}}&grp={{request.grp}}&usr={{request.usr}}&sid={{sid}}&cid={{cid}} height="100%" width="100%"></div>`).ready();
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
