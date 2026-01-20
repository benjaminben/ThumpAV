
import json

def onHoverStartGetAccept(comp, info):
	return True # accept what is being dragged

def onDropGetResults(comp, info):
	return {'droppedOn': comp}

def onDragStartGetItems(comp, info):
	preset = json.loads(comp.op('preset').text)
	dragItems = ['PLUGIN_PRESET', preset] # drag the comp itself
	op.LiveLauncher.par.Showfxdroparea = True
	#debug('\nonDragStartGetItems comp:', comp.path, '- info:\n', info)
	return dragItems

def onDragEnd(comp, info):
	op.LiveLauncher.par.Showfxdroparea = False