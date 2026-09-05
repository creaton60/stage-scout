"""헥사고날 의존 규칙을 테스트로 강제한다.

이 테스트가 깨지면 설계가 무너지고 있다는 뜻이므로, 예외를 추가하지 말고
코드를 옳은 레이어로 옮긴다.
"""

from __future__ import annotations

import ast
from pathlib import Path

SRC = Path(__file__).resolve().parents[3] / "src" / "stage_scout"


def _imports_of(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def _modules_under(layer: str) -> list[Path]:
    return [p for p in (SRC / layer).rglob("*.py") if p.name != "__init__.py"]


def test_domain_depends_on_nothing_else() -> None:
    for module in _modules_under("domain"):
        for imported in _imports_of(module):
            assert not imported.startswith("stage_scout.application"), module
            assert not imported.startswith("stage_scout.adapter"), module
            assert not imported.startswith("stage_scout.config"), module


def test_application_does_not_depend_on_adapter() -> None:
    for module in _modules_under("application"):
        for imported in _imports_of(module):
            assert not imported.startswith("stage_scout.adapter"), module


def test_only_composition_root_imports_adapters() -> None:
    """어댑터 구현체를 아는 곳은 config/container.py 하나뿐이어야 한다."""
    offenders = []
    for module in _modules_under("adapter"):
        for imported in _imports_of(module):
            if imported.startswith("stage_scout.application.usecase"):
                offenders.append(module)
    assert not offenders, f"어댑터가 유스케이스 구현체를 직접 import 함: {offenders}"
