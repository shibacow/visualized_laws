.PHONY: exec
# set jython path
JYTHON = /Users/kshibao/jython2.7.0/bin/jython
CLASSPATH=gephi-toolkit-0.9.1-all.jar
exec:
	export LANG=ja_JP.UTF-8
	CLASSPATH=$(CLASSPATH) $(JYTHON)  show_node_color.py
