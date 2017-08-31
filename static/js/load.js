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
        gexfpath,
        { // Here is the ID of the DOM element that
            // will contain the graph:
            container: 'sigma-container-'+catname,
            settings: {
                defaultEdgeType: 'curve',
            }
        },
        function(s) {
            s.graph.edges().forEach(function(edge){ 
                edge.type = 'curve';
            });
            s.refresh();     
        }
    );
}

