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

function onclickednode(event){
    console.log(event.data.node.label);
}

function gexfload(gexfpath,catname){
    // Instantiate sigma:
    var container='sigma-container-'+catname;
    s = new sigma({
        renderer: {
            container: document.getElementById(container),
            type: 'canvas'
        },
        settings: {
            edgeLabelSize: 'proportional',
            //minArrowSize: '7',
            defaultEdgeType: 'curve',
            minEdgeSize: 0.1,
            maxEdgeSize: 0.1,
        }
    });

    sigma.parsers.gexf(
        gexfpath,
        s,
        function(s){
            s.refresh();
        }
    );
    s.bind('clickNode',onclickednode);
}

