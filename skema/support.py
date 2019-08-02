import json

log = lambda *x: None # print
# log = print

pretty = lambda x: print(json.dumps(x, indent=4, default=repr))