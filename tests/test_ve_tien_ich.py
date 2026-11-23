"""Unit cho các phần thêm vào ve.py sau phản hồi của người dùng - không cần browser.

Mỗi lớp ứng với một mục phản hồi: lỗi spec chỉ đích danh element (3), mũi tên
nhiều điểm thẳng mặc định và gợi ý chỗ sửa (4), flow giải thích từng bước (2),
tách nhãn để dịch và trang nhiều hình (7).
"""
import json
import pathlib

import pytest

import ve

HOP = [
    {'t': 'box', 'id': 'a', 'x': 0, 'y': 0, 'w': 120, 'h': 56, 'text': 'A'},
    {'t': 'box', 'id': 'm', 'x': 220, 'y': 0, 'w': 120, 'h': 56, 'text': 'M'},
    {'t': 'box', 'id': 'b', 'x': 440, 'y': 0, 'w': 120, 'h': 56, 'text': 'B'},
]


# ── lỗi spec phải chỉ đích danh element ─────────────────────────────
class TestLoiSpec:
    def test_thieu_w_neu_ten_element(self):
        with pytest.raises(ve.Loi) as e:
            ve.dung([{'t': 'box', 'id': 'svc', 'x': 0, 'y': 0, 'h': 40, 'text': 'Order Service'}])
        msg = str(e.value)
        assert "t='box'" in msg and "id='svc'" in msg and 'Order Service' in msg
        assert 'missing property w' in msg

    def test_so_viet_thanh_chuoi(self):
        with pytest.raises(ve.Loi, match='w must be a number, got "120"'):
            ve.dung([{'t': 'box', 'x': 0, 'y': 0, 'w': '120', 'h': 40}])

    def test_macro_sai_kieu_neu_ten_element(self):
        with pytest.raises(ve.Loi) as e:
            ve.dung([{'t': 'cells', 'id': 'c', 'x': 0, 'y': 0, 'cw': '40', 'ch': 40, 'labels': ['a']}])
        assert "t='cells'" in str(e.value) and "id='c'" in str(e.value)

    def test_points_hong(self):
        with pytest.raises(ve.Loi, match=r'points must be a list of two or more \[x, y\] pairs'):
            ve.dung([{'t': 'arrow', 'points': [[0, 0]]}])

    def test_mui_ten_thieu_dau(self):
        with pytest.raises(ve.Loi, match='needs `points`, or both `from` and `to`'):
            ve.dung([HOP[0], {'t': 'arrow', 'from': 'a'}])

    def test_co_la_va_thieu_gia_tri(self):
        with pytest.raises(ve.Loi, match='unknown option --bogus'):
            ve.doc_co(['a.json', '--bogus'])
        with pytest.raises(ve.Loi, match='--out needs a value'):
            ve.doc_co(['a.json', '--out'])

    def test_doc_co(self):
        co, specs = ve.doc_co(['a.json', '--lang', 'en', '--open', 'b.json', '--lib', 'x.lib'])
        assert specs == ['a.json', 'b.json']
        assert co['--lang'] == 'en' and co['--open'] is True and co['--lib'] == ['x.lib']

    def test_engine_thieu_playwright_in_lenh_cai(self, monkeypatch):
        import builtins
        that = builtins.__import__

        def gia(name, *a, **k):
            if name == 'excalidraw':
                raise ModuleNotFoundError('No module named playwright', name='playwright')
            return that(name, *a, **k)
        monkeypatch.setattr(ve, 'X', None)
        monkeypatch.setattr(builtins, '__import__', gia)
        with pytest.raises(ve.Loi) as e:
            ve._engine()
        assert 'playwright install chromium' in str(e.value)
        assert 'pip install -r' in str(e.value)


# ── mũi tên `points` thẳng mặc định ─────────────────────────────────
class TestDuongThang:
    def _mui(self, **kw):
        sk, *_ = ve.dung([dict({'t': 'arrow', 'points': [[0, 0], [100, 60], [200, 0]]}, **kw)])
        return next(o for o in sk if o['type'] == 'arrow')

    def test_ba_diem_thang(self):
        assert self._mui()['roundness'] is None

    def test_smooth_thi_cong(self):
        assert self._mui(smooth=True)['roundness'] == {'type': 2}

    def test_bend_van_cong(self):
        sk, *_ = ve.dung(HOP[:2] + [{'t': 'arrow', 'from': 'a', 'to': 'm', 'bend': 30}])
        assert next(o for o in sk if o['type'] == 'arrow')['roundness'] == {'type': 2}


# ── gợi ý chỗ sửa ───────────────────────────────────────────────────
class TestGoiY:
    def test_mui_ten_xuyen_hop_duoc_goi_y_cach_thoat(self):
        _, _, hinh, lint, _ = ve.dung(HOP + [{'t': 'arrow', 'from': 'a', 'to': 'b'}])
        than = [h for h in hinh.values() if h['t'] in ve.SHAPES]
        goi = ve._goi_y_duong(lint[0][4], hinh['a'], hinh['b'], than)
        assert goi
        # gợi ý phải thật sự thoát: áp vào rồi không còn xuyên hộp nào
        thu = json.loads('{' + goi + '}')
        pts, _ = ve._duong(dict(lint[0][4], **thu), hinh['a'], hinh['b'])
        assert ve._xuyen(pts, hinh['a'], hinh['b'], than) is None

    def test_ra_vao_canh_tren(self):
        f = {'x': 10, 'y': 40, 'width': 50, 'height': 20}
        s = {'x': 0, 'y': 50, 'width': 200, 'height': 100}
        assert ve._ra_vao(f, s) == 'y≈24 puts it above, y≈56 inside'


class TestKichThuoc:
    @staticmethod
    def _chu(y, text='x', h=20):
        return {'type': 'text', 'id': f't{y}', 'x': 0, 'y': y, 'width': 60, 'height': h, 'text': text}

    def test_hinh_thap_khong_nhac(self):
        assert ve.kich_thuoc([self._chu(0)], 600, 600, 666) == []

    def test_hinh_cao_chi_cho_cat_gan_giua(self):
        conv = [self._chu(y, f'dòng {y}') for y in range(0, 1200, 100)]     # nội dung 0-1120, giữa là 560
        nhac = ve.kich_thuoc(conv, 400, 1300, 666)
        assert len(nhac) == 1
        assert 'split it into 2 figures' in nhac[0]
        assert 'y≈560' in nhac[0] and '“dòng 500”' in nhac[0] and '“dòng 600”' in nhac[0]

    def test_hinh_rong_qua_cot(self):
        conv = [{'type': 'rectangle', 'id': 'a', 'x': 0, 'y': 0, 'width': 400, 'height': 50},
                {'type': 'rectangle', 'id': 'b', 'x': 500, 'y': 0, 'width': 500, 'height': 50}]
        nhac = ve.kich_thuoc(conv, 1000, 90, 666)
        assert len(nhac) == 1 and '1000 units wide' in nhac[0] and 'x≈450' in nhac[0]


# ── flow giải thích từng bước ───────────────────────────────────────
class TestFlow:
    SPEC = {'t': 'flow', 'id': 'f', 'x': 0, 'y': 0, 'steps': [
        {'title': 'Lấy 3 byte', 'text': '24 bit', 'example': 'M→77'},
        {'title': 'Ghép lại', 'example': '"TWFu"', 'color': 'node', 'edge': 'đủ bit'}]}

    def test_moi_buoc_mot_hop_mot_so_mot_vi_du(self):
        els = ve.bung([self.SPEC])
        hop = [e for e in els if e.get('id') in ('f.0', 'f.1')]
        assert [h['text'] for h in hop] == ['Lấy 3 byte', 'Ghép lại']
        assert hop[0]['y'] < hop[1]['y']
        so = [e['text'] for e in els if e.get('ghost')]
        assert so == ['1', '2']
        assert any(e['t'] == 'text' and e['text'] == 'M→77' for e in els)

    def test_mui_ten_thang_noi_hai_buoc_co_nhan(self):
        sk, _, _, lint, _ = ve.dung([self.SPEC])
        a, b, pts, *_ = lint[0]
        assert (a, b) == ('f.0', 'f.1')
        assert len(pts) == 2 and pts[0][0] == pts[1][0]
        assert any(o['type'] == 'text' and o['text'] == 'đủ bit' for o in sk)

    def test_buoc_co_mau_to_nen_va_so(self):
        els = ve.bung([self.SPEC])
        h1 = next(e for e in els if e.get('id') == 'f.1')
        assert h1['color'] == 'node' and h1['fill'] == 'node'


# ── nhãn sang ngôn ngữ khác ─────────────────────────────────────────
class TestNhan:
    SPEC = {'caption': 'Câu chú thích', 'elements': [
        {'t': 'box', 'id': 'nut', 'x': 0, 'y': 0, 'w': 100, 'h': 40, 'text': 'Gửi đơn', 'color': 'l4', 'fill': 'l4'},
        {'t': 'icon', 'id': 'i', 'name': 'firewall', 'x': 0, 'y': 60, 'h': 40, 'text': 'tường lửa'},
        {'t': 'table', 'id': 't', 'x': 0, 'y': 120, 'cols': [60, 60], 'head': ['id', 'tên'], 'rows': [['1', 'Lan']]},
        {'t': 'arrow', 'from': 'nut', 'to': 't', 'head': 'many', 'text': 'có'},
        {'t': 'cells', 'id': 'c', 'x': 0, 'y': 300, 'cw': 40, 'ch': 40, 'labels': ['', '7', 'k']}]}

    def _rut(self):
        thay = []
        ve._chu(self.SPEC, lambda s: thay.append(s) or s)
        return thay

    def test_rut_chi_lay_chu_nguoi_doc_thay(self):
        thay = self._rut()
        for s in ('Câu chú thích', 'Gửi đơn', 'tường lửa', 'id', 'tên', 'Lan', 'có', 'k'):
            assert s in thay
        # id, token màu, tên icon, kiểu đầu mũi tên, chuỗi rỗng và số không phải chữ để dịch
        for s in ('nut', 'l4', 'firewall', 'many', 'box', '', '7', '1'):
            assert s not in thay

    def test_dich_va_bao_nhan_thieu(self, tmp_path):
        src = tmp_path / 'hinh.json'
        src.write_text(json.dumps(self.SPEC, ensure_ascii=False), encoding='utf-8')
        ve.rut_nhan(src, 'en')
        f = tmp_path / 'hinh.en.labels.json'
        bang = json.loads(f.read_text(encoding='utf-8'))
        assert bang['Gửi đơn'] == 'Gửi đơn'
        bang['Gửi đơn'] = 'Submit'
        del bang['tường lửa']
        f.write_text(json.dumps(bang, ensure_ascii=False), encoding='utf-8')
        els, _, thieu = ve.dich(src, 'en', ve.nap(src), self.SPEC['caption'])
        assert els[0]['text'] == 'Submit' and els[0]['id'] == 'nut'
        assert els[1]['name'] == 'firewall'
        assert thieu == ['tường lửa']
        # chạy lại giữ bản dịch cũ, thêm lại nhãn đã xoá
        ve.rut_nhan(src, 'en')
        bang = json.loads(f.read_text(encoding='utf-8'))
        assert bang['Gửi đơn'] == 'Submit' and bang['tường lửa'] == 'tường lửa'

    def test_thieu_file_nhan(self, tmp_path):
        src = tmp_path / 'hinh.json'
        src.write_text('{"elements": []}', encoding='utf-8')
        with pytest.raises(ve.Loi, match='--extract-labels en'):
            ve.dich(src, 'en', [], None)


# ── trang nhiều hình ────────────────────────────────────────────────
class TestTrang:
    SVG = ('<svg viewBox="0 0 100 50" class="dg"><mask id="mask-_arrow3"></mask>'
           '<path mask="url(#mask-_arrow3)" fill="var(--ink)"/></svg>')

    def test_id_tung_hinh_khong_dung_nhau(self, tmp_path):
        doc = ve.trang([('a', self.SVG, 100, 'Câu một'), ('b', self.SVG, 100, None)],
                       tmp_path / 'p.html', 'Tiêu đề', 'Chú thích chung', 'vi')
        assert 'id="h1-mask-_arrow3"' in doc and 'url(#h1-mask-_arrow3)' in doc
        assert 'id="h2-mask-_arrow3"' in doc and 'url(#h2-mask-_arrow3)' in doc
        assert '<b>Hình 1.</b> Câu một' in doc
        assert doc.count('<figcaption>') == 1
        assert '<h1>Tiêu đề</h1>' in doc and 'Chú thích chung' in doc
        # một file tự đủ: token màu và font nằm ngay trong trang
        assert '--ink:' in doc and 'data:font/woff2;base64,' in doc
        assert 'url(nunito' not in doc

    def test_chu_thich_duoc_escape(self, tmp_path):
        doc = ve.trang([('a', self.SVG, 100, 'a < b & c')], tmp_path / 'p.html', None, None, 'en')
        assert '<b>Figure 1.</b> a &lt; b &amp; c' in doc


class TestMo:
    def test_mo_dung_lenh_he_dieu_hanh(self, monkeypatch):
        import subprocess
        goi = []
        monkeypatch.setattr(subprocess, 'run', lambda cmd, **k: goi.append(cmd))
        monkeypatch.setattr(ve.sys, 'platform', 'darwin')
        ve.mo([pathlib.Path('/tmp/a-light.png')])
        assert goi == [['open', '/tmp/a-light.png']]
        monkeypatch.setattr(ve.sys, 'platform', 'linux')
        ve.mo([pathlib.Path('/tmp/a-light.png')])
        assert goi[-1] == ['xdg-open', '/tmp/a-light.png']


class TestTrinhDuyet:
    def test_bi_sandbox_giet_bao_mot_dong(self):
        # log thật từ sandbox của plugin eval trên macOS (2026-11-24)
        e = Exception('BrowserType.launch: Target page, context or browser has been closed\nBrowser logs:\n'
                      '[0124/0101:FATAL:mach_port_rendezvous_mac.cc(155)] Check failed: kr == KERN_SUCCESS. '
                      'bootstrap_check_in org.chromium.Chromium.MachPortRendezvousServer.1: Permission denied (1100)')
        with pytest.raises(ve.Loi) as k:
            ve._khong_chay(e)
        msg = str(k.value)
        assert 'could not start' in msg and 'MachPortRendezvousServer' in msg and 'sandbox' in msg
        assert 'Traceback' not in msg
