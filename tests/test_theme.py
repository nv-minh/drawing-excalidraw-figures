"""Unit cho engine/theme.py - phần màu chịu lực của cả hệ.

Mỗi hàm ở đây từng gây bug thật (xem docstring trong theme.py):
_is_id_ref tạo cảnh báo giả 2 lần (dbi-4, f2-copy), _NEAR = 30 là ngưỡng
đo đếm được giữa l6/l7. Đổi gì trong theme phải qua các test này.
"""
import theme as T


# ── _canon / _parse_rgb: mọi dạng màu về (#RRGGBB, alpha) ─────────
class TestCanon:
    def test_hex_3_ky_tu(self):
        assert T._canon('#fff') == ('#FFFFFF', 1.0)

    def test_hex_6_thuong(self):
        assert T._canon('#0f9f95') == ('#0F9F95', 1.0)

    def test_hex_8_co_alpha(self):
        hx, a = T._canon('#111A2BAA')
        assert hx == '#111A2B'
        assert abs(a - 0xAA / 255) < 1e-6

    def test_rgb_dau_phay(self):
        assert T._canon('rgb(255, 0, 0)') == ('#FF0000', 1.0)

    def test_rgb_khoang_trang_va_phan_tram(self):
        # 50% cua 255 = 127.5 -> lam tron 128 = 0x80
        assert T._canon('rgb(100%, 0%, 50%)') == ('#FF0080', 1.0)

    def test_rgba_alpha_thap_phan(self):
        hx, a = T._canon('rgba(17, 26, 43, 0.55)')
        assert hx == '#111A2B'
        assert a == 0.55

    def test_khoang_trang_xung_quanh(self):
        assert T._canon('  #FFF  ') == ('#FFFFFF', 1.0)

    def test_khong_phai_mau(self):
        assert T._canon('red') == (None, 1.0)


# ── _is_id_ref: `#abc` là tham chiếu id, không phải màu ───────────
    def test_hex_4_ky_tu_la_rgba(self):
        hx, a = T._canon('#1234')
        assert hx == '#112233'
        assert abs(a - 0x44 / 255) < 1e-6


class TestChuKhongPhaiMau:
    # "lỗi #1480" trong nhãn từng làm render chết (int('', 16)), "issue #123"
    # từng bị đổi âm thầm thành "issue var(--ink)". Chữ là nội dung, không là màu.
    SVG = '<svg><text x="1" fill="#111A2B">issue #123 · lỗi #1480 · #ff0000</text><path fill="#111A2B"/></svg>'

    def test_tokenize_khong_dung_vao_chu(self):
        out = T.tokenize(self.SVG)
        assert 'issue #123 · lỗi #1480 · #ff0000' in out
        assert 'fill="var(--ink)"' in out
        assert '#111A2B' not in out

    def test_audit_bo_qua_chu(self):
        assert T.audit(T.tokenize(self.SVG)) == []

    def test_mau_trong_tspan_van_bat(self):
        svg = '<text>a<tspan fill="#ff0000">b</tspan> #abc</text>'
        assert T.audit(svg) == ['#ff0000']

    def test_5_va_7_ky_tu_khong_phai_mau(self):
        assert not T._COLOR_RE.fullmatch('#14801')
        assert not T._COLOR_RE.fullmatch('#1480123')
        assert T._COLOR_RE.fullmatch('#1480')


class TestIsIdRef:
    def test_url_marker(self):
        # '#f2c' trong url(#f2c-arw) la tham chieu marker, khong duoc remap
        src = 'xxx url(#f2c-arw)'
        i = src.index('#')
        assert T._is_id_ref(src, i) is True

    def test_href(self):
        src = 'href="#f2c"'
        assert T._is_id_ref(src, src.index('#')) is True

    def test_mau_binh_thuong(self):
        src = 'stroke="#f2c"'
        assert T._is_id_ref(src, src.index('#')) is False

    def test_dau_chuoi_khong_co_boi_canh(self):
        assert T._is_id_ref('#fff', 0) is False


# ── tokenize: hex nướng sẵn -> var(--token) ───────────────────────
class TestTokenize:
    def test_token_thang(self):
        assert T.tokenize('<path stroke="#1E5AE8"/>') == '<path stroke="var(--l4)"/>'

    def test_fill_token(self):
        assert T.tokenize('<rect fill="#D4D8DF"/>') == '<rect fill="var(--fill-l2)"/>'

    def test_trang_dat_nen_card(self):
        assert T.tokenize('<rect fill="#FFFFFF"/>') == '<rect fill="var(--card)"/>'

    def test_mau_leak(self):
        # LEAKED: sac do mermaid/echarts tu dan xuat
        assert T.tokenize('<path stroke="#0F9F95"/>') == '<path stroke="var(--l3)"/>'

    def test_gan_dung_bang_khoang_cach(self):
        # trong 30 don vi thi gan ve token gan nhat
        out = T.tokenize('<path stroke="#1F5BE9"/>')   # lech 1/1/1 khoi l4
        assert out == '<path stroke="var(--l4)"/>'

    def test_id_ref_khong_bi_doi(self):
        svg = '<path mask="url(#f2c-arw)" stroke="#1E5AE8"/>'
        assert 'url(#f2c-arw)' in T.tokenize(svg)
        assert 'url(var(' not in T.tokenize(svg)

    def test_mau_la_xa_duoc_giu_nguyen(self):
        # khong thuoc bang nao, qua xa bat ky token nao -> y nguyen vi day la
        # mau chu dinh nghia tay, tokenize khong duoc doan
        assert T.tokenize('<path stroke="#FF00FF"/>') == '<path stroke="#FF00FF"/>'

    def test_hien_tuong_che_mau_khong_xay_ra(self):
        # ca chu va nen cung bi thay cung luc - kiem tra chuoi dai
        svg = '<g stroke="#111A2B"><g fill="#111A2B"/></g>'
        assert T.tokenize(svg).count('var(--ink)') == 2


# ── audit: màu sẽ vỡ ở dark mode ──────────────────────────────────
class TestAudit:
    def test_mau_toi_bi_bat(self):
        assert T.audit('<path stroke="#111111"/>') == ['#111111']

    def test_trang_dac_bi_bat(self):
        assert '#FFFFFF' in T.audit('<rect fill="#FFFFFF"/>')

    def test_trong_suot_hoan_toan_vo_hai(self):
        assert T.audit('<rect fill="rgba(0, 0, 0, 0)"/>') == []

    def test_ten_mau_an_toan(self):
        assert T.audit('<rect fill="none" stroke="transparent" color="currentColor"/>') == []

    def test_id_ref_khong_bi_bao_gia(self):
        assert T.audit('<path mask="url(#f2c-arw)"/>') == []

    def test_mau_sang_khac_trang_khong_bat(self):
        # lum >= 0.86, khong phai trang dat -> khong lo che chu o dark mode
        assert T.audit('<rect fill="#FFFFE0"/>') == []

    def test_alpha_0_trong_hex_8_ky_tu(self):
        assert T.audit('<rect fill="#111A2B00"/>') == []


# ── _nearest: tra hex ngược về token ──────────────────────────────
class TestNearest:
    def test_dung_bang(self):
        assert T._nearest('#8F74BE') == 'l6'

    def test_qua_xa_tra_none(self):
        assert T._nearest('#FF00FF') is None


# ── bất biến hệ màu ───────────────────────────────────────────────
class TestInvariants:
    def test_lit_token_giong_het_ca_hai_theme(self):
        # y nghia cua lit-dark/lit-light la DO SANG THAT cua vat: khong duoc dao
        for k in ('lit-dark', 'lit-light'):
            assert T.UI_TOKENS[k][0] == T.UI_TOKENS[k][1]

    def test_moi_token_do_dao_giua_hai_theme(self):
        # mot token khong dao = dark mode vo tinh mat mot mau; lit-* la ngoai le
        # duy nhat (o UI_TOKENS, da test rieng o tren)
        for bang in (T.TOKENS, T.FILL_TOKENS):
            for k, (s, d) in bang.items():
                assert s != d, f'{k} cung gia tri o ca hai theme'

    def test_lit_hex_song_sot_nho_thu_tu_thay_truoc_tokenize(self):
        # HAI hex lit ĐỀU nằm trong bán kính 30 của một token (_nearest bắt
        # về ink/paper) - đúng cho hex mermaid/echarts, SAI cho lit. Lit chỉ
        # sống sót nhờ ve.py thay hex -> var(--lit-*) TRƯỚC khi gọi tokenize.
        # Đổi thứ tự đó là mất màu thật của vật ở cả hai theme; test golden
        # (test_render_golden.py) xác nhận trên 29 SVG thật.
        assert T._nearest('#24272D') == 'ink'
        assert T._nearest('#F4EFE4') == 'paper'

    def test_dist_tokens_css_khong_drift(self):
        # dist/assets/tokens.css la artifact da commit, sinh boi stylesheet()
        import pathlib
        css = (pathlib.Path(__file__).resolve().parents[1] / 'dist' / 'assets' / 'tokens.css').read_text()
        assert css == T.stylesheet()

    def test_stylesheet_co_lit_o_ca_ba_khoi(self):
        # :root sang, media dark, [data-theme=dark] - lit phai giong het ca ba
        css = T.stylesheet()
        assert css.count('--lit-dark:#24272D;') == 3
        assert css.count('--lit-light:#F4EFE4;') == 3
