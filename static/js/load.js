function genSig(gexf,divelm){
    var sigInst = sigma.init(document.getElementById(divelm)).drawingProperties({
	defaultLabelColor: '#fff',
	defaultLabelSize: 14,
	defaultLabelBGColor: '#fff',
	defaultLabelHoverColor: '#000',
	labelThreshold: 12,
	defaultEdgeType: 'curve'
    }).graphProperties({
	minNodeSize: 0.5,
	maxNodeSize: 20,
	minEdgeSize: 1,
	maxEdgeSize: 1,
	sideMargin: 50
    }).mouseProperties({
	maxRatio: 32
    });
    sigInst.parseGexf(gexf);
    return sigInst;
}
function gexfload(gexfpath,catname){
    sigma.parsers.gexf(
	'/static/gexf/憲法.gexf',
	{ // Here is the ID of the DOM element that
	    // will contain the graph:
	    container: 'sigma-container-憲法'
	},
	function(s) {
	    // This function will be executed when the
	    // graph is displayed, with "s" the related
	    // sigma instance.
	    console.log(s);
	    //s.graph.nodes().forEach(function(node, i, a) {
	    // On a circle:
	    //node.x = Math.cos(Math.PI * 2 * i / a.length);
	    //node.y = Math.sin(Math.PI * 2 * i / a.length);
	    // Default size:
	    //node.size = 1;
	    //});
	    //s.refresh();
	}
    );
}

/*function init() {
    // Instanciate sigma.js and customize rendering :
     
    // Parse a GEXF encoded file to fill the graph
    // (requires "sigma.parseGexf.js" to be included)
    //sigInst.parseGexf('/static/keiji.gexf');
    //sigInst.parseGexf('/static/arctic.gexf');
    var sigInsts = new Array();
    sigInsts.push(genSig('/static/憲法.gexf','sigma-container'));

    sigInsts.forEach(function(v){
	v.draw();
    });
}
*/
/*
function init(){
}
*/  
/*
if (document.addEventListener) {
    document.addEventListener("DOMContentLoaded", init, false);
} else {
    window.onload = init;
}
*/
