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
        {'t': 'arrow', 'from': 'nut', 'to': 't', 'head': 'many', 'text': 'có', 'labelColor': 'muted', 'badgeColor': 'l2'},
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
        for s in ('nut', 'l4', 'firewall', 'many', 'box', '', '7', '1', 'muted', 'l2'):
            assert s not in thay

    def test_so_thap_phan_duoc_rut_de_doi_dau(self):
        # "16,1" is written "16.1" in English: a bare decimal is a label to translate, a bare integer is not
        thay = []
        ve._chu({'elements': [{'t': 'text', 'text': '16,1'}, {'t': 'text', 'text': '200.000'}, {'t': 'text', 'text': '20'}]},
                lambda s: thay.append(s) or s)
        assert thay == ['16,1', '200.000']

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
        els, _, thieu, _ = ve.dich(src, 'en', ve.nap(src), self.SPEC['caption'])
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


# ── đường đọc, payload, số liệu với nguồn, chiến lược ───────────────
def _doc(spec, strat=None, conv=None):
    """Chạy duong_doc trên spec đã biên dịch; conv giả: mỗi phần tử cơ sở thành một hình chữ nhật/chữ."""
    sk, _, _, lint, goc = ve.dung(spec)
    if conv is None:
        conv = [{'type': 'text' if o['type'] == 'text' else 'rectangle', 'id': o['id'], 'x': o['x'], 'y': o['y'],
                 'width': o.get('width', 0), 'height': o.get('height', 0), 'text': o.get('text', '')}
                for o in sk if 'x' in o]
    return ve.duong_doc(conv, goc, lint, strat)


CHINH = [{'t': 'box', 'id': 'a', 'x': 0, 'y': 0, 'w': 100, 'h': 50, 'text': 'A'},
         {'t': 'box', 'id': 'b', 'x': 200, 'y': 0, 'w': 100, 'h': 50, 'text': 'B'},
         {'t': 'arrow', 'from': 'a', 'to': 'b', 'text': 'gọi'}]


class TestDuongDoc:
    def test_khung_dung_roi_bi_nhac(self):
        _, nhac = _doc(CHINH + [{'t': 'code', 'id': 'c', 'x': 0, 'y': 120, 'title': 'intrinsic', 'text': 'ghi 64 byte'}])
        assert any('panel “intrinsic”' in n and 'no arrow or note' in n for n in nhac)

    def test_khung_co_mui_ten_thi_im(self):
        spec = CHINH + [{'t': 'code', 'id': 'c', 'x': 0, 'y': 120, 'title': 'intrinsic', 'text': 'ghi 64 byte'},
                        {'t': 'arrow', 'points': [[50, 118], [50, 56]], 'dashed': True}]
        _, nhac = _doc(spec)
        assert not any('panel' in n for n in nhac)

    def test_cap_so_sanh_chi_can_noi_mot_ben(self):
        spec = CHINH + [{'t': 'code', 'id': 'c1', 'x': 0, 'y': 120, 'w': 140, 'title': 'thường', 'text': 'a'},
                        {'t': 'code', 'id': 'c2', 'x': 160, 'y': 120, 'w': 140, 'title': 'nhanh', 'text': 'b'},
                        {'t': 'arrow', 'points': [[230, 118], [230, 56]], 'dashed': True}]
        _, nhac = _doc(spec)
        assert not any('panel' in n for n in nhac)

    def test_so_badge_nhay_va_lap(self):
        spec = [{'t': 'badge', 'x': 0, 'y': 0, 'n': 1}, {'t': 'badge', 'x': 40, 'y': 0, 'n': 3},
                {'t': 'badge', 'x': 80, 'y': 0, 'n': 3}]
        _, nhac = _doc(spec)
        assert any('skip 2' in n for n in nhac) and any('badge 3 is used twice' in n for n in nhac)

    def test_chien_luoc_co_thu_tu_doi_danh_so(self):
        spec = CHINH + [{'t': 'code', 'id': 'c', 'x': 0, 'y': 120, 'title': 't', 'text': 'x'},
                        {'t': 'arrow', 'points': [[50, 118], [50, 56]], 'dashed': True}]
        _, khong = _doc(spec, 'architecture')
        _, co = _doc(spec, 'incident')
        assert not any('no badge' in n for n in khong)
        assert any("strategy 'incident'" in n and 'no badge' in n for n in co)

    def test_payload_cung_khi_la_lo_hong(self):
        spec = [{'t': 'text', 'x': 0, 'y': 0, 'text': 'input: ' + 'A' * 64 + '='}]
        cung, _ = _doc(spec, 'vulnerability')
        _, nhac = _doc(spec, 'mechanism')
        assert cung and 'attack input' in cung[0]
        assert any('attack input' in n for n in nhac)
        cung, nhac = _doc([{'t': 'text', 'x': 0, 'y': 0, 'text': '64 ký tự Base64 + "="'}], 'vulnerability')
        assert not cung and not any('attack' in n for n in nhac)

    def test_quan_he_phai_co_nhan(self):
        spec = [{'t': 'box', 'id': 'a', 'x': 0, 'y': 0, 'w': 100, 'h': 50, 'text': 'ngủ ít'},
                {'t': 'box', 'id': 'b', 'x': 200, 'y': 0, 'w': 100, 'h': 50, 'text': 'cà phê'},
                {'t': 'arrow', 'from': 'a', 'to': 'b'}, {'t': 'arrow', 'from': 'b', 'to': 'a', 'text': '+', 'bend': 30}]
        _, nhac = _doc(spec, 'life-problem')
        assert any('1 of 2 arrows carry no label' in n for n in nhac)
        _, nhac = _doc(spec, 'mechanism')
        assert not any('carry no label' in n for n in nhac)

    def test_mau_chu_giai_va_mui_ten_chi_khong_can_nhan(self):
        spec = [{'t': 'box', 'id': 'a', 'x': 0, 'y': 0, 'w': 100, 'h': 50, 'text': 'biển'},
                {'t': 'box', 'id': 'b', 'x': 200, 'y': 0, 'w': 100, 'h': 50, 'text': 'mây'},
                {'t': 'arrow', 'from': 'a', 'to': 'b', 'text': 'bay hơi', 'dashed': True},
                {'t': 'legend', 'x': 0, 'y': 120, 'items': [{'line': True, 'text': 'nước lỏng'}]},
                {'t': 'arrow', 'points': [[50, 200], [50, 56]], 'dashed': True, 'color': 'muted', 'weight': 1}]
        _, nhac = _doc(spec, 'knowledge-summary')
        assert not any('carry no label' in n for n in nhac)
        # a dashed arrow drawn at full weight is a relation (vapour), so it still needs its label
        spec[2] = {'t': 'arrow', 'from': 'a', 'to': 'b', 'dashed': True}
        _, nhac = _doc(spec, 'knowledge-summary')
        assert any('1 of 1 arrows carry no label' in n for n in nhac)

    def test_tong_hop_qua_nhieu_khoi(self):
        spec = [{'t': 'box', 'id': f'k{i}', 'x': i * 120, 'y': 0, 'w': 100, 'h': 40, 'text': f'ý {i}'} for i in range(11)]
        _, nhac = _doc(spec, 'knowledge-summary')
        assert any('11 main shapes, above 9' in n for n in nhac)

    def test_chien_luoc_moi_co_mat(self):
        for k in ('concept', 'knowledge-summary', 'note', 'life-problem', 'vulnerability', 'incident'):
            assert k in ve.STRATEGIES


class TestSoVoiNguon:
    def test_chuan_hoa_cach_viet_so(self):
        assert ve._so('200 000 lần, 200_000, 0,25 giây') == {'200000', '025'}
        assert ve._so('mask 0xFFFF_FFFF') == {'0XFFFFFFFF'}

    def test_liet_ke_so_khong_co_trong_nguon(self):
        conv = [{'type': 'text', 'text': 'mảng 50 byte, ghi 64 byte, 17 × 3 - 1 = 50, bước 2'},
                {'type': 'text', 'text': 'decode() × 200 000'}]
        nhac = ve.so_voi_nguon(conv, 'allocates a 50-byte array; 64 bytes are written; 200_000 times', 'bai.md')
        assert len(nhac) == 1 and ': 17.' in nhac[0]
        assert ve.so_voi_nguon(conv[:1][:0], 'x', 'bai.md') == []

    def test_ten_thang_tieng_anh_khop_ngay_viet(self):
        conv = [{'type': 'text', 'text': 'bản vá 17/11/2026'}]
        assert ve.so_voi_nguon(conv, 'Oracle released a patch at 1:00pm PT on Nov 17, 2026.', 'bai.md') == []

    def test_ket_qua_co_phep_tinh_khong_bi_nhac(self):
        conv = [{'type': 'text', 'text': '40 nhà × 2 lần\n= 80 lượt'}, {'type': 'text', 'text': 'tổng 95 lượt'}]
        nhac = ve.so_voi_nguon(conv, '40 nhà, mỗi nhà 2 lần', 'bai.md')
        assert len(nhac) == 1 and ': 95.' in nhac[0] and '80' not in nhac[0]

    def test_don_vi_nghin_trieu_khop_so_day_du(self):
        # a translated figure spells the source's "200 nghìn" / "3,6 triệu" in full, and the other way round
        conv = [{'type': 'text', 'text': 'lose 200,000 VND, 3,600,000 VND, 1.5 million'}]
        assert ve.so_voi_nguon(conv, 'mất 200 nghìn, máy 3,6 triệu, thang 1,5 triệu', 'bai.md') == []
        conv = [{'type': 'text', 'text': 'mất 200 nghìn, 12 triệu'}]
        nhac = ve.so_voi_nguon(conv, 'a fee of 200,000 VND', 'bai.md')
        assert len(nhac) == 1 and ': 12.' in nhac[0]

    def test_so_phien_ban_tach_phan(self):
        conv = [{'type': 'text', 'text': 'cả bản 21, 25'}]
        assert ve.so_voi_nguon(conv, 'vulnerable: 17.0.21.0.3, 21.0.13.0.3, 25.0.5.0.3', 'bai.md') == []


class TestHinhPhinh:
    def test_goi_y_hinh_thoi_tinh_theo_nua_giua(self):
        # a diamond holds text in its middle half: the box formula said 206 for a one-liner that needed about 320
        sk = [{'id': 'd', 'type': 'diamond', 'x': 0, 'y': 0, 'width': 200, 'height': 80, 'strokeColor': '#000',
               'label': {'text': 'Có thẻ BHYT không?', 'fontSize': 16}}]
        conv = [{'id': 'd', 'type': 'diamond', 'x': 0, 'y': 0, 'width': 200, 'height': 150, 'strokeColor': '#000',
                 'backgroundColor': 'transparent', 'angle': 0}]
        cung, _ = ve.soat(conv, {}, [], [], sk)
        assert len(cung) == 1 and 'middle half' in cung[0]
        can = int(cung[0].split('`w` at least 2 × text width + 24 = ')[1].split(',')[0])
        assert can >= 320


# ── sáu chỗ hở còn mở sau bộ 13 hình mẫu ────────────────────────────
class TestChoHoCuoi:
    def test_yticks_ve_nhan_truc_y(self):
        sk, *_ = ve.dung([{'t': 'plot', 'x': 60, 'y': 260, 'w': 200, 'h': 200, 'max': 100,
                           'bars': [{'value': 40}], 'yticks': [{'value': 50, 'label': '50'}, {'at': 1, 'label': '100'}]}])
        ys = {o['text']: o['y'] for o in sk if o['type'] == 'text' and o['text'] in ('50', '100')}
        assert set(ys) == {'50', '100'} and ys['100'] < ys['50']       # 100 sits above 50

    def test_span_doc(self):
        sk, *_ = ve.dung([{'t': 'span', 'dir': 'y', 'x': 300, 'y1': 60, 'y2': 260, 'text': '200 ms'}])
        main = next(o for o in sk if o['type'] == 'line' and o.get('points') and o['points'][1][0] == 0)
        assert main['points'][1][1] == 200                              # vertical, 200 long
        txt = next(o for o in sk if o['type'] == 'text')
        assert txt['x'] > 300                                           # label on the right by default

    def test_er_dung_mot_hai_vach(self):
        sk, *_ = ve.dung([{'t': 'box', 'id': 'a', 'x': 0, 'y': 0, 'w': 100, 'h': 50},
                          {'t': 'box', 'id': 'b', 'x': 0, 'y': 200, 'w': 100, 'h': 50},
                          {'t': 'arrow', 'from': 'a', 'to': 'b', 'tail': 'exactly-one', 'head': 'many'}])
        assert any(str(o.get('id', '')).startswith('_bar') for o in sk)
        ar = next(o for o in sk if o['type'] == 'arrow' and o.get('startArrowhead'))
        assert ar['startArrowhead'] == 'crowfoot_one'

    def test_swimlane_thanh_re_nhanh(self):
        spec = [{'t': 'swimlane', 'x': 0, 'y': 0, 'lanes': [{'id': 'a', 'label': 'A'}, {'id': 'b', 'label': 'B'}],
                 'nodes': [{'id': 's', 'lane': 'a', 'row': 0, 'text': 'S'},
                           {'id': 'f', 'lane': 'a', 'row': 1, 'kind': 'bar', 'w': 200},
                           {'id': 'x', 'lane': 'a', 'row': 2, 'text': 'X'},
                           {'id': 'y', 'lane': 'b', 'row': 2, 'text': 'Y'}],
                 'edges': [{'from': 's', 'to': 'f'}, {'from': 'f', 'to': 'x'}, {'from': 'f', 'to': 'y'}]}]
        sk, _, hinh, lint, _ = ve.dung(spec)
        assert hinh['f']['h'] == 8
        cung, nhac = ve.soat([], hinh, lint, [], sk)
        assert not any('same direction' in n for n in nhac)             # the shared trunk of a fork is the point

    def test_mui_ten_cat_mui_ten(self):
        def pts(a, b):
            return (None, None, [a, b], 1, {'t': 'arrow'})
        _, nhac = ve.soat([], {}, [pts((0, 0), (100, 100)), pts((0, 100), (100, 0))], [])
        assert any('crosses arrow' in n for n in nhac)
        gio = (None, None, [(0, 100), (100, 0)], 1, {'t': 'arrow', 'color': 'muted'})
        _, nhac = ve.soat([], {}, [pts((0, 0), (100, 100)), gio], [])
        assert not any('crosses arrow' in n for n in nhac)

    def test_chu_de_len_vien_o_bang(self):
        o = {'type': 'rectangle', 'id': 'c1', 'x': 0, 'y': 0, 'width': 100, 'height': 40, 'strokeColor': '#000',
             'backgroundColor': 'transparent'}
        chu = {'type': 'text', 'id': 't1', 'x': 90, 'y': 8, 'width': 40, 'height': 22, 'text': '1,234', 'fontSize': 16}
        _, nhac = ve.soat([o, chu], {}, [], [])
        assert any('crosses the border' in n or 'straddles' in n for n in nhac)


# ── sửa lỗi macro, kiểm tương phản nền tối, đầu mũi tên, dịch nhãn ──
class TestCaiTienHeThong:
    def test_sequence_step_hep_khong_de_khung_alt(self):
        spec = [{'t': 'sequence', 'x': 0, 'y': 0, 'gap': 200, 'step': 34,
                 'actors': [{'id': 'a', 'label': 'A'}, {'id': 'b', 'label': 'B'}],
                 'messages': [
                     {'from': 'a', 'to': 'b', 'text': 'msg 1'},
                     {'alt': 'ok'},
                     {'from': 'b', 'to': 'a', 'text': 'msg 2'},
                     {'else': 'err'},
                     {'from': 'b', 'to': 'a', 'text': 'msg 3'},
                     {'end': True}]}]
        els = ve.bung(spec)
        arrows = [e for e in els if e['t'] == 'arrow']
        frame = next(e for e in els if e['t'] == 'box' and e.get('under'))
        sep = next(e for e in els if e['t'] == 'line' and e.get('dashed') and '~life~' not in str(e.get('id', '')))
        y_m1 = arrows[0]['points'][0][1]
        y_m2 = arrows[1]['points'][0][1]
        y_m3 = arrows[2]['points'][0][1]
        assert frame['y'] >= y_m1 + 10
        assert sep['points'][0][1] >= y_m2 + 10
        assert frame['y'] + frame['h'] >= y_m3 + 12

    def test_sequence_bao_loi_actor_khong_ton_tai(self):
        spec = [{'t': 'sequence', 'x': 0, 'y': 0, 'actors': [{'id': 'a', 'label': 'A'}],
                 'messages': [{'from': 'a', 'to': 'ghost', 'text': 'hi'}]}]
        with pytest.raises(ve.Loi, match="to='ghost' matches no actor"):
            ve.dung(spec)

    def test_stack_neo_om_het_lop_sau(self):
        _, _, hinh, lint, _ = ve.dung([
            {'t': 'box', 'id': 'lb', 'x': 0, 'y': 100, 'w': 60, 'h': 60, 'text': 'LB'},
            {'t': 'stack', 'id': 's', 'x': 100, 'y': 100, 'w': 120, 'h': 60, 'n': 4, 'text': 'web'},
            {'t': 'box', 'id': 'b', 'x': 300, 'y': 100, 'w': 100, 'h': 60, 'text': 'db'},
            {'t': 'arrow', 'from': 'lb', 'to': 's'},
            {'t': 'arrow', 'from': 's', 'to': 'b'}])
        # n=4 -> offset = 3 * 8 = 24: front box stays (100, 100, 120, 60) so lb->s stays level (y=130),
        # while padR=24 pushes s->b past the back boxes (x >= 244).
        assert hinh['s']['padR'] == 24 and hinh['s']['padT'] == 24
        assert lint[0][2][0][1] == lint[0][2][-1][1] == 130
        assert lint[1][2][0][0] >= 244 and lint[1][2][0][1] == 130

    def test_badge_ha_mau_chu_khi_nen_toi_thap_tuong_phan(self):
        els = ve.bung([{'t': 'badge', 'x': 0, 'y': 0, 'n': 1, 'color': 'l4'}])
        num = next(e for e in els if e.get('ghost'))
        assert num['color'] == 'ink'

    def test_cells_grid_table_ho_tro_textColor(self):
        els = ve.bung([
            {'t': 'cells', 'id': 'c', 'x': 0, 'y': 0, 'cw': 40, 'ch': 30, 'labels': ['A', '='],
             'marks': {'1': {'color': 'muted', 'textColor': 'muted'}}},
            {'t': 'table', 'id': 'tb', 'x': 0, 'y': 60, 'cols': [60], 'rows': [['v']],
             'marks': {'0,0': {'color': 'err', 'textColor': 'ink'}}},
            {'t': 'grid', 'id': 'g', 'x': 0, 'y': 120, 'cw': 40, 'ch': 30, 'rows': [['X']],
             'marks': {'0,0': {'color': 'l4', 'textColor': 'ink', 'dashed': True}}}])
        c1 = next(e for e in els if e.get('id') == 'c.1')
        assert c1['textColor'] == 'muted'
        g0 = next(e for e in els if e.get('id') == 'g.0.0')
        assert g0['textColor'] == 'ink' and g0['dashed'] is True
        tb0 = next(e for e in els if e.get('id') == 'tb.0.0')
        assert tb0['textColor'] == 'ink'

    def test_group_dim_giu_code_fg_va_ha_textColor(self):
        els = ve.bung([{'t': 'group', 'dim': True, 'elements': [
            {'t': 'code', 'id': 'cd', 'x': 0, 'y': 0, 'text': 'x = 1'},
            {'t': 'box', 'id': 'b', 'x': 0, 'y': 100, 'w': 100, 'h': 40, 'text': 'hi', 'textColor': 'l4'}]}])
        code_txt = next(e for e in els if e.get('t') == 'text' and e.get('text') == 'x = 1')
        assert code_txt['color'] == 'code-fg' and code_txt['opacity'] == 65
        box = next(e for e in els if e.get('id') == 'b')
        assert box['textColor'] == 'muted'

    def test_note_chuyen_tiep_route_va_fromAt(self):
        els = ve.bung([
            {'t': 'box', 'id': 'a', 'x': 0, 'y': 0, 'w': 100, 'h': 50},
            {'t': 'note', 'x': 200, 'y': 100, 'text': 'chú thích', 'to': 'a', 'route': 'hv', 'toSide': 'right', 'toAt': 0.2}])
        ar = next(e for e in els if e['t'] == 'arrow')
        assert ar['route'] == 'hv' and ar['toSide'] == 'right' and ar['toAt'] == 0.2 and ar.get('note_ptr') is True

    def test_payload_bo_qua_duong_gach_ngang(self):
        cung, nhac = _doc([{'t': 'text', 'x': 0, 'y': 0, 'text': '--------------------'}], 'vulnerability')
        assert not cung and not any('attack input' in n for n in nhac)

    def test_so_voi_nguon_bo_qua_chi_so_o_va_vach_giua_nhung_giu_hai_dau(self):
        conv = [
            {'type': 'text', 'id': 'c~idx~15', 'text': '15'},
            {'type': 'text', 'id': 'ax~tick~0', 'text': '10'},
            {'type': 'text', 'id': 'ax~tick~1', 'text': '25'},
            {'type': 'text', 'id': 'ax~tick~2', 'text': '40'},
            {'type': 'text', 'id': 'ax~tick~3', 'text': '99'},
        ]
        nhac = ve.so_voi_nguon(conv, 'runs from 10 to 50', 'bai.md')
        # 15 (cell index) and 25, 40 (intermediate axis ticks) are skipped; 99 (endpoint) is still flagged
        assert len(nhac) == 1 and ': 99.' in nhac[0] and '15' not in nhac[0] and '25' not in nhac[0]

    def test_fromAt_khong_co_fromSide_duoc_nhac(self):
        _, _, hinh, lint, goc = ve.dung(HOP[:2] + [{'t': 'arrow', 'from': 'a', 'to': 'm', 'fromAt': 0.2}])
        _, nhac = ve.soat([], hinh, lint, goc)
        assert any('fromAt without fromSide' in n for n in nhac)

    def test_nhan_mui_ten_cham_dau_mui_ten(self):
        ar = {'type': 'arrow', 'id': 'ar1', 'x': 0, 'y': 0, 'width': 68, 'height': 0,
              'endArrowhead': 'arrow', 'startArrowhead': None}
        lb = {'type': 'text', 'id': 't1', 'containerId': 'ar1', 'x': 15, 'y': -10, 'width': 38, 'height': 20, 'text': 'chưa'}
        _, nhac = ve.soat([ar, lb], {}, [], [])
        assert any('overlaps its own arrowhead' in n for n in nhac)

    def test_canh_dau_mui_ten_dam_vao_hop(self):
        hinh = {'b': {'t': 'box', 'id': 'b', 'x': 190, 'y': 200, 'w': 50, 'h': 100}}
        # Grazing arrow ends at (189, 232) from (160, 96): tip is 1 unit left of box, right wing stabs inside x=190
        lint = [(None, None, [(160, 96), (189, 232)], 1, {'t': 'arrow'})]
        _, nhac = ve.soat([], hinh, lint, [])
        assert any('arrowhead wing' in n and "'b'" in n for n in nhac)

    def test_mui_ten_chi_cham_dau_mui_ten_khac(self):
        # Both tip landing on arrowhead and shaft shooting across arrowhead are caught
        for ptr_pts in ([(300, 100), (205, 100)], [(300, 96), (160, 102)]):
            lint = [
                (None, None, [(0, 100), (200, 100)], 1, {'t': 'arrow'}),
                (None, None, ptr_pts, 1, {'t': 'arrow', 'dashed': True, 'weight': 1, 'color': 'muted'}),
            ]
            _, nhac = ve.soat([], {}, lint, [])
            assert any("another arrow's arrowhead" in n for n in nhac)

    def test_chu_trong_hop_khong_bao_gia_vuot_vien(self):
        # Text inside box with 99% area inside and < 3px protrusion on Patrick Hand span should NOT trigger
        box = {'type': 'rectangle', 'id': 'c1', 'x': 0, 'y': 0, 'width': 200, 'height': 60, 'strokeColor': '#000',
               'backgroundColor': 'transparent'}
        txt = {'type': 'text', 'id': 't1', 'x': 10, 'y': 10, 'width': 195, 'height': 36, 'text': 'hello world',
               'fontSize': 16, 'fontFamily': 1, 'textAlign': 'left'}
        _, nhac = ve.soat([box, txt], {}, [], [])
        assert not any('crosses the border' in n for n in nhac)

    def test_tuong_phan_chu_tu_do_tren_nen_dac(self):
        bg = {'type': 'rectangle', 'id': 'data', 'x': 0, 'y': 0, 'width': 300, 'height': 200,
              'strokeColor': 'transparent', 'backgroundColor': ve.T.FILL_LIGHT['fill-l2'], 'fillStyle': 'solid'}
        err_txt = {'type': 'text', 'id': 't1', 'x': 20, 'y': 40, 'width': 120, 'height': 22,
                   'strokeColor': ve.T.LIGHT['err'], 'text': 'dừng 40 phút', 'fontSize': 16}
        ink_txt = {'type': 'text', 'id': 't2', 'x': 20, 'y': 100, 'width': 120, 'height': 22,
                   'strokeColor': ve.T.LIGHT['ink'], 'text': 'dữ liệu', 'fontSize': 16}
        _, nhac = ve.soat([bg, err_txt, ink_txt], {}, [], [])
        assert any("dừng 40 phút" in n and "dark mode" in n for n in nhac)
        assert not any("dữ liệu" in n and "contrast" in n for n in nhac)

    def test_mask_rects_to_paths_them_dem_doc_cho_lo_nhan(self):
        svg = ('<mask id="m1"><rect x="0" y="0" width="200" height="100" fill="var(--pre-fg)"></rect>'
               '<rect x="50" y="40" width="60" height="20" fill="var(--pre-bg)" opacity="1"></rect></mask>')
        out = ve.mask_rects_to_paths(svg)
        assert '<rect' not in out
        assert 'M0 0h200v100h-200Z' in out
        assert 'M50 38h60v24h-60Z' in out

    def test_chua_dich_bat_nhan_tieng_viet_bo_quen(self):
        bang = {
            'SHA-256': 'SHA-256',
            'Bình thường': 'Normal',
            'Bản này viết riêng cho CPU': 'Bản này viết riêng cho CPU',
        }
        assert ve._chua_dich(bang, 'en') == ['Bản này viết riêng cho CPU']
        assert ve._chua_dich(bang, 'vi') == []

    def test_sequence_note_trong_alt_nam_gon_trong_khung(self):
        spec = [{'t': 'sequence', 'x': 0, 'y': 0, 'gap': 200,
                 'actors': [{'id': 'a', 'label': 'A'}, {'id': 'b', 'label': 'B'}],
                 'messages': [
                     {'alt': 'ok'},
                     {'note': 'chi tiết', 'over': ['a', 'b']},
                     {'end': True}]}]
        els = ve.bung(spec)
        frame = next(e for e in els if e['t'] == 'box' and e.get('under'))
        note = next(e for e in els if e['t'] == 'box' and e.get('text') == 'chi tiết')
        assert note['x'] >= frame['x'] + 6
        assert note['x'] + note['w'] <= frame['x'] + frame['w'] - 6

    def test_route_cung_chieu_hv_vh_bi_nhac(self):
        _, _, hinh, lint, goc = ve.dung([
            {'t': 'box', 'id': 'a', 'x': 100, 'y': 0, 'w': 120, 'h': 40},
            {'t': 'box', 'id': 'b', 'x': 0, 'y': 100, 'w': 100, 'h': 40},
            {'t': 'arrow', 'from': 'a', 'to': 'b', 'fromSide': 'bottom', 'toSide': 'top', 'route': 'vh'}])
        _, nhac = ve.soat([], hinh, lint, goc)
        assert any("use 'vhv'" in n for n in nhac)

    def test_so_voi_nguon_bo_qua_day_o_lien_tiep_va_cot_0_den_n_tru_1(self):
        conv = [
            {'type': 'text', 'id': 't0', 'containerId': 'p0.0', 'text': '40'},
            {'type': 'text', 'id': 't1', 'containerId': 'p0.1', 'text': '41'},
            {'type': 'text', 'id': 't2', 'containerId': 'p0.2', 'text': '42'},
            {'type': 'text', 'id': 't3', 'containerId': 'p0.3', 'text': '43'},
        ] + [{'type': 'text', 'id': f'tp:b~tick~{i}', 'text': f'p{i}'} for i in range(12)]
        assert ve.so_voi_nguon(conv, 'topic 12 partition, offset 40 to 43', 'bai.md') == []

    def test_mui_ten_chi_cham_nganh_sau_dau_mui_ten(self):
        # Pointer tip at (454, 519) brushing arrowhead barb of horizontal arrow ending at (492, 523)
        lint = [
            (None, None, [(285, 523), (492, 523)], 1, {'t': 'arrow'}),
            (None, None, [(550, 494), (454, 494), (454, 519)], 1, {'t': 'arrow', 'dashed': True, 'weight': 1, 'color': 'muted'}),
        ]
        _, nhac = ve.soat([], {}, lint, [])
        assert any("another arrow's arrowhead" in n for n in nhac)

    def test_card_mono_du_rong_cho_freetype(self):
        els = ve.m_card({'t': 'card', 'x': 0, 'y': 0, 'mono': True, 'text': 'writes bytes 48-111'})
        box = next(e for e in els if e['t'] == 'box')
        # 19 mono chars at 15px render ~179px at 1x DPR; box needs >= 179 + 28 padding so right border stays clear
        assert box['w'] >= 210

    def test_span_va_plot_ho_tro_textColor(self):
        sp = ve.m_span({'t': 'span', 'x1': 0, 'x2': 100, 'y': 20, 'color': 'l4', 'textColor': 'ink', 'text': 'chưa đọc'})
        assert next(e for e in sp if e['t'] == 'text')['color'] == 'ink'
        pl = ve.m_plot({'t': 'plot', 'x': 0, 'y': 100, 'w': 100, 'h': 80,
                        'bars': [{'label': 'p0', 'value': 10, 'text': '10', 'color': 'l4', 'textColor': 'ink'}]})
        assert next(e for e in pl if e['t'] == 'text' and e['text'] == '10')['color'] == 'ink'
