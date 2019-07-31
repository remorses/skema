
import os.path
import sys
import json
import skema
import subprocess
import os, random

class temporary_write:
        def __init__(self,  data, path=str(random.random())[3:]):
                self.path = os.path.abspath(path)
                self.data = data
                f = open(self.path, 'w')
                f.write(self.data)
                f.close()

        __enter__ = lambda self: self.path
        __exit__ = lambda self, a, b, c: os.remove(self.path)

def get_result_file(skema_path, extension):
    skema_path = os.path.abspath(skema_path)
    result_dir = os.path.dirname(skema_path)
    name, _ = os.path.splitext(skema_path)
    name = name.split('/')[-1]
    result_file = os.path.join(result_dir, name + extension)
    print(result_file)
    return result_file

def generate_types(skema_path, extension, args):
    with open(skema_path) as f:
        data = f.read()
        json_schema = skema.to_jsonschema(data,)
    root_name = json_schema.get('$ref').split('/')[-1]
    json_schema = json.dumps(json_schema, indent=4, default=str)
    print(json_schema)
    result_file = get_result_file(skema_path, extension)
    with temporary_write(json_schema) as schema_path:
            command = f'quicktype "{schema_path}#/definitions/" -o {result_file}  --top-level {root_name} --src-lang schema {args}'
            print(command)
            try:
                res = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE)
                print(res.stdout.decode())
            except subprocess.CalledProcessError as e:
                print(e.stderr)


# main('example.skema')