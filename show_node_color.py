import org.gephi.project.api as project
from org.openide.util import Lookup
import org.gephi.graph.api as graph
import org.gephi.preview.api as preview
import org.gephi.io.importer.api as importer
import org.gephi.io.exporter.api as exporter
import org.gephi.filters.api as filters
import org.gephi.appearance.api as appearance
from java.io import File
from java.awt import Color
import org.gephi.io.processor.plugin as processor
import org.gephi.filters.plugin.graph.DegreeRangeBuilder as degree_range_builder
import sys
import org.gephi.layout.plugin.force as force
import org.gephi.statistics.plugin as statistics
import org.gephi.io.importer.api.EdgeDirectionDefault
import os
from glob import glob
import logging
FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG,format=FORMAT)
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

class GexfPdfer(object):
    def __initialize(self):
        lookup = Lookup.getDefault().lookup
        self.lookup=lookup
        pc =ProjectController(lookup)
        pc.newProject()
        workspace = pc.getCurrentWorkspace()
        self.workspace=workspace
        graph_model = GraphController(lookup).getGraphModel()
        logging.info(graph_model)
        self.graph_model=graph_model
        self.preview_model = PreviewController(lookup).getModel()
        logging.info(self.preview_model)
        import_controller = ImportController(lookup)
        logging.info(import_controller)
        self.import_controller=import_controller
        filter_controller = FilterController(lookup)
        logging.info(filter_controller)
        appearance_controller = AppearanceController(lookup)
        logging.info(appearance_controller)
        appearance_model = appearance_controller.getModel()
        logging.info(appearance_model)
    def readfile(self,f):
        try:
            logging.info(File(f).length())
            container = self.import_controller.importFile(File(f))
            logging.info(container)
            container.getLoader().setEdgeDefault(importer.EdgeDirectionDefault.DIRECTED)
        except Exception,err:
            logging.info(err)
        self.import_controller.process(container,processor.DefaultProcessor(),self.workspace)
        graph = self.graph_model.getDirectedGraph()
        logging.info(graph)
    
    def nodeshow(self):
        #print(f)
        #print(graph.getNodeCount())
        #print(graph.getEdgeCount())
        #msg="f={} node_cnt={} edged_count={}".format(f.encode('utf-8'),graph.getNodeCount(),graph.getEdgeCount())
        #print(msg)
        #dkt={}
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
    def export(self,i):
        print("start to set preview")
        #preview_model=self.preview_model
        #v=self.preview_model.getProperties().getValue(preview.PreviewProperty.NODE_BORDER_WIDTH)
        #print("v={}".format(v))
        self.preview_model.getProperties().putValue(preview.PreviewProperty.NODE_BORDER_WIDTH,0.0)
        self.preview_model.getProperties().putValue(preview.PreviewProperty.SHOW_NODE_LABELS,True)
        self.preview_model.getProperties().putValue(preview.PreviewProperty.EDGE_COLOR,preview_types.EdgeColor(preview_types.EdgeColor.Mode.MIXED))
        self.preview_model.getProperties().putValue(preview.PreviewProperty.EDGE_THICKNESS,1.0)
        self.preview_model.getProperties().putValue(preview.PreviewProperty.NODE_LABEL_FONT,
                                               self.preview_model.getProperties().getFontValue(preview.PreviewProperty.NODE_LABEL_FONT).deriveFont(8))
        print("end to set preview")
        ec = ExportController(self.lookup)
        try:
            fname="out/cat_"+self.basef+".pdf"
            ec.exportFile(File(fname))
        except Exception,err:
            print(err)

    def __init__(self,f):
        df=os.path.basename(f)
        (basef,ext)=os.path.splitext(df)
        self.basef=basef
        self.__initialize()

def show_files():
    for i,f in enumerate(glob("gexf/*.gexf")):
        gx=GexfPdfer(f)
        gx.readfile(f)
        gx.export(i)
def main():
    show_files()
if __name__=='__main__':main()
