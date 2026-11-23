"""Golden render: cả 30 ví dụ trong examples/ phải vẽ sạch.

Đây là phép thử bao trùm mọi macro m_* mà không phải test từng macro: chạy
ve.py thật (Chromium thật) qua subprocess và bám vào đúng cam kết công khai
của skill - exit 0 (không dòng ✗ nào: không chữ tràn, không mũi tên xuyên
hộp, không chữ quá nhỏ, không màu ngoài token).

Chạy:  python3 -m pytest tests/test_render_golden.py     (~2 phút, cần Chromium)
Bỏ qua khi chỉ muốn test nhanh:  python3 -m pytest -m "not slow"
"""
import json
import pathlib
import subprocess
import sys

import pytest

import theme as T

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXAMPLES = sorted((ROOT / 'examples').glob('*.json'))

pytestmark = [pytest.mark.slow]


def test_examples_render_clean(tmp_path):
    assert len(EXAMPLES) >= 20, 'examples/ phải có đủ bộ template'
    r = subprocess.run(
        [sys.executable, str(ROOT / 'scripts' / 've.py'),
         *[str(f) for f in EXAMPLES], '--out', str(tmp_path)],
        capture_output=True, text=True, timeout=1800)
    assert r.returncode == 0, (
        f've.py thoát mã {r.returncode}:\n{r.stdout}\n{r.stderr}')

    van_de = []
    for f in EXAMPLES:
        ten = f.stem
        svg = (tmp_path / f'{ten}.svg').read_text(encoding='utf-8')
        # cam kết 1: không còn màu ngoài token (ve.py đã chặn, đây là dây đai)
        sot = T.audit(svg)
        if sot:
            van_de.append(f'{ten}: màu ngoài token {sot}')
        # cam kết 2: màu là biến CSS, kể cả lit (không sót hex thô của lit)
        if 'var(--' not in svg:
            van_de.append(f'{ten}: SVG không chứa var(--) nào')
        for hx in ('#24272D', '#F4EFE4'):
            if hx.lower() in svg.lower():
                van_de.append(f'{ten}: lit hex thô {hx} chưa thành var()')
        # cam kết 3: file .excalidraw là cảnh hợp lệ mở được trên excalidraw.com
        canh = json.loads((tmp_path / f'{ten}.excalidraw').read_text(encoding='utf-8'))
        if not canh.get('elements'):
            van_de.append(f'{ten}: cảnh .excalidraw rỗng')
    assert not van_de, '\n'.join(van_de)

    # mỗi ví dụ một dòng ✓ trong stdout (✗ thì returncode đã khác 0)
    for f in EXAMPLES:
        assert f'✓ {f.stem}:' in r.stdout, f'{f.stem}: không có dòng ✓ trong:\n{r.stdout}'
