<p align="center"><img src="MarkKISS-logo.ico" alt="MarkKISS"></p>

# MarkKISS — Keep It Simple, Stupid!

> *The definitive "dumb" Markdown editor that just works.*

---

## Language Selection / Выбор языка / 언어 선택 / 言語の選択 / 语言选择 / Sprachauswahl / Selección de idioma / Sélection de la langue

* [English](#english)
* [Русский](#русский)
* [한국어](#한국어)
* [日本語](#日本語)
* [简体中文](#简体中文)
* [繁體中文](#繁體中文)
* [Deutsch](#deutsch)
* [Español](#español)
* [Français](#français)

---

# English

**MarkKISS** is an offline, standalone Markdown and LaTeX editor built out of pure frustration with modern "smart" software. It does exactly what you tell it to do, handles raw AI answers seamlessly, and exports pixel-perfect PDFs with a built-in preview.

## 🤬 The Backstory & Critique of Existing Solutions

Modern software is broken. The developer spent **3 hours digging through gigabytes of absolute junk** looking for a simple, lightweight Markdown editor that could just parse AI answers and export them to PDF. Instead, the market offers nothing but bloatware:
* **Obsidian / Joplin:** Drag along massive local databases, telemetry, and heavy plug-in ecosystems.
* **MarkText:** Throws a tantrum and refuses to render valid math formulas if they don't match its strict structural expectations.
* **ReText:** Completely struggles with normal, modern Markdown parsing.

To make matters worse, modern development deployment is just as broken. After spending **5 painful hours fighting builders and compilers** (Nuitka, PyInstaller) to package `QtWebEngine` (which is essentially a whole Chromium browser architecture resisting being forced into a single executable), a minimalist epiphany was reached.

Why use a heavy truck to deliver a single letter? The solution was to ditch the complex packaging entirely. MarkKISS solves this with an elegant, ultra-portable structure powered by an embedded Python folder and run natively through a lightweight script (.vbs/.bat).

## 💡 Project Philosophy

* **KISS Principle:** Keep It Simple, Stupid. No accounts, no internet requirements, no cloud sync, and 100% private.
* **Zero AI Bloat / Zero Databases:** The application doesn't have an embedded database (only a local `config.json`) and features no built-in AI "features". It relies entirely on your own brain.
* **Tailored for AI Ingestion:** Modern editors feature "smart" visual parsing that breaks instantly when you paste text from ChatGPT, Claude, or DeepSeek because AI outputs often copy over invisible styling, HTML remnants, or multi-format LaTeX structures (`\[ ... \]`, `\( ... \)`). MarkKISS uses robust heuristic parsing (like automatic tag-to-heading translation) designed to clean up and beautifully render raw AI copy-pastes without destroying the layout.

## 🚀 Features & Controls

* **Tab Management:** Open, create, and modify multiple documents simultaneously.
* **Synchronized Scrollbars:** A single unified scrolling experience anchors both the markdown code and the live HTML rendering side-by-side.
* **Adjustable Split Screen:** The editor and preview panes are separated by a **vertical partition wall**. You can drag this wall left or right to dynamically resize your workspace.
* **PDF Preview & Conversion:** Tweak margins, page sizing, and orientation, preview the document exactly as it will print, and export it instantly.

### ⌨️ Hotkeys
* `Ctrl + N` : New document
* `Ctrl + O` : Open file
* `Ctrl + S` : Save file
* `Ctrl + Shift + S` : Save file as
* `Ctrl + W` : Close current tab
* `Ctrl + Shift + P` : Export to PDF (opens PDF parameters and preview)
* `Ctrl + Shift + V` : Paste raw content safely converted into clean Markdown (HTML → MD)
* `Ctrl + Tab` : Switch to the next tab
* `Ctrl + Shift + Tab` : Switch to the previous tab
* `Ctrl+Shift+D` — Export to DOCX

## 📦 What's Inside the Release Archive
* `python/` : Portable embedded Python environment (`pythonw.exe`, `python.exe`, `._pth`).
* `libs/` : Standalone pre-installed library dependencies (`PyQt6`, `markdown`, `pygments`, etc.).
* `katex/` : Offline local assets (CSS/JS) for rendering formulas beautifully without internet.
* `editor.py` : The primary application source code.
* `config.json` : Editor and layout configuration.
* `MarkKISS.bat` : Standard launch batch script.
* `MarkKISS.vbs` : Visual Basic Script to launch the application silently in the background without opening an ugly command prompt terminal window.
* `MarkKISS-logo.ico` : Application icon asset.

---

# Русский

**MarkKISS** — это полностью автономный редактор Markdown и LaTeX, рождённый из глубокого разочарования в современном «умном» софте. Он делает ровно то, что ему говорят, идеально принимает сырые ответы от ИИ и экспортирует документы в PDF с полноценным предварительным просмотром.

## 🤬 Предыстория и критика существующих решений

Современный софт свернул не туда. Разработчик потратил **3 часа на поиск готового решения среди гигабайтов хлама**, пытаясь найти простой и легкий редактор, в который можно без проблем вставить ответ от нейросети, перегнать в PDF и отправить друзьям. Вместо этого рынок предлагает тяжелый мусор:
* **Obsidian / Joplin:** Тащат за собой целые базы данных, кучу скрытых индексов, плагинов и телеметрии.
* **MarkText:** Капризничает при виде математических формул и наотрез отказывается их отображать, если они слегка отклоняются от его строгого формата.
* **ReText:** Вообще не способен адекватно обрабатывать современную разметку Markdown.

Инструменты сборки оказались не лучше. После **5 часов изнурительной борьбы с упаковщиками** (Nuitka, PyInstaller) при попытке скомпилировать `QtWebEngine` (который сопротивлялся, будучи полноценным движком Chromium со своей сложной архитектурой процессов), пришло осознание. Зачем использовать грузовик для перевозки одного письма? В итоге всё разрешилось созданием своего минималистичного редактора и его простейшим запуском через скрипты без лишних слоев абстракции.

## 💡 Философия проекта

* **Принцип KISS:** Keep It Simple, Stupid! Никаких учётных записей, никаких серверов, никакой облачной синхронизации. 100% автономность и приватность.
* **Никакого ИИ-мусора и баз данных:** Внутри программы нет никаких встроенных «умных» генераторов, функций или тяжелых БД (только файл настроек `config.json`). Программа использует исключительно ваш собственный интеллект.
* **Адаптация под вставку из ИИ:** Большинство современных «умных» редакторов ломают вёрстку при вставке ответов из ChatGPT, Claude или DeepSeek, так как ИИ часто копирует скрытый HTML-мусор, стили или нетипичные маркеры формул (`\[ ... \]`, `\( ... \)`). MarkKISS снабжен эвристическим парсингом (например, автоматическим превращением жирных блоков HTML в аккуратные Markdown-заголовки). Он «тупо» и полезно принимает грязь, очищает её и рендерит так, как надо.

## 🚀 Возможности и управление

* **Вкладки:** Создавайте, открывайте и редактируйте несколько документов одновременно.
* **Единый скроллбар:** Область ввода разметки и окно просмотра синхронизированы общим ползунком прокрутки.
* **Гибкий интерфейс:** Области кода разметки и отображения результата разделены общей **вертикальной «стенкой»**. Вы можете менять их размеры, просто сдвинув эту стенку влево или вправо.
* **Конвертация в PDF с предпросмотром:** Настраивайте формат страницы, ориентацию, отступы и проверяйте финальный вид документа прямо в приложении перед сохранением.

### ⌨️ Горячие клавиши
* `Ctrl + N` : Новый документ
* `Ctrl + O` : Открыть файл
* `Ctrl + S` : Сохранить файл
* `Ctrl + Shift + S` : Сохранить как...
* `Ctrl + W` : Закрыть текущую вкладку
* `Ctrl + Shift + P` : Экспорт в PDF (открывает параметры и предпросмотр)
* `Ctrl + Shift + V` : Вставить текст из буфера с безопасным преобразованием (HTML → MD)
* `Ctrl + Tab` : Переключиться на следующую вкладку
* `Ctrl + Shift + Tab` : Переключиться на предыдущую вкладку
* `Ctrl+Shift+D` — Экспорт в DOCX

## 📦 Содержимое релизного архива
* `python/` : Встроенный портативный Python (`pythonw.exe`, `python.exe`, `._pth`).
* `libs/` : Папка с изолированными библиотеками (`PyQt6`, `markdown`, `pygments` и т.д.).
* `katex/` : Локальные файлы CSS/JS для работы формул без интернета.
* `editor.py` : Основной скрипт программы.
* `config.json` : Конфигурация и настройки.
* `MarkKISS.bat` : Запускной батник.
* `MarkKISS.vbs` : VBS-скрипт для бесшумного запуска приложения без открытия черного окна консоли.
* `MarkKISS-logo.ico` : Иконка приложения.

---

# 한국어

**MarkKISS**는 복잡하고 "스마트"한 현대 소프트웨어에 지쳐 직접 만든 오프라인 단독 Markdown 및 LaTeX 편집기입니다. 사용자의 지시를 정확히 수행하며, AI의 답변을 서식 깨짐 없이 그대로 받아들이고, 미리보기가 포함된 고품질 PDF 내보내기를 지원합니다.

## 🤬 개발 배경 및 기존 솔루션 비판

현대 소프트웨어 시장은 왜곡되어 있습니다. 개발자는 AI 답변을 붙여넣고 PDF로 변환해 공유할 수 있는 가볍고 평범한 Markdown 편집기를 찾기 위해 **수 기가바이트의 쓰레기 소프트웨어 속에서 3시간 동안 헤맸습니다**. 하지만 시장에 남은 것은 무거운 프로그램뿐이었습니다:
* **Obsidian / Joplin:** 무거운 로컬 데이터베이스, 인덱스, 플러그인, 원치 않는 텔레메트리를 강제합니다.
* **MarkText:** 자체 기준에 맞지 않으면 올바른 수학 공식조차 파싱하지 못하고 렌더링을 거부합니다.
* **ReText:** 기본적인 현대 Markdown 파싱조차 제대로 처리하지 못합니다.

배포 도구 역시 마찬가지였습니다. 크로미움 브라우저 아키텍처를 포함하는 `QtWebEngine`을 단일 실행 파일로 묶기 위해 **패키징 도구(Nuitka, PyInstaller)와 5시간 동안 사투를 벌인 끝에**, 개발자는 단순함의 진리를 깨달았습니다. 편지 한 장을 배달하기 위해 대형 트럭을 쓸 필요가 없듯이, 복잡한 컴파일을 버리고 임베디드 Python 폴더와 가벼운 스크립트(.vbs/.bat)를 통한 네이티브 실행 방식으로 모든 문제를 해결했습니다.

## 💡 프로젝트 철학

* **KISS 원칙:** Keep It Simple, Stupid! 계정 생성이 없고, 인터넷 연결이 필요 없으며, 클라우드 동기화가 없는 100% 오프라인 및 프라이빗 편집기입니다.
* **AI 쓰레기 및 데이터베이스 배제:** 프로그램 내부에는 어떠한 내장 AI 기능도, 무거운 데이터베이스도 존재하지 않습니다(설정용 `config.json`만 존재). 오직 사용자의 지적 능력만을 도구로 사용합니다.
* **AI 답변 붙여넣기 최적화:** Notion이나 Obsidian 같은 기존 편집기들은 ChatGPT, Claude, DeepSeek의 답변을 붙여넣을 때 서식이 자주 깨집니다. AI 출력이 눈에 보이지 않는 HTML 쓰레기, 스타일, 비표준 LaTeX 마커(`\[ ... \]`, `\( ... \)`)를 포함하기 때문입니다. MarkKISS는 자체 휴리스틱 파싱(예: HTML 두꺼운 글씨 블록을 Markdown 제목으로 자동 변환)을 사용하여 들어오는 텍스트를 깨끗하게 다듬고 완벽하게 렌더링합니다.

## 🚀 주요 기능 및 조작 방법

* **탭 관리:** 여러 문서를 동시에 열고, 생성하고, 편집할 수 있습니다.
* **동기화된 스크롤바:** 마크업 편집 영역과 라이브 HTML 미리보기 창이 하나의 스크롤바로 완벽히 동기화되어 움직입니다.
* **크기 조절 가능한 분할 화면:** 편집창과 미리보기창은 하나의 **수직 분할 벽**으로 나뉘어 있습니다. 이 벽을 마우스로 좌우로 드래그하여 작업 영역의 크기를 자유롭게 조절할 수 있습니다.
* **미리보기가 포함된 PDF 변환:** 페이지 크기, 방향, 여백을 자유롭게 설정하고 저장 전 최종 인쇄 형태를 앱 내에서 미리 확인할 수 있습니다.

### ⌨️ 단축키
- `Ctrl + N` : 새 문서 생성
- `Ctrl + O` : 파일 열기
- `Ctrl + S` : 파일 저장
- `Ctrl + Shift + S` : 다른 이름으로 저장
- `Ctrl + W` : 현재 탭 닫기
- `Ctrl + Shift + P` : PDF로 내보내기 (설정 및 미리보기 창 오픈)
- `Ctrl + Shift + V` : 복사된 HTML을 깨끗한 Markdown으로 안전하게 변환하여 붙여넣기 (HTML → MD)
- `Ctrl + Tab` : 다음 탭으로 이동
- `Ctrl + Shift + Tab` : 이전 탭으로 이동
- `Ctrl+Shift+D` — DOCX로 내보내기

## 📦 릴리스 압축 파일 구성 품목

- `python/` : 내장형 포터블 Python 환경 (`pythonw.exe`, `python.exe`, `._pth`).
- `libs/` : 독립된 사전 설치 라이브러리 폴더 (`PyQt6`, `markdown`, `pygments` 등).
- `katex/` : 인터넷 연결 없이 수식을 렌더링하기 위한 오프라인 로컬 CSS/JS 파일.
- `editor.py` : 프로그램 메인 소스 코드 스크립트.
- `config.json` : 편집기 및 레이아웃 설정 파일.
- `MarkKISS.bat` : 실행용 배치 파일.
- `MarkKISS.vbs` : 검은색 콘솔 창을 띄우지 않고 백그라운드에서 깔끔하게 앱을 실행해주는 VBS 스크립트.
- `MarkKISS-logo.ico` : 애플리케이션 아이콘 파일.

---

## 日本語

**MarkKISS**は、肥大化し「スマート」になりすぎた現代のソフトウェアへの不満から生まれた、完全オフライン・スタンドアロンのMarkdown & LaTeXエディタです。指示されたことだけを忠実に実行し、AIの生の回答を崩さずに受け入れ、プレビュー付きで美しいPDFへとエクスポートします。

## 🤬 開発の背景と既存製品への批判

現代のソフトウェアは壊れています。開発者は、AIの回答を貼り付けてPDFに変換し、友人に送るためだけの「シンプルで軽量なMarkdownエディタ」を求め、**数ギガバイトのゴミソフトの山を3時間かけて掘り返しました**。しかし、市場にあるのは肥大化したツールばかりでした：

- **Obsidian / Joplin:** 巨大なローカルデータベース、インデックス、プラグイン、そして不要なテレメトリを引きずり回します。
- **MarkText:** 独自の厳格なフォーマットから少しでも外れると、正しい数式であっても表示を拒否します。
- **ReText:** 現代の標準的なMarkdownパージ処理にすら満足に対応できません。

開発ツールも同様に悲惨でした。HTMLをレンダリングする`QtWebEngine`（本質的にはChromiumブラウザそのもの）を単一の実行ファイルにパッケージ化しようと、**ビルドツール（Nuitka, PyInstaller）と5時間もの死闘を繰り広げた末**、ミニマリズムの本質に気づきました。手紙を1通届けるために大型トラックを運転する必要はありません。複雑なコンパイルを完全に捨て去り、組み込みのPythonフォルダと軽量なスクリプト（.vbs / .bat）によるネイティブ実行という、最もシンプルなアプローチで解決しました。

## 💡 プロジェクトの哲学

- **KISSの原則:** Keep It Simple, Stupid!（シンプルにしておけ、この愚か者め！）。アカウント不要、インターネット不要、クラウド同期なし。100%ローカルでプライベート。
- **AIゴミ機能・データベースの排除:** アプリ内にはAI機能も、重いデータベースもありません（設定用の`config.json`のみ）。頼るべきは、あなた自身の頭脳だけです。
- **AI回答の貼り付けに特化:** ChatGPT、Claude、DeepSeekなどの回答をコピーして既存の「スマート」なエディタに貼り付けると、レイアウトが崩れることがよくあります。これは、AIの出力に目に見えないHTMLのゴミやスタイル、変則的なLaTeX記法（`\[ ... \]`, `\( ... \)`）が含まれているためです。MarkKISSは強力なヒューリスティック解析（HTMLの太字ブロックを自動的にMarkdownの見出しに変換するなど）を備えており、コピーしたテキストを自動的にクリーンアップして美しくレンダリングします。

## 🚀 機能と操作方法

- **タブ管理:** 複数のドキュメントを同時に作成・開封・編集できます。
- **同期スクロール:** マークアップ入力エリアとHTMLプレビュー画面が、1つのスクロールバーで完全に同期して動きます。
- **可変分割画面:** エディタ領域とプレビュー領域は、1本の**「垂直な仕切り壁」**で区切られています。この壁をマウスで左右にドラッグするだけで、それぞれの領域のサイズを自由に変更できます。
- **プレビュー付きPDF変換:** ページサイズ、向き、余バックを自由に設定し、保存前に最終的な印刷状態をアプリ内で確認できます。

## ⌨️ ショートカットキー

- `Ctrl + N` : 新規ドキュメント
- `Ctrl + O` : ファイルを開く
- `Ctrl + S` : ファイルを保存
- `Ctrl + Shift + S` : 名前を付けて保存
- `Ctrl + W` : 現在のタブを閉じる
- `Ctrl + Shift + P` : PDFへエクスポート（設定とプレビュー画面を開く）
- `Ctrl + Shift + V` : コピーしたHTMLをクリーンなMarkdownに安全に変換して貼り付け（HTML → MD）
- `Ctrl + Tab` : 次のタブへ切り替え
- `Ctrl + Shift + Tab` : 前のタブへ切り替え
- `Ctrl+Shift+D` — DOCXにエクスポート

## 📦 リリースアーカイブの構成内容

- `python/` : 組み込み用ポータブルPython環境（`pythonw.exe`, `python.exe`, `._pth`）。
- `libs/` : 隔離された事前インストール済みライブラリ群（`PyQt6`, `markdown`, `pygments`など）。
- `katex/` : ネット環境なしで数式をレンダリングするためのローカルCSS/JSファイル。
- `editor.py` : アプリケーションのメインソースコード。
- `config.json` : エディタおよびレイアウトの設定ファイル。
- `MarkKISS.bat` : 通常起動用のバッチファイル。
- `MarkKISS.vbs` : 黒いコンソール画面を出さずに、バックグラウンドで静かにアプリを起動するためのVBSスクリプト。
- `MarkKISS-logo.ico` : アプリケーションのアイコンファイル。

---

## 简体中文

**MarkKISS** 是一款完全离线、自主运行的 Markdown 和 LaTeX 编辑器。它诞生于对现代“智能”软件的极度失望。它只做你让它做的事，能够完美直接粘贴 AI 的原始回答，并支持带完整预览的高清 PDF 导出。

## 🤬 开发背景与现有软件批判

现代软件已经误入歧途。开发者为了寻找一款简单、轻量，能把 AI 回答无缝转换成 PDF 发给朋友的 Markdown 编辑器，**在数 GB 的垃圾软件里苦苦淘了 3 个小时**。然而市场上除了一堆臃肿的工业垃圾别无他物：

- **Obsidian / Joplin:** 强行捆绑沉重的本地数据库、索引、插件系统和后台无用的遥测数据。
- **MarkText:** 极其挑剔，只要数学公式稍微不符合其死板的结构预期，就直接拒绝渲染。
- **ReText:** 甚至连现代基础的 Markdown 语法都无法正常解析。

不仅产品臃肿，现代开发部署工具也一样糟糕。为了把包含完整 Chromium 浏览器架构的 `QtWebEngine` 打包成单个可执行文件，开发者**和打包工具（Nuitka、PyInstaller）死磕了 5 个小时**。在经历痛苦后，开发者终于回归极简本质：送一封信何必动用重型卡车？最终，通过引入内嵌的便携 Python 文件夹，并采用最简单的脚本（.vbs/.bat）直接原生启动，彻底甩掉了所有臃肿的中间层。

## 💡 项目哲学

- **KISS 原则:** Keep It Simple, Stupid!（保持简单，傻瓜）。无需注册账号、无需联网、没有云端同步，100% 本地与隐私安全。
- **零 AI 垃圾 / 零数据库:** 软件内部没有任何内置的“智能”生成器、无用功能或沉重的数据库（仅有一个本地 `config.json` 配置文件）。它只依赖你自己的大脑。
- **专为承接 AI 回答而生:** 当你从 ChatGPT、Claude 或 DeepSeek 复制代码并粘贴到传统的“智能”编辑器中时，排版往往会瞬间崩溃。因为 AI 的输出经常夹杂着不可见的 HTML 残留、样式表或非标准的 LaTeX 标记（如 `\[ ... \]`, `\( ... \)`）。MarkKISS 采用了强健的启发式解析（例如自动将 HTML 的粗体块转换为标准的 Markdown 标题），能够“单纯”而高效地容纳这些脏数据，将其清洗并完美渲染。

## 🚀 功能特性与控制

- **多标签页管理:** 支持同时创建、打开和编辑多个文档。
- **双窗同步滚动:** 源码输入区和 live HTML 预览区通过一个统一的滚动条进行完美同步。
- **可调分割屏幕:** 编辑区域和预览区域由一面**中央垂直“隔墙”**分开。只需用鼠标将这面墙向左或向右拖动，即可动态调整两边视窗的大小。
- **带预览 PDF 转换:** 支持自由微调纸张尺寸、方向、页边距，并在保存前在软件内直接查看最终打印效果。

## ⌨️ 快捷键

- `Ctrl + N` : 新建文档
- `Ctrl + O` : 打开文件
- `Ctrl + S` : 保存文件
- `Ctrl + Shift + S` : 另存为...
- `Ctrl + W` : 关闭当前标签页
- `Ctrl + Shift + P` : 导出为 PDF（打开参数配置与预览视窗）
- `Ctrl + Shift + V` : 粘贴剪贴板内容并安全转换为纯净 Markdown（HTML → MD）
- `Ctrl + Tab` : 切换到下一个标签页
- `Ctrl + Shift + Tab` : 切换到上一个标签页
- `Ctrl+Shift+D` — 导出为 DOCX

## 📦 发行版压缩包目录结构

- `python/` : 内嵌的便携式 Python 运行环境 (`pythonw.exe`, `python.exe`, `._pth`)。
- `libs/` : 隔离的预装第三方依赖库文件夹 (`PyQt6`, `markdown`, `pygments` 等)。
- `katex/` : 本地 KaTeX 静态资源（CSS/JS），用于在完全断网时完美渲染数学公式。
- `editor.py` : 核心应用程序源码脚本。
- `config.json` : 编辑器与主题配置文件。
- `MarkKISS.bat` : 批处理启动脚本。
- `MarkKISS.vbs` : VBS 脚本，用于在后台静默启动程序，绝不弹丑陋的黑色控制台终端窗口。
- `MarkKISS-logo.ico` : 应用程序图标资源。

---

## 繁體中文

**MarkKISS** 是一款完全離線、自主運行的 Markdown 和 LaTeX 編輯器。它誕生於對現代「智能」軟體的極度失望。它只做你讓它做的事，能夠完美直接貼上 AI 的原始回答，並支援帶完整預覽的高清 PDF 匯出。

## 🤬 開發背景與現有軟體批判

現代軟體已經誤入歧途。開發者為了尋找一款簡單、輕量，能把 AI 回答無縫轉換成 PDF 發給朋友的 Markdown 編輯器，**在數 GB 的垃圾軟體裡苦苦淘了 3 個小時**。然而市場上除了一堆臃腫的工業垃圾別無他物：

- **Obsidian / Joplin:** 強行捆綁沉重的在地資料庫、索引、外掛系統和背景無用的遙測數據。
- **MarkText:** 極其挑剔，只要數學公式稍微不符合其死板的結構預期，就直接拒絕渲染。
- **ReText:** 甚至連現代基礎的 Markdown 語法都無法正常解析。

不僅產品臃腫，現代開發部署工具也一樣糟糕。為了把包含完整 Chromium 瀏覽器架構的 `QtWebEngine` 打包成單個可執行檔，開發者**和打包工具（Nuitka、PyInstaller）死磕了 5 個小時**。在經歷痛苦後，開發者終於回歸極簡本質：送一封信何必動用重型卡車？最終，透過引入內嵌的便攜 Python 資料夾，並採用最簡單的指令碼（.vbs/.bat）直接原生啟動，徹底甩掉了所有臃腫的中間層。

## 💡 專案哲學

- **KISS 原則:** Keep It Simple, Stupid!（保持簡單，傻瓜）。無需註冊帳號、無需連網、沒有雲端同步，100% 在地與隱私安全。
- **零 AI 垃圾 / 零資料庫:** 軟體內部沒有任何內置的「智能」產生器、無用功能或沉重的資料庫（僅有一個在地 `config.json` 設定檔）。它只依賴你自己的大腦。
- **專為承接 AI 回答而生:** 當你從 ChatGPT、Claude 或 DeepSeek 複製代碼並貼上到傳統的「智能」編輯器中時，排版往往會瞬間崩潰。因為 AI 的輸出經常夾雜著不可見的 HTML 殘留、樣式表或非標準的 LaTeX 標記（如 `\[ ... \]`, `\( ... \)`）。MarkKISS 採用了強健的啟發式解析（例如自動將 HTML 的粗體塊轉換為標準的 Markdown 標題），能夠「單純」而高效地容納這些髒數據，將其清洗並完美渲染。

## 🚀 功能特性與控制

- **多分頁管理:** 支援同時建立、開啟和編輯多個文件。
- **雙窗同步捲動:** 原始碼輸入區和 live HTML 預覽區透過一個統一的捲軸進行完美同步。
- **可調分割螢幕:** 編輯區域和預覽區域由一面**中央垂直「隔牆」**分開。只需用滑鼠將這面牆向左或向右拖曳，即可動態調整兩邊視窗的大小。
- **帶預覽 PDF 轉換:** 支援自由微調紙張尺寸、方向、頁邊距，並在儲存前在軟體內直接查看最終列印效果。

## ⌨️ 快捷鍵

- `Ctrl + N` : 新增文件
- `Ctrl + O` : 開啟檔案
- `Ctrl + S` : 儲存檔案
- `Ctrl + Shift + S` : 另存新檔...
- `Ctrl + W` : 關閉當前分頁
- `Ctrl + Shift + P` : 匯出為 PDF（開啟參數配置與預覽視窗）
- `Ctrl + Shift + V` : 貼上剪貼簿內容並安全轉換為純淨 Markdown（HTML → MD）
- `Ctrl + Tab` : 切換到下一個分頁
- `Ctrl + Shift + Tab` : 切換到上一個分頁
- `Ctrl+Shift+D` — 匯出為 DOCX

## 📦 發行版壓縮包目錄結構

- `python/` : 內嵌的便攜式 Python 執行環境 (`pythonw.exe`, `python.exe`, `._pth`)。
- `libs/` : 隔離的預裝第三方依賴庫資料夾 (`PyQt6`, `markdown`, `pygments` 等)。
- `katex/` : 在地 KaTeX 靜態資源（CSS/JS），用於在完全斷網時完美渲染數學公式。
- `editor.py` : 核心應用程式原始碼指令碼。
- `config.json` : 編輯器與主題設定檔。
- `MarkKISS.bat` : 批次處理啟動指令碼。
- `MarkKISS.vbs` : VBS 指令碼，用於在背景靜默啟動程式，絕不彈醜陋的黑色主控台終端視窗。
- `MarkKISS-logo.ico` : 應用程式圖示資源。

---

## Deutsch

**MarkKISS** ist ein vollständig eigenständiger Offline-Markdown- und LaTeX-Editor, der aus reiner Frustration über moderne, überladene „intelligente“ Software entstanden ist. Er tut genau das, was Sie ihm sagen, verarbeitet KI-Antworten fehlerfrei und exportiert PDFs mit einer integrierten Live-Vorschau.

## 🤬 Die Hintergrundgeschichte & Kritik an bestehenden Lösungen

Moderne Software ist fehlerhaft. Der Entwickler verbrachte **3 Stunden damit, Gigabytes an absolutem Müll zu durchwühlen**, um einen einfachen, leichten Markdown-Editor zu finden, der KI-Antworten parsen und in PDF exportieren kann. Stattdessen bietet der Markt nur Bloatware:

- **Obsidian / Joplin:** Schleppen riesige lokale Datenbanken, Indizes, komplexe Plugins und unerwünschte Telemetrie mit sich herum.
- **MarkText:** Verweigert die Anzeige korrekter mathematischer Formeln, wenn diese nicht exakt den starren strukturellen Erwartungen des Parsers entsprechen.
- **ReText:** Scheitert bereits an der fehlerfreien Verarbeitung von modernem Markdown.

Und die Entwicklungswerkzeuge sind nicht besser. Nach **5 quälenden Stunden des Kampfes mit Compilern** (Nuitka, PyInstaller) beim Versuch, `QtWebEngine` (was im Grunde die gesamte Chromium-Browserarchitektur ist) in eine einzige Exe-Datei zu packen, folgte die Erkenntnis: Warum einen schweren Lkw benutzen, um einen einzigen Brief zuzustellen? Die Lösung bestand darin, die komplexe Kompilierung aufzugeben. MarkKISS löst dies durch eine portable Struktur mit einem integrierten Python-Ordner, der nativ über ein einfaches Skript (.vbs/.bat) ausgeführt wird.

## 💡 Projektphilosophie

- **KISS-Prinzip:** Keep It Simple, Stupid! Keine Benutzerkonten, kein Internet erforderlich, keine Cloud-Synchronisation. 100 % lokal und privat.
- **Kein KI-Müll / Keine Datenbanken:** Die Anwendung enthält keine integrierten KI-Generatoren oder Datenbanken (nur eine lokale `config.json`). Sie verlässt sich ausschließlich auf Ihre eigene Intelligenz.
- **Optimiert für KI-Inhalte:** Moderne Editoren brechen beim Einfügen von Texten aus ChatGPT, Claude oder DeepSeek ab, da KI-Ausgaben unsichtbaren HTML-Müll, Stile oder unübliche LaTeX-Marker (`\[ ... \]`, `\( ... \)`) enthalten. MarkKISS verwendet robuste heuristische Analysen (z. B. die automatische Umwandlung von fettgedrucktem HTML in saubere Markdown-Überschriften), um die Daten ohne Layoutfehler zu bereinigen und perfekt darzustellen.

## 🚀 Funktionen & Bedienung

- **Tab-Verwaltung:** Erstellen, öffnen und bearbeiten Sie mehrere Dokumente gleichzeitig.
- **Synchronisierte Scrollbalken:** Der Markup-Codebereich und die HTML-Vorschau sind über einen einzigen Scrollbalken perfekt miteinander synchronisiert.
- **Einstellbarer geteilter Bildschirm:** Die Editor- und Vorschaufenster sind durch eine **vertikale Trennwand** getrennt. Sie können diese Wand nach links oder rechts verschieben, um die Größe der Arbeitsbereiche anzupassen.
- **PDF-Konvertierung mit Vorschau:** Passen Sie Seitenformat, Ausrichtung und Ränder an und überprüfen Sie das Dokument vor dem Speichern in der Live-Vorschau.

## ⌨️ Tastenkombinationen

- `Ctrl + N` : Neues Dokument
- `Ctrl + O` : Datei öffnen
- `Ctrl + S` : Datei speichern
- `Ctrl + Shift + S` : Speichern unter...
- `Ctrl + W` : Aktuellen Tab schließen
- `Ctrl + Shift + P` : Als PDF exportieren (öffnet Einstellungen und Vorschau)
- `Ctrl + Shift + V` : Inhalt einfügen und sicher in sauberes Markdown umwandeln (HTML → MD)
- `Ctrl + Tab` : Zum nächsten Tab wechseln
- `Ctrl + Shift + Tab` : Zum vorherigen Tab wechseln
- `Ctrl+Shift+D` — Export nach DOCX

## 📦 Inhalt des Release-Archivs

- `python/` : Integrierte portable Python-Umgebung (`pythonw.exe`, `python.exe`, `._pth`).
- `libs/` : Ordner mit isolierten, vorinstallierten Bibliotheken (`PyQt6`, `markdown`, `pygments` usw.).
- `katex/` : Lokale CSS/JS-Dateien zur Offline-Anzeige von Formeln ohne Internetverbindung.
- `editor.py` : Der Hauptquellcode der Anwendung.
- `config.json` : Konfigurationsdatei für Editor und Layout.
- `MarkKISS.bat` : Batch-Skript zum Starten.
- `MarkKISS.vbs` : VBS-Skript zum lautlosen Starten der Anwendung im Hintergrund ohne das hässliche schwarze Konsolenfenster.
- `MarkKISS-logo.ico` : Anwendungssymbol (Icon).

---

## Español

**MarkKISS** es un editor de Markdown y LaTeX offline y completamente independiente, nacido de la pura frustración con el software "inteligente" moderno. Hace exactamente lo que se le indica, procesa respuestas de IA sin romper el diseño y exporta PDFs con una vista previa integrada de alta calidad.

## 🤬 El trasfondo y la crítica a las soluciones existentes

El software moderno está roto. El desarrollador pasó **3 horas buscando entre gigabytes de basura absoluta** para encontrar un editor de Markdown simple y ligero en el que pegar respuestas de IA y exportarlas a PDF. En cambio, el mercado solo ofrece programas inflados:

- **Obsidian / Joplin:** Arrastran pesadas bases de datos locales, índices, complejos ecosistemas de plugins y telemetría no deseada.
- **MarkText:** Se niega a renderizar fórmulas matemáticas correctas si no cumplen exactamente con sus rígidas expectativas estructurales.
- **ReText:** Tiene serios problemas para procesar correctamente el Markdown moderno.

Las herramientas de compilación no se quedaron atrás. Después de pasar **5 dolorosas horas luchando contra empaquetadores** (Nuitka, PyInstaller) para compilar `QtWebEngine` (que es esencialmente la arquitectura completa del navegador Chromium resistiéndose a ser forzada en un solo archivo ejecutable), se llegó a una epifanía minimalista. ¿Por qué usar un camión pesado para entregar una sola carta? La solución fue abandonar la compilación compleja. MarkKISS resuelve esto con una estructura portátil que incluye una carpeta de Python embebida y se ejecuta de forma nativa a través de un simple script (.vbs/.bat).

## 💡 Filosofía del proyecto

- **Principio KISS:** Keep It Simple, Stupid! (¡Hazlo simple, estúpido!). Sin cuentas, sin necesidad de internet y sin sincronización en la nube. 100% privado y local.
- **Cero basura de IA / Cero bases de datos:** La aplicación no contiene generadores de IA integrados ni bases de datos pesadas (solo un archivo local `config.json`). Se basa únicamente en su propio cerebro.
- **Adaptado para respuestas de IA:** Los editores modernos rompen el diseño al pegar texto desde ChatGPT, Claude o DeepSeek porque las respuestas de las IA suelen incluir código HTML invisible, estilos o marcadores LaTeX no estándar (`\[ ... \]`, `\( ... \)`). MarkKISS utiliza un robusto análisis heurístico (como la traducción automática de bloques de HTML en negrita a encabezados de Markdown) diseñado para limpiar y renderizar el texto perfectamente sin alterar el formato.

## 🚀 Características y uso

- **Gestión de pestañas:** Cree, abra y edite múltiples documentos simultáneamente.
- **Barra de desplazamiento sincronizada:** El área del código fuente y la vista previa HTML se mueven de forma idéntica con una sola barra de desplazamiento.
- **Pantalla dividida ajustable:** Las áreas del código de marcado y del resultado están separadas por una **"pared vertical"** común. Puede cambiar sus tamaños simplemente deslizando esta pared hacia la izquierda o hacia la derecha.
- **Conversión a PDF con vista previa:** Ajuste el tamaño de página, la orientación y los márgenes, y verifique el diseño final dentro de la aplicación antes de guardarlo.

## ⌨️ Atajos de teclado

- `Ctrl + N` : Nuevo documento
- `Ctrl + O` : Abrir archivo
- `Ctrl + S` : Guardar archivo
- `Ctrl + Shift + S` : Guardar como...
- `Ctrl + W` : Cerrar pestaña actual
- `Ctrl + Shift + P` : Exportar a PDF (abre la configuración y la vista previa)
- `Ctrl + Shift + V` : Pegar contenido convirtiéndolo de forma segura a Markdown limpio (HTML → MD)
- `Ctrl + Tab` : Cambiar a la siguiente pestaña
- `Ctrl + Shift + Tab` : Cambiar a la pestaña anterior
- `Ctrl+Shift+D` — Exportar a DOCX

## 📦 Contenido del archivo de lanzamiento

- `python/` : Entorno portable de Python embebido (`pythonw.exe`, `python.exe`, `._pth`).
- `libs/` : Carpeta con librerías aisladas e preinstaladas (`PyQt6`, `markdown`, `pygments`, etc.).
- `katex/` : Archivos locales CSS/JS para renderizar fórmulas matemáticas sin conexión a internet.
- `editor.py` : El código fuente principal de la aplicación.
- `config.json` : Archivo de configuración del editor y diseño.
- `MarkKISS.bat` : Script por lotes para el lanzamiento.
- `MarkKISS.vbs` : Script VBS para lanzar la aplicación de forma silenciosa en segundo plano sin abrir la molesta ventana negra de la consola.
- `MarkKISS-logo.ico` : Icono de la aplicación.

---

## Français

**MarkKISS** est un éditeur de Markdown et LaTeX 100% hors ligne et autonome, né d'une profonde frustration face aux logiciels modernes dits « intelligents ». Il fait exactement ce que vous lui demandez, accepte les réponses brutes d'IA sans casser la mise en page, et exporte des PDF parfaits avec un aperçu intégré.

## 🤬 Contexte et critique des solutions existantes

Les logiciels modernes ont pris une mauvaise direction. Le développeur a passé **3 heures à fouiller dans des gigaoctets de logiciels indésirables** à la recherche d'un éditeur Markdown simple et léger, capable de coller une réponse d'IA et de l'exporter en PDF pour l'envoyer à des amis. À la place, le marché ne propose que des outils lourds et encombrants :

- **Obsidian / Joplin :** Traînent de lourdes bases de données locales, des index, des systèmes de plugins complexes et de la télémétrie non désirée.
- **MarkText :** Refuse catégoriquement de rendre les formules mathématiques correctes si elles s'écartent un tant soit peu de sa structure rigide.
- **ReText :** Rencontre de grandes difficultés à traiter correctement le Markdown moderne de base.

Les outils de déploiement ne valent pas mieux. Après avoir passé **5 heures éprouvantes à se battre avec des outils de compilation** (Nuitka, PyInstaller) pour packager `QtWebEngine` (qui est en fait l'architecture complète d'un navigateur Chromium résistant à l'idée d'être forcé dans un seul exécutable), une prise de conscience minimaliste a eu lieu. Pourquoi utiliser un poids lourd pour livrer une simple lettre ? La solution consistait à abandonner la compilation complexe. MarkKISS résout ce problème grâce à une structure portable incluant un dossier Python embarqué, lancé nativement via un simple script (.vbs/.bat).

## 💡 Philosophie du projet

- **Principe KISS :** Keep It Simple, Stupid! (Fais simple, idiot !). Pas de compte, pas de connexion internet requise, aucune synchronisation cloud. 100% local et privé.
- **Zéro IA intégrée / Zéro base de données :** L'application ne contient aucun générateur d'IA ni base de données lourde (uniquement un fichier local `config.json`). Elle s'appuie exclusivement sur votre propre cerveau.
- **Adapté pour les copier-coller d'IA :** Les éditeurs modernes corrompent la mise en page lorsque vous collez du texte provenant de ChatGPT, Claude ou DeepSeek, car les réponses d'IA contiennent souvent du code HTML invisible, des styles ou des marqueurs LaTeX non standards (`\[ ... \]`, `\( ... \)`). MarkKISS utilise une analyse heuristique robuste (comme la conversion automatique des blocs HTML en gras en titres Markdown propres) conçue pour nettoyer et afficher le texte parfaitement, sans altérer le format.

## 🚀 Fonctionnalités et commandes

- **Gestion des onglets :** Créez, ouvrez et modifiez plusieurs documents simultanément.
- **Défilement synchronisé :** La zone de saisie du code et la fenêtre de prévisualisation HTML se déplacent de manière identique avec une seule barre de défilement.
- **Écran partagé ajustable :** Les zones de texte et de prévisualisation sont séparées par une **« cloison verticale »** commune. Vous pouvez modifier leur taille en faisant simplement glisser cette cloison vers la gauche ou vers la droite.
- **Conversion PDF avec aperçu :** Ajustez le format de page, l'orientation et les marges, et vérifiez le rendu final directement dans l'application avant l'enregistrement.

## ⌨️ Raccourcis clavier

- `Ctrl + N` : Nouveau document
- `Ctrl + O` : Ouvrir un fichier
- `Ctrl + S` : Enregistrer le fichier
- `Ctrl + Shift + S` : Enregistrer sous...
- `Ctrl + W` : Fermer l'onglet actuel
- `Ctrl + Shift + P` : Exporter en PDF (ouvre les paramètres et l'aperçu)
- `Ctrl + Shift + V` : Coller le contenu en le convertissant proprement en Markdown (HTML → MD)
- `Ctrl + Tab` : Passer à l'onglet suivant
- `Ctrl + Shift + Tab` : Passer à l'onglet précédent
- `Ctrl+Shift+D` — Exporter en DOCX

## 📦 Contenu de l'archive de version

- `python/` : Environnement de runtime Python portable embarqué (`pythonw.exe`, `python.exe`, `._pth`).
- `libs/` : Dossier contenant les bibliothèques tierces préinstallées et isolées (`PyQt6`, `markdown`, `pygments`, etc.).
- `katex/` : Fichiers locaux CSS/JS pour afficher les formules mathématiques sans connexion internet.
- `editor.py` : Le code source principal de l'application.
- `config.json` : Fichier de configuration de l'éditeur et du rendu.
- `MarkKISS.bat` : Script batch standard pour le lancement.
- `MarkKISS.vbs` : Script VBS pour lancer l'application silencieusement en arrière-plan sans ouvrir la vilaine fenêtre noire de la console.
- `MarkKISS-logo.ico` : Icône de l'application.
