//document.onload = (function(d3, saveAs, Blob, undefined){
  "use strict";

  // define graphcreator object
  var GraphCreator = function(svg, nodes, edges, userID, cmID, grpID, session){
    console.log(svg);
    var thisGraph = this;
        thisGraph.idct = 0;
    thisGraph.nodes = nodes || [];
    thisGraph.edges = edges || [];
    
    thisGraph.state = {
      selectedNode: null,
      selectedEdge: null,
      mouseDownNode: null,
      mouseDownLink: null,
      justDragged: false,
      justScaleTransGraph: false,
      lastKeyDown: -1,
      shiftNodeDrag: false,
      selectedText: null,
      linkType: 0, //Added by jbarriapineda | current type of link selected by the user ["solid":0,"dashed":1]
      nodeColor: "#c2c2c2", //Added by jbarriapineda | current node color
      strokeType: 0, //Added by jbarriapineda | current type of node stroke selected by the user ["solid":0,"dashed":1]
      conceptList: [],
      userID: userID,
      cmID: cmID
      
    };
    
    //dbGetConceptList(thisGraph.state.userID,thisGraph);

    // define arrow markers for graph links
    var defs = svg.append('svg:defs');
    defs.append('svg:marker')
      .attr('id', 'end-arrow')
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', "32")
      .attr('markerWidth', 2.5)
      .attr('markerHeight', 2.5)
      .attr('orient', 'auto')
      .append('svg:path')
      .attr('d', 'M0,-5L15,0L0,5');

    // define arrow markers for leading arrow
    defs.append('svg:marker')
      .attr('id', 'mark-end-arrow')
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 7)
      .attr('markerWidth', 2.5)
      .attr('markerHeight', 2.5)
      .attr('orient', 'auto')
      .append('svg:path')
      .attr('d', 'M0,-5L10,0L0,5');

    thisGraph.svg = svg;
    thisGraph.svgG = svg.append("g")
          .classed(thisGraph.consts.graphClass, true);
    var svgG = thisGraph.svgG;

    // displayed when dragging between nodes
    thisGraph.dragLine = svgG.append('svg:path')
          .attr('class', 'link dragline hidden')
          .attr('d', 'M0,0L0,0')
          .style('marker-end', 'url(#mark-end-arrow)');
          /*.style("stroke-dasharray", function(d){//added by jbarriapineda for showing the creation of solid or dashed links according to user selection
            var linkType = thisGraph.state.linkType;
            switch(linkType) {
              case 0:
                  return "none";
                  //break;
              case 1:
                  return ("5,5");
                  //break;
              default:
                  return "none";
            }
          });//end of code added by jbarriapineda*/

    // svg nodes and edges 
    thisGraph.paths = svgG.append("g").selectAll("g");
    thisGraph.circles = svgG.append("g").selectAll("g");

    thisGraph.drag = d3.behavior.drag()
          .origin(function(d){
            return {x: d.x, y: d.y};
          })
          .on("drag", function(args){
            thisGraph.state.justDragged = true;
            thisGraph.dragmove.call(thisGraph, args);
          })
          .on("dragend", function() {
            // todo check if edge-mode is selected
          });

    // listen for key events
    d3.select(window).on("keydown", function(){
      thisGraph.svgKeyDown.call(thisGraph);
    })
    .on("keyup", function(){
      thisGraph.svgKeyUp.call(thisGraph);
    });
    svg.on("mousedown", function(d){thisGraph.svgMouseDown.call(thisGraph, d);});
    svg.on("mouseup", function(d){thisGraph.svgMouseUp.call(thisGraph, d);});

    // listen for dragging
      //TODO: Zoom deactivated, activate it via parameters
    /*var dragSvg = d3.behavior.zoom()
          .on("zoom", function(){
            if (d3.event.sourceEvent.shiftKey){
              // TODO  the internal d3 state is still changing
              return false;
            } else{
              thisGraph.zoomed.call(thisGraph);
            }
            return true;
          })
          .on("zoomstart", function(){
            var ael = d3.select("#" + thisGraph.consts.activeEditId).node();
            if (ael){
              ael.blur();
            }
            if (!d3.event.sourceEvent.shiftKey) d3.select('body').style("cursor", "move");
          })
          .on("zoomend", function(){
            d3.select('body').style("cursor", "auto");
          });
    
    svg.call(dragSvg).on("dblclick.zoom", null);*/

    // listen for resize
    window.onresize = function(){thisGraph.updateWindow(svg,svg.node().parentNode);};

    // handle download data
    d3.select("#download-input").on("click", function(){
      var saveEdges = [];
      thisGraph.edges.forEach(function(val, i){
        saveEdges.push({source: val.source.id, target: val.target.id, type: val.type, title: val.title});
      });
      //console.log(thisGraph.nodes);//code added by jbarriapineda for testing
      console.log("download");
      var blob = new Blob([window.JSON.stringify({"nodes": thisGraph.nodes, "edges": saveEdges})], {type: "text/plain;charset=utf-8"});
      saveAs(blob, "conceptmap.json");
    });


    // handle uploaded data
    d3.select("#upload-input").on("click", function(){
      document.getElementById("hidden-file-upload").click();
    });
    d3.select("#hidden-file-upload").on("change", function(){
      if (window.File && window.FileReader && window.FileList && window.Blob) {
        var uploadFile = this.files[0];
        var filereader = new window.FileReader();
        
        filereader.onload = function(){
          var txtRes = filereader.result;
          // TODO better error handling
          try{
            var jsonObj = JSON.parse(txtRes);
            thisGraph.deleteGraph(true);
            thisGraph.nodes = jsonObj.nodes;
            thisGraph.setIdCt(jsonObj.nodes.length + 1);
            var newEdges = jsonObj.edges;
            newEdges.forEach(function(e, i){
              newEdges[i] = {source: thisGraph.nodes.filter(function(n){return n.id == e.source;})[0],
                             target: thisGraph.nodes.filter(function(n){return n.id == e.target;})[0],
                             type: e.type,
                             title: e.title};//code added by jbarriapineda to include type of links in uploaded json to draw the graph
            });
            thisGraph.edges = newEdges;
            thisGraph.updateGraph();
          }catch(err){
            window.alert("Error parsing uploaded file\nerror message: " + err.message);
            return;
          }
        };
        filereader.readAsText(uploadFile);
        
      } else {
        alert("Your browser won't let you save this graph -- try upgrading your browser to IE 10+ or Chrome or Firefox.");
      }

    });

    // handle delete graph
    d3.select("#delete-graph").on("click", function(){
      thisGraph.deleteGraph(false);
    });
    
    d3.select("#save-graph").on("click", function(){
        thisGraph.saveGraph(thisGraph.state.userID);
    });

    /*//code added by jbarriapineda
    // handle selection of solid links
    d3.select("#solid-link").on("click", function(){
      thisGraph.state.linkType = 0;
      thisGraph.dragLine.style("stroke-dasharray","none");

      d3.select("#dashed-link").classed("active",false);
      d3.select("#dashed-link").classed("inactive",true);

      d3.select("#solid-link").classed("inactive",false);
      d3.select("#solid-link").classed("active",true);
    });

    //handle selection of dashed links
    d3.select("#dashed-link").on("click", function(){
      thisGraph.state.linkType = 1;
      thisGraph.dragLine.style("stroke-dasharray",("12,5"));

      d3.select("#solid-link").classed("active",false);
      d3.select("#solid-link").classed("inactive",true);

      d3.select("#dashed-link").classed("inactive",false);
      d3.select("#dashed-link").classed("active",true);
    });

    d3.select("#solid-link").classed("active",true);
    d3.select("#dashed-link").classed("inactive",true);

    //handle selection of solid node stroke
    d3.select("#solid-stroke").on("click", function(){
      thisGraph.state.strokeType = 0;

      d3.select("#dashed-stroke").classed("active",false);
      d3.select("#dashed-stroke").classed("inactive",true);

      d3.select("#solid-stroke").classed("inactive",false);
      d3.select("#solid-stroke").classed("active",true);
    });

    //handle selection of dashed node stroke
    d3.select("#dashed-stroke").on("click", function(){
      thisGraph.state.strokeType = 1;

      d3.select("#solid-stroke").classed("active",false);
      d3.select("#solid-stroke").classed("inactive",true);

      d3.select("#dashed-stroke").classed("inactive",false);
      d3.select("#dashed-stroke").classed("active",true);
    });

    d3.select("#solid-stroke").classed("active",true);
    d3.select("#dashed-stroke").classed("inactive",true);  
    //end of code added by jbarriapineda */
  };

  GraphCreator.prototype.setIdCt = function(idct){
    this.idct = idct;
  };

  GraphCreator.prototype.consts =  {
    selectedClass: "selected",
    connectClass: "connect-node",
    circleGClass: "conceptG",
    graphClass: "graph",
    activeEditId: "active-editing",
    BACKSPACE_KEY: 8,
    DELETE_KEY: 46,
    ENTER_KEY: 13,
    nodeRadius: 25
  };

  /* PROTOTYPE FUNCTIONS */

  GraphCreator.prototype.dragmove = function(d) {
    var thisGraph = this;
    if (thisGraph.state.shiftNodeDrag){
      thisGraph.dragLine.attr('d', 'M' + d.x + ',' + d.y + 'L' + d3.mouse(thisGraph.svgG.node())[0] + ',' + d3.mouse(this.svgG.node())[1]);
    } else{
      d.x += d3.event.dx;
      d.y +=  d3.event.dy;
      thisGraph.updateGraph();
    }
  };

  GraphCreator.prototype.deleteGraph = function(skipPrompt){
    var thisGraph = this,
        doDelete = true;
    if (!skipPrompt){
      doDelete = window.confirm("Press OK to delete this graph");
    }
    if(doDelete){
      thisGraph.nodes = [];
      thisGraph.edges = [];
      thisGraph.updateGraph();
    }
  };
  
  //Function created by jbarriapineda to save concept maps associated with their creators
  GraphCreator.prototype.saveGraph = function(){
    var thisGraph = this,
        doDelete = true;
    var saveEdges = [];
      thisGraph.edges.forEach(function(val, i){
        saveEdges.push({source: val.source.id, target: val.target.id, type: val.type, title: val.title});
      });
      //console.log(thisGraph.nodes);//code added by jbarriapineda for testing
      var cmName = $("#graph-name").val();
      if (cmName!=""){
    	  var json = window.JSON.stringify({"nodes": thisGraph.nodes, "edges": saveEdges});
    	  dbSaveConceptMap(json,cmName,thisGraph.state.cmID,thisGraph.state.userID);
      }else{
    	  window.alert("You have to specify a name for your Concept Map before saving (or downloading) it");
      }
  };

  /* select all text in element: taken from http://stackoverflow.com/questions/6139107/programatically-select-text-in-a-contenteditable-html-element */
  GraphCreator.prototype.selectElementContents = function(el) {
    //Old version of the function but it was changed because it failed randomly and it didn't work at all in Firefox
    /*var range = document.createRange();
    range.selectNodeContents(el);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);*/
	  
    var range, selection;
    if (document.body.createTextRange) {
      range = document.body.createTextRange();
      range.moveToElementText(el);
      range.select();
    } else if (window.getSelection) {
      selection = window.getSelection();
      range = document.createRange();
      range.selectNodeContents(el);
      selection.removeAllRanges();
      selection.addRange(range);
    }
    
  };

  GraphCreator.prototype.selectLinkElementContents = function(el) {
    var range, selection;
    if (document.body.createTextRange) {
      range = document.body.createTextRange();
      range.moveToElementText(el);
      range.select();
    } else if (window.getSelection) {
      selection = window.getSelection();
      range = document.createRange();
      range.selectNodeContents(el);
      selection.removeAllRanges();
      selection.addRange(range);
    }
  };


  /* insert svg line breaks: taken from http://stackoverflow.com/questions/13241475/how-do-i-include-newlines-in-labels-in-d3-charts */
  GraphCreator.prototype.insertTitleLinebreaks = function (gEl, title) {
	title = title ? title : "Concept name"; 
    var words = title.split(/\s+/g),
        nwords = words.length;
    var el = gEl.append("text")
          .attr("text-anchor","middle")
          .attr("dy", "-" + (nwords-1)*7.5)
          .style("pointer-events","none");

    for (var i = 0; i < words.length; i++) {
      var tspan = el.append('tspan').text(words[i]);
      if (i > 0)
        tspan.attr('x', 0).attr('dy', '15');
    }
  };

  GraphCreator.prototype.insertTitleLinebreaksLink = function (gEl, linkInfo) {
    var title = linkInfo.title ? linkInfo.title : "Relationship name"; 
    gEl.selectAll("text").remove();
    var words = title.split(/\s+/g),
        nwords = words.length;
    var el = gEl.append("text")
          .attr("text-anchor","middle")
          .attr("class","shadow")
          .attr("dy", "-" + (nwords-1)*7.5)
          .style("pointer-events","none")
          .attr("transform", "translate(" + (linkInfo.source.x + linkInfo.target.x) / 2 + "," 
            + (linkInfo.source.y + linkInfo.target.y) / 2 + ")");
    for (var i = 0; i < words.length; i++) {
      var tspan = el.append('tspan').text(words[i]);
      if (i > 0)
        tspan.attr('x', 0).attr('dy', '15');
    }
  };
  
  // remove edges associated with a node
  GraphCreator.prototype.spliceLinksForNode = function(node) {
    var thisGraph = this,
        toSplice = thisGraph.edges.filter(function(l) {
      return (l.source === node || l.target === node);
    });
    toSplice.map(function(l) {
      thisGraph.edges.splice(thisGraph.edges.indexOf(l), 1);
    });
  };

  GraphCreator.prototype.replaceSelectEdge = function(d3Path, edgeData){
    var thisGraph = this;
    d3Path.classed(thisGraph.consts.selectedClass, true);
    if (thisGraph.state.selectedEdge){
      thisGraph.removeSelectFromEdge();
    }
    thisGraph.state.selectedEdge = edgeData;
  };

  GraphCreator.prototype.replaceSelectNode = function(d3Node, nodeData){
    var thisGraph = this;
    d3Node.classed(this.consts.selectedClass, true);
    if (thisGraph.state.selectedNode){
      thisGraph.removeSelectFromNode();
    }
    thisGraph.state.selectedNode = nodeData;
  };
  
  GraphCreator.prototype.removeSelectFromNode = function(){
    var thisGraph = this;
    thisGraph.circles.filter(function(cd){
      return cd.id === thisGraph.state.selectedNode.id;
    }).classed(thisGraph.consts.selectedClass, false);
    thisGraph.state.selectedNode = null;
  };

  GraphCreator.prototype.removeSelectFromEdge = function(){
    var thisGraph = this;
    thisGraph.paths.filter(function(cd){
      return cd === thisGraph.state.selectedEdge;
    })
      .selectAll("path")
      .classed(thisGraph.consts.selectedClass, false);
    thisGraph.state.selectedEdge = null;
  };

  GraphCreator.prototype.pathMouseDown = function(d3path, d){
    var thisGraph = this,
        state = thisGraph.state;
    d3.event.stopPropagation();
    state.mouseDownLink = d;

    if (state.selectedNode){
      thisGraph.removeSelectFromNode();
    }
    
    var prevEdge = state.selectedEdge;
    if (!prevEdge || prevEdge !== d){
      thisGraph.replaceSelectEdge(d3path, d);
      if (d3.event.shiftKey){
    	  d3.event.preventDefault();
          // shift-clicked link: edit text content
          var txtG = d3path.select(function(){return this.parentNode;});
          
          var d3txt = thisGraph.changeTextOfLink(txtG,d);
          var txtNode = d3txt.node();
          thisGraph.selectLinkElementContents(txtNode);
          window.setTimeout(function () { 
        	   txtNode.focus(); 
          }, 1);
      }
    }else{
        thisGraph.removeSelectFromEdge(); 
    }
  };

  // mousedown on node
  GraphCreator.prototype.circleMouseDown = function(d3node, d){
    var thisGraph = this,
        state = thisGraph.state;
    d3.event.stopPropagation();
    state.mouseDownNode = d;
    if (d3.event.shiftKey){
      state.shiftNodeDrag = d3.event.shiftKey;
      // reposition dragged directed edge
      thisGraph.dragLine.classed('hidden', false)
        .attr('d', 'M' + d.x + ',' + d.y + 'L' + d.x + ',' + d.y);
      return;
    }
  };

  /* place editable text on node in place of svg text */
  GraphCreator.prototype.changeTextOfNode = function(d3node, d){
    var thisGraph= this,
        consts = thisGraph.consts,
        htmlEl = d3node.node();

    var oldText = d3node.node().__data__.title;

    d3node.selectAll("text").remove();

    var svgPositions = thisGraph.svg.node().getBoundingClientRect();
    var svgX = svgPositions.left;
    var svgY = svgPositions.top;

    var nodeBCR = htmlEl.getBoundingClientRect(),
        curScale = nodeBCR.width/consts.nodeRadius,
        placePad  =  5*curScale,
        useHW = curScale > 1 ? nodeBCR.width*0.71 : consts.nodeRadius*1.42;

    var d3txt = thisGraph.svg.selectAll("foreignObject")
          .data([d])
          .enter()
          .append("foreignObject")
          .attr("x", nodeBCR.left - svgX + placePad )
          .attr("y", nodeBCR.top - svgY + placePad)
          .attr("height", 2*useHW)
          .attr("width", useHW)
          .append("xhtml:p")
          .attr("id", consts.activeEditId)
          .attr("contentEditable", "true")
          .text(d.title)
          .on("mousedown", function(d){
            d3.event.stopPropagation();
          })
          .on("keydown", function(d){
            d3.event.stopPropagation();
            if (d3.event.keyCode == consts.ENTER_KEY && !d3.event.shiftKey){
              this.blur();
            }
          })
          .on("blur", function(d){
            d.title = this.textContent.trim().replace(/\s+/g,' ');
            thisGraph.insertTitleLinebreaks(d3node, d.title);
            d3.select(this.parentElement).remove();
            var conceptName = d.title;
            /*if (!dbConceptExists(conceptName,thisGraph.state.conceptList)){
            	dbCreateConcept(d.title,"1",thisGraph);
            }*/

            //Log new concept or concept renaming
            var target = "";
            var action = "";
            if(oldText==="Concept name"){
              target = "";
              action = "new-concept";
            }else{
              target = oldText;
              action = "rename-concept";
            }
            thisGraph.logAction(action,target,conceptName);
          });
    /*var conceptList = Object.keys(thisGraph.state.conceptList).map(function(k){return thisGraph.state.conceptList[k]});
    $("#"+consts.activeEditId).autocomplete({
        source: conceptList
      });*/

    return d3txt;
  };

  /* place editable text on node in place of svg text */
  GraphCreator.prototype.changeTextOfLink = function(d3path, d){
    var thisGraph= this,
        consts = thisGraph.consts,
        state = thisGraph.state,
        htmlEl = d3path.node();

    var svgPositions = thisGraph.svg.node().getBoundingClientRect();
    var svgX = svgPositions.left;
    var svgY = svgPositions.top;

    var nodeBCR = htmlEl.getBoundingClientRect(),
        curScale = nodeBCR.width/consts.nodeRadius,
        placePad  =  5*curScale,
        useHW = curScale > 1 ? nodeBCR.width*0.71 : consts.nodeRadius*1.42;

    var oldLinkName = d3path.node().__data__.title;

    d3path.selectAll("text").remove();
    // replace with editable content text
    var d3txt = thisGraph.svg.selectAll("foreignObject")
          .data([d])
          .enter()
          .append("foreignObject")
          .attr("x", nodeBCR.left - svgX + placePad )
          .attr("y", nodeBCR.top - svgY + placePad)
          .attr("height", 2*useHW)
          .attr("width", useHW)
          .append("xhtml:p")
          .attr("id", consts.activeEditId)
          .attr("contentEditable", "true")
          .text(d.title)
          .on("mousedown", function(d){
            d3.event.stopPropagation();
          })
          .on("keydown", function(d){
            d3.event.stopPropagation();
            if (d3.event.keyCode == consts.ENTER_KEY && !d3.event.shiftKey){
              this.blur();
              //thisGraph.removeSelectFromEdge();
              //d3.select(this.parentElement).remove();
              
            }
          })
          .on("blur", function(d){
            d.title = this.textContent;
            thisGraph.insertTitleLinebreaksLink(d3path, d);
            d3.select(this.parentElement).remove();
            thisGraph.removeSelectFromEdge();

            //Log new link or link renaming
            var action = "";
            var target = "";
            var newLinkName = d.title;
            if (oldLinkName==="Relationship name"){
              target = d.source.title+"|"+d.target.title;
              action = "new-link";
            }else{
              target = d.source.title+">"+oldLinkName+">"+d.target.title;
              action = "rename-link";
            }

            thisGraph.logAction(action,target,newLinkName);
          });
    //To Do: autocomplete of relationships in the future
    /*$("#"+consts.activeEditId).autocomplete({
      source: thisGraph.state.conceptList
    });*/

    return d3txt;
  };

  // mouseup on nodes
  GraphCreator.prototype.circleMouseUp = function(d3node, d){
    var thisGraph = this,
        state = thisGraph.state,
        consts = thisGraph.consts;
    // reset the states
    state.shiftNodeDrag = false;    
    d3node.classed(consts.connectClass, false);
    
    var mouseDownNode = state.mouseDownNode;
    
    if (!mouseDownNode) return;

    thisGraph.dragLine.classed("hidden", true);

    if (mouseDownNode !== d){
      // we're in a different node: create new edge for mousedown edge and add to graph
      var newEdge = {source: mouseDownNode, target: d, type: thisGraph.state.linkType, title: "Relationship name"};// type: thisGraph.state.linkType added by jbarriapineda
      var filtRes = thisGraph.paths.filter(function(d){
        if (d.source === newEdge.target && d.target === newEdge.source){
          thisGraph.edges.splice(thisGraph.edges.indexOf(d), 1); // check if the inverted link exist and allow to add a new link between these two nodes but in the opposite direction
        }
        if (d.source === newEdge.source && d.target === newEdge.target && d.type != thisGraph.state.linkType){
          thisGraph.edges.splice(thisGraph.edges.indexOf(d), 1); // check if the link exist and allow to add a new link between these two nodes but of a different type
        }
        return d.source === newEdge.source && d.target === newEdge.target & d.type === thisGraph.state.linkType; //you can replace an existing link between two nodes in the same direction only if the link type selected by the user is different than the current link type
      });
      if (!filtRes[0].length){
        thisGraph.edges.push(newEdge);
        thisGraph.updateGraph();

        var txtG = d3.selectAll(".linkG").filter(function(dval){
          return (dval.source === d & dval.target === mouseDownNode) || (dval.source === mouseDownNode && dval.target === d );
          });

        var linkInfo = thisGraph.edges.filter(function(dval){
          return (dval.source === d & dval.target === mouseDownNode) || (dval.source === mouseDownNode && dval.target === d );
          });
        
        var d3txt = thisGraph.changeTextOfLink(txtG,linkInfo[0]);
        var txtNode = d3txt.node();
        thisGraph.selectLinkElementContents(txtNode);

        txtNode.focus();



      }
    } else{
      // we're in the same node
      if (state.justDragged) {
        // dragged, not clicked
        state.justDragged = false;
        var action="move-concept";
        var target=d.title;
        thisGraph.logAction(action,target,"");
      } else{
        // clicked, not dragged
        if (d3.event.shiftKey){
          // shift-clicked node: edit text content
          var d3txt = thisGraph.changeTextOfNode(d3node, d);
          var txtNode = d3txt.node();
          thisGraph.selectElementContents(txtNode);
          txtNode.focus();
        } else{
          if (state.selectedEdge){
            thisGraph.removeSelectFromEdge();
          }
          var prevNode = state.selectedNode;            
          
          if (!prevNode || prevNode.id !== d.id){
            thisGraph.replaceSelectNode(d3node, d);
          } else{
            thisGraph.removeSelectFromNode();
          }
        }
      }
    }
    state.mouseDownNode = null;
    return;
    
  }; // end of circles mouseup

  // mousedown on main svg
  GraphCreator.prototype.svgMouseDown = function(){
    this.state.graphMouseDown = true;
  };

  // mouseup on main svg
  GraphCreator.prototype.svgMouseUp = function(){
    var thisGraph = this,
        state = thisGraph.state;
    if (state.justScaleTransGraph) {
      // dragged not clicked
      state.justScaleTransGraph = false;
    } else if (state.graphMouseDown && d3.event.shiftKey){
      //Section for creating a new node
      // clicked not dragged from svg
      var xycoords = d3.mouse(thisGraph.svgG.node()),
          d = {id: thisGraph.idct++, title: "Concept name", x: xycoords[0], y: xycoords[1], color: thisGraph.state.nodeColor, stroke: thisGraph.state.strokeType};
      thisGraph.nodes.push(d);
      thisGraph.updateGraph();
      // make title of text immediently editable
      var d3txt = thisGraph.changeTextOfNode(thisGraph.circles.filter(function(dval){
        return dval.id === d.id;
      }), d),
          txtNode = d3txt.node();
      thisGraph.selectElementContents(txtNode);
      txtNode.focus();

    } else if (state.shiftNodeDrag){
      // dragged from node
      state.shiftNodeDrag = false;
      thisGraph.dragLine.classed("hidden", true);
    }
    state.graphMouseDown = false;
  };

  // keydown on main svg
  GraphCreator.prototype.svgKeyDown = function() {
    var thisGraph = this,
        state = thisGraph.state,
        consts = thisGraph.consts;
    // make sure repeated key presses don't register for each keydown
    if(state.lastKeyDown !== -1) return;

    state.lastKeyDown = d3.event.keyCode;
    var selectedNode = state.selectedNode,
        selectedEdge = state.selectedEdge;

    switch(d3.event.keyCode) {
    case consts.BACKSPACE_KEY:
    case consts.DELETE_KEY:
      d3.event.preventDefault();
      var action = "";
      var target = ""
      if (selectedNode){
        action = "delete-concept";
        target = "concept";
        thisGraph.nodes.splice(thisGraph.nodes.indexOf(selectedNode), 1);
        thisGraph.spliceLinksForNode(selectedNode);
        if(selectedNode){
          target = selectedNode.title;
        }
        state.selectedNode = null;
        thisGraph.updateGraph();
      } else if (selectedEdge){
        action = "delete-link";
        target = "link";
        thisGraph.edges.splice(thisGraph.edges.indexOf(selectedEdge), 1);
        if(selectedEdge){
          target = selectedEdge.source.title+"|"+selectedEdge.target.title;
        }
        state.selectedEdge = null;
        thisGraph.updateGraph();
      }

      //Log concept/link deletion
      thisGraph.logAction(action,target,"");

      break;
    }
  };

  GraphCreator.prototype.svgKeyUp = function() {
    this.state.lastKeyDown = -1;
  };

  // call to propagate changes to graph
  GraphCreator.prototype.updateGraph = function(){
    
    var thisGraph = this,
        consts = thisGraph.consts,
        state = thisGraph.state;
    
    thisGraph.paths = thisGraph.paths.data(thisGraph.edges, function(d){
      return String(d.source.id) + "+" + String(d.target.id) + "+" + String(d.type);//+ String(d.type) added by jbarriapineda to allow same direction links be treated as different if they have different types
    });
    
    var paths = thisGraph.paths;

    // update existing paths & text
    paths.select("path").style('marker-end', 'url(#end-arrow)')
      .classed(consts.selectedClass, function(d){
        return d === state.selectedEdge;
      })
      .attr("d", function(d){
        return "M" + d.source.x + "," + d.source.y + "L" + d.target.x + "," + d.target.y;
      });

    paths.selectAll("text").attr("transform", function(d) {
          return "translate(" + (d.source.x + d.target.x) / 2 + "," 
          + (d.source.y + d.target.y) / 2 + ")"; 
      });

    // add new paths & text
    var newpaths = paths.enter()
      .append("g")
      .attr("class","linkG");

    newpaths.append("path")
      .style('marker-end','url(#end-arrow)')
      .classed("link", true)
      .attr("d", function(d){
          return "M" + d.source.x + "," + d.source.y + "L" + d.target.x + "," + d.target.y;
      })
      .style("stroke-dasharray", function(d){//added by jbarriapineda for drawing solid or dashed links
        var linkType = d.type;
        switch(linkType) {
          case 0:
              return "none";
              //break;
          case 1:
              return ("12,5");
              //break;
          default:
              return "none";
        }
      })
//end of code added by jbarriapineda
      .on("mousedown", function(d){
        thisGraph.pathMouseDown.call(thisGraph, d3.select(this), d);
        }
      )
      .on("mouseup", function(d){
        state.mouseDownLink = null;
      });

    //Code added by jbarriapineda
    //var linkLabels = d3.selectAll(".g-link")
    newpaths.each(function(d){
      thisGraph.insertTitleLinebreaksLink(d3.select(this),d);
    });
    //end of code added by jbarriapineda
    

    // remove old links
    paths.exit().remove();
    
    // update existing nodes
    thisGraph.circles = thisGraph.circles.data(thisGraph.nodes, function(d){ return d.id;});
    thisGraph.circles.attr("transform", function(d){return "translate(" + d.x + "," + d.y + ")";});

    // add new nodes
    var newGs= thisGraph.circles.enter()
          .append("g");

    newGs.classed(consts.circleGClass, true)
      .attr("transform", function(d){return "translate(" + d.x + "," + d.y + ")";})
      .on("mouseover", function(d){       
          d3.select(this).classed(consts.connectClass, true);
      })
      .on("mouseout", function(d){
        d3.select(this).classed(consts.connectClass, false);
      })
      .on("mousedown", function(d){
        thisGraph.circleMouseDown.call(thisGraph, d3.select(this), d);
      })
      .on("mouseup", function(d){
        thisGraph.circleMouseUp.call(thisGraph, d3.select(this), d);
      })
      .call(thisGraph.drag);

    newGs.append("circle")
      .attr("r", String(consts.nodeRadius))
      //Code added by jbarriapineda to include node coloring
      // .style("fill",function(d){
      //   if (d.color){
      //     return d.color;
      //   }else{
      //     return thisGraph.state.nodeColor;
      //   }
      // })
      //Code added by jbarriapineda to include changes in nodes' stroke
      .style("stroke-dasharray",function(d){
        var strokeType = d.stroke;
        if (d.stroke==null){
          strokeType = thisGraph.state.strokeType; 
        }
        switch(strokeType) {
          case 0:
            return "none";
            //break;
          case 1:
            return ("12,5");
            //break;
          default:
            return "none";
        }
      });
      //end of code added by jbarriapineda

    newGs.each(function(d){
      thisGraph.insertTitleLinebreaks(d3.select(this), d.title);
    });

    // remove old nodes
    thisGraph.circles.exit().remove();
  };

  //TODO: Zoom deactivated, activate it via parameters
  /*GraphCreator.prototype.zoomed = function(){
    this.state.justScaleTransGraph = true;
    d3.select("." + this.consts.graphClass)
      .attr("transform", "translate(" + d3.event.translate + ") scale(" + d3.event.scale + ")"); 
  };*/

  GraphCreator.prototype.updateWindow = function(svg,svg_parent){
    /*var docEl = document.documentElement,
          bodyEl = document.getElementsByTagName('body')[0];
    var x = window.innerWidth || docEl.clientWidth || bodyEl.clientWidth;
    var y = window.innerHeight|| docEl.clientHeight|| bodyEl.clientHeight;*/
    var x = $(svg_parent).innerWidth();
    var y = $(svg_parent).innerHeight();
    svg.attr("width", x).attr("height", y);
  };

  // Log modifications done on the concept map
  GraphCreator.prototype.logAction = function(action, target, value){
    var thisGraph = this;
    //Update the db of saved concept maps
    var saveEdges = [];
    thisGraph.edges.forEach(function(val, i){
      saveEdges.push({source: val.source.id, target: val.target.id, type: val.type, title: val.title});
    });
    var concept_map = {"nodes": thisGraph.nodes, "edges": saveEdges};
    var action_json = {"type": action, "target": target, "val": value};
    //Register a log of concept mapping activity
    $.post( "http://localhost:8000/api/knowledgevis/concept_map_log", JSON.stringify({ user: this.state.userID, group: "IRSpring2018", section: this.state.cmID, session: "test", conceptMap: concept_map, action: action_json}) );

  }

  function drawNewConceptMap(svg, userID){
      var nodes = [{title: "Concept name", id: 0, x: xLoc, y: yLoc, color: "#c2c2c2", stroke:0},//color added by Jjbarriapineda
                   {title: "Concept name", id: 1, x: xLoc, y: yLoc + 200, color: "#c2c2c2", stroke:0}];//color added by jbarriapineda
      var edges = [{source: nodes[1], target: nodes[0], type: 0, title:"Relationship name"}];//type and title added by jbarriapineda
      var graph = new GraphCreator(svg, nodes, edges, userID, null);
      graph.setIdCt(2);
      graph.updateGraph();

      $('#colorpicker').change(function(){
            var nodeColor = $(this).find("option:selected").attr('value');
            graph.state.nodeColor=nodeColor;
      });
}
  
  function drawExistentConceptMap(svg,cmID,userID){
		var dataString = "svc=getConceptMap&cmID="+cmID+"&userID="+userID;
		$.ajax({
	        type: "POST",
	        url: "ConceptManager",
	        data: dataString,
	        dataType: "json",
	       
	        //if received a response from the server
	        success: function( data, textStatus, jqXHR) {
	        	if(data.success){
	        		var jsonCM = JSON.parse(data.conceptMap);
	        		var nodes = jsonCM.nodes;
	        		var edges = jsonCM.edges;
	        		edges.forEach(function(e, i){
	                    edges[i] = {source: nodes.filter(function(n){return n.id == e.source;})[0],
	                                   target: nodes.filter(function(n){return n.id == e.target;})[0],
	                                   type: e.type,
	                                   title: e.title};//code added by jbarriapineda to include type of links in uploaded json to draw the graph
	                  });
	        		var graph = new GraphCreator(svg, nodes, edges, userID, cmID);
	        		graph.setIdCt(2);
	        		graph.updateGraph();
	        		$('#colorpicker').change(function(){
	        	        var nodeColor = $(this).find("option:selected").attr('value');
	        	        graph.state.nodeColor=nodeColor;
	        	    });
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

  /**** MAIN ****/

  // warn the user when leaving
  /*window.onbeforeunload = function(){
    return "Make sure to save your graph locally before leaving :-)";
  };*/

  /*var docEl = document.documentElement,
      bodyEl = document.getElementsByTagName('body')[0];*/
  
  /*var width = $("#concept-map-div").innerWidth(),//window.innerWidth || docEl.clientWidth || bodyEl.clientWidth,
      height =  $("#concept-map-div").innerHeight();//window.innerHeight|| docEl.clientHeight|| bodyEl.clientHeight;*/

  /*var xLoc = width/2 - 25,
      yLoc = 100;*/
  
  //var graph = null;
  // initial node data
  // If the user wants to edit an existant concept map 

  /** MAIN SVG **/
  /* var concept_map_svg = d3.select("#concept-map-div").append("svg")
         .attr("width", width)
         .attr("height", height);*/
 
  /*var graph = new GraphCreator(svg, nodes, edges);
  graph.setIdCt(2);
  graph.updateGraph();*/

  //Code added by jbarriapineda to include a colorpicker in the graph creator toolbox
  //$('select[name="colorpicker-picker-longlist"]').simplecolorpicker({picker: true, theme: 'glyphicons'});
  

//})(window.d3, window.saveAs, window.Blob);
