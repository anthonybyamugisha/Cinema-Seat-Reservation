import ast
import sys
from pathlib import Path

ALLOWED = {
    "domain": set(),
    "application": {"domain"},
    "infrastructure": {"application", "domain"},
    "interface": {"application", "infrastructure", "domain"},
}


def layer_of(module: str):
    parts = module.split(".")
    if len(parts) >= 2 and parts[0] == "src" and parts[1] in ALLOWED:
        return parts[1]
    return None


def main() -> int:
    src = Path("src")
    found = {layer: set() for layer in ALLOWED}
    violations = []

    for path in sorted(src.rglob("*.py")):
        layer = layer_of(".".join(path.with_suffix("").parts))
        if layer is None:
            continue
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            modules = []
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules = [node.module]
            for module in modules:
                target = layer_of(module)
                if target and target != layer:
                    found[layer].add(target)
                    if target not in ALLOWED[layer]:
                        violations.append(f"{path}: {layer} imports {target} ({module})")

    for layer, targets in found.items():
        print(f"{layer:15} -> {', '.join(sorted(targets)) or '(nothing)'}")

    if violations:
        print("\nVIOLATIONS:")
        for line in violations:
            print("  " + line)
        return 1

    print("\nOK: all imports point inward.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
