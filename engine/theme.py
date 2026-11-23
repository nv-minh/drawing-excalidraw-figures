"""Nguồn duy nhất cho hệ màu.

base.css, mermaid và echarts đều đọc từ đây. Nhờ vậy dark mode không bị vỡ ở
sơ đồ: mermaid/echarts nướng ra hex cố định, ta remap chúng về `var(--token)`
rồi `audit()` chặn mọi hex tối còn sót lại — leak mới sẽ làm build đỏ chứ không
âm thầm lên site.
"""
import re

# ── token màu ──────────────────────────────────────────────────
# Khoá = tên biến CSS (không có `--`). Giá trị = (sáng, tối).
TOKENS = {
    'paper':     ('#EDF0F4', '#0D1219'),
    'card':      ('#FFFFFF', '#141C26'),
    'ink':       ('#111A2B', '#E8EEF7'),
    'muted':     ('#5C6B82', '#93A3BA'),
    'line':      ('#C9D4E3', '#2A3746'),
    'fill-soft': ('#F2F6FB', '#1B2532'),
    # màu mã hoá tầng OSI + mức nghiêm trọng — sáng hơn ở dark để đủ tương phản
    'l2':        ('#64748B', '#8B9AB0'),
    'l3':        ('#008F79', '#64D3C2'),
    'l4':        ('#1E5AE8', '#5B8DFF'),
    'l6':        ('#8F74BE', '#B49ADD'),
    'l7':        ('#4D3399', '#7C5FFF'),
    'err':       ('#D6294B', '#FF6B85'),
    'warn':      ('#E8930C', '#F0A93A'),
    'node':      ('#14621C', '#479A46'),
    # màu của khoá học không gộp được vào họ nào sẵn có
    'heap':      ('#96470C', '#D99456'),   # dữ liệu thật nằm trên đĩa
    'hot':       ('#BE1D72', '#F27BC4'),   # đường đi của query đang chạy
}

LIGHT = {k: v[0] for k, v in TOKENS.items()}
DARK  = {k: v[1] for k, v in TOKENS.items()}

# Token chỉ dùng cho CSS — KHÔNG tham gia remap màu sơ đồ.
# Tách riêng vì `tokenize()` tra ngược hex → token; thêm token có hex trùng
# (vd pre-bg cũng là #111A2B như ink) sẽ làm bảng tra nhập nhằng.
UI_TOKENS = {
    'code-bg':   ('#F2F6FB', '#1B2532'),
    'code-fg':   ('#0C3A9E', '#9DC0FF'),
    'code-line': ('#E1E9F3', '#2A3746'),
    'line-strong': ('#AEBBCC', '#3A4655'),  # kẻ nhấn, viền khung code
    'pre-bg':    ('#111A2B', '#080D14'),
    'pre-fg':    ('#DCE6F5', '#C9D8EE'),
    'chip-fg':   ('#FFFFFF', '#0D1219'),
    'mark-bg':   ('#FFF0B8', '#5A4A12'),
    'hot-bg':    ('#FDF0F2', '#3A1520'),
    'hot-line':  ('#F3C6CE', '#5E2634'),
    'ok-bg':     ('#EFFAF6', '#0F2A22'),
    'ok-line':   ('#B9E5D6', '#1F5145'),
    'overlay':   ('rgba(17,26,43,.55)', 'rgba(0,0,0,.66)'),
    'shadow':    ('rgba(17,26,43,.07)', 'rgba(0,0,0,.45)'),
    'hover':     ('#FFFFFF', '#1F2A38'),
    # Nhận diện "Sổ tay bản vẽ" - CHỈ cho phần khung (nền trang, dòng kẻ ô).
    # Giấy kẻ ô nằm DƯỚI các bề mặt --card (trắng / #141C26), nên --bg phải đủ
    # sẫm hơn --card ở theme sáng và đủ tối ở theme tối để thẻ nổi lên. --grid
    # là nét mảnh trên --bg, cố ý chỉ lệch ~1,1:1: nó là hoạ tiết nền, không
    # mang thông tin. KHÔNG thay --paper: --paper vẫn là nền của sơ đồ và bài
    # đọc, hàng nghìn phép đo tương phản dựa vào nó. tools/contrast.py::
    # gate_chrome_tokens() đo chữ và màu chủ đề trên --bg.
    # Màu "thật" của vật thể (bướm sẫm, thân cây ám khói, tờ giấy trắng): GIỐNG
    # NHAU ở cả hai theme, vì nghĩa của hình nằm ở chính độ sáng tối đó. Mọi
    # token khác đảo ở dark mode, nên một con bướm sẫm vẽ bằng `ink` sẽ thành
    # bướm sáng - hai lần chạy eval chọn lọc tự nhiên đều vấp đúng chỗ này.
    # Không mang chữ: --ink tự đảo nên luôn có một theme chữ chìm vào nền này.
    'lit-dark':  ('#24272D', '#24272D'),
    'lit-light': ('#F4EFE4', '#F4EFE4'),
    'bg':        ('#E8EDF4', '#0A1526'),
    'grid':      ('#D5DEEA', '#13223A'),
}

# Màu syntax highlight. KHÔNG vào TOKENS: `_BY_HEX` tra ngược hex - token và chỉ
# dựng từ LIGHT của TOKENS, nên thêm vào đó sẽ làm bảng tra màu sơ đồ nhập nhằng.
#
# Vì sao lấy bản DARK cho CẢ HAI theme: nền code là `--pre-bg`, tối ở cả hai
# theme (#111A2B / #080D14) - nó là token duy nhất không đảo. Bản light của
# token tầng được chọn để nằm trên nền SÁNG nên đặt lên đây thì thiếu tương
# phản; đo thật: --l7 chỉ được 2,90:1. Bản dark đạt 5,36–8,55.
CODE_TOKENS = {
    'code-kw':  (DARK['l4'],    DARK['l4']),      # keyword, toán tử
    'code-str': (DARK['l3'],    DARK['l3']),      # chuỗi, template
    'code-com': (DARK['muted'], DARK['muted']),   # comment
    'code-num': (DARK['l6'],    DARK['l6']),      # số, hằng, null
    'code-fn':  (DARK['l7'],    DARK['l7']),      # tên hàm, method
    'code-typ': (DARK['l2'],    DARK['l2']),      # type, class, interface
    'code-bad': (DARK['err'],   DARK['err']),     # marker ❌
    'code-ok':  (DARK['node'],  DARK['node']),    # marker ✅
}

# Tint nhạt của tám màu tầng/mức nghiêm trọng, dùng làm NỀN ĐẶC (fill) cho
# hình khối Excalidraw - "mảng màu phẳng bên trong mỗi ô" là khác biệt lớn
# nhất so với bản outline-only cũ (xem engine/excalidraw.py VÁ 6). Khác
# UI_TOKENS/CODE_TOKENS (đứng NGOÀI _BY_HEX để khỏi làm nhập nhằng bảng tra
# màu sơ đồ - hai nhóm đó không bao giờ xuất hiện trong SVG nướng sẵn), tám
# token này LÀ màu sơ đồ thật: excalidraw.py tự đặt ĐÚNG BẰNG các hex này làm
# backgroundColor, nên chúng PHẢI tham gia _BY_HEX để tokenize() ánh xạ ngược
# lại - xem đoạn `_BY_HEX.update(...)` bên dưới.
#
# Đảo giá trị y như mọi token khác (nhạt ở theme sáng, TỐI ở theme tối) để chữ
# --ink - cũng tự đảo - luôn đọc được: --ink tối ở theme sáng cần nền đủ
# sáng, --ink sáng ở theme tối cần nền đủ tối. Đo bằng
# tools/contrast.py::gate_fill_tokens(), ngưỡng 4,5:1 - khắt hơn cổng chung
# 3:1 (MIN ở tools/contrast.py) vì đây là nền mang chữ cỡ thân bài bên trong
# hộp sơ đồ, không phải viền/nhãn trang trí. Cả 8 tint đạt ≥5,25:1 ở cả hai
# theme, dư khá xa ngưỡng (xem bảng in ra từ gate_fill_tokens()).
FILL_TOKENS = {
    'fill-l2':   ('#D4D8DF', '#4A5462'),
    'fill-l3':   ('#A0F2E3', '#00433A'),
    'fill-l4':   ('#C0D1F9', '#324E8A'),
    'fill-l6':   ('#E7D5FF', '#45375B'),
    'fill-l7':   ('#EDDAFF', '#3F325C'),
    'fill-err':  ('#F4C3CD', '#843C4C'),
    'fill-warn': ('#F9E1BB', '#7D5C27'),
    'fill-node': ('#C5EDBF', '#1E411D'),
    'fill-heap': ('#F5E3C6', '#4A3418'),
    'fill-hot':  ('#F9D8EA', '#4A1D38'),
}

FILL_LIGHT = {k: v[0] for k, v in FILL_TOKENS.items()}

FONTS = {
    'sans': "'Be Vietnam Pro',system-ui,sans-serif",
    'mono': "'IBM Plex Mono','Be Vietnam Pro',ui-monospace,monospace",
    # Hai font của phần khung. KHÔNG bao giờ đặt lên body/main/.dgc/.keybox hay
    # thứ gì một SVG nội tuyến có thể kế thừa: sơ đồ đo bề rộng chữ theo
    # --sans/--mono, đổi font kế thừa là lệch phép đo. Chỉ dùng qua selector
    # tường minh cho tiêu đề trang khung (display) và nhãn bản đồ (hand).
    'display': "'Bricolage Grotesque','Be Vietnam Pro',system-ui,sans-serif",
    'hand':    "'Patrick Hand','Be Vietnam Pro',system-ui,sans-serif",
}

# Thang đo của phần khung. Khác màu, thang đo KHÔNG đổi theo theme nên chỉ phát
# một lần ở khối :root sáng. Tên `--r-*` chứ không phải `--radius-*`: Tailwind
# v4 đã dùng `--radius-*` làm biến theme (src/styles/course.css) và hai bên sẽ
# đè nhau.
SCALE = {
    'sp-1': '4px',  'sp-2': '8px',  'sp-3': '12px', 'sp-4': '16px',
    'sp-5': '24px', 'sp-6': '32px', 'sp-7': '48px', 'sp-8': '64px',
    'r-1': '4px',   'r-2': '8px',   'r-3': '14px',
}

# ── alias: tên của khoá học trỏ vào token sẵn có ─────────────────
# Khoá học mang theo bảng màu ngữ nghĩa riêng. Nhét thêm tám màu cạnh tám màu
# cũ sẽ tạo ra năm cặp gần trùng mang nghĩa khác nhau: người đọc thấy teal sẽ
# không biết nó là "tầng giao vận" hay "đang nằm trong RAM".
#
# Thay vào đó, những cặp vốn cùng họ màu được GỘP, và tên của khoá thành alias.
# Một sắc độ mang một nghĩa, cả site đọc như một hệ, và code của khoá không
# phải sửa dòng nào: `var(--cache)` vẫn chạy, chỉ là nó trỏ vào `var(--l3)`.
#
# Alias KHÔNG vào TOKENS: TOKENS tham gia _BY_HEX để tokenize() tra ngược
# hex - token cho SVG nướng sẵn, mà alias không có hex nào để tra.
ALIASES = {
    # màu ngữ nghĩa của khoá
    'index':  'l4',     # cấu trúc tra cứu, B-tree
    'cache':  'l3',     # đang nằm trong RAM
    'wal':    'l6',     # bản ghi bền vững
    'lock':   'err',    # chờ khoá, xung đột
    'good':   'node',   # cách làm đúng
    'dead':   'l2',     # tuple chết, cần dọn
    'container': 'l7',  # ranh giới của một tiến trình
    'wire': 'l4',       # kết nối, byte trên dây
    'queue': 'l7',      # hàng đợi, tin chờ được chuyển
    # bề mặt
    'sunk':   'fill-soft',   # mặt chìm: khối code, ô nhập
    # nền đặc cùng nghĩa, dùng làm fill cho hình trong sơ đồ
    'fill-index': 'fill-l4',
    'fill-cache': 'fill-l3',
    'fill-wal':   'fill-l6',
    'fill-lock':  'fill-err',
    'fill-good':  'fill-node',
    'fill-dead':  'fill-l2',
    'fill-container': 'fill-l7',
    'fill-wire': 'fill-l4',
    'fill-queue': 'fill-l7',
    # màu cho mark trong biểu đồ của khoá: cùng sắc với token tầng, chỉ khác
    # vai trò, nên không cần sắc riêng.
    'mark-index':  'l4',
    'mark-bitmap': 'l3',
    'mark-seq':    'warn',
    # shiki của khoá phát ra ĐÚNG những tên này. Đặt tên khác đi thì code
    # trong bài vẫn hiện, chỉ là không màu - và cổng tương phản vẫn xanh vì
    # nó đo những token không ai dùng. Đã dính một lần thật ở repo khoá.
    'shiki-foreground':              'pre-fg',
    'shiki-background':              'fill-soft',
    'shiki-token-keyword':           'code-kw',
    'shiki-token-string':            'code-str',
    'shiki-token-string-expression': 'code-str',
    'shiki-token-comment':           'code-com',
    'shiki-token-constant':          'code-num',
    'shiki-token-function':          'code-fn',
    'shiki-token-punctuation':       'muted',
    'shiki-token-parameter':         'pre-fg',
    'shiki-token-link':              'code-kw',
}


def _block(sel, which):
    rows = [f'  --{k}:{v[which]};' for k, v in TOKENS.items()]
    rows += [f'  --{k}:{v[which]};' for k, v in UI_TOKENS.items()]
    rows += [f'  --{k}:{v[which]};' for k, v in CODE_TOKENS.items()]
    rows += [f'  --{k}:{v[which]};' for k, v in FILL_TOKENS.items()]
    if which == 0:
        # Alias và font chỉ khai ở khối SÁNG. var() phân giải lại theo giá trị
        # hiện hành của token đích trên cùng element, nên một lần khai là đúng
        # ở cả hai theme - khai lại ở khối dark chỉ tạo thêm một bản để trôi.
        rows += [f'  --{k}:var(--{v});' for k, v in ALIASES.items()]
        rows += [f'  --{k}:{v};' for k, v in FONTS.items()]
        rows += [f'  --{k}:{v};' for k, v in SCALE.items()]
    return sel + '{\n' + '\n'.join(rows) + '\n}'


def stylesheet():
    """tokens.css — sáng mặc định, tối theo hệ thống, và [data-theme] thắng cả hai.

    Ba khối là cố ý: người chưa chọn gì thì theo hệ thống; người bấm nút toggle
    thì `data-theme` phải thắng ở CẢ hai chiều, nên khối dark phải xuất hiện
    dưới cả `prefers-color-scheme` (loại trừ data-theme=light) và `[data-theme=dark]`.
    """
    return '\n\n'.join([
        '/* Sinh bởi engine/theme.py — đừng sửa tay. */',
        _block(':root', 0),
        '@media (prefers-color-scheme:dark){\n' +
        _block(':root:not([data-theme="light"])', 1) + '\n}',
        _block(':root[data-theme="dark"]', 1),
    ]) + '\n' 


# ── theme cho mermaid (build từ token sáng) ────────────────────
MERMAID_THEME = {
    'primaryColor':        LIGHT['fill-soft'],
    'primaryTextColor':    LIGHT['ink'],
    'primaryBorderColor':  LIGHT['l4'],
    'secondaryColor':      '#EFFAF6',
    'tertiaryColor':       '#FFF8EC',
    'background':          LIGHT['card'],
    'mainBkg':             LIGHT['fill-soft'],
    'nodeBorder':          LIGHT['l4'],
    'nodeTextColor':       LIGHT['ink'],
    'textColor':           LIGHT['ink'],
    'titleColor':          LIGHT['ink'],
    'lineColor':           LIGHT['muted'],
    'defaultLinkColor':    LIGHT['muted'],
    'edgeLabelBackground': LIGHT['card'],
    'labelTextColor':      LIGHT['ink'],
    'labelBoxBkgColor':    LIGHT['fill-soft'],
    'labelBoxBorderColor': LIGHT['line'],
    'clusterBkg':          LIGHT['fill-soft'],
    'clusterBorder':       LIGHT['line'],
    'actorBkg':            LIGHT['fill-soft'],
    'actorBorder':         LIGHT['l4'],
    'actorTextColor':      LIGHT['ink'],
    'actorLineColor':      LIGHT['line'],
    'signalColor':         LIGHT['ink'],
    'signalTextColor':     LIGHT['ink'],
    'noteBkgColor':        '#FFF8EC',
    'noteTextColor':       LIGHT['ink'],
    'noteBorderColor':     LIGHT['warn'],
    'sequenceNumberColor': LIGHT['card'],
    'altBackground':       LIGHT['fill-soft'],
    # Chỉ chi phối ~24/1261 sơ đồ "mermaid fallback" (stateDiagram-v2/erDiagram/
    # subgraph - loại bộ chuyển Excalidraw không đỡ, xem bẫy 16 CLAUDE.md).
    # 1237 scene Excalidraw KHÔNG đọc giá trị này: engine/excalidraw.py:389 gọi
    # bộ chuyển mermaid->excalidraw với { fontSize: 16 } hardcode ngay tại chỗ
    # gọi. Giá trị 16px ở đây và 16 hardcode ở excalidraw.py trùng nhau do
    # TRÙNG HỢP của lần đổi này, không do cấu tạo - đổi số này không kéo theo
    # excalidraw.py, và ngược lại.
    'fontSize':            '16px',
}

ECHARTS_THEME = {
    'color': [LIGHT['l4'], LIGHT['l3'], LIGHT['l7'],
              LIGHT['warn'], LIGHT['err'], LIGHT['l2']],
    # 15px tràn khung (verify.py đo 118 lỗi): yAxis.name render text-anchor="middle",
    # neo tại trục (~80px từ trái) - chữ đơn vị dài (quy ước kho: đơn vị đặt ở
    # yAxis.name) đẩy MÉP TRÁI ra ngoài canvas, không phải mép phải như tưởng
    # ban đầu. Hạ 1 mức xuống 14px theo đúng cơ chế Step 4 (hạ mức, nướng lại,
    # kiểm lại) giảm được 118→72 lỗi; phần còn lại sửa ở từng file markdown
    # bằng nameTextStyle.align:"left" (đổi neo, chữ kéo dài sang phải - dư
    # ~500-600px) và grid.right/top cho vài biểu đồ label cạnh bar/tràn trên.
    'textStyle': {'fontFamily': 'Be Vietnam Pro, system-ui, sans-serif',
                  'color': LIGHT['ink'], 'fontSize': 14},
    'backgroundColor': 'transparent',
    'grid': {'left': 52, 'right': 20, 'top': 34, 'bottom': 34, 'containLabel': True},
    # axisLabel (số trên trục, tên hạng mục) KHÔNG đọc textStyle.fontSize ở trên -
    # ECharts cho nó một mặc định 12px riêng, và đây là loại chữ xuất hiện NHIỀU
    # NHẤT trong mọi biểu đồ (vd 13 lần/biểu đồ so với 1-2 lần của tên trục).
    # Phải khai fontSize riêng ở đây thì tick label mới lên cùng tầng với tên trục.
    # 14px tràn 8 lỗi (số lớn có dấu phẩy, nhãn hạng mục dài) - hạ xuống 13px.
    'xAxis': {'axisLine': {'lineStyle': {'color': LIGHT['line']}},
              'axisLabel': {'color': LIGHT['muted'], 'fontSize': 13},
              'splitLine': {'lineStyle': {'color': LIGHT['line']}}},
    # nameTextStyle.align:"left" mặc định cho MỌI yAxis một trục: yAxis.name
    # neo gần trục trái (xem comment tràn trái ở trên), căn trái cho chữ kéo
    # dài sang phải thay vì lấn trái - và làm 386 biểu đồ neo GIỐNG NHAU thay
    # vì để lẻ tẻ vài chục biểu đồ neo trái cạnh phần lớn còn lại neo giữa.
    # merge() ở engine/echarts.cjs:6-13 THAY THẾ TOÀN BỘ (không merge đệ quy)
    # khi giá trị override là MẢNG - yAxis dạng nhiều trục ("yAxis":[{...}]) vì
    # thế không nhận được default này, phải khai nameTextStyle riêng ở từng
    # phần tử mảng đó (xem content/database/01-van-hanh-tuning.md).
    'yAxis': {'axisLine': {'lineStyle': {'color': LIGHT['line']}},
              'axisLabel': {'color': LIGHT['muted'], 'fontSize': 13},
              'nameTextStyle': {'align': 'left'},
              'splitLine': {'lineStyle': {'color': LIGHT['line']}}},
    'legend': {'textStyle': {'color': LIGHT['muted']}},
    'title': {'textStyle': {'color': LIGHT['ink']}},
}


# ── remap hex → var(--token) ───────────────────────────────────
# Gồm token của ta + màu mermaid/echarts tự sinh mà ta không điều khiển được.
_BY_HEX = {v.upper(): k for k, v in LIGHT.items()}
# FILL_TOKENS THAM GIA _BY_HEX - khác UI_TOKENS/CODE_TOKENS (đứng ngoài vì
# chúng không phải màu sơ đồ). Tint fill LÀ màu sơ đồ thật do excalidraw.py
# tự đặt, nên phải tra ngược được về đúng token 'fill-xxx', không rơi vào
# _nearest() đoán mò (mọi tint đều có luminance < 0,86 nên audit() sẽ coi là
# "chưa remap" nếu tokenize() không bắt được - xem audit() bên dưới).
_BY_HEX.update({v.upper(): k for k, v in FILL_LIGHT.items()})

LEAKED = {           # màu mermaid nhúng cứng, không đến từ themeVariables
    '#000000': 'ink', '#000': 'ink', '#0B0B0B': 'ink', '#000713': 'ink',
    '#333333': 'ink', '#333': 'ink',
    '#666666': 'muted', '#666': 'muted', '#999999': 'muted', '#999': 'muted',
    '#F4F4F4': 'fill-soft', '#EAEAEA': 'fill-soft', '#E0E0E0': 'line',
    '#ECECFF': 'fill-soft', '#9370DB': 'l7', '#CCCCFF': 'fill-soft',
    '#B9B9B9': 'line',
    '#EFFAF6': 'fill-soft', '#FFF8EC': 'fill-soft',
    '#FFF5AD': 'warn', '#EDF2AE': 'warn', '#A3947D': 'muted',
    # mặc định của echarts
    '#CCCCCC': 'line', '#E0E6F1': 'line', '#6E7079': 'muted', '#B9B8CE': 'muted',
    '#464646': 'ink', '#2163FF': 'l4', '#5470C6': 'l4', '#333333': 'ink',
    '#AAAAAA': 'muted', '#DDDDDD': 'line', '#EEEEEE': 'fill-soft',
    # Viền emphasis mermaid tự nhúng. Trước Task 4 nó lọt qua NHỜ TÌNH CỜ:
    # cách --l3 cũ (#0E9188) đúng 19,1 nên _nearest() bắt được trong ngưỡng 30.
    # --l3 mới (#008F79) cách nó 35,6 nên rơi ra ngoài và build đỏ ở 2 sơ đồ
    # (frontend/06-react-co-ban-hooks, frontend/21-data-state-nang-cao).
    # Khai tường minh chứ không nới ngưỡng: nới là làm yếu cổng cho cả bảng màu
    # để chữa một màu, còn khai thẳng thì đúng việc LEAKED sinh ra để làm.
    '#0F9F95': 'l3',
}

# Chỉ bốn độ dài CSS chấp nhận (#RGB #RGBA #RRGGBB #RRGGBBAA). Bản {3,8} cũ bắt cả `#1480`
# (5 ký tự) trong nhãn "lỗi #1480", rồi _nearest() chết với
# "invalid literal for int() with base 16".
_COLOR_RE = re.compile(r'#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b|rgba?\([^)]*\)')
_TEXT_RE = re.compile(r'<text\b[^>]*>(.*?)</text>', re.S)


def _text_spans(src):
    """(đầu, cuối) phần chữ của mọi phần tử <text>."""
    return [m.span(1) for m in _TEXT_RE.finditer(src)]


def _in_text(src, i, spans):
    """Vị trí i nằm trong CHỮ của một <text>, không nằm trong thuộc tính.

    Chữ trong hình là nội dung, không bao giờ là màu: "issue #123" từng thành
    "issue var(--ink)", còn "lỗi #1480" làm render chết. Màu chỉ nằm trong giá trị
    thuộc tính và khối <style>.
    """
    for a, b in spans:
        if a <= i < b:
            return src.rfind('<', a, i) <= src.rfind('>', a, i)
        if a > i:
            break
    return False


def _parse_rgb(c):
    """rgb()/rgba() cả cú pháp phẩy và cú pháp khoảng trắng → (#RRGGBB, alpha)."""
    nums = re.findall(r'[\d.]+%?', c)
    if len(nums) < 3:
        return None, 1.0

    def chan(x):
        return int(round(float(x[:-1]) * 255 / 100)) if x.endswith('%') else int(round(float(x)))
    r, g, b = (max(0, min(255, chan(n))) for n in nums[:3])
    a = float(nums[3].rstrip('%')) / (100 if nums[3].endswith('%') else 1) if len(nums) > 3 else 1.0
    return f'#{r:02X}{g:02X}{b:02X}', a


def _canon(c):
    """Chuẩn hoá để tra bảng: hex hoa 6 ký tự. Trả về (hex, alpha)."""
    c = c.strip()
    if c.startswith('#'):
        h = c.upper()
        if re.fullmatch(r'#[0-9A-F]{3,4}', h):          # #RGB, #RGBA
            h = '#' + ''.join(ch * 2 for ch in h[1:])
        if re.fullmatch(r'#[0-9A-F]{8}', h):          # #RRGGBBAA
            return h[:7], int(h[7:], 16) / 255
        return h[:7], 1.0
    return _parse_rgb(c)


def _lum(hx):
    h = hx.lstrip('#')
    if len(h) < 6:
        return 1.0
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255


# Trắng trong đầu ra mermaid/echarts là NỀN nhãn, không phải chữ trên nền đậm.
# Ở dark mode chữ thành sáng, nên nền trắng sẽ che mất chữ → phải là var(--card).
_WHITE = {'#FFFFFF', '#FEFEFE'}


_RGB = {k: tuple(int(v.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        for k, v in LIGHT.items()}

# mermaid/echarts tự dẫn xuất sắc độ sáng-tối từ màu palette (vd #0F9F95 cho
# viền emphasis). Không thể liệt kê hết, nên bắt bằng khoảng cách.
# Ngưỡng 30 an toàn vì cặp token cùng sắc gần nhau nhất là l6↔l7, đo được
# 99,7 ở theme sáng và 88,2 ở tối - không thể gán lẫn sắc. (Con số này từng là
# 42 trước Task 4, khi l6 và l7 còn dùng CHUNG một sắc 307; Task 4 tách chúng
# bằng chroma nên biên an toàn rộng hơn gấp đôi.)
# Lẫn giữa các màu trung tính (paper↔fill-soft = 10) là vô hại vì cả hai đều
# đảo đúng ở dark mode.
_NEAR = 30


def _nearest(hx):
    r, g, b = (int(hx[i:i + 2], 16) for i in (1, 3, 5))
    best, bd = None, 1e9
    for k, (r2, g2, b2) in _RGB.items():
        d = ((r - r2) ** 2 + (g - g2) ** 2 + (b - b2) ** 2) ** 0.5
        if d < bd:
            best, bd = k, d
    return best if bd <= _NEAR else None


def _is_id_ref(src, i):
    """`#abc` tại vị trí i là THAM CHIẾU ID, không phải màu.

    `url(#f2c-arw)` và `href="#f2c-arw"` khớp _COLOR_RE vì `f2c` đều là ký tự hex
    và dấu `-` tạo ranh giới `\b`. Hai hệ quả khác nhau, cái sau nặng hơn:
      · audit()   → cảnh báo giả "hardcode màu #f2c"; agent phải đổi tên marker
                    cho vừa regex (đã xảy ra 2 lần: dbi-4, rồi f2-copy).
      · tokenize() → THAY luôn `#f2c` thành `var(--…)` → `url(#f2c-arw)` trỏ vào
                    id không tồn tại → mũi nhọn biến mất, không có cảnh báo nào.
    Chỉ tham chiếu mới có `#`; `id="f2c-arw"` không có nên không cần loại trừ.
    """
    head = src[max(0, i - 6):i]
    return head.endswith('url(') or head.endswith('href="') or head.endswith("href='")


def tokenize(svg):
    """Đổi mọi màu đã biết trong SVG nướng sẵn thành var(--token).

    Chỉ dùng cho đầu ra mermaid/echarts. SVG viết tay đã dùng token sẵn và
    có `#fff` cố ý (chữ trắng trên nền đậm) — đừng chạy hàm này lên chúng.
    """
    spans = _text_spans(svg)

    def sub(m):
        if _is_id_ref(m.string, m.start()) or _in_text(m.string, m.start(), spans):
            return m.group(0)
        hx, _a = _canon(m.group(0))
        if hx is None:
            return m.group(0)
        if hx in _WHITE:
            return 'var(--card)'
        tok = _BY_HEX.get(hx) or LEAKED.get(hx) or _nearest(hx)
        return f'var(--{tok})' if tok else m.group(0)
    return _COLOR_RE.sub(sub, svg)


# Sau tokenize, chỉ "không màu" mới được phép còn lại ở dạng thô.
_SAFE_RAW = {'NONE', 'TRANSPARENT', 'CURRENTCOLOR'}


def audit(svg):
    """Màu còn sót trong SVG nướng sẵn mà sẽ vỡ ở dark mode. Rỗng = an toàn."""
    bad = set()
    spans = _text_spans(svg)
    for m in _COLOR_RE.finditer(svg):
        raw = m.group(0)
        if raw.strip().upper() in _SAFE_RAW:
            continue
        if _is_id_ref(svg, m.start()) or _in_text(svg, m.start(), spans):
            continue
        hx, a = _canon(raw)
        if hx is None:
            bad.add(raw)
            continue
        if a == 0:                       # trong suốt hoàn toàn — vô hại
            continue
        if _lum(hx) < 0.86:              # đủ tối để lộ trên nền tối
            bad.add(raw)
        elif hx in _WHITE:               # trắng đặc → che chữ ở dark mode
            bad.add(raw)
    return sorted(bad)
