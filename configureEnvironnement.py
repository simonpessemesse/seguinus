
import os
if os.name=="posix":
	import readline

sep=";"
if os.name=="posix":
	sep=":"
os.environ['DJANGO_SETTINGS_MODULE']='seguinus.settings'
os.chdir("seguinus")
p=os.path.abspath(".")+os.sep+".."
p+=sep+os.path.abspath(".")
os.environ['PYTHONPATH']=p
os.putenv("PYTHONPATH",p)

