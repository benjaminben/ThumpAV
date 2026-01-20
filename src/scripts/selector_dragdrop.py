def onHoverStartGetAccept(comp, info):
	return True # accept what is being dragged

def onDropGetResults(comp, info):
	return {'droppedOn': comp}

def onDragStartGetItems(comp, info):
	p = comp
	dragItems = ['PLUGIN_GROUP', [op(f'{p.path}/Wrapper')]]
	#debug('\nonDragStartGetItems comp:', comp.path, '- info:\n', info)
	return dragItems