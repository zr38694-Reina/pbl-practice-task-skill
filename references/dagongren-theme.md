# 打工人系列「视频同款」主题（任务页触发式换肤）

> **触发关键词**：用户消息里出现「**打工人的AI入门系列**」「**打工人AI办公系列**」「**打工人系列**」，或明确说「**视频同款 / 课件视觉规范 / 用视频那套风格**」时，**Step 6 生成的实战任务页（HTML）** 一律走本主题；任务包（Markdown）不受影响，照常出。
> **没触发就走默认**：不命中关键词的任务页，视觉仍按 `references/task-page-spec.md` 的方块科技风，不要擅自换肤。

> 主题资产在本 skill 的 `assets/themes/dagongren/`（skin.css + 4 字体 + 视觉规范.md 原文）。**换肤方法与 learning-page-builder 的 `references/11-打工人系列视频同款主题.md` 同源**；3D 黏土道具图库（60 张 WebP）与组件展示页不复制过来了，需要道具时去 `~/.workbuddy/skills/learning-page-builder/assets/themes/dagongren/props/` 取。

**只换外观**：五块必备（任务名称 / 场景与对象 / 任务目标 / 步骤 / 常见错误）、五个大标题用块名、不上验收表、任务名 ≤14 字、布置语两句话格式、步骤 ≤2 步、复制按钮脚本——**全部照旧**。与 `task-page-spec.md` 的 UI 规范冲突时（直角 / 无阴影 / 科技蓝 / 单色相），**以本主题为准**。

## 1. 一句话风格

暖白方格纸上的白色圆角卡片，墨黑粗体大字，一处橙色焦点；流程图/色块处整屏高饱和色块，布置语和页脚换黑金暗场。详见 `assets/themes/dagongren/视觉规范.md`。

## 2. 为什么任务页能直接换肤

任务页模板（`assets/task-page-template.html`）和 learning-page-builder 的页面模板**同一套设计令牌命名**：`--bg / --surface / --card / --ink / --muted / --accent / --accent-rgb / --accent-ink / --hairline / --r-card / --r-sm / --r-ctl / --r-chip / --font` 全部同名。skin.css 的令牌映射层贴上去后，**顶栏、hero、场景四格、AI 分工、目标列表、流程图节点、步骤详情卡、错误对照卡、交付物、复制按钮全部自动换肤**，不改类名、不改脚本。

skin.css 里针对学习页组件的选择器（`.ans-stack`、`.fact-card`、`.demo`、`.coach`、`.note` 等）在任务页没有对应元素，是**无害的死规则**，不用删。

## 3. 换肤四步（Step 6 落地时照做）

**第 1 步 · 贴 skin.css**：把 `assets/themes/dagongren/skin.css` **全文粘贴到** `task-page-template.html` 的 `<style>` **最后面**（单文件产物，不用 `<link>`）。
⚠ 实操坑（2026-11-11 在 learning-page-builder 踩过）：skin.css 只是覆盖层，**模板自己的基础样式不能漏**——从模板出发改，别只复制 skin.css 就当整页样式；漏了基础样式，hero 不成形、流程图节点竖排散开。

**第 2 步 · 字体内嵌（单文件必做）**：skin.css 的 `@font-face` 默认走相对路径 `fonts/…`，单文件页面必须改 base64：

- **必嵌两个**：`NotoSansSC-900.woff`（标题/大字的视觉签名，约 1.7MB base64）+ `Inter-var.woff`（任务编号/数字，约 165KB）。4 条 `@font-face` 里**只保留 900 与 Inter 两条**，src 改 `url("data:font/woff;base64,…")`；
- **500/700 不内嵌**，回退系统黑体（`PingFang SC` 等）；单文件只增重约 1.9MB 而不是 5.6MB。

**第 3 步 · 道具图（可选）**：hero 或色块条想放黏土道具时，从 learning-page-builder 的 props 图库取，用到的转 base64 `data:image/webp` 写进 `<img src>`（单张 20–60KB），套 `.prop` / `.ch-prop` 类。**不用 emoji / 线性图标 / 照片当主图**。

**第 4 步 · 每页加这几样**（都是 skin.css 已带的新组件，HTML 写法参考 learning-page-builder 的 `assets/themes/dagongren/skin.css` 注释与组件展示页）：

| 加什么 | 落在哪 | 纪律 |
|---|---|---|
| `.hud` 角标 | hero 顶部（`.eyebrow` 之前或替换）：`第 NN / MM 集 ｜ 打工人的AI入门系列` | 系列名以用户口径为准；集数没说就问，不确认按「第 01/14 集」兜底并在交付时说明 |
| `.hl` 马克笔 | H1 任务名里**标一个词**（任务名 ≤14 字，只标一处） | 黄色马克笔，自动带入场动画 |
| `.ch-band` 色块章节条（可选，最多 1–2 条） | 「步骤」块最像章节，建议给它包一条；**`.ch-title` 里必须原样写块名「步骤」**，不许文案化 | 颜色从 橙→紫→青→黄→墨 轮换；色块里不塞长段落 |
| `.stamp` 印章（可选，最多 1 个） | 交付物块给「退回重做 / 直接交」这类结论盖章 | 只给结论，不给普通说明 |

布置语 `.brief` 黑底块、页脚 `.foot` 会被 skin 自动变成黑金暗场（B 底），不用手动加。任务页没有学习页的「知识总结黄块」，别硬造。

## 4. 追加自检（Step 5 / Step 6 验证时加上这几条）

- [ ] skin.css 已贴在模板基础样式**之后**（顺序反了会被模板默认值盖掉）
- [ ] 900 + Inter 字体已 base64 内嵌；断网打开标题仍是超粗黑体
- [ ] `.hud` 角标在 hero 顶部，集数与系列名和用户口径一致
- [ ] H1 有一处 `.hl` 马克笔；五个块名标题未被文案化
- [ ] 用了 `.ch-band` 时标题仍是块名原文；色块里没有长段落
- [ ] 方格纸底纹可见（浅色模式），暗色模式整页黑金
- [ ] 320 / 1280 两档不横向溢出；流程图可点可播、复制按钮可用
- [ ] 内容零改动：任务名、场景、目标、步骤、错误、布置语与任务卡逐字一致

## 5. 批量换肤的落地坑（2026-11-11 任务页流水线实测）

批量给任务页换肤时，用脚本做模板级注入（参考 `assets/themes/dagongren/inject_theme.py`：`skin_css()` / `themed_template()` / `extra_data()` 三个函数），不要逐页手贴：

- **H1 马克笔要单独占位符**：任务页模板的 `{{TITLE}}` 同时出现在 `<title>` 和 `<h1>` 里。直接往 `{{TITLE}}` 里塞 `<span class="hl">` 会把 span 带进浏览器标签页标题。模板改造一步：`<h1>` 改用 `{{TITLE_HL}}`，`<title>` 保持纯文本 `{{TITLE}}`。
- **马克笔词必须按「渲染后的任务名」匹配**：名字里的空格在渲染时可能被去掉或调整（如「第一个 Skill」），关键词先对渲染名做 `in` 断言再 replace。
- **QA 计数判据**：`ch-glyph` 出现次数 = 2（skin.css 选择器 + 页面元素）才是对的，=1 说明元素没注入；`data:font/woff;base64` 必须 = 2（900 + Inter）；`data:image/webp;base64` = 每页道具数。
- **2MB 单文件的首帧全白**：内嵌 1.9MB 字体后，打开头 1–2 秒可能整页空白，是字体解码不是 JS 挂了——验证时等 1.5s 再截图，别误判。
- **截图去重**：同一张截图换个文件名再 Read，避免工具按内容去重误报「与之前相同」。
