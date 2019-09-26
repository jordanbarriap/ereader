function dbConceptExists(concept , conceptList){
	/*var conceptExists = conceptList.indexOf(concept);
	if (conceptExists>0) return true;
	else return false;*/
	var filteredConcept=concept.toLowerCase();
	filteredConcept=filteredConcept.replace(/\s\s+/g, " ");
	filteredConcept=filteredConcept.replace(" ","-");
	var conceptExists = conceptList[filteredConcept];
	if (conceptExists != undefined){
		return true;
	}else{
		return false;
	}
}

function dbGetConceptList(userID , thisGraph){
	dataString = "svc=getConceptList&userID="+userID;
	var conceptList = [];
	$.ajax({
        type: "POST",
        url: "ConceptManager",
        data: dataString,
        dataType: "json",
       
        //if received a response from the server
        success: function( data, textStatus, jqXHR) {
            //our country code was correct so we have some information to display
            
        	if(data.success){
        		console.log(data.conceptList);
        		conceptList = data.conceptList;
        		thisGraph.state.conceptList=conceptList;
             } 
             //display error message
             else {
                 $("#ajaxResponse").html("<div><b>Something bad happened!</b></div>");
             }
        },
       
        //If there was no response from the server
        error: function(jqXHR, textStatus, errorThrown){
             console.log("Something really bad happened " + textStatus);
              $("#ajaxResponse").html(jqXHR.responseText);
        },
       
        //capture the request before it was sent to server
        beforeSend: function(jqXHR, settings){
            //adding some Dummy data to the request
            settings.data += "&dummyData=whatever";
            //disable the button until we get the response
            //$('#sendAnswers').attr("disabled", true);
        },
       
        //this is called after the response or error functions are finished
        //so that we can take some action
        complete: function(jqXHR, textStatus){
            //enable the button 
            //$('#sendAnswers').attr("disabled", false);
        }
    }); 
}

function dbCreateConcept(conceptName , userID , thisGraph){
	dataString = "svc=createConcept&conceptName="+conceptName+"&userID="+userID;
	$.ajax({
        type: "POST",
        url: "ConceptManager",
        data: dataString,
        dataType: "json",
       
        //if received a response from the server
        success: function( data, textStatus, jqXHR) {
            //our country code was correct so we have some information to display
            console.log(data);
        	if(data.success){
        		console.log(conceptName+" was created in DB");
        		var conceptID = data.conceptID;
        		var concept   = data.concept; 
        		thisGraph.state.conceptList[conceptID]=concept;
        		console.log(thisGraph.state.conceptList);
             } 
             //display error message
             else {
                 $("#ajaxResponse").html("<div><b>Something bad happened!</b></div>");
             }
        },
       
        //If there was no response from the server
        error: function(jqXHR, textStatus, errorThrown){
             console.log("Something really bad happened " + textStatus);
              $("#ajaxResponse").html(jqXHR.responseText);
        },
       
        //capture the request before it was sent to server
        beforeSend: function(jqXHR, settings){
            //adding some Dummy data to the request
            settings.data += "&dummyData=whatever";
            //disable the button until we get the response
            //$('#sendAnswers').attr("disabled", true);
        },
       
        //this is called after the response or error functions are finished
        //so that we can take some action
        complete: function(jqXHR, textStatus){
            //enable the button 
            //$('#sendAnswers').attr("disabled", false);
        }

    });        
}

function dbSaveConceptMap(json, name, cmID, userID){
	dataString = "svc=saveConceptMap&json="+json+"&cmID="+cmID+"&userID="+userID+"&name="+name;
	$.ajax({
        type: "POST",
        url: "ConceptManager",
        data: dataString,
        dataType: "json",
       
        //if received a response from the server
        success: function( data, textStatus, jqXHR) {
            //our country code was correct so we have some information to display
            console.log(data);
        	if(data.success){
        		if (cmID){
        			window.alert("The changes in your Concept Map were saved correctly");
        		}else{
        			window.alert("Your Concept Map was saved correctly")
        		}
             } 
             //display error message
             else {
                 $("#ajaxResponse").html("<div><b>Something bad happened!</b></div>");
             }
        },
       
        //If there was no response from the server
        error: function(jqXHR, textStatus, errorThrown){
             console.log("Something really bad happened " + textStatus);
              $("#ajaxResponse").html(jqXHR.responseText);
        },
       
        //capture the request before it was sent to server
        beforeSend: function(jqXHR, settings){
            //adding some Dummy data to the request
            settings.data += "&dummyData=whatever";
            //disable the button until we get the response
            //$('#sendAnswers').attr("disabled", true);
        },
       
        //this is called after the response or error functions are finished
        //so that we can take some action
        complete: function(jqXHR, textStatus){
            //enable the button 
            //$('#sendAnswers').attr("disabled", false);
        }

    });        
}
