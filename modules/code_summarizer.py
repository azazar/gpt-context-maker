from typing import Dict, List
from ast import parse, iter_fields, AST, Name, Constant, FunctionDef, Assign, ClassDef, If
from pathlib import Path

def summarize(code: str, filename: str) -> Dict[str, List[str]]:
    try:
        tree = parse(code)
    except SyntaxError as e:
        return {"filename": filename, "error": f"SyntaxError: {e}"}

    def get_assign_targets(node):
        if isinstance(node, Name):
            return node.id
        elif isinstance(node, (list, tuple)):
            return ', '.join(get_assign_targets(e) for e in node)
        return ''

    def summarize_function(func: FunctionDef) -> str:
        args = ', '.join(arg.arg for arg in func.args.args)
        return f"  - {func.name}({args})"

    def summarize_class(cls: ClassDef) -> str:
        fields = [f"- {get_assign_targets(target)} = {value.value} ..."
                  for target, value in
                  [(get_assign_targets(node.targets), node.value)
                   for node in cls.body if isinstance(node, Assign)]]
        methods = [summarize_function(func) for func in cls.body if isinstance(func, FunctionDef)]
        return f"### `{cls.name}` Fields\n" + '\n'.join(fields) + "\n### `{cls.name}` Functions\n" + '\n'.join(methods)

    def summarize_assign(node: Assign) -> str:
        if isinstance(node.value, Constant):  # Constant value like: x = 1 or x = "string"
            value_str = str(node.value.value)
        elif isinstance(node.value, Name):  # Variable like: x = y
            value_str = node.value.id
        elif isinstance(node.value, (list, tuple, set, dict)):  # Compound types
            value_str = str(node.value)
        else:
            value_str = "..."

        # Truncate long values
        if len(value_str) > 50:
            value_str = value_str[:50] + "..."

        return f"- {get_assign_targets(node.targets)} = {value_str}"

    summary = {"filename": filename, "variables": [], "functions": [], "classes": [], "extra_code": ""}

    for node in tree.body:
        if isinstance(node, Assign):
            summary["variables"].append(summarize_assign(node))
        elif isinstance(node, FunctionDef):
            summary["functions"].append(summarize_function(node))
        elif isinstance(node, ClassDef):
            summary["classes"].append(summarize_class(node))
        elif isinstance(node, If) and isinstance(node.test, Name) and node.test.id == "__name__":
            summary["extra_code"] = "\n".join(code.split("\n")[node.lineno-1:node.end_lineno])

    # If no elements were found, return a default summary
    if not any(summary.values()):
        summary["extra_code"] = "No variables, functions, or classes found to summarize."

    return summary