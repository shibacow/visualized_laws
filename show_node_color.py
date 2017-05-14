#/usr/bin/env jython
# -*- coding:utf-8 -*-
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
logging.basicConfig(level=logging.INFO,format=FORMAT)
import org.gephi.preview.types as preview_types
from java.awt import GraphicsEnvironment
from java.awt import Font
from com.itextpdf.text import FontFactory
import ruamel.yaml
from pprint import pprint
import csv

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
                self.font=f
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
        defcfg=colors[u'憲法']
        cfg=colors.get(cat,defcfg)
        h=cfg['h']
        s=cfg['s']
        b=cfg['b']
        return Color.getHSBColor(h,s,b)
    def __detect_threshold_degree(self,limit=0.5):
        deglist=[node.getDegree() for node in self.graph.getNodes()]
        deglist=sorted(deglist)
        sz=len(deglist)
        sz=int(sz*limit)
        return deglist[sz]

    def nodeshow(self):
        thresh_hold_deg=self.__detect_threshold_degree(0.97)
        logging.info("thresh_hold={}".format(thresh_hold_deg))
        for i,node in enumerate(self.graph.getNodes()):
            if i==0:
                for k in dir(node):
                    logging.debug("k={}".format(k))
                for k in node.getAttributeKeys():
                    logging.debug("ak={}".format(k))
            v=node.getDegree()
            l=node.label
            if self.shortcut.has_key(l):
                s=self.shortcut[l]
                node.setLabel(s)
            if v<thresh_hold_deg:
                node.setLabel(None)
                node.setSize(20.0)
            if v<thresh_hold_deg/2.0:
                node.setSize(14.0)
            cat=node.getAttribute("modularity")
            c=self.__get_color(cat)
            node.setColor(c)
    def export(self,i):
        logging.info("start to set preview")
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
        logging.info("end to set preview")
        ec = ExportController(self.lookup)
        try:
            fname="out/cat_"+self.basef+".pdf"
            ec.exportFile(File(fname))
            svgname="out/cat_"+self.basef+".svg"
            ec.exportFile(File(svgname))
        except Exception,err:
            logging.error(err)

    def __init__(self,f,config,shortcut):
        df=os.path.basename(f)
        (basef,ext)=os.path.splitext(df)
        self.basef=basef
        self.config=config
        self.shortcut=shortcut
        self.__initialize()

def show_files(config,shortcut):
    for i,f in enumerate(glob("gexf/*.gexf")):
        gx=GexfPdfer(f,config,shortcut)
        gx.readfile(f)
        gx.nodeshow()
        gx.export(i)
def load_yaml():
    return ruamel.yaml.load(open("config/config.yaml"),Loader=ruamel.yaml.Loader)
def load_shortcut():
    dkt={}
    for r in csv.reader(open('config/shortcut.csv')):
        k=r[0]
        v=r.pop()
        while not v:
            v=r.pop()
        k=unicode(k,'utf-8')
        v=unicode(v,'utf-8')
        dkt[k]=v
    return dkt
def main():
    config=load_yaml()
    shortcut=load_shortcut()
    show_files(config,shortcut)
if __name__=='__main__':main()
