import org.gephi.project.api as project
from org.openide.util import Lookup
import org.gephi.graph.api as graph
import org.gephi.preview.api as preview
import org.gephi.io.importer.api as importer
import org.gephi.filters.api as filters
import org.gephi.appearance.api as appearance
from java.io import File
import org.gephi.io.processor.plugin as processor
import org.gephi.filters.plugin.graph.DegreeRangeBuilder as degree_range_builder
import sys
import org.gephi.layout.plugin.force as force
import org.gephi.statistics.plugin as statistics
#import org.gephi.io.importer.api.EdgeDirectionDefault
from glob import glob


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


def show_node_color(f):
    lookup = Lookup.getDefault().lookup
    pc =ProjectController(lookup)
    pc.newProject()
    workspace = pc.getCurrentWorkspace()
    graph_model = GraphController(lookup).getGraphModel()
    print(graph_model)
    preview_model = PreviewController(lookup)
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
        print(File(f).length())
        container = import_controller.importFile(File(f))
        print(container)
        container.getLoader().setEdgeDefault(importer.EdgeDirectionDefault.DIRECTED)
    except Exception,err:
        print(err)
    import_controller.process(container,processor.DefaultProcessor(),workspace)
    graph = graph_model.getDirectedGraph()
    #print(f)
    #print(graph.getNodeCount())
    #print(graph.getEdgeCount())
    msg="f={} node_cnt={} edged_count={}".format(f.encode('utf-8'),graph.getNodeCount(),graph.getEdgeCount())
    print(msg)
    dkt={}
    for node in graph.getNodes():
        #print(dir(node))
        #print(node.label)
        label=node.label
        color=node.color
        cat=node.getAttribute("modularity")
        r=color.red
        g=color.green
        b=color.blue
        msg="cat={} r={} g={} b={}".format(cat.encode("utf-8"),r,g,b)
        #print(msg)
        dkt[cat]=color
    return dkt

def show_files():
    for f in glob("resources/law.gexf"):
        dkt=show_node_color(f)
        print(len(dkt))
        for k in dkt:
            v=dkt[k]
            r=v.red
            g=v.green
            b=v.blue
            msg="k={} r={} g={} b={}".format(k.encode("utf-8"),r,g,b)
            print(msg)
def main():
    show_files()

if __name__=='__main__':main()
