def onHoverStartGetAccept(comp, info):
	try:
		if len(info['dragItems']) != 1:
			return False
		else:
			return True # accept what is being dragged
	except:
		return False

def onDropGetResults(comp, info):
	first = info['dragItems'][0]
	cueIdx = comp.parent().digits
	trackIdx = comp.digits
	try:
		if type(first) == tdu.FileInfo:
			comp.parent.Browser.DropFileInCell(cueIdx, trackIdx, first.path)
			return True
		if 'src' in first:
			comp.parent.Browser.DropFileInCell(cueIdx, trackIdx, first['src'])
		if 'cell' in first:
			comp.parent.Browser.DropFileInCell(cueIdx, trackIdx, first['cell']['source'])
	except Exception as e:
		print(e)
		return False
	return {'droppedOn': comp}

def onDragStartGetItems(comp, info):
	cueIdx = comp.parent().digits
	trackIdx = comp.digits
	dragItems = []
	if comp.panel.select:
		dragItems = [{ "src": comp.op('bg').par.file.eval(), "cue": cueIdx, "track": trackIdx }]
	elif comp.panel.rselect:
		dragItems = [{ "cell": comp.par.Data.eval() }]
	#debug('\nonDragStartGetItems comp:', comp.path, '- info:\n', info)
	return dragItems