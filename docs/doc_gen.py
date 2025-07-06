import os
import inspect
import importlib
from typing import List

def scan_module(path: str) -> List[str]:
    files = []
    for root, _, filenames in os.walk(path):
        for f in filenames:
            if f.endswith('.py') and not f.startswith('__'):
                files.append(os.path.join(root, f))
    return files

def extract_info(filepath: str):
    rel = os.path.relpath(filepath).replace('\\','/').replace('.py','')
    module_name = rel.replace('/', '.')
    try:
        mod = importlib.import_module(module_name)
    except Exception as e:
        return f"### {module_name}\nFailed to import: {e}\n"
    doc = f"### `{module_name}`\n"
    for name, obj in inspect.getmembers(mod):
        if inspect.isclass(obj):
            doc += f"- Class `{name}`\n"
            for mname, method in inspect.getmembers(obj, inspect.isfunction):
                doc += f"  - Method `{mname}()`\n"
        elif inspect.isfunction(obj):
            doc += f"- Function `{name}()`\n"
    doc += "\n"
    return doc

if __name__ == "__main__":
    modules = scan_module('core') + scan_module('controllers') + scan_module('utils') + scan_module('solver')
    docs = "# 📘 Auto-Generated Module Index\n\n"
    for mod in modules:
        docs += extract_info(mod)
    with open("docs/autogen_index.md","w",encoding="utf-8") as f:
        f.write(docs)
    print("✅ 文档结构已生成至 docs/autogen_index.md")
