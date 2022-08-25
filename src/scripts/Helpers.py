def filter_string(*args, text=''):
  for arg in args:
    if not re.match(f'.*{arg}', text):
      return False
  return True