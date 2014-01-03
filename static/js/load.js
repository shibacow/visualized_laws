function init() {
    // Instanciate sigma.js and customize rendering :
    var sigInst = sigma.init(document.getElementById('sigma-example')).drawingProperties({
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
     
    // Parse a GEXF encoded file to fill the graph
    // (requires "sigma.parseGexf.js" to be included)
    //sigInst.parseGexf('/static/keiji.gexf');
    //sigInst.parseGexf('/static/arctic.gexf');
    sigInst.parseGexf('/static/法令.gexf');

    console.log(sigInst);
    // Draw the graph :
    sigInst.draw();
    console.log('fuga');
    
}
     
if (document.addEventListener) {
    document.addEventListener("DOMContentLoaded", init, false);
} else {
    window.onload = init;
}
     

