/**
 * 
 * @param {string} url_host 
 * @param {function} callback_f 
 * @param {json} request_data default {name : 'iir-2.1', type: 'simple'}
 *
    - Section Articles: http://scythian.exp.sis.pitt.edu/Textbook/ir/sectionkey.php?name=[Section_Name]&type=[“simple/details”]
    - Question Articles: http://scythian.exp.sis.pitt.edu/Textbook/ir/questionkey.php?name=[Question_Name]&type=[“simple/details”]

    These APIs generate two version of the results (simple/details) which can be specified in the URL
    Simple results returns a list of item with “Rank”, “Title” and “Score” properties. Detail returns the same with the addition of the article summary from wikipedia.

    Here are some examples:

    Relevant Articles for Section iir-2.1 ->    http://scythian.exp.sis.pitt.edu/Textbook/ir/sectionkey.php?name=iir-2.1&type=simple
    Relevant Articles for Question q380 ->   http://scythian.exp.sis.pitt.edu/Textbook/ir/questionkey.php?name=q380&type=detail    

 */
function fetchWikiContent(url_host,resource_id,page_num, user_id,group_id, callback_f,request_data = { 
    origin:'localhost',
    action: 'query',
    page: 'human information processing',
    list:'search',
    srsearch: 'Cognitive Psychology: History and Overview', 
    srlimit: 500,
    format: 'json' 
}){

    
    if(false) {console.log("inside fetch Wiki content",last_page_read);}
    if(false) {console.log("inside fetch wiki content",request_data.srsearch);}
    // alternate url "http://"+url_host+"/api/wiki_resources_content",

    if (false){
        
        var reader_info = new FormData();
        reader_info.append('name','iir-2.1');
        reader_info.append('type','simple');

        /*** testing out behnam's wiki api   
         * TODO: Fix content-type errors - 
         * The script from “http://scythian.exp.sis.pitt.edu/Textbook/ir/sectionkey.php?name=iir-2.1&type=simple&callback=jQuery191012263205460860849_1657271613395&_=1657271613396” 
         * was loaded even though its MIME type (“text/html”) is not a valid JavaScript MIME type.
         * https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options
        */
        $.ajax({
            url: "http://scythian.exp.sis.pitt.edu/Textbook/ir/sectionkey.php?name=iir-2.1&type=simple",
            processData: false,
            dataType:'jsonp',
            contentType: false,
            crossDomain: true,
            success:function(res){
                console.log("wikipedia responses",res);
                callback_f(res.recommended_articles);
            },
            error: function(res, options, err){
                console.log("display wiki content call failed",res.status,err);
            }
        });
    }
    
    if(false) { topic = window.getSelection().toString()};
    if (false && (topic === "" || topic === undefined)) { topic = "pet_door"}

    if(false) {var wiki_url = `http://en.wikipedia.org/w/api.php?action=${request_data.action}&list=${request_data.list}&srsearch=${request_data.srsearch}&srlimit=${request_data.srlimit}&format=${request_data.format}`; }

    var wiki_url = "http://"+url_host+"/api/wiki_resources_content";
    
    var reader_info = new FormData();
    if (page_num.length != 0) reader_info.append('resource_id',`${resource_id}-${page_num}`);
    if (false) reader_info.append('resource_id',`${resource_id}`);

    $.ajax({
        url: wiki_url,
        type:"POST",
        data: reader_info,
        processData: false,
        contentType: false,
        crossDomain: true,
        success:function(res){
            if (false) {recommended_articles = res['query']['search'];}
            if (false) {console.log("wikipedia responses",recommended_articles);}
            callback_f(res,url_host,user_id,group_id);
        },
        error: function(res, options, err){
            console.log("display wiki content call failed",res.status,err);
        }
    });
    
    if (false) {displayReadWikiContent({},url_host,user_id,group_id);} // keep hidden for now.
    
    $(document).on('slideouttabopen', function(evt){
        console.log("tab open",evt.target.id);
        if (evt.target.id === 'read-wiki-links'){
            
            var read_wiki_url = `http://${url_host}/api/get_wiki_articles_read?user_id=${user_id}&group_id=${group_id}&resource_id=${resource_id}-${page_num}`;

            $.ajax({
                url: read_wiki_url,
                type:"GET",
                processData: false,
                contentType: false,
                crossDomain: true,
                success:function(res){
                    displayReadWikiContent(res,url_host,user_id,group_id);
                },
                error: function(res, options, err){
                    console.log("display wiki read content call failed",res.status,err);
                }
            });
        }
    });

    displayRatedWikiContent({},url_host,user_id,group_id);

    $(document).on('slideouttabopen', function(evt){
        console.log("tab open",evt.target.id);
        if (evt.target.id === 'rated-wiki-links'){
            
            var read_wiki_url = `http://${url_host}/api/get_wiki_articles_rated?user_id=${user_id}&group_id=${group_id}&resource_id=${resource_id}-${page_num}`;

            $.ajax({
                url: read_wiki_url,
                type:"GET",
                processData: false,
                contentType: false,
                crossDomain: true,
                success:function(res){
                    displayRatedWikiContent(res,url_host,user_id,group_id);
                },
                error: function(res, options, err){
                    console.log("display wiki rated content call failed",res.status,err);
                }
            });
        }
    });

}

function displayWikiContent(wiki_links,url_host,user_id,group_id){
    console.debug("baton passed to display Wiki content");
    console.log("inside display", wiki_links);

    wiki_links.sort(function(a, b) {
        return parseFloat(b.score) - parseFloat(a.score);
    });

    if($("#right-wiki-links").length == 0){
        $('#reader-div').append('<div id="right-wiki-links">' +
        '<a id="right-handle" class="handle ui-slideouttab-handle ui-slideouttab-handle-rounded">Wiki Links <i class="fas fa-book"></i></i></a>' +
        '      <div id="right-subpanel">' +
        '      <div id="wiki-link-list"></div>' +
        '      </div>' +
        '</div>');

        $('#right-wiki-links').tabSlideOut({
        tabLocation: 'right',
        offsetReverse: true, // position the panel from the bottom of the page, rather than the top
        offset: '100px',
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

    $('#wiki-link-list').empty();
    for(var slc_id=0; slc_id < wiki_links.length; slc_id++){
        var programming_activity_interface = $(
            '<a id="'+slc_id+'" href="#" class="slc">' + wiki_links[slc_id].concept 
            +'</a><br/>');
        $('#wiki-link-list').append(programming_activity_interface);
    }

    $(".slc").click(function(evt){
        evt.preventDefault();
        var wikimodal = document.getElementsByClassName("modal")[0];
        
        wikimodal.style.display="block";
        wikimodal.style.width = "50%";

        if(false) { html(wiki_links[this.id].concept);}

        $('.quiz-title').empty();
        $('.modal-header').height("3%");
        $('.modal-body').height("87%");
        $('.modal-footer').height("10%");
        
        $('.modal-body').empty();

        if(false){$(".modal-body").append(wiki_links[this.id].snippet).ready();}
        if(false) {$(".modal-body").append('<iframe src=https://en.wikipedia.org/w/index.php?curid=' + wiki_links[this.id].pageid+' height="100%" width="100%"></iframe>').ready();}
        var checked = ["","","",""];
        
        $(".modal-body").append(`<div>
            <div id="wikipage" style="overflow:auto;height:100%;width:100%;">
                <iframe src=${wiki_links[this.id].wikipage} height="5000px" width="100%" scrolling="no" frameborder="0"></iframe>
            </div>
            <span id="article-id" style="display:none;">${this.id}</span>
            <span id="concept" style="display:none;">${wiki_links[this.id].concept}</span>
        `).ready();
        
        $('.modal-footer').empty();

        $('.modal-footer').append(`
            <span id="wiki-feedback-prompt-text">Please, read this wikipedia article to rate it</span>
            <table id="feedback-table">
                <tr>
                    <td>Is this article Relevant?</td>
                    <td><span class="tooltip"><input type="radio" name="relevance" value="0" ${checked[0]}><i class="fas fa-thumbs-down"></i><span class="tooltiptext">No Relevance</span></span></td>
                    <td><span class="tooltip"><input type="radio" name="relevance" value="1" ${checked[1]}><img src="${star2}" alt="1 star" width="15"><span class="tooltiptext">Relevant to the course, not this section</span></span></td>
                    <td><span class="tooltip"><input type="radio" name="relevance" value="2" ${checked[2]}><img src="${star3}" alt="2 star" width="30"><span class="tooltiptext">Partly relevant to the section</span></span></td>
                    <td><span class="tooltip"><input type="radio" name="relevance" value="3" ${checked[3]}><img src="${star4}" alt="3 star" width="45"><span class="tooltiptext">Relevant to the section</span></span></td>
                </tr>
                <tr>
                    <td>Is this concept/article difficult to understand?</td>
                    <td><input type="radio" name="difficulty" value="0" ${checked[0]}><span>Easy <i class="fas fa-grin"></i></span></td>
                    <td><input type="radio" name="difficulty" value="1" ${checked[1]}>Medium <i class="fas fa-meh"></i></td>
                    <td><input type="radio" name="difficulty" value="2" ${checked[2]}>Hard <i class="fas fa-sad-cry"></i></td>
                </tr>
            </table>
        `)
        
        if (false){
            `<div width="100%">
                <span id="prompt-video-watching">
                    Please rate the concepts related covered by this article
                </span> <br />

                    <tr>
                        <td>Type</td>
                        <td><input type="radio" name="concept_type" value="0" ${checked[0]}>Prerequisite</td>
                        <td><input type="radio" name="concept_type" value="1" ${checked[1]}>Explained</td>
                    </tr>
                </table>
                <br />
                <textarea id="missing_concepts" class='textual' rows='1' placeholder="what concepts do you think are missing in this page?"/><br />
                <textarea id="rec_concepts" class='textual' rows='1' placeholder="what concepts would you like to see on this page?"/>
                
            </div>`
        }

        submitWikiFeedback(url_host,user_id,group_id,"open_wiki");
        
        $('input[name="relevance"]').change(function(event){
            console.log("relevance checked");
            submitWikiFeedback(url_host, user_id, group_id,"relevance_feedback");
        });

        $('input[name="difficulty"]').change(function(event){
            console.log("difficulty checked");
            submitWikiFeedback(url_host, user_id, group_id,"difficulty_feedback");
        });

        $("#wikipage").on('scroll',function(event){
            submitWikiFeedback(url_host,user_id,group_id,"scroll_event");
        });
    });

}


function displayReadWikiContent(read_wiki_links, url_host, user_id, group_id){
    

    var bcolor = randomColor({ luminosity:"dark", format:'rgb'});
    if($("#read-wiki-links").length == 0){
        $('#reader-div').append(`<div id="read-wiki-links">
            <a id="right-handle" class="handle ui-slideouttab-handle ui-slideouttab-handle-rounded" style="background-color:${bcolor};width:100px;">Read Wiki <i class="fas fa-book-open"></i></a>
            <div id="right-subpanel">
            <div id="read-wiki-link-list"></div>
            </div>
        </div>`);

        $('#read-wiki-links').tabSlideOut({
        tabLocation: 'right',
        offset: '200px',         // offset from bottom
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

    $('#read-wiki-link-list').empty();
    for(var slc_id=0; slc_id < read_wiki_links.length; slc_id++){
        var programming_activity_interface = $(
            '<span id="'+read_wiki_links[slc_id].article_id+'" class="slc">' + read_wiki_links[slc_id].concept 
            +'</span><br/>');
        $('#read-wiki-link-list').append(programming_activity_interface);
    }

}


function submitWikiFeedback(url_host,user_id,group_id,action_type){
    if (false) console.log("inside wiki feedback"); // enable for debugging
    var resource_id = last_page_read["resourceid"];
    var page_num = last_page_read["page"];

    var article_id = ($('#article-id').html() == undefined)? -1:$('#article-id').html();
    var wiki_rating = ($('input[name="relevance"]:checked').val() === undefined)? -1:$('input[name="relevance"]:checked').val();
    var currentDate = new Date();
    var date_time = currentDate.toISOString();
    var difficulty_rating = ($('input[name="difficulty"]:checked').val() === undefined)? -1:$('input[name="difficulty"]:checked').val();
    var concept_type = ($('input[name="concept_type"]:checked').val() === undefined)? -1: $('input[name="concept_type"]:checked').val();
    var action_type = action_type;
    var concept = ($('#concept').html() == undefined)? -1:$('#concept').html();
    var rec_concepts =  ($('textarea#rec_concepts').val() === undefined)? "":$('textarea#rec_concepts').val();
    var feedback_url = "http://"+url_host+"/api/wiki_content_feedback";

    var feedback_data = new FormData();

    feedback_data.append("article_id", article_id);
    feedback_data.append("user_id", user_id);
    feedback_data.append("group_id", group_id);
    feedback_data.append("date_added", date_time);
    feedback_data.append("resource_id",`${resource_id}-${page_num}`);
    feedback_data.append("concept",concept);
    feedback_data.append("relevance_rating",wiki_rating);
    feedback_data.append("difficulty_rating",difficulty_rating);
    feedback_data.append("concept_type",concept_type);
    feedback_data.append("action_type",action_type);
    feedback_data.append("rec_concepts",rec_concepts);

    if( action_type !== "scroll" ) {loaderOn();}

    $.ajax({
        url: feedback_url,
        type:"POST",
        data: feedback_data,
        processData: false,
        contentType: false,
        crossDomain: true,
        success:function(res){
            if(res["answer"] == 1) {}   // do nothing

        },
        error: function(res, options, err){
            console.log("error sending feedback, failed!",res.status,err);
            
        }
    });
    
    if( action_type !== "scroll") {loaderOff();}

}


function displayRatedWikiContent(rated_wiki_links,url_host, user_id, group_id){
    var bcolor = randomColor({ luminosity:"dark", format:'rgb'});
    if($("#rated-wiki-links").length == 0){
        $('#reader-div').append(`<div id="rated-wiki-links">
            <a id="right-handle" class="handle ui-slideouttab-handle ui-slideouttab-handle-rounded" style="background-color:${bcolor};width:100px;">Rated Wiki <i class="fas fa-book-open"></i></a>
            <div id="right-subpanel">
            <div id="rated-wiki-link-list"></div>
            </div>
        </div>`);

        $('#rated-wiki-links').tabSlideOut({
        tabLocation: 'right',
        offset: '320px',         // offset from bottom
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

    $('#rated-wiki-link-list').empty();
    
    for(var slc_id=0; slc_id < rated_wiki_links.length; slc_id++){
        var programming_activity_interface = $(
            '<span id="'+rated_wiki_links[slc_id].article_id+'" class="slc">' + rated_wiki_links[slc_id].concept 
            +'</span><br/>');
        $('#rated-wiki-link-list').append(programming_activity_interface);
    }
}




