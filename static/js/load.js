
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
function init() {
    // Instanciate sigma.js and customize rendering :
     
    // Parse a GEXF encoded file to fill the graph
    // (requires "sigma.parseGexf.js" to be included)
    //sigInst.parseGexf('/static/keiji.gexf');
    //sigInst.parseGexf('/static/arctic.gexf');
    var sigInsts = new Array();
    sigInsts.push(genSig('/static/法令.gexf','sigma-example01'));
    sigInsts.push(genSig('/static/刑事.gexf','sigma-example02'));
    sigInsts.push(genSig('/static/民事.gexf','sigma-example03'));
    sigInsts.push(genSig('/static/憲法.gexf','sigma-example04'));
    sigInsts.push(genSig('/static/教育.gexf','sigma-example05'));
    sigInsts.push(genSig('/static/地方自治.gexf','sigma-example06'));
    sigInsts.push(genSig('/static/財務通則.gexf','sigma-example07'));

    sigInsts.forEach(function(v){
	v.draw();
    });
}
     
if (document.addEventListener) {
    document.addEventListener("DOMContentLoaded", init, false);
} else {
    window.onload = init;
}
     

