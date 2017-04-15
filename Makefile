.PHONY: exec

exec:
	export LANG=ja_JP.UTF-8
	CLASSPATH=gephi-toolkit-0.9.1-all.jar jython  headless_sample.py
#	CLASSPATH=gephi-toolkit-0.9.1-all.jar jython  show_node_color.py
