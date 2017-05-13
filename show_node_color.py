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
from java.awt import GraphicsEnvironment
from java.awt import Font
from com.itextpdf.text import FontFactory
import ruamel.yaml
from pprint import pprint

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
        ge = GraphicsEnvironment.getLocalGraphicsEnvironment()
        for f in ge.getAllFonts():
            n=f.getName()
            if n=="Yu Gothic UI Regular":
                #print(dir(f))
                self.font=f
                #self.font.size=20
            #print("font={}".format(str(f)))
        #    print(dir(f))
        #for fm in ge.getAvailableFontFamilyNames():
            #print("font famiry={}".format(str(fm)))
        #    print(fm)
    def readfile(self,f):
        try:
            logging.info(File(f).length())
            container = self.import_controller.importFile(File(f))
            logging.info(container)
            container.getLoader().setEdgeDefault(importer.EdgeDirectionDefault.DIRECTED)
        except Exception,err:
            logging.info(err)
        self.import_controller.process(container,processor.DefaultProcessor(),self.workspace)
        self.graph = self.graph_model.getDirectedGraph()
        logging.info(graph)
    def __get_color(self,cat):
        colors=self.config['COLORS']
        if cat=='cat':
            cat=self.basef
        cfg=colors[cat]
        h=cfg['h']
        s=cfg['s']
        b=cfg['b']
        return Color.getHSBColor(h,s,b)

    def nodeshow(self):
        for i,node in enumerate(self.graph.getNodes()):
            if i==0:
                for k in dir(node):
                    print("k={}".format(k))
                for k in node.getAttributeKeys():
                    print("ak={}".format(k))
            v=node.getDegree()
            #sz=node.size()
            l=node.label
            #lent=len(l)
            #node.setLabel(str(lent))
            if v<20:
                node.setSize(20.0)
                node.setLabel(None)
            #print("v={} sz={}".format(v,sz))
            #if v<10:
            #    sz=
            #if i==0:
            #    label=node.label
            #    
            #color=node.color
            cat=node.getAttribute("modularity")
            c=self.__get_color(cat)
            node.setColor(c)
            #r=color.red
            #g=color.green
            #b=color.blue
            #msg="cat={} r={} g={} b={}".format(cat.encode("utf-8"),r,g,b)
            #print(msg)
            #dkt[cat]=color
        #return dkt
    def edgeshow(self):
        for i,edge in enumerate(self.graph.getEdges()):
            edge.setWeight(0.0)
            #if i==0:
            #for k in dir(edge):
                    #v=getattr(edge,k)
                    #msg="k={} v={}".format(k,v)
                    #print("k={}".format(k))
                    #print edge.weight
                    #print edge.getWeight()
            #        edge.setWeight(0.001)
    def export(self,i):
        print("start to set preview")
        FontFactory.register("/usr/share/fonts")
        FontFactory.register("/usr/share/fonts/YuGothM.ttc","Yu Gothic UI Regular")
        self.preview_model.getProperties().putValue(preview.PreviewProperty.EDGE_THICKNESS,3.0)
        #self.preview_model.getProperties().putValue(preview.PreviewProperty.EDGE_BORDER_WIDTH,0.0)
        assert(self.config['NODE_BORDER'])
        if self.config.get('NODE_BORDER',False)==True:
            border_width=1.0
        else:
            border_width=0.0
        self.preview_model.getProperties().putValue(preview.PreviewProperty.NODE_BORDER_WIDTH,border_width)
        self.preview_model.getProperties().putValue(preview.PreviewProperty.SHOW_NODE_LABELS,True)
        self.preview_model.getProperties().putValue(preview.PreviewProperty.EDGE_COLOR,preview_types.EdgeColor(preview_types.EdgeColor.Mode.MIXED))
        self.preview_model.getProperties().putValue(preview.PreviewProperty.NODE_LABEL_FONT,
                                               self.preview_model.getProperties().getFontValue(preview.PreviewProperty.NODE_LABEL_FONT).deriveFont(20))
        #self.preview_model.getProperties().putValue(preview.PreviewProperty.NODE_LABEL_FONT,Font({"name":"Yu Gothic Medium"}))
        #self.preview_model.getProperties().putValue(preview.PreviewProperty.NODE_LABEL_FONT,self.font)
        #f=self.preview_model.getProperties().getFontValue(preview.PreviewProperty.NODE_LABEL_FONT)
        #print(f)
        print("end to set preview")
        ec = ExportController(self.lookup)
        try:
            fname="out/cat_"+self.basef+".pdf"
            ec.exportFile(File(fname))
            svgname="out/svg_"+self.basef+".svg"
            ec.exportFile(File(svgname))
        except Exception,err:
            print(err)

    def __init__(self,f,config):
        df=os.path.basename(f)
        (basef,ext)=os.path.splitext(df)
        self.basef=basef
        self.config=config
        self.__initialize()

def show_files(config):
    for i,f in enumerate(glob("gexf/*.gexf")):
        gx=GexfPdfer(f,config)
        gx.readfile(f)
        gx.nodeshow()
        gx.edgeshow()
        gx.export(i)
def load_yaml():
    return ruamel.yaml.load(open("config/config.yaml"),Loader=ruamel.yaml.Loader)
def main():
    config=load_yaml()
    show_files(config)
if __name__=='__main__':main()
