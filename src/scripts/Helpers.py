def filter_string(*args, text=''):
  for arg in args:
    if not re.match(f'.*{arg}', text):
      return False
  return True

def tryExcept(func, fall):
	try:
		return func()
	except:
		return fall