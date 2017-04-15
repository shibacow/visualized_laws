import org.gephi.project.api as project
from org.openide.util import Lookup
import org.gephi.graph.api as graph
import org.gephi.preview.api as preview
import org.gephi.io.importer.api as importer
import org.gephi.io.exporter.api as exporter
import org.gephi.filters.api as filters
import org.gephi.appearance.api as appearance
import org.gephi.appearance.plugin as appearance_plugin
from java.io import File
from java.awt import Color
import org.gephi.io.processor.plugin as processor
import org.gephi.filters.plugin.graph.DegreeRangeBuilder as degree_range_builder
import sys
import org.gephi.layout.plugin.force as force
import org.gephi.statistics.plugin as statistics
import org.gephi.preview.types as preview_types


def ProjectController(lookup):
    return lookup(project.ProjectController)
def GraphController(lookup):
    return lookup(graph.GraphController)
def PreviewController(lookup):
    return lookup(preview.PreviewController)
def ImportController(lookup):
    return lookup(importer.ImportController)
def FilterController(lookup):
    return lookup(filters.FilterController)
def AppearanceController(lookup):
    return lookup(appearance.AppearanceController)
def ExportController(lookup):
    return lookup(exporter.ExportController)

def headless():
    lookup = Lookup.getDefault().lookup
    pc =ProjectController(lookup)
    pc.newProject()
    workspace = pc.getCurrentWorkspace()
    graph_model = GraphController(lookup).getGraphModel()
    print(graph_model)
    preview_model = PreviewController(lookup).getModel()
    print(preview_model)
    import_controller = ImportController(lookup)
    print(import_controller)
    filter_controller = FilterController(lookup)
    print(filter_controller)
    appearance_controller = AppearanceController(lookup)
    print(appearance_controller)
    appearance_model = appearance_controller.getModel()
    print(appearance_model)
    try:
        container = import_controller.importFile(File('resources/polblogs.gml'))
        container.getLoader().setEdgeDefault(importer.EdgeDirectionDefault.DIRECTED)
    except Exception,err:
        print(err)
    import_controller.process(container,processor.DefaultProcessor(),workspace)
    graph = graph_model.getDirectedGraph()
    print(graph.getNodeCount())
    print(graph.getEdgeCount())
    degreefilter=degree_range_builder.DegreeRangeFilter()
    degreefilter.init(graph)
    degreefilter.setRange(filters.Range(30,sys.maxint))
    query = FilterController(lookup).createQuery(degreefilter)
    view = FilterController(lookup).filter(query)
    graph_model.setVisibleView(view)
    graph_visible = graph_model.getUndirectedGraphVisible()
    print(graph_visible.getNodeCount())
    print(graph_visible.getEdgeCount())
    layout = force.yifanHu.YifanHuLayout(None,force.StepDisplacement(1))
    layout.setGraphModel(graph_model)
    layout.resetPropertiesValues()
    layout.setOptimalDistance(200.0)
    layout.initAlgo()
    for i in  range(100):
        v=layout.getAverageEdgeLength(graph)
        print("i={} ratio={}".format(i,v))
        if layout.canAlgo():
            layout.goAlgo()
        else:
            break
    layout.endAlgo()

    distance = statistics.GraphDistance()
    distance.setDirected(True)
    distance.execute(graph_model)

    #//Rank color by Degree
    #System.out.println("start color by Degree");
    print("start color by degree")
    degreeRanking = appearance_model.getNodeFunction(graph, appearance_model.GraphFunction.NODE_DEGREE, appearance_plugin.RankingElementColorTransformer)
    degreeTransformer = degreeRanking.getTransformer()
    degreeTransformer.setColors([Color(0xFEF0D9),Color(0xB30000)])
    degreeTransformer.setColorPositions([0.0,1.0])
    AppearanceController(lookup).transform(degreeRanking)
    print("end color degree")


    #//Rank size by centrality
    print("start size by centrallity")
    centralityColumn = graph_model.getNodeTable().getColumn(statistics.GraphDistance.BETWEENNESS)
    centralityRanking  = appearance_model.getNodeFunction(graph,centralityColumn,appearance_plugin.RankingNodeSizeTransformer)
    centralityTransformer = centralityRanking.getTransformer()
    centralityTransformer.setMinSize(3)
    centralityTransformer.setMaxSize(10)
    AppearanceController(lookup).transform(centralityRanking)
    print("end size by centrality")

    print("start to set preview")
    preview_model.getProperties().putValue(preview.PreviewProperty.SHOW_NODE_LABELS,True)
    preview_model.getProperties().putValue(preview.PreviewProperty.EDGE_COLOR,preview_types.EdgeColor(Color.GRAY))
    preview_model.getProperties().putValue(preview.PreviewProperty.EDGE_THICKNESS,1.0)
    preview_model.getProperties().putValue(preview.PreviewProperty.NODE_LABEL_FONT,
                                           preview_model.getProperties().getFontValue(preview.PreviewProperty.NODE_LABEL_FONT).deriveFont(8))
    print("end to set preview")
    ec = ExportController(lookup)
    try:
        ec.exportFile(File("resources/headless_simple.pdf"))
    except Exception,err:
        print(err)
def main():
    headless()
if __name__=='__main__':main()
