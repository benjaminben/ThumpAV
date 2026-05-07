# Global drag/drop callbacks for plugin ctrl widgets.
# Each ctrl_<Name> containerCOMP has this as its `dragdropcallbacks` script.
# Resolves the bound Par by name convention only: ctrl_<Suffix> -> Effect.par.<Suffix>.
# Components built outside this family either conform to the convention or accept
# the limitation (drag will return [comp] which downstream targets will ignore).

def onHoverStartGetAccept(comp, info):
	try:
		return True
	except Exception as e:
		debug("[CtrlDragDrop] onHoverStartGetAccept error:", e)
		return True

def onHoverEnd(comp, info):
	return

def onDropGetResults(comp, info):
	try:
		drag_items = info.get("dragItems", []) if info else []
		if not drag_items:
			return {"droppedOn": comp}
		o = drag_items[0]
		if not isinstance(o, Channel):
			return {"droppedOn": comp}
		par = _resolve_ctrl_par(comp)
		if par is None:
			return {"droppedOn": comp}
		LinkParToChannel(par, o)
	except Exception as e:
		debug("[CtrlDragDrop] onDropGetResults error:", e)
	return {"droppedOn": comp}

def onDragStartGetItems(comp, info):
	try:
		par = _resolve_ctrl_par(comp)
		if par is not None:
			return [par]
	except Exception as e:
		debug("[CtrlDragDrop] onDragStartGetItems error:", e)

def onDragEnd(comp, info):
	return


def _resolve_ctrl_par(comp):
	"""Walk up to the nearest ctrl_<Suffix> ancestor; resolve Effect.par.<Suffix>."""
	try:
		cur = comp
		while cur is not None and not getattr(cur, 'name', '').startswith("ctrl_"):
			cur = cur.parent()
		if cur is None or "_" not in cur.name:
			return None
		suffix = cur.name.split("_", 1)[1]
		effect = cur.parent.Effect  # ctrl -> Settings -> Effect
		return getattr(effect.par, suffix, None)
	except Exception as e:
		debug("[CtrlDragDrop] _resolve_ctrl_par error:", e)
		return None


def LinkParToChannel(par, channel):
	"""EXPRESSION-mode link of par to a CHOP channel. Returns True/False with rollback on failure."""
	prev_mode = None
	prev_expr = None
	try:
		prev_mode = par.mode
		prev_expr = par.expr
		chop = channel.owner
		if chop is None:
			return False
		chop_ref = _chop_shortcut_ref(chop)
		par.expr = f"{chop_ref}[\"{channel.name}\"]"
		par.mode = type(par.mode).EXPRESSION
		return True
	except Exception as e:
		debug("[CtrlDragDrop] LinkParToChannel error, rolling back:", e)
		try:
			if prev_expr is not None:
				par.expr = prev_expr
			if prev_mode is not None:
				par.mode = prev_mode
			else:
				par.mode = type(par.mode).CONSTANT
		except Exception as rollback_err:
			debug("[CtrlDragDrop] LinkParToChannel rollback failed:", rollback_err)
		return False


def UnlinkPar(par):
	"""Restore par to CONSTANT at its current eval value. Safe-no-op on failure."""
	try:
		current = par.eval()
		par.mode = type(par.mode).CONSTANT
		try:
			par.val = current
		except Exception:
			pass
		return True
	except Exception as e:
		debug("[CtrlDragDrop] UnlinkPar error:", e)
		return False


def _chop_shortcut_ref(chop):
	try:
		if op.channelData and chop.path.startswith(op.channelData.path + "/"):
			sub = chop.path[len(op.channelData.path) + 1:]
			return f"op.channelData.op(\"{sub}\")"
	except Exception:
		pass
	try:
		if op.Audio and chop.path.startswith(op.Audio.path + "/"):
			sub = chop.path[len(op.Audio.path) + 1:]
			return f"op.Audio.op(\"{sub}\")"
	except Exception:
		pass
	try:
		if op.channelData and chop.path == op.channelData.path:
			return "op.channelData"
	except Exception:
		pass
	try:
		if op.Audio and chop.path == op.Audio.path:
			return "op.Audio"
	except Exception:
		pass
	return f"op(\"{chop.path}\")"
