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
	
	try:
		if type(first) == tdu.FileInfo:
			ext.LiveLauncher.SetSource(parent().digits, first.path)
			return True
		if 'src' in first:
			ext.LiveLauncher.SetSource(parent().digits, first['src'])
		if 'cell' in first:
			ext.LiveLauncher.SetLayer(parent().digits, first['cell'])
		if 'top' in first:
			ext.LiveLauncher.SetSelect(parent().digits, first['top'])
	except:
		return False
	return {'droppedOn': comp}

def onDragStartGetItems(comp, info):
	dragItems = [parent.Monitor.par.Bus.eval().op('fin')] # drag the comp itself
	#debug('\nonDragStartGetItems comp:', comp.path, '- info:\n', info)
	return dragItems