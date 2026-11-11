# -*- coding: utf-8 -*-
"""打工人系列任务页「视频同款」批量换肤注入器（dagongren-theme.md 第 3 节的脚本化落地）

用法（批量渲染任务页时）：
    import inject_theme
    THEMED_TPL = inject_theme.themed_template(TPL.read_text(encoding='utf-8'))
    data = {
        ...原任务页占位符...,
        **inject_theme.extra_data(no, name, total_min),   # no='01'，name=任务名，total_min='20'
    }
    # 之后照常做占位符替换，写单文件 HTML。

换肤四步（见 references/dagongren-theme.md）：
  1. skin.css 全文贴到模板 <style> 最后（本函数自动做）；
  2. 900 + Inter 两个字体 base64 内嵌，500/700 回退系统黑体（自动做）；
  3. 道具图可选，extra_data() 按任务号取 learning-page-builder 的 props 图库转 base64；
  4. 每页注入 .hud 角标（替换 .eyebrow）、H1 一处 .hl 马克笔、步骤区块前一条 .ch-band 色块章节条。

每个课程要改的只有下面 HL / PROP 两个表（马克笔词、道具图）；
BAND 是色块颜色轮换（橙→紫→青→黄→墨），一般不用动。
"""
import base64, pathlib, re

SKILL = pathlib.Path.home() / '.workbuddy/skills/pbl-practice-task'
THEME = SKILL / 'assets/themes/dagongren'
PROPS = pathlib.Path.home() / '.workbuddy/skills/learning-page-builder/assets/themes/dagongren/props'

# 示例：打工人的AI入门系列 14 集（换成自己的课程时改这两张表）
HL = {
    '01': '干完', '02': '三个小实验', '03': '长报告', '04': '挑',
    '05': '知识库', '06': '一套考卷', '07': '提示词模板', '08': '拆解',
    '09': '写提示词', '10': '对照表', '11': '脱敏', '12': '智能体',
    '13': '第一个 Skill', '14': '一件真实的活',
}
PROP = {
    '01': 'pencil', '02': 'magnifier', '03': 'open_book', '04': 'balance_scale',
    '05': 'database', '06': 'clipboard', '07': 'handbook', '08': 'puzzle',
    '09': 'robot_type', '10': 'chart_board', '11': 'padlock', '12': 'robot_think',
    '13': 'gears', '14': 'trophy',
}
BAND = ['is-orange', 'is-purple', 'is-teal', 'is-yellow', 'is-ink']


def _b64(path, mime):
    return 'data:%s;base64,%s' % (mime, base64.b64encode(path.read_bytes()).decode())


def skin_css():
    """skin.css 全文：500/700 @font-face 删掉（回退系统黑体），900 与 Inter 改 base64。"""
    css = (THEME / 'skin.css').read_text(encoding='utf-8')
    css = re.sub(r'@font-face\{font-family:"KV Sans";src:url\("fonts/NotoSansSC-(500|700)\.woff"\)[^}]*\}\n?', '', css)
    assert 'NotoSansSC-500' not in css and 'NotoSansSC-700' not in css
    css = css.replace('url("fonts/NotoSansSC-900.woff")', 'url("%s")' % _b64(THEME / 'fonts/NotoSansSC-900.woff', 'font/woff'))
    css = css.replace('url("fonts/Inter-var.woff")', 'url("%s")' % _b64(THEME / 'fonts/Inter-var.woff', 'font/woff'))
    assert 'url("fonts/' not in css
    return css


def themed_template(tpl_text):
    """对任务页模板做三处模板级改造，返回可直接做占位符替换的模板文本。"""
    t = tpl_text.replace('</style>', skin_css() + '\n</style>')
    # ① hero 顶部 hud 角标（替换 eyebrow）
    t = t.replace(
        '<p class="eyebrow" data-rv>实战任务 {{NO}} / {{TOTAL}}</p>',
        '<div class="hud" data-rv>'
        '<div class="hud-ep">第 <b>{{NO}}</b> / {{TOTAL}} 集<i class="hud-sep"></i>'
        '<span>{{SERIES}}</span></div></div>')
    assert 'class="hud"' in t
    # ② H1 马克笔用独立占位符（{{TITLE}} 还要进 <title>，不能带 span）
    t = t.replace('<h1 data-rv style="--d:60ms">{{TITLE}}</h1>',
                  '<h1 data-rv style="--d:60ms">{{TITLE_HL}}</h1>')
    # ③ 步骤区块前插色块章节条（ch-title 必须是块名原文「步骤」）
    band = (
        '<div class="ch-band {{BAND_CLASS}}" data-rv>\n'
        '  <div class="shell">\n'
        '    <span class="ch-glyph" aria-hidden="true">{{NO}}</span>\n'
        '    <p class="ch-no">两步 · 共 {{MIN}} 分钟</p>\n'
        '    <h2 class="ch-title">步骤</h2>\n'
        '    {{CH_PROP}}\n'
        '  </div>\n'
        '</div>\n'
        '<section class="sec" id="steps">')
    t = t.replace('<section class="sec" id="steps">', band, 1)
    t = t.replace('      <h2 class="sec-h" style="margin:0" data-rv>步骤</h2>\n', '')
    assert 'ch-title' in t and '<h2 class="sec-h" style="margin:0"' not in t
    return t


def extra_data(no, name, total_min, series='打工人的AI入门系列'):
    """换肤新增的占位符数据。hl 词必须能对上渲染名（注意空格），对不上会 assert。"""
    key = HL[no]
    assert key in name, '马克笔词 %s 不在任务名 %s 里' % (key, name)
    prop_b64 = _b64(PROPS / ('%s.webp' % PROP[no]), 'image/webp')
    return {
        'SERIES': series,
        'TITLE_HL': name.replace(key, '<span class="hl">%s</span>' % key, 1),
        'BAND_CLASS': BAND[(int(no) - 1) % len(BAND)],
        'CH_NO': '两步 · 共 %s 分钟' % total_min,
        'CH_PROP': '<img class="ch-prop" src="%s" alt="" aria-hidden="true">' % prop_b64,
    }
