import sys
import os
import re
import json
import markdown
from bs4 import BeautifulSoup
from markdownify import markdownify as md_convert
from pygments.formatters import HtmlFormatter

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QSplitter, QFileDialog, QMessageBox, QStatusBar,
    QDialog, QFormLayout, QComboBox, QSpinBox, QDialogButtonBox, QPushButton,
    QCheckBox, QGroupBox, QLabel, QTabWidget
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineScript, QWebEngineSettings
from PyQt6.QtCore import (
    Qt, QUrl, QTimer, QBuffer, QIODevice, QMarginsF, QSizeF, QRegularExpression
)
from PyQt6.QtGui import (
    QAction, QKeySequence, QPageLayout, QPageSize, QSyntaxHighlighter,
    QTextCharFormat, QFont, QColor, QCloseEvent
)
from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KATEX_DIR = os.path.join(BASE_DIR, "katex")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
APP_VERSION = "1.0"
APP_NAME = "MarkKISS"

DEFAULT_SETTINGS = {
    "font_family": "system",
    "text_align": "left",
    "font_size": 16,
    "max_width": 900,
    "language": "en"
}

DEFAULT_PDF_SETTINGS = {
    "page_size": "A4",
    "orientation": "portrait",
    "margin_top": 20,
    "margin_bottom": 20,
    "margin_left": 20,
    "margin_right": 20,
    "page_numbers": True
}

# ---------------------------------------------------------------------------
# Localization
# ---------------------------------------------------------------------------

LANGUAGES = [
    ("en", "English"),
    ("ru", "Русский"),
    ("ko", "한국어"),
    ("ja", "日本語"),
    ("zh_CN", "简体中文"),
    ("zh_TW", "繁體中文"),
    ("de", "Deutsch"),
    ("es", "Español"),
    ("fr", "Français"),
]

TRANSLATIONS = {
    "en": {
        "menu_file": "File",
        "menu_edit": "Edit",
        "menu_settings": "Settings",
        "menu_help": "Help",
        "menu_language": "Language",
        "action_new": "New document",
        "action_open": "Open...",
        "action_save": "Save",
        "action_save_as": "Save as...",
        "action_close_tab": "Close tab",
        "action_export_pdf": "Export to PDF...",
        "action_exit": "Exit",
        "action_undo": "Undo",
        "action_redo": "Redo",
        "action_paste_md": "Paste as Markdown (HTML → MD)",
        "action_next_tab": "Next tab",
        "action_prev_tab": "Previous tab",
        "action_text_settings": "Text settings...",
        "action_pdf_settings": "PDF settings...",
        "action_about": "About",
        "dialog_settings_title": "Editor settings",
        "label_font": "Font:",
        "font_system": "System (default)",
        "label_align": "Text alignment:",
        "align_left": "Left",
        "align_justify": "Justify",
        "align_center": "Center",
        "label_font_size": "Font size:",
        "label_text_width": "Text width:",
        "dialog_pdf_title": "PDF export settings",
        "group_page": "Page",
        "label_format": "Format:",
        "label_orientation": "Orientation:",
        "orient_portrait": "Portrait",
        "orient_landscape": "Landscape",
        "group_margins": "Margins (mm)",
        "label_margin_top": "Top:",
        "label_margin_bottom": "Bottom:",
        "label_margin_left": "Left:",
        "label_margin_right": "Right:",
        "check_page_numbers": "Number pages (centered at bottom)",
        "pdf_preview_title": "PDF preview — before saving",
        "btn_save": "Save...",
        "btn_cancel": "Cancel",
        "btn_ok": "OK",
        "save_pdf_title": "Save PDF",
        "error": "Error",
        "error_save_pdf": "Failed to save PDF:\n{e}",
        "error_open_file": "Failed to open file:\n{e}",
        "error_save_file": "Failed to save file:\n{e}",
        "error_load_export": "Failed to load document for export.",
        "error_generate_pdf": "Failed to generate PDF.",
        "error_open_folder": "Failed to open folder:\n{e}",
        "unsaved_title": "Unsaved changes",
        "unsaved_text": "“{name}” has unsaved changes.\nSave them?",
        "new_doc": "New document",
        "not_saved": "Not saved",
        "state_modified": "modified",
        "state_saved": "saved",
        "status_new_memory": "New document created (in memory)",
        "status_opened": "Opened: {path}",
        "status_saved": "Saved: {path}",
        "status_pasted_md": "Pasted as Markdown",
        "status_pdf_exported": "PDF exported: {path}",
        "status_error": "Error: {e}",
        "placeholder": "Type Markdown here...\n\nExample: # Heading\n\n$E = mc^2$",
        "preview_empty": "Start typing Markdown...",
        "preview_error": "Error: {e}",
        "export_empty_title": "Export",
        "export_empty_text": "Document is empty.",
        "done_title": "Done",
        "pdf_saved_text": "PDF saved:\n{path}",
        "btn_show_in_folder": "Show in folder",
        "about_title": "About",
        "about_text": (
            "MarkKISS v{version}\n\n"
            "• Works 100% offline and privately, independent of corporation servers and third-party tools\n"
            "• No databases, no AI tools, no other junk — just pure Markdown and LaTeX\n"
            "• Create, open, save Markdown files and export them to PDF\n"
            "• Heuristic parsing of headings, formulas and code — paste AI answers from browser without hassle\n"
            "• Single scrollbar for both the markup language area and the preview\n"
            "• PDF preview before conversion\n"
            "• Tab management: Ctrl+T — new, Ctrl+W — close, Ctrl+Tab / Ctrl+Shift+Tab — switch\n"
            "• Dependencies: pip install markdownify beautifulsoup4 pygments markdown pymdown-extensions\n"
            "_______________________________________________________________________________________\n"
            "Created with the help of DeepSeek and the 'Keep It Simple, Stupid!' principle by a person "
            "who dug through gigabytes of junk software.\n"
            "Yours truly, Dharma485"
        ),
        "window_title": "{name} {version} (100% Offline / KaTeX)",
        "window_title_doc": "{star}{name} — {app}",
        "language_names": {
            "en": "English", "ru": "Русский", "ko": "한국어", "ja": "日本語",
            "zh_CN": "简体中文", "zh_TW": "繁體中文", "de": "Deutsch",
            "es": "Español", "fr": "Français",
        },
    },
    "ru": {
        "menu_file": "Файл",
        "menu_edit": "Правка",
        "menu_settings": "Настройки",
        "menu_help": "Справка",
        "menu_language": "Язык",
        "action_new": "Новый документ",
        "action_open": "Открыть...",
        "action_save": "Сохранить",
        "action_save_as": "Сохранить как...",
        "action_close_tab": "Закрыть вкладку",
        "action_export_pdf": "Экспорт в PDF...",
        "action_exit": "Выход",
        "action_undo": "Отменить",
        "action_redo": "Повторить",
        "action_paste_md": "Вставить как Markdown (HTML → MD)",
        "action_next_tab": "Следующая вкладка",
        "action_prev_tab": "Предыдущая вкладка",
        "action_text_settings": "Параметры текста...",
        "action_pdf_settings": "Параметры PDF...",
        "action_about": "О редакторе",
        "dialog_settings_title": "Настройки редактора",
        "label_font": "Шрифт:",
        "font_system": "Системный (по умолчанию)",
        "label_align": "Выравнивание текста:",
        "align_left": "По левому краю",
        "align_justify": "По ширине (Justify)",
        "align_center": "По центру",
        "label_font_size": "Размер шрифта:",
        "label_text_width": "Ширина текста:",
        "dialog_pdf_title": "Параметры экспорта в PDF",
        "group_page": "Страница",
        "label_format": "Формат:",
        "label_orientation": "Ориентация:",
        "orient_portrait": "Книжная (портрет)",
        "orient_landscape": "Альбомная (ландшафт)",
        "group_margins": "Поля (мм)",
        "label_margin_top": "Верхнее:",
        "label_margin_bottom": "Нижнее:",
        "label_margin_left": "Левое:",
        "label_margin_right": "Правое:",
        "check_page_numbers": "Нумеровать страницы (по центру внизу)",
        "pdf_preview_title": "Предпросмотр PDF — перед сохранением",
        "btn_save": "Сохранить...",
        "btn_cancel": "Отмена",
        "btn_ok": "OK",
        "save_pdf_title": "Сохранить PDF",
        "error": "Ошибка",
        "error_save_pdf": "Не удалось сохранить PDF:\n{e}",
        "error_open_file": "Не удалось открыть файл:\n{e}",
        "error_save_file": "Не удалось сохранить файл:\n{e}",
        "error_load_export": "Не удалось загрузить документ для экспорта.",
        "error_generate_pdf": "Не удалось сгенерировать PDF.",
        "error_open_folder": "Не удалось открыть папку:\n{e}",
        "unsaved_title": "Несохранённые изменения",
        "unsaved_text": "«{name}» содержит несохранённые изменения.\nСохранить их?",
        "new_doc": "Новый документ",
        "not_saved": "Не сохранён",
        "state_modified": "изменён",
        "state_saved": "сохранён",
        "status_new_memory": "Создан новый документ (в памяти)",
        "status_opened": "Открыт: {path}",
        "status_saved": "Сохранено: {path}",
        "status_pasted_md": "Вставлено как Markdown",
        "status_pdf_exported": "PDF экспортирован: {path}",
        "status_error": "Ошибка: {e}",
        "placeholder": "Введите Markdown здесь...\n\nПример: # Заголовок\n\n$E = mc^2$",
        "preview_empty": "Начните вводить Markdown...",
        "preview_error": "Ошибка: {e}",
        "export_empty_title": "Экспорт",
        "export_empty_text": "Документ пуст.",
        "done_title": "Готово",
        "pdf_saved_text": "PDF сохранён:\n{path}",
        "btn_show_in_folder": "Показать в папке",
        "about_title": "О редакторе",
        "about_text": (
            "MarkKISS v{version}\n\n"
            "• Работает 100% автономно и приватно, независимо от серверов корпораций и сторонних инструментов\n"
            "• Не тянет за собой базы данных, AI-инструменты и прочий мусор — только чистый Markdown и LaTeX\n"
            "• Позволяет создавать, открывать, сохранять и экспортировать Markdown-файлы в PDF\n"
            "• Эвристический парсинг заголовков, формул и кода — ответы ИИ вставляются из браузера без танцев с бубном\n"
            "• Единый ползунок прокрутки для области языка разметки и просмотра\n"
            "• Предпросмотр PDF перед конвертацией\n"
            "• Управление вкладками: Ctrl+T — новая, Ctrl+W — закрыть, Ctrl+Tab / Ctrl+Shift+Tab — переключение\n"
            "• Зависимости: pip install markdownify beautifulsoup4 pygments markdown pymdown-extensions\n"
            "_______________________________________________________________________________________\n"
            "Создано при помощи DeepSeek и принципа 'Keep It Simple, Stupid!' человеком, перерывшим гигабайты мусорного софта.\n"
            "Ваш покорный слуга, Dharma485"
        ),
        "window_title": "{name} {version} (100% Автономный / KaTeX)",
        "window_title_doc": "{star}{name} — {app}",
        "language_names": {
            "en": "English", "ru": "Русский", "ko": "한국어", "ja": "日本語",
            "zh_CN": "简体中文", "zh_TW": "繁體中文", "de": "Deutsch",
            "es": "Español", "fr": "Français",
        },
    },
    "ko": {
        "menu_file": "파일",
        "menu_edit": "편집",
        "menu_settings": "설정",
        "menu_help": "도움말",
        "menu_language": "언어",
        "action_new": "새 문서",
        "action_open": "열기...",
        "action_save": "저장",
        "action_save_as": "다른 이름으로 저장...",
        "action_close_tab": "탭 닫기",
        "action_export_pdf": "PDF로 내보내기...",
        "action_exit": "종료",
        "action_undo": "실행 취소",
        "action_redo": "다시 실행",
        "action_paste_md": "Markdown으로 붙여넣기 (HTML → MD)",
        "action_next_tab": "다음 탭",
        "action_prev_tab": "이전 탭",
        "action_text_settings": "텍스트 설정...",
        "action_pdf_settings": "PDF 설정...",
        "action_about": "정보",
        "dialog_settings_title": "편집기 설정",
        "label_font": "글꼴:",
        "font_system": "시스템 (기본값)",
        "label_align": "텍스트 정렬:",
        "align_left": "왼쪽",
        "align_justify": "양쪽 정렬",
        "align_center": "가운데",
        "label_font_size": "글꼴 크기:",
        "label_text_width": "텍스트 너비:",
        "dialog_pdf_title": "PDF 내보내기 설정",
        "group_page": "페이지",
        "label_format": "형식:",
        "label_orientation": "방향:",
        "orient_portrait": "세로",
        "orient_landscape": "가로",
        "group_margins": "여백 (mm)",
        "label_margin_top": "위:",
        "label_margin_bottom": "아래:",
        "label_margin_left": "왼쪽:",
        "label_margin_right": "오른쪽:",
        "check_page_numbers": "페이지 번호 매기기 (하단 중앙)",
        "pdf_preview_title": "PDF 미리보기 — 저장 전",
        "btn_save": "저장...",
        "btn_cancel": "취소",
        "btn_ok": "확인",
        "save_pdf_title": "PDF 저장",
        "error": "오류",
        "error_save_pdf": "PDF를 저장하지 못했습니다:\n{e}",
        "error_open_file": "파일을 열지 못했습니다:\n{e}",
        "error_save_file": "파일을 저장하지 못했습니다:\n{e}",
        "error_load_export": "내보내기용 문서를 불러오지 못했습니다.",
        "error_generate_pdf": "PDF를 생성하지 못했습니다.",
        "error_open_folder": "폴더를 열지 못했습니다:\n{e}",
        "unsaved_title": "저장되지 않은 변경사항",
        "unsaved_text": "«{name}»에 저장되지 않은 변경사항이 있습니다.\n저장하시겠습니까?",
        "new_doc": "새 문서",
        "not_saved": "저장되지 않음",
        "state_modified": "수정됨",
        "state_saved": "저장됨",
        "status_new_memory": "새 문서가 생성되었습니다 (메모리 내)",
        "status_opened": "열림: {path}",
        "status_saved": "저장됨: {path}",
        "status_pasted_md": "Markdown으로 붙여넣었습니다",
        "status_pdf_exported": "PDF 내보내기 완료: {path}",
        "status_error": "오류: {e}",
        "placeholder": "여기에 Markdown을 입력하세요...\n\n예: # 제목\n\n$E = mc^2$",
        "preview_empty": "Markdown 입력을 시작하세요...",
        "preview_error": "오류: {e}",
        "export_empty_title": "내보내기",
        "export_empty_text": "문서가 비어 있습니다.",
        "done_title": "완료",
        "pdf_saved_text": "PDF 저장됨:\n{path}",
        "btn_show_in_folder": "폴더에서 보기",
        "about_title": "정보",
        "about_text": (
            "MarkKISS v{version}\n\n"
            "• 100% 오프라인 및 비공개로 작동하며, 기업 서버나 타사 도구에 의존하지 않습니다\n"
            "• 데이터베이스, AI 도구 및 기타 불필요한 요소 없이 순수 Markdown과 LaTeX만 사용합니다\n"
            "• Markdown 파일을 생성, 열기, 저장하고 PDF로 내보낼 수 있습니다\n"
            "• 제목, 수식, 코드의 휴리스틱 파싱 — 브라우저에서 AI 답변을 번거로움 없이 붙여넣기\n"
            "• 마크업 영역과 미리보기를 위한 단일 스크롤바\n"
            "• 변환 전 PDF 미리보기\n"
            "• 탭 관리: Ctrl+T — 새 탭, Ctrl+W — 닫기, Ctrl+Tab / Ctrl+Shift+Tab — 전환\n"
            "• 종속성: pip install markdownify beautifulsoup4 pygments markdown pymdown-extensions\n"
            "_______________________________________________________________________________________\n"
            "DeepSeek와 'Keep It Simple, Stupid!' 원칙의 도움으로, 기가바이트의 쓰레기 소프트웨어를 뒤진 사람이 만들었습니다.\n"
            "Dharma485 드림"
        ),
        "window_title": "{name} {version} (100% 오프라인 / KaTeX)",
        "window_title_doc": "{star}{name} — {app}",
        "language_names": {
            "en": "English", "ru": "Русский", "ko": "한국어", "ja": "日本語",
            "zh_CN": "简体中文", "zh_TW": "繁體中文", "de": "Deutsch",
            "es": "Español", "fr": "Français",
        },
    },
    "ja": {
        "menu_file": "ファイル",
        "menu_edit": "編集",
        "menu_settings": "設定",
        "menu_help": "ヘルプ",
        "menu_language": "言語",
        "action_new": "新規ドキュメント",
        "action_open": "開く...",
        "action_save": "保存",
        "action_save_as": "名前を付けて保存...",
        "action_close_tab": "タブを閉じる",
        "action_export_pdf": "PDFにエクスポート...",
        "action_exit": "終了",
        "action_undo": "元に戻す",
        "action_redo": "やり直す",
        "action_paste_md": "Markdownとして貼り付け (HTML → MD)",
        "action_next_tab": "次のタブ",
        "action_prev_tab": "前のタブ",
        "action_text_settings": "テキスト設定...",
        "action_pdf_settings": "PDF設定...",
        "action_about": "情報",
        "dialog_settings_title": "エディタ設定",
        "label_font": "フォント:",
        "font_system": "システム (デフォルト)",
        "label_align": "テキスト配置:",
        "align_left": "左揃え",
        "align_justify": "両端揃え",
        "align_center": "中央揃え",
        "label_font_size": "フォントサイズ:",
        "label_text_width": "テキスト幅:",
        "dialog_pdf_title": "PDFエクスポート設定",
        "group_page": "ページ",
        "label_format": "フォーマット:",
        "label_orientation": "向き:",
        "orient_portrait": "縦",
        "orient_landscape": "横",
        "group_margins": "余白 (mm)",
        "label_margin_top": "上:",
        "label_margin_bottom": "下:",
        "label_margin_left": "左:",
        "label_margin_right": "右:",
        "check_page_numbers": "ページ番号を付ける (下部中央)",
        "pdf_preview_title": "PDFプレビュー — 保存前",
        "btn_save": "保存...",
        "btn_cancel": "キャンセル",
        "btn_ok": "OK",
        "save_pdf_title": "PDFを保存",
        "error": "エラー",
        "error_save_pdf": "PDFの保存に失敗しました:\n{e}",
        "error_open_file": "ファイルを開けませんでした:\n{e}",
        "error_save_file": "ファイルの保存に失敗しました:\n{e}",
        "error_load_export": "エクスポート用ドキュメントの読み込みに失敗しました。",
        "error_generate_pdf": "PDFの生成に失敗しました。",
        "error_open_folder": "フォルダを開けませんでした:\n{e}",
        "unsaved_title": "未保存の変更",
        "unsaved_text": "「{name}」に未保存の変更があります。\n保存しますか?",
        "new_doc": "新規ドキュメント",
        "not_saved": "未保存",
        "state_modified": "変更済み",
        "state_saved": "保存済み",
        "status_new_memory": "新規ドキュメントを作成しました (メモリ内)",
        "status_opened": "開きました: {path}",
        "status_saved": "保存しました: {path}",
        "status_pasted_md": "Markdownとして貼り付けました",
        "status_pdf_exported": "PDFエクスポート完了: {path}",
        "status_error": "エラー: {e}",
        "placeholder": "ここにMarkdownを入力...\n\n例: # 見出し\n\n$E = mc^2$",
        "preview_empty": "Markdownの入力を開始してください...",
        "preview_error": "エラー: {e}",
        "export_empty_title": "エクスポート",
        "export_empty_text": "ドキュメントが空です。",
        "done_title": "完了",
        "pdf_saved_text": "PDFを保存しました:\n{path}",
        "btn_show_in_folder": "フォルダで表示",
        "about_title": "情報",
        "about_text": (
            "MarkKISS v{version}\n\n"
            "• 100%オフラインでプライベートに動作し、企業サーバーやサードパーティツールに依存しません\n"
            "• データベース、AIツール、その他の不要なものを含まず、純粋なMarkdownとLaTeXのみ\n"
            "• Markdownファイルの作成、開く、保存、PDFへのエクスポートが可能\n"
            "• 見出し、数式、コードのヒューリスティック解析 — ブラウザからAIの回答を手間なく貼り付け\n"
            "• マークアップ領域とプレビュー用の単一スクロールバー\n"
            "• 変換前のPDFプレビュー\n"
            "• タブ管理: Ctrl+T — 新規、Ctrl+W — 閉じる、Ctrl+Tab / Ctrl+Shift+Tab — 切り替え\n"
            "• 依存関係: pip install markdownify beautifulsoup4 pygments markdown pymdown-extensions\n"
            "_______________________________________________________________________________________\n"
            "DeepSeekと「Keep It Simple, Stupid!」の原則の助けを借りて、ギガバイトの不要なソフトウェアを掘り下げた人が作成しました。\n"
            "Dharma485より"
        ),
        "window_title": "{name} {version} (100% オフライン / KaTeX)",
        "window_title_doc": "{star}{name} — {app}",
        "language_names": {
            "en": "English", "ru": "Русский", "ko": "한국어", "ja": "日本語",
            "zh_CN": "简体中文", "zh_TW": "繁體中文", "de": "Deutsch",
            "es": "Español", "fr": "Français",
        },
    },
    "zh_CN": {
        "menu_file": "文件",
        "menu_edit": "编辑",
        "menu_settings": "设置",
        "menu_help": "帮助",
        "menu_language": "语言",
        "action_new": "新建文档",
        "action_open": "打开...",
        "action_save": "保存",
        "action_save_as": "另存为...",
        "action_close_tab": "关闭标签页",
        "action_export_pdf": "导出为 PDF...",
        "action_exit": "退出",
        "action_undo": "撤销",
        "action_redo": "重做",
        "action_paste_md": "粘贴为 Markdown (HTML → MD)",
        "action_next_tab": "下一个标签页",
        "action_prev_tab": "上一个标签页",
        "action_text_settings": "文本设置...",
        "action_pdf_settings": "PDF 设置...",
        "action_about": "关于",
        "dialog_settings_title": "编辑器设置",
        "label_font": "字体:",
        "font_system": "系统 (默认)",
        "label_align": "文本对齐:",
        "align_left": "左对齐",
        "align_justify": "两端对齐",
        "align_center": "居中",
        "label_font_size": "字体大小:",
        "label_text_width": "文本宽度:",
        "dialog_pdf_title": "PDF 导出设置",
        "group_page": "页面",
        "label_format": "格式:",
        "label_orientation": "方向:",
        "orient_portrait": "纵向",
        "orient_landscape": "横向",
        "group_margins": "页边距 (mm)",
        "label_margin_top": "上:",
        "label_margin_bottom": "下:",
        "label_margin_left": "左:",
        "label_margin_right": "右:",
        "check_page_numbers": "页码 (底部居中)",
        "pdf_preview_title": "PDF 预览 — 保存前",
        "btn_save": "保存...",
        "btn_cancel": "取消",
        "btn_ok": "确定",
        "save_pdf_title": "保存 PDF",
        "error": "错误",
        "error_save_pdf": "保存 PDF 失败:\n{e}",
        "error_open_file": "打开文件失败:\n{e}",
        "error_save_file": "保存文件失败:\n{e}",
        "error_load_export": "加载导出文档失败。",
        "error_generate_pdf": "生成 PDF 失败。",
        "error_open_folder": "打开文件夹失败:\n{e}",
        "unsaved_title": "未保存的更改",
        "unsaved_text": "“{name}” 有未保存的更改。\n是否保存?",
        "new_doc": "新建文档",
        "not_saved": "未保存",
        "state_modified": "已修改",
        "state_saved": "已保存",
        "status_new_memory": "已创建新文档 (内存中)",
        "status_opened": "已打开: {path}",
        "status_saved": "已保存: {path}",
        "status_pasted_md": "已粘贴为 Markdown",
        "status_pdf_exported": "PDF 已导出: {path}",
        "status_error": "错误: {e}",
        "placeholder": "在此输入 Markdown...\n\n示例: # 标题\n\n$E = mc^2$",
        "preview_empty": "开始输入 Markdown...",
        "preview_error": "错误: {e}",
        "export_empty_title": "导出",
        "export_empty_text": "文档为空。",
        "done_title": "完成",
        "pdf_saved_text": "PDF 已保存:\n{path}",
        "btn_show_in_folder": "在文件夹中显示",
        "about_title": "关于",
        "about_text": (
            "MarkKISS v{version}\n\n"
            "• 100% 离线私密运行，不依赖企业服务器和第三方工具\n"
            "• 无数据库、无 AI 工具、无其他杂项 — 只有纯 Markdown 和 LaTeX\n"
            "• 创建、打开、保存 Markdown 文件并导出为 PDF\n"
            "• 标题、公式和代码的启发式解析 — 从浏览器粘贴 AI 答案毫不费力\n"
            "• 标记语言区域和预览共用一个滚动条\n"
            "• 转换前预览 PDF\n"
            "• 标签页管理: Ctrl+T — 新建, Ctrl+W — 关闭, Ctrl+Tab / Ctrl+Shift+Tab — 切换\n"
            "• 依赖: pip install markdownify beautifulsoup4 pygments markdown pymdown-extensions\n"
            "_______________________________________________________________________________________\n"
            "在 DeepSeek 和 'Keep It Simple, Stupid!' 原则的帮助下，由一位翻遍数 GB 垃圾软件的人创建。\n"
            "您忠实的 Dharma485"
        ),
        "window_title": "{name} {version} (100% 离线 / KaTeX)",
        "window_title_doc": "{star}{name} — {app}",
        "language_names": {
            "en": "English", "ru": "Русский", "ko": "한국어", "ja": "日本語",
            "zh_CN": "简体中文", "zh_TW": "繁體中文", "de": "Deutsch",
            "es": "Español", "fr": "Français",
        },
    },
    "zh_TW": {
        "menu_file": "檔案",
        "menu_edit": "編輯",
        "menu_settings": "設定",
        "menu_help": "說明",
        "menu_language": "語言",
        "action_new": "新增文件",
        "action_open": "開啟...",
        "action_save": "儲存",
        "action_save_as": "另存新檔...",
        "action_close_tab": "關閉分頁",
        "action_export_pdf": "匯出為 PDF...",
        "action_exit": "結束",
        "action_undo": "復原",
        "action_redo": "重做",
        "action_paste_md": "貼上為 Markdown (HTML → MD)",
        "action_next_tab": "下一個分頁",
        "action_prev_tab": "上一個分頁",
        "action_text_settings": "文字設定...",
        "action_pdf_settings": "PDF 設定...",
        "action_about": "關於",
        "dialog_settings_title": "編輯器設定",
        "label_font": "字型:",
        "font_system": "系統 (預設)",
        "label_align": "文字對齊:",
        "align_left": "靠左對齊",
        "align_justify": "兩端對齊",
        "align_center": "置中",
        "label_font_size": "字型大小:",
        "label_text_width": "文字寬度:",
        "dialog_pdf_title": "PDF 匯出設定",
        "group_page": "頁面",
        "label_format": "格式:",
        "label_orientation": "方向:",
        "orient_portrait": "縱向",
        "orient_landscape": "橫向",
        "group_margins": "邊界 (mm)",
        "label_margin_top": "上:",
        "label_margin_bottom": "下:",
        "label_margin_left": "左:",
        "label_margin_right": "右:",
        "check_page_numbers": "頁碼 (底部置中)",
        "pdf_preview_title": "PDF 預覽 — 儲存前",
        "btn_save": "儲存...",
        "btn_cancel": "取消",
        "btn_ok": "確定",
        "save_pdf_title": "儲存 PDF",
        "error": "錯誤",
        "error_save_pdf": "儲存 PDF 失敗:\n{e}",
        "error_open_file": "開啟檔案失敗:\n{e}",
        "error_save_file": "儲存檔案失敗:\n{e}",
        "error_load_export": "載入匯出文件失敗。",
        "error_generate_pdf": "產生 PDF 失敗。",
        "error_open_folder": "開啟資料夾失敗:\n{e}",
        "unsaved_title": "未儲存的變更",
        "unsaved_text": "「{name}」有未儲存的變更。\n是否儲存?",
        "new_doc": "新增文件",
        "not_saved": "未儲存",
        "state_modified": "已修改",
        "state_saved": "已儲存",
        "status_new_memory": "已建立新文件 (記憶體中)",
        "status_opened": "已開啟: {path}",
        "status_saved": "已儲存: {path}",
        "status_pasted_md": "已貼上為 Markdown",
        "status_pdf_exported": "PDF 已匯出: {path}",
        "status_error": "錯誤: {e}",
        "placeholder": "在此輸入 Markdown...\n\n範例: # 標題\n\n$E = mc^2$",
        "preview_empty": "開始輸入 Markdown...",
        "preview_error": "錯誤: {e}",
        "export_empty_title": "匯出",
        "export_empty_text": "文件為空。",
        "done_title": "完成",
        "pdf_saved_text": "PDF 已儲存:\n{path}",
        "btn_show_in_folder": "在資料夾中顯示",
        "about_title": "關於",
        "about_text": (
            "MarkKISS v{version}\n\n"
            "• 100% 離線私密執行，不依賴企業伺服器和第三方工具\n"
            "• 無資料庫、無 AI 工具、無其他雜項 — 只有純 Markdown 和 LaTeX\n"
            "• 建立、開啟、儲存 Markdown 檔案並匯出為 PDF\n"
            "• 標題、公式和程式碼的啟發式解析 — 從瀏覽器貼上 AI 回答毫不費力\n"
            "• 標記語言區域和預覽共用一個捲軸\n"
            "• 轉換前預覽 PDF\n"
            "• 分頁管理: Ctrl+T — 新增, Ctrl+W — 關閉, Ctrl+Tab / Ctrl+Shift+Tab — 切換\n"
            "• 相依性: pip install markdownify beautifulsoup4 pygments markdown pymdown-extensions\n"
            "_______________________________________________________________________________________\n"
            "在 DeepSeek 和 'Keep It Simple, Stupid!' 原則的幫助下，由一位翻遍數 GB 垃圾軟體的人建立。\n"
            "您忠實的 Dharma485"
        ),
        "window_title": "{name} {version} (100% 離線 / KaTeX)",
        "window_title_doc": "{star}{name} — {app}",
        "language_names": {
            "en": "English", "ru": "Русский", "ko": "한국어", "ja": "日本語",
            "zh_CN": "简体中文", "zh_TW": "繁體中文", "de": "Deutsch",
            "es": "Español", "fr": "Français",
        },
    },
    "de": {
        "menu_file": "Datei",
        "menu_edit": "Bearbeiten",
        "menu_settings": "Einstellungen",
        "menu_help": "Hilfe",
        "menu_language": "Sprache",
        "action_new": "Neues Dokument",
        "action_open": "Öffnen...",
        "action_save": "Speichern",
        "action_save_as": "Speichern unter...",
        "action_close_tab": "Tab schließen",
        "action_export_pdf": "Als PDF exportieren...",
        "action_exit": "Beenden",
        "action_undo": "Rückgängig",
        "action_redo": "Wiederholen",
        "action_paste_md": "Als Markdown einfügen (HTML → MD)",
        "action_next_tab": "Nächster Tab",
        "action_prev_tab": "Vorheriger Tab",
        "action_text_settings": "Texteinstellungen...",
        "action_pdf_settings": "PDF-Einstellungen...",
        "action_about": "Info",
        "dialog_settings_title": "Editor-Einstellungen",
        "label_font": "Schriftart:",
        "font_system": "System (Standard)",
        "label_align": "Textausrichtung:",
        "align_left": "Linksbündig",
        "align_justify": "Blocksatz",
        "align_center": "Zentriert",
        "label_font_size": "Schriftgröße:",
        "label_text_width": "Textbreite:",
        "dialog_pdf_title": "PDF-Export-Einstellungen",
        "group_page": "Seite",
        "label_format": "Format:",
        "label_orientation": "Ausrichtung:",
        "orient_portrait": "Hochformat",
        "orient_landscape": "Querformat",
        "group_margins": "Ränder (mm)",
        "label_margin_top": "Oben:",
        "label_margin_bottom": "Unten:",
        "label_margin_left": "Links:",
        "label_margin_right": "Rechts:",
        "check_page_numbers": "Seiten nummerieren (unten zentriert)",
        "pdf_preview_title": "PDF-Vorschau — vor dem Speichern",
        "btn_save": "Speichern...",
        "btn_cancel": "Abbrechen",
        "btn_ok": "OK",
        "save_pdf_title": "PDF speichern",
        "error": "Fehler",
        "error_save_pdf": "PDF konnte nicht gespeichert werden:\n{e}",
        "error_open_file": "Datei konnte nicht geöffnet werden:\n{e}",
        "error_save_file": "Datei konnte nicht gespeichert werden:\n{e}",
        "error_load_export": "Dokument für den Export konnte nicht geladen werden.",
        "error_generate_pdf": "PDF konnte nicht generiert werden.",
        "error_open_folder": "Ordner konnte nicht geöffnet werden:\n{e}",
        "unsaved_title": "Ungespeicherte Änderungen",
        "unsaved_text": "„{name}“ hat ungespeicherte Änderungen.\nSpeichern?",
        "new_doc": "Neues Dokument",
        "not_saved": "Nicht gespeichert",
        "state_modified": "geändert",
        "state_saved": "gespeichert",
        "status_new_memory": "Neues Dokument erstellt (im Speicher)",
        "status_opened": "Geöffnet: {path}",
        "status_saved": "Gespeichert: {path}",
        "status_pasted_md": "Als Markdown eingefügt",
        "status_pdf_exported": "PDF exportiert: {path}",
        "status_error": "Fehler: {e}",
        "placeholder": "Markdown hier eingeben...\n\nBeispiel: # Überschrift\n\n$E = mc^2$",
        "preview_empty": "Beginnen Sie mit der Eingabe von Markdown...",
        "preview_error": "Fehler: {e}",
        "export_empty_title": "Export",
        "export_empty_text": "Dokument ist leer.",
        "done_title": "Fertig",
        "pdf_saved_text": "PDF gespeichert:\n{path}",
        "btn_show_in_folder": "Im Ordner anzeigen",
        "about_title": "Info",
        "about_text": (
            "MarkKISS v{version}\n\n"
            "• Funktioniert 100% offline und privat, unabhängig von Unternehmensservern und Drittanbieter-Tools\n"
            "• Keine Datenbanken, keine KI-Tools, kein anderer Müll — nur reines Markdown und LaTeX\n"
            "• Markdown-Dateien erstellen, öffnen, speichern und als PDF exportieren\n"
            "• Heuristische Analyse von Überschriften, Formeln und Code — KI-Antworten aus dem Browser problemlos einfügen\n"
            "• Ein einziger Scrollbalken für Markup-Bereich und Vorschau\n"
            "• PDF-Vorschau vor der Konvertierung\n"
            "• Tab-Verwaltung: Ctrl+T — neu, Ctrl+W — schließen, Ctrl+Tab / Ctrl+Shift+Tab — wechseln\n"
            "• Abhängigkeiten: pip install markdownify beautifulsoup4 pygments markdown pymdown-extensions\n"
            "_______________________________________________________________________________________\n"
            "Erstellt mit Hilfe von DeepSeek und dem Prinzip 'Keep It Simple, Stupid!' von einer Person, "
            "die Gigabytes an Müllsoftware durchwühlt hat.\n"
            "Ihr ergebener Dharma485"
        ),
        "window_title": "{name} {version} (100% Offline / KaTeX)",
        "window_title_doc": "{star}{name} — {app}",
        "language_names": {
            "en": "English", "ru": "Русский", "ko": "한국어", "ja": "日本語",
            "zh_CN": "简体中文", "zh_TW": "繁體中文", "de": "Deutsch",
            "es": "Español", "fr": "Français",
        },
    },
    "es": {
        "menu_file": "Archivo",
        "menu_edit": "Edición",
        "menu_settings": "Configuración",
        "menu_help": "Ayuda",
        "menu_language": "Idioma",
        "action_new": "Nuevo documento",
        "action_open": "Abrir...",
        "action_save": "Guardar",
        "action_save_as": "Guardar como...",
        "action_close_tab": "Cerrar pestaña",
        "action_export_pdf": "Exportar a PDF...",
        "action_exit": "Salir",
        "action_undo": "Deshacer",
        "action_redo": "Rehacer",
        "action_paste_md": "Pegar como Markdown (HTML → MD)",
        "action_next_tab": "Siguiente pestaña",
        "action_prev_tab": "Pestaña anterior",
        "action_text_settings": "Configuración de texto...",
        "action_pdf_settings": "Configuración de PDF...",
        "action_about": "Acerca de",
        "dialog_settings_title": "Configuración del editor",
        "label_font": "Fuente:",
        "font_system": "Sistema (predeterminada)",
        "label_align": "Alineación del texto:",
        "align_left": "Izquierda",
        "align_justify": "Justificado",
        "align_center": "Centrado",
        "label_font_size": "Tamaño de fuente:",
        "label_text_width": "Ancho del texto:",
        "dialog_pdf_title": "Configuración de exportación a PDF",
        "group_page": "Página",
        "label_format": "Formato:",
        "label_orientation": "Orientación:",
        "orient_portrait": "Vertical",
        "orient_landscape": "Horizontal",
        "group_margins": "Márgenes (mm)",
        "label_margin_top": "Superior:",
        "label_margin_bottom": "Inferior:",
        "label_margin_left": "Izquierdo:",
        "label_margin_right": "Derecho:",
        "check_page_numbers": "Numerar páginas (centrado abajo)",
        "pdf_preview_title": "Vista previa de PDF — antes de guardar",
        "btn_save": "Guardar...",
        "btn_cancel": "Cancelar",
        "btn_ok": "Aceptar",
        "save_pdf_title": "Guardar PDF",
        "error": "Error",
        "error_save_pdf": "No se pudo guardar el PDF:\n{e}",
        "error_open_file": "No se pudo abrir el archivo:\n{e}",
        "error_save_file": "No se pudo guardar el archivo:\n{e}",
        "error_load_export": "No se pudo cargar el documento para exportar.",
        "error_generate_pdf": "No se pudo generar el PDF.",
        "error_open_folder": "No se pudo abrir la carpeta:\n{e}",
        "unsaved_title": "Cambios sin guardar",
        "unsaved_text": "«{name}» tiene cambios sin guardar.\n¿Guardarlos?",
        "new_doc": "Nuevo documento",
        "not_saved": "Sin guardar",
        "state_modified": "modificado",
        "state_saved": "guardado",
        "status_new_memory": "Nuevo documento creado (en memoria)",
        "status_opened": "Abierto: {path}",
        "status_saved": "Guardado: {path}",
        "status_pasted_md": "Pegado como Markdown",
        "status_pdf_exported": "PDF exportado: {path}",
        "status_error": "Error: {e}",
        "placeholder": "Escriba Markdown aquí...\n\nEjemplo: # Encabezado\n\n$E = mc^2$",
        "preview_empty": "Empiece a escribir Markdown...",
        "preview_error": "Error: {e}",
        "export_empty_title": "Exportar",
        "export_empty_text": "El documento está vacío.",
        "done_title": "Hecho",
        "pdf_saved_text": "PDF guardado:\n{path}",
        "btn_show_in_folder": "Mostrar en carpeta",
        "about_title": "Acerca de",
        "about_text": (
            "MarkKISS v{version}\n\n"
            "• Funciona 100% offline y de forma privada, independiente de servidores corporativos y herramientas de terceros\n"
            "• Sin bases de datos, sin herramientas de IA, sin otra basura — solo Markdown puro y LaTeX\n"
            "• Crear, abrir, guardar archivos Markdown y exportarlos a PDF\n"
            "• Análisis heurístico de encabezados, fórmulas y código — pegue respuestas de IA desde el navegador sin complicaciones\n"
            "• Una sola barra de desplazamiento para el área de marcado y la vista previa\n"
            "• Vista previa de PDF antes de la conversión\n"
            "• Gestión de pestañas: Ctrl+T — nueva, Ctrl+W — cerrar, Ctrl+Tab / Ctrl+Shift+Tab — cambiar\n"
            "• Dependencias: pip install markdownify beautifulsoup4 pygments markdown pymdown-extensions\n"
            "_______________________________________________________________________________________\n"
            "Creado con la ayuda de DeepSeek y el principio 'Keep It Simple, Stupid!' por una persona "
            "que ha rebuscado en gigabytes de software basura.\n"
            "Su servidor, Dharma485"
        ),
        "window_title": "{name} {version} (100% Offline / KaTeX)",
        "window_title_doc": "{star}{name} — {app}",
        "language_names": {
            "en": "English", "ru": "Русский", "ko": "한국어", "ja": "日本語",
            "zh_CN": "简体中文", "zh_TW": "繁體中文", "de": "Deutsch",
            "es": "Español", "fr": "Français",
        },
    },
    "fr": {
        "menu_file": "Fichier",
        "menu_edit": "Édition",
        "menu_settings": "Paramètres",
        "menu_help": "Aide",
        "menu_language": "Langue",
        "action_new": "Nouveau document",
        "action_open": "Ouvrir...",
        "action_save": "Enregistrer",
        "action_save_as": "Enregistrer sous...",
        "action_close_tab": "Fermer l'onglet",
        "action_export_pdf": "Exporter en PDF...",
        "action_exit": "Quitter",
        "action_undo": "Annuler",
        "action_redo": "Rétablir",
        "action_paste_md": "Coller en Markdown (HTML → MD)",
        "action_next_tab": "Onglet suivant",
        "action_prev_tab": "Onglet précédent",
        "action_text_settings": "Paramètres du texte...",
        "action_pdf_settings": "Paramètres PDF...",
        "action_about": "À propos",
        "dialog_settings_title": "Paramètres de l'éditeur",
        "label_font": "Police:",
        "font_system": "Système (par défaut)",
        "label_align": "Alignement du texte:",
        "align_left": "Gauche",
        "align_justify": "Justifié",
        "align_center": "Centré",
        "label_font_size": "Taille de police:",
        "label_text_width": "Largeur du texte:",
        "dialog_pdf_title": "Paramètres d'export PDF",
        "group_page": "Page",
        "label_format": "Format:",
        "label_orientation": "Orientation:",
        "orient_portrait": "Portrait",
        "orient_landscape": "Paysage",
        "group_margins": "Marges (mm)",
        "label_margin_top": "Haut:",
        "label_margin_bottom": "Bas:",
        "label_margin_left": "Gauche:",
        "label_margin_right": "Droite:",
        "check_page_numbers": "Numéroter les pages (centré en bas)",
        "pdf_preview_title": "Aperçu PDF — avant enregistrement",
        "btn_save": "Enregistrer...",
        "btn_cancel": "Annuler",
        "btn_ok": "OK",
        "save_pdf_title": "Enregistrer le PDF",
        "error": "Erreur",
        "error_save_pdf": "Échec de l'enregistrement du PDF:\n{e}",
        "error_open_file": "Échec de l'ouverture du fichier:\n{e}",
        "error_save_file": "Échec de l'enregistrement du fichier:\n{e}",
        "error_load_export": "Échec du chargement du document pour l'export.",
        "error_generate_pdf": "Échec de la génération du PDF.",
        "error_open_folder": "Échec de l'ouverture du dossier:\n{e}",
        "unsaved_title": "Modifications non enregistrées",
        "unsaved_text": "« {name} » contient des modifications non enregistrées.\nLes enregistrer?",
        "new_doc": "Nouveau document",
        "not_saved": "Non enregistré",
        "state_modified": "modifié",
        "state_saved": "enregistré",
        "status_new_memory": "Nouveau document créé (en mémoire)",
        "status_opened": "Ouvert: {path}",
        "status_saved": "Enregistré: {path}",
        "status_pasted_md": "Collé en Markdown",
        "status_pdf_exported": "PDF exporté: {path}",
        "status_error": "Erreur: {e}",
        "placeholder": "Saisissez le Markdown ici...\n\nExemple: # Titre\n\n$E = mc^2$",
        "preview_empty": "Commencez à saisir du Markdown...",
        "preview_error": "Erreur: {e}",
        "export_empty_title": "Export",
        "export_empty_text": "Le document est vide.",
        "done_title": "Terminé",
        "pdf_saved_text": "PDF enregistré:\n{path}",
        "btn_show_in_folder": "Afficher dans le dossier",
        "about_title": "À propos",
        "about_text": (
            "MarkKISS v{version}\n\n"
            "• Fonctionne 100% hors ligne et en privé, indépendamment des serveurs d'entreprise et des outils tiers\n"
            "• Pas de bases de données, pas d'outils d'IA, pas d'autres déchets — uniquement du Markdown pur et du LaTeX\n"
            "• Créer, ouvrir, enregistrer des fichiers Markdown et les exporter en PDF\n"
            "• Analyse heuristique des titres, formules et code — collez les réponses d'IA depuis le navigateur sans difficulté\n"
            "• Une seule barre de défilement pour la zone de balisage et l'aperçu\n"
            "• Aperçu PDF avant conversion\n"
            "• Gestion des onglets: Ctrl+T — nouveau, Ctrl+W — fermer, Ctrl+Tab / Ctrl+Shift+Tab — changer\n"
            "• Dépendances: pip install markdownify beautifulsoup4 pygments markdown pymdown-extensions\n"
            "_______________________________________________________________________________________\n"
            "Créé avec l'aide de DeepSeek et du principe 'Keep It Simple, Stupid!' par une personne "
            "qui a fouillé des gigaoctets de logiciels indésirables.\n"
            "Votre serviteur, Dharma485"
        ),
        "window_title": "{name} {version} (100% Hors ligne / KaTeX)",
        "window_title_doc": "{star}{name} — {app}",
        "language_names": {
            "en": "English", "ru": "Русский", "ko": "한국어", "ja": "日本語",
            "zh_CN": "简体中文", "zh_TW": "繁體中文", "de": "Deutsch",
            "es": "Español", "fr": "Français",
        },
    },
}


def get_translations(lang):
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"])


def tr(lang, key, **kwargs):
    t = get_translations(lang)
    s = t.get(key, TRANSLATIONS["en"].get(key, key))
    if kwargs:
        return s.format(**kwargs)
    return s


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

def load_settings():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {**DEFAULT_SETTINGS, **data.get("text", {})}
        except Exception:
            pass
    return DEFAULT_SETTINGS.copy()


def load_pdf_settings():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {**DEFAULT_PDF_SETTINGS, **data.get("pdf", {})}
        except Exception:
            pass
    return DEFAULT_PDF_SETTINGS.copy()


def save_settings(settings, pdf_settings):
    data = {"text": settings, "pdf": pdf_settings}
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def _read_local_file(filename):
    path = os.path.join(KATEX_DIR, filename)
    if not os.path.exists(path):
        return f"/* File not found: {filename} */"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# HTML -> Markdown
# ---------------------------------------------------------------------------

def restore_latex(html: str) -> str:
    if not html:
        return html
    try:
        soup = BeautifulSoup(html, "html.parser")
    except Exception:
        return html

    for ann in soup.select('annotation[encoding="application/x-tex"]'):
        tex = ann.get_text()
        parent_math = ann.find_parent("math")
        if parent_math is None:
            continue
        display = (parent_math.get("display") == "block")
        wrapper = f"$${tex}$$" if display else f"${tex}$"
        parent_math.replace_with(wrapper)
    return str(soup)


def _promote_bold_blocks_to_headings(html: str) -> str:
    try:
        soup = BeautifulSoup(html, "html.parser")
    except Exception:
        return html

    candidates = soup.find_all(["div", "p", "span"])
    existing_levels = [int(t.name[1]) for t in soup.find_all(re.compile(r"^h[1-6]$"))]
    next_level = (max(existing_levels) + 1) if existing_levels else 1
    next_level = min(next_level, 6)

    for block in candidates:
        if block.find_parent(["blockquote", "li", "pre", "code", "table"]):
            continue
        text = block.get_text(strip=True)
        if not text or len(text) > 200:
            continue
        if text.startswith("#"):
            continue

        style = block.get("style", "").lower().replace(" ", "")
        classes = " ".join(block.get("class", [])).lower()

        is_heading = False
        level_hint = None

        for cls, lvl in (
            ("text-4xl", 1), ("text-3xl", 1), ("text-2xl", 2),
            ("text-xl", 3), ("text-lg", 4),
            ("font-bold", None), ("font-semibold", None), ("font-extrabold", None),
        ):
            if cls in classes:
                if lvl is not None:
                    is_heading = True
                    level_hint = lvl if level_hint is None else min(level_hint, lvl)
                else:
                    is_heading = True

        m = re.search(r"font-size:(\d+(?:\.\d+)?)px", style)
        if m:
            px = float(m.group(1))
            if px >= 24:
                is_heading, level_hint = True, 1
            elif px >= 20:
                is_heading, level_hint = True, 2
            elif px >= 18:
                is_heading, level_hint = True, 3
            elif px >= 16 and "font-weight:bold" in style:
                is_heading, level_hint = True, 4

        if not is_heading:
            if re.search(r"font-weight:(bold|700|800|900)", style) and len(text) <= 120:
                is_heading = True

        if not is_heading and block.name in ("p", "div"):
            kids = [c for c in block.contents if getattr(c, "name", None)]
            if len(kids) == 1 and kids[0].name in ("strong", "b") and len(text) <= 120:
                is_heading = True

        if not is_heading:
            continue

        if level_hint is not None:
            lvl = level_hint
        else:
            lvl = next_level
            next_level = min(next_level + 1, 6)

        new_tag = soup.new_tag(f"h{lvl}")
        for child in list(block.contents):
            new_tag.append(child.extract())
        block.replace_with(new_tag)

    return str(soup)


def html_to_markdown(html: str) -> str:
    if not html:
        return ""
    html = restore_latex(html)
    html = _promote_bold_blocks_to_headings(html)
    text = md_convert(
        html,
        heading_style="ATX",
        bullets="-",
        strong_em_symbol="*",
        escape_underscores=False,
        escape_asterisks=False,
        strip=["script", "style", "noscript", "svg"],
    )
    if not text:
        return ""
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    return text.strip() + "\n"


# ---------------------------------------------------------------------------
# Syntax highlighting
# ---------------------------------------------------------------------------

class MarkdownHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.rules = []

        fmt_h = QTextCharFormat()
        fmt_h.setFontWeight(QFont.Weight.Bold)
        fmt_h.setForeground(QColor("#61AFEF"))
        self.rules.append((QRegularExpression(r"^#{1,6}\s.*$"), fmt_h))

        fmt_b = QTextCharFormat()
        fmt_b.setFontWeight(QFont.Weight.Bold)
        fmt_b.setForeground(QColor("#E5C07B"))
        self.rules.append((QRegularExpression(r"\*\*[^\*]+\*\*"), fmt_b))

        fmt_i = QTextCharFormat()
        fmt_i.setFontItalic(True)
        fmt_i.setForeground(QColor("#ABB2BF"))
        self.rules.append((QRegularExpression(r"(?<!\*)\*[^\*]+\*(?!\*)"), fmt_i))

        fmt_c = QTextCharFormat()
        fmt_c.setFontFamily("Consolas")
        fmt_c.setForeground(QColor("#E06C75"))
        self.rules.append((QRegularExpression(r"`[^`]+`"), fmt_c))

        fmt_l = QTextCharFormat()
        fmt_l.setForeground(QColor("#61AFEF"))
        fmt_l.setFontUnderline(True)
        self.rules.append((QRegularExpression(r"\[[^\]]+\]\([^\)]+\)"), fmt_l))

        fmt_f = QTextCharFormat()
        fmt_f.setForeground(QColor("#C678DD"))
        fmt_f.setFontFamily("Consolas")
        self.rules.append((QRegularExpression(r"\$\$[^\$]+\$\$"), fmt_f))
        self.rules.append((QRegularExpression(r"(?<!\$)\$[^\$\n]+\$(?!\$)"), fmt_f))

        self.fmt_codeblock = QTextCharFormat()
        self.fmt_codeblock.setFontFamily("Consolas")
        self.fmt_codeblock.setForeground(QColor("#98C379"))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                m = it.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), fmt)

        self.setCurrentBlockState(0)
        if self.previousBlockState() == 1:
            start = 0
            end = text.find("```")
            if end == -1:
                self.setFormat(0, len(text), self.fmt_codeblock)
                self.setCurrentBlockState(1)
                return
            else:
                self.setFormat(0, end + 3, self.fmt_codeblock)
                return
        idx = text.find("```")
        if idx != -1:
            self.setFormat(idx, len(text) - idx, self.fmt_codeblock)
            self.setCurrentBlockState(1)


class MarkdownTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighter = MarkdownHighlighter(self.document())
        font = QFont("Consolas", 11)
        self.setFont(font)

    def insertFromMimeData(self, source):
        if source is not None and source.hasHtml():
            try:
                md_text = html_to_markdown(source.html())
                if md_text.strip():
                    cursor = self.textCursor()
                    cursor.insertText(md_text)
                    return
            except Exception:
                pass
        super().insertFromMimeData(source)


# ---------------------------------------------------------------------------
# Dialogs
# ---------------------------------------------------------------------------

class SettingsDialog(QDialog):
    def __init__(self, parent=None, settings=None):
        super().__init__(parent)
        self.settings = settings or DEFAULT_SETTINGS.copy()
        self.lang = self.settings.get("language", "en")
        self.setWindowTitle(tr(self.lang, "dialog_settings_title"))
        layout = QFormLayout(self)

        self.font_combo = QComboBox()
        self.font_combo.addItem(tr(self.lang, "font_system"))
        self.font_combo.addItems(["Times New Roman", "Arial", "Georgia", "Courier New"])
        font_map = {"system": 0, "Times New Roman": 1, "Arial": 2, "Georgia": 3, "Courier New": 4}
        self.font_combo.setCurrentIndex(font_map.get(self.settings["font_family"], 0))
        layout.addRow(tr(self.lang, "label_font"), self.font_combo)

        self.align_combo = QComboBox()
        self.align_combo.addItem(tr(self.lang, "align_left"))
        self.align_combo.addItem(tr(self.lang, "align_justify"))
        self.align_combo.addItem(tr(self.lang, "align_center"))
        align_map = {"left": 0, "justify": 1, "center": 2}
        self.align_combo.setCurrentIndex(align_map.get(self.settings["text_align"], 0))
        layout.addRow(tr(self.lang, "label_align"), self.align_combo)

        self.size_spin = QSpinBox()
        self.size_spin.setRange(10, 32)
        self.size_spin.setValue(self.settings["font_size"])
        layout.addRow(tr(self.lang, "label_font_size"), self.size_spin)

        self.width_spin = QSpinBox()
        self.width_spin.setRange(400, 2000)
        self.width_spin.setSingleStep(50)
        self.width_spin.setValue(self.settings["max_width"])
        self.width_spin.setSuffix(" px")
        layout.addRow(tr(self.lang, "label_text_width"), self.width_spin)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_settings(self):
        fonts = ["system", "Times New Roman", "Arial", "Georgia", "Courier New"]
        aligns = ["left", "justify", "center"]
        return {
            "font_family": fonts[self.font_combo.currentIndex()],
            "text_align": aligns[self.align_combo.currentIndex()],
            "font_size": self.size_spin.value(),
            "max_width": self.width_spin.value()
        }


class PdfExportDialog(QDialog):
    PAGE_SIZES = [
        ("A4 (210 × 297 mm)", "A4"),
        ("Letter (216 × 279 mm)", "Letter"),
        ("Legal (216 × 356 mm)", "Legal"),
        ("A3 (297 × 420 mm)", "A3"),
        ("A5 (148 × 210 mm)", "A5"),
    ]

    def __init__(self, parent=None, settings=None, lang="en"):
        super().__init__(parent)
        self.settings = settings or DEFAULT_PDF_SETTINGS.copy()
        self.lang = lang
        self.setWindowTitle(tr(self.lang, "dialog_pdf_title"))
        layout = QVBoxLayout(self)

        page_group = QGroupBox(tr(self.lang, "group_page"))
        page_layout = QFormLayout(page_group)
        self.size_combo = QComboBox()
        for label, key in self.PAGE_SIZES:
            self.size_combo.addItem(label, key)
        for i, (_, key) in enumerate(self.PAGE_SIZES):
            if key == self.settings.get("page_size", "A4"):
                self.size_combo.setCurrentIndex(i)
                break
        page_layout.addRow(tr(self.lang, "label_format"), self.size_combo)

        self.orientation_combo = QComboBox()
        self.orientation_combo.addItem(tr(self.lang, "orient_portrait"), "portrait")
        self.orientation_combo.addItem(tr(self.lang, "orient_landscape"), "landscape")
        if self.settings.get("orientation", "portrait") == "landscape":
            self.orientation_combo.setCurrentIndex(1)
        page_layout.addRow(tr(self.lang, "label_orientation"), self.orientation_combo)
        layout.addWidget(page_group)

        margins_group = QGroupBox(tr(self.lang, "group_margins"))
        margins_layout = QFormLayout(margins_group)
        self.top_spin = QSpinBox(); self.top_spin.setRange(0, 100); self.top_spin.setValue(self.settings.get("margin_top", 20))
        margins_layout.addRow(tr(self.lang, "label_margin_top"), self.top_spin)
        self.bottom_spin = QSpinBox(); self.bottom_spin.setRange(0, 100); self.bottom_spin.setValue(self.settings.get("margin_bottom", 20))
        margins_layout.addRow(tr(self.lang, "label_margin_bottom"), self.bottom_spin)
        self.left_spin = QSpinBox(); self.left_spin.setRange(0, 100); self.left_spin.setValue(self.settings.get("margin_left", 20))
        margins_layout.addRow(tr(self.lang, "label_margin_left"), self.left_spin)
        self.right_spin = QSpinBox(); self.right_spin.setRange(0, 100); self.right_spin.setValue(self.settings.get("margin_right", 20))
        margins_layout.addRow(tr(self.lang, "label_margin_right"), self.right_spin)
        layout.addWidget(margins_group)

        self.page_numbers_check = QCheckBox(tr(self.lang, "check_page_numbers"))
        self.page_numbers_check.setChecked(self.settings.get("page_numbers", True))
        layout.addWidget(self.page_numbers_check)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_settings(self):
        return {
            "page_size": self.size_combo.currentData(),
            "orientation": self.orientation_combo.currentData(),
            "margin_top": self.top_spin.value(),
            "margin_bottom": self.bottom_spin.value(),
            "margin_left": self.left_spin.value(),
            "margin_right": self.right_spin.value(),
            "page_numbers": self.page_numbers_check.isChecked(),
        }


class PdfPreviewDialog(QDialog):
    def __init__(self, pdf_data: bytes, parent=None, suggested_name: str = "document.pdf", lang="en"):
        super().__init__(parent)
        self.pdf_data = pdf_data
        self.suggested_name = suggested_name
        self.saved_path = None
        self.lang = lang
        self.setWindowTitle(tr(self.lang, "pdf_preview_title"))
        self.resize(1000, 800)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.pdf_view = QPdfView(self)
        self.pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
        self.pdf_view.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        self.pdf_view.setStyleSheet("background-color: #525252;")

        self.document = QPdfDocument(self)
        self._buffer = QBuffer(self)
        self._buffer.setData(pdf_data)
        self._buffer.open(QIODevice.OpenModeFlag.ReadOnly)
        self.document.load(self._buffer)
        self.pdf_view.setDocument(self.document)
        layout.addWidget(self.pdf_view, 1)

        buttons = QDialogButtonBox(self)
        save_btn = buttons.addButton(tr(self.lang, "btn_save"), QDialogButtonBox.ButtonRole.AcceptRole)
        cancel_btn = buttons.addButton(tr(self.lang, "btn_cancel"), QDialogButtonBox.ButtonRole.RejectRole)
        save_btn.clicked.connect(self._on_save)
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(buttons)

    def _on_save(self):
        path, _ = QFileDialog.getSaveFileName(
            self, tr(self.lang, "save_pdf_title"), self.suggested_name, "PDF (*.pdf)"
        )
        if not path:
            return
        try:
            with open(path, 'wb') as f:
                f.write(self.pdf_data)
        except Exception as e:
            QMessageBox.critical(self, tr(self.lang, "error"), tr(self.lang, "error_save_pdf", e=e))
            return
        self.saved_path = path
        self.accept()


# ---------------------------------------------------------------------------
# Document tab
# ---------------------------------------------------------------------------

class DocumentTab(QWidget):
    """A single tab: editor + preview + file state."""

    def __init__(self, window: "MarkdownEditor", text: str = "", path: str | None = None):
        super().__init__()
        self.window = window
        self.current_file = path
        self._modified = False
        self._loading = False
        self._sync_scroll_lock = False
        self._preview_timer = QTimer(self)
        self._preview_timer.setSingleShot(True)
        self._preview_timer.timeout.connect(self.update_preview)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        left = QWidget()
        left_l = QVBoxLayout(left)
        left_l.setContentsMargins(4, 4, 4, 4)
        self.editor = MarkdownTextEdit()
        self.editor.setPlaceholderText(tr(self.window.settings.get("language", "en"), "placeholder"))
        self.editor.textChanged.connect(self._on_text_changed)
        left_l.addWidget(self.editor)

        right = QWidget()
        right_l = QVBoxLayout(right)
        right_l.setContentsMargins(4, 4, 4, 4)
        self.preview = QWebEngineView()
        self.preview.settings().setAttribute(
            QWebEngineSettings.WebAttribute.ShowScrollBars, False
        )
        right_l.addWidget(self.preview)

        self.splitter.addWidget(left)
        self.splitter.addWidget(right)
        self.splitter.setSizes([600, 600])
        layout.addWidget(self.splitter)

        self.editor.verticalScrollBar().valueChanged.connect(self._on_editor_scrolled)
        self._scroll_poll_timer = QTimer(self)
        self._scroll_poll_timer.setInterval(100)
        self._scroll_poll_timer.timeout.connect(self._poll_preview_scroll)
        self._scroll_poll_timer.start()

        if text:
            self._loading = True
            self.editor.setPlainText(text)
            self._loading = False
        self.update_preview()

    def is_modified(self) -> bool:
        return self._modified

    def display_name(self) -> str:
        if self.current_file:
            return os.path.basename(self.current_file)
        return tr(self.window.settings.get("language", "en"), "new_doc")

    def tab_title(self) -> str:
        return ("*" if self._modified else "") + self.display_name()

    def mark_saved(self, path: str):
        self.current_file = path
        self._modified = False
        self.window.refresh_tab_title(self)
        self.window.update_title_and_status()

    def set_text(self, text: str):
        self._loading = True
        self.editor.setPlainText(text)
        self._loading = False
        self._modified = False
        self.update_preview()
        self.window.refresh_tab_title(self)

    def _on_text_changed(self):
        if not self._loading and not self._modified:
            self._modified = True
            self.window.refresh_tab_title(self)
            self.window.update_title_and_status()
        self._preview_timer.stop()
        self._preview_timer.start(300)

    def _on_editor_scrolled(self, value):
        if self._sync_scroll_lock:
            return
        sb = self.editor.verticalScrollBar()
        if sb.maximum() <= 0:
            return
        ratio = value / sb.maximum()
        self._sync_scroll_lock = True
        js = f"""
        (function() {{
            var el = document.scrollingElement || document.documentElement;
            var max = el.scrollHeight - el.clientHeight;
            if (max > 0) window.scrollTo(0, max * {ratio:.6f});
        }})();
        """
        self.preview.page().runJavaScript(js)
        QTimer.singleShot(50, lambda: setattr(self, '_sync_scroll_lock', False))

    def _poll_preview_scroll(self):
        if self._sync_scroll_lock:
            return
        js = """
        (function() {
            var el = document.scrollingElement || document.documentElement;
            var max = el.scrollHeight - el.clientHeight;
            if (max <= 0) return null;
            return el.scrollTop / max;
        })();
        """
        def cb(ratio):
            if ratio is None or self._sync_scroll_lock:
                return
            sb = self.editor.verticalScrollBar()
            if sb.maximum() <= 0:
                return
            self._sync_scroll_lock = True
            sb.setValue(int(ratio * sb.maximum()))
            QTimer.singleShot(50, lambda: setattr(self, '_sync_scroll_lock', False))
        self.preview.page().runJavaScript(js, cb)

    def update_preview(self):
        text = self.editor.toPlainText()
        lang = self.window.settings.get("language", "en")
        if not text.strip():
            self.preview.setHtml(
                f"<p style='color:#999;'>{tr(lang, 'preview_empty')}</p>"
            )
            return
        try:
            js_get_scroll = """
            (function() {
                var el = document.scrollingElement || document.documentElement;
                var max = el.scrollHeight - el.clientHeight;
                if (max <= 0) return "0";
                return (el.scrollTop / max).toString();
            })();
            """
            def on_scroll_saved(ratio):
                body = self.window._convert_markdown_to_html(text)
                html = self.window._wrap_html(body, for_print=False)
                scroll_js = f"""
                <script>
                window.addEventListener('load', function() {{
                    var el = document.scrollingElement || document.documentElement;
                    var max = el.scrollHeight - el.clientHeight;
                    if (max > 0) window.scrollTo(0, max * {ratio});
                }});
                </script>
                """
                html = html.replace("</body>", scroll_js + "</body>")
                base_url = QUrl.fromLocalFile(KATEX_DIR + os.sep)
                self.preview.setHtml(html, base_url)
            self.preview.page().runJavaScript(js_get_scroll, on_scroll_saved)
        except Exception as e:
            self.preview.setHtml(f"<p style='color:red;'>{tr(lang, 'preview_error', e=e)}</p>")


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------

class MarkdownEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        self.pdf_settings = load_pdf_settings()
        self.lang = self.settings.get("language", "en")
        self.setWindowTitle(
            tr(self.lang, "window_title", name=APP_NAME, version=APP_VERSION)
        )
        self.resize(1200, 800)
        self._init_ui()
        self._init_menu()
        self._add_new_tab()
        self._startup_tab_consumed = False
        self.update_title_and_status()

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------
    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)
        self.tabs.tabCloseRequested.connect(self._close_tab_at)
        self.tabs.currentChanged.connect(self._on_tab_changed)
        layout.addWidget(self.tabs)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.file_label = QLabel("")
        self.status_bar.addPermanentWidget(self.file_label)

    def _init_menu(self):
        menubar = self.menuBar()
        menubar.clear()
        lang = self.lang

        file_menu = menubar.addMenu(tr(lang, "menu_file"))

        new_action = QAction(tr(lang, "action_new"), self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self._new_file)
        file_menu.addAction(new_action)

        open_action = QAction(tr(lang, "action_open"), self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self._open_file)
        file_menu.addAction(open_action)

        save_action = QAction(tr(lang, "action_save"), self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self._save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction(tr(lang, "action_save_as"), self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self._save_file_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        close_tab_action = QAction(tr(lang, "action_close_tab"), self)
        close_tab_action.setShortcut(QKeySequence("Ctrl+W"))
        close_tab_action.triggered.connect(self._close_current_tab)
        file_menu.addAction(close_tab_action)

        file_menu.addSeparator()

        export_pdf_action = QAction(tr(lang, "action_export_pdf"), self)
        export_pdf_action.setShortcut(QKeySequence("Ctrl+Shift+P"))
        export_pdf_action.triggered.connect(self._export_pdf)
        file_menu.addAction(export_pdf_action)

        file_menu.addSeparator()

        exit_action = QAction(tr(lang, "action_exit"), self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu(tr(lang, "menu_edit"))

        undo_action = QAction(tr(lang, "action_undo"), self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(self._undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction(tr(lang, "action_redo"), self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(self._redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        paste_md_action = QAction(tr(lang, "action_paste_md"), self)
        paste_md_action.setShortcut(QKeySequence("Ctrl+Shift+V"))
        paste_md_action.triggered.connect(self._paste_as_markdown)
        edit_menu.addAction(paste_md_action)

        edit_menu.addSeparator()

        next_tab_action = QAction(tr(lang, "action_next_tab"), self)
        next_tab_action.setShortcut(QKeySequence("Ctrl+Tab"))
        next_tab_action.triggered.connect(lambda: self._next_tab(+1))
        edit_menu.addAction(next_tab_action)

        prev_tab_action = QAction(tr(lang, "action_prev_tab"), self)
        prev_tab_action.setShortcut(QKeySequence("Ctrl+Shift+Tab"))
        prev_tab_action.triggered.connect(lambda: self._next_tab(-1))
        edit_menu.addAction(prev_tab_action)

        settings_menu = menubar.addMenu(tr(lang, "menu_settings"))

        config_action = QAction(tr(lang, "action_text_settings"), self)
        config_action.triggered.connect(self._open_settings)
        settings_menu.addAction(config_action)

        pdf_config_action = QAction(tr(lang, "action_pdf_settings"), self)
        pdf_config_action.triggered.connect(self._open_pdf_settings)
        settings_menu.addAction(pdf_config_action)

        # Language submenu under Settings menu
        lang_menu = settings_menu.addMenu(tr(lang, "menu_language"))
        lang_group = []
        for code, name in LANGUAGES:
            action = QAction(name, self)
            action.setCheckable(True)
            action.setChecked(code == lang)
            action.triggered.connect(lambda checked, c=code: self._change_language(c))
            lang_menu.addAction(action)
            lang_group.append(action)
        self._lang_actions = lang_group

        help_menu = menubar.addMenu(tr(lang, "menu_help"))
        about_action = QAction(tr(lang, "action_about"), self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _change_language(self, code: str):
        if code == self.lang:
            return
        self.lang = code
        self.settings["language"] = code
        save_settings(self.settings, self.pdf_settings)
        # Update UI texts that depend on language
        self._init_menu()
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            if tab:
                tab.editor.setPlaceholderText(tr(code, "placeholder"))
                tab.update_preview()
                self.refresh_tab_title(tab)
        self.update_title_and_status()

    # ------------------------------------------------------------------
    # Tab handling
    # ------------------------------------------------------------------
    def current_tab(self) -> DocumentTab | None:
        return self.tabs.currentWidget()

    def _add_new_tab(self, text: str = "", path: str | None = None) -> DocumentTab:
        tab = DocumentTab(self, text, path)
        idx = self.tabs.addTab(tab, tab.tab_title())
        self.tabs.setTabToolTip(idx, path or tr(self.lang, "not_saved"))
        self.tabs.setCurrentIndex(idx)
        return tab

    def _is_pristine_tab(self, tab: DocumentTab | None) -> bool:
        return (
            tab is not None
            and tab.current_file is None
            and not tab.is_modified()
            and not tab.editor.toPlainText().strip()
        )

    def refresh_tab_title(self, tab: DocumentTab):
        idx = self.tabs.indexOf(tab)
        if idx != -1:
            self.tabs.setTabText(idx, tab.tab_title())
            self.tabs.setTabToolTip(idx, tab.current_file or tr(self.lang, "not_saved"))

    def _on_tab_changed(self, _idx):
        self.update_title_and_status()

    def _next_tab(self, step: int = 1):
        n = self.tabs.count()
        if n <= 1:
            return
        self.tabs.setCurrentIndex((self.tabs.currentIndex() + step) % n)

    def _close_tab_at(self, index: int):
        tab = self.tabs.widget(index)
        if tab is None:
            return
        if not self._maybe_save_changes(tab):
            return
        self.tabs.removeTab(index)
        tab.deleteLater()
        if self.tabs.count() == 0:
            self.close()
        else:
            self.update_title_and_status()

    def _close_current_tab(self):
        self._close_tab_at(self.tabs.currentIndex())

    def _undo(self):
        tab = self.current_tab()
        if tab:
            tab.editor.undo()

    def _redo(self):
        tab = self.current_tab()
        if tab:
            tab.editor.redo()

    # ------------------------------------------------------------------
    # Window title and status bar
    # ------------------------------------------------------------------
    def update_title_and_status(self):
        tab = self.current_tab()
        lang = self.lang
        if tab is None:
            self.file_label.setText("")
            self.setWindowTitle(
                tr(lang, "window_title", name=APP_NAME, version=APP_VERSION)
            )
            return
        name = tab.display_name()
        state = tr(lang, "state_modified") if tab.is_modified() else tr(lang, "state_saved")
        if tab.current_file:
            self.file_label.setText(f"  {name}  ({state})  ")
            self.setWindowTitle(
                tr(lang, "window_title_doc",
                   star="*" if tab.is_modified() else "",
                   name=name, app=APP_NAME)
            )
        else:
            has_text = bool(tab.editor.toPlainText().strip())
            self.file_label.setText(
                f"  {tr(lang, 'new_doc')}  ({tr(lang, 'not_saved')})  "
                if has_text else f"  {tr(lang, 'new_doc')}  "
            )
            self.setWindowTitle(
                tr(lang, "window_title_doc",
                   star="*" if has_text else "",
                   name=tr(lang, "new_doc"), app=APP_NAME)
                if has_text
                else tr(lang, "window_title", name=APP_NAME, version=APP_VERSION)
            )

    # ------------------------------------------------------------------
    # Saving / opening
    # ------------------------------------------------------------------
    def _maybe_save_changes(self, tab: DocumentTab | None = None) -> bool:
        tab = tab or self.current_tab()
        if tab is None or not tab.is_modified():
            return True
        self.tabs.setCurrentWidget(tab)
        reply = QMessageBox.question(
            tab, tr(self.lang, "unsaved_title"),
            tr(self.lang, "unsaved_text", name=tab.display_name()),
            QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel,
        )
        if reply == QMessageBox.StandardButton.Save:
            self._save_file(tab)
            return not tab.is_modified()
        if reply == QMessageBox.StandardButton.Discard:
            return True
        return False

    def _new_file(self):
        self._add_new_tab()
        self.status_bar.showMessage(tr(self.lang, "status_new_memory"), 3000)

    def _open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, tr(self.lang, "action_open"), "",
            "Markdown (*.md *.markdown);;All files (*)"
        )
        if not path:
            return
        for i in range(self.tabs.count()):
            t = self.tabs.widget(i)
            if t.current_file and os.path.normcase(t.current_file) == os.path.normcase(path):
                self.tabs.setCurrentIndex(i)
                return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            QMessageBox.critical(self, tr(self.lang, "error"),
                                 tr(self.lang, "error_open_file", e=e))
            return

        current = self.current_tab()
        if (
            not self._startup_tab_consumed
            and self.tabs.count() == 1
            and self._is_pristine_tab(current)
        ):
            self._startup_tab_consumed = True
            current.current_file = path
            current.set_text(content)
            self.refresh_tab_title(current)
            self.status_bar.showMessage(
                tr(self.lang, "status_opened", path=path), 3000
            )
        else:
            tab = self._add_new_tab(content, path)
            self.refresh_tab_title(tab)
            self.status_bar.showMessage(
                tr(self.lang, "status_opened", path=path), 3000
            )
        self.update_title_and_status()

    def _save_file(self, tab: DocumentTab | None = None):
        tab = tab or self.current_tab()
        if tab is None:
            return
        if tab.current_file:
            self._write_file(tab, tab.current_file)
        else:
            self._save_file_as(tab)

    def _save_file_as(self, tab: DocumentTab | None = None):
        tab = tab or self.current_tab()
        if tab is None:
            return
        start_path = tab.current_file or ""
        path, _ = QFileDialog.getSaveFileName(
            self, tr(self.lang, "action_save_as"), start_path,
            "Markdown (*.md);;All files (*)"
        )
        if path:
            self._write_file(tab, path)

    def _write_file(self, tab: DocumentTab, path: str):
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(tab.editor.toPlainText())
        except Exception as e:
            QMessageBox.critical(self, tr(self.lang, "error"),
                                 tr(self.lang, "error_save_file", e=e))
            return
        tab.mark_saved(path)
        self.status_bar.showMessage(
            tr(self.lang, "status_saved", path=path), 3000
        )

    def _paste_as_markdown(self):
        tab = self.current_tab()
        if tab is None:
            return
        cb = QApplication.clipboard()
        mime = cb.mimeData()
        if mime and mime.hasHtml():
            try:
                md_text = html_to_markdown(mime.html())
                if md_text.strip():
                    tab.editor.textCursor().insertText(md_text)
                    self.status_bar.showMessage(
                        tr(self.lang, "status_pasted_md"), 2000
                    )
                    return
            except Exception as e:
                self.status_bar.showMessage(
                    tr(self.lang, "status_error", e=e), 3000
                )
        if mime and mime.hasText():
            tab.editor.textCursor().insertText(mime.text())

    # ------------------------------------------------------------------
    # Window closing
    # ------------------------------------------------------------------
    def closeEvent(self, event: QCloseEvent):
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            if not self._maybe_save_changes(tab):
                event.ignore()
                return
        event.accept()

    # ------------------------------------------------------------------
    # Hotkeys (more reliable than QAction for Ctrl+Tab)
    # ------------------------------------------------------------------
    def keyPressEvent(self, event):
        mods = event.modifiers()
        key = event.key()
        if mods == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_Tab:
            self._next_tab(+1)
            return
        if (mods == (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier)
                and key == Qt.Key.Key_Tab):
            self._next_tab(-1)
            return
        super().keyPressEvent(event)

    # ------------------------------------------------------------------
    # Settings
    # ------------------------------------------------------------------
    def _open_settings(self):
        dialog = SettingsDialog(self, self.settings)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.settings.update(dialog.get_settings())
            self.settings["language"] = self.lang
            save_settings(self.settings, self.pdf_settings)
            for i in range(self.tabs.count()):
                self.tabs.widget(i).update_preview()

    def _open_pdf_settings(self):
        dialog = PdfExportDialog(self, self.pdf_settings, self.lang)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.pdf_settings = dialog.get_settings()
            save_settings(self.settings, self.pdf_settings)

    # ------------------------------------------------------------------
    # Markdown -> HTML conversion
    # ------------------------------------------------------------------
    def _convert_markdown_to_html(self, text: str) -> str:
        parts = re.split(r'(```.*?```)', text, flags=re.DOTALL)
        processed_parts = []
        for part in parts:
            if part.startswith("```"):
                processed_parts.append(part)
            else:
                part = re.sub(r'(?<!_)_(?!_)', r'\_', part)
                part = part.replace(r"\[", "\n$$").replace(r"\]", "$$\n")
                part = re.sub(r'(?m)^\s*\\\((.*?)\\\)\s*$', r'$$ \1 $$', part)
                part = part.replace(r"\(", "$").replace(r"\)", "$")
                processed_parts.append(part)
        text = "".join(processed_parts)

        md = markdown.Markdown(
            extensions=['pymdownx.arithmatex', 'fenced_code', 'codehilite', 'tables', 'toc'],
            extension_configs={
                'pymdownx.arithmatex': {'generic': True},
                'codehilite': {'guess_lang': False, 'css_class': 'highlight', 'noclasses': False, 'linenums': False}
            }
        )
        html = md.convert(text)
        html = re.sub(
            r'<p>\s*(<span class="arithmatex">.*?</span>)\s*</p>',
            r'<p style="text-align: center;">\1</p>',
            html, flags=re.DOTALL
        )
        return html

    def _wrap_html(self, body_html: str, for_print: bool = False) -> str:
        katex_css = _read_local_file("katex.min.css")
        katex_js = _read_local_file("katex.min.js")
        auto_render_js = _read_local_file(os.path.join("contrib", "auto-render.min.js"))
        pygments_css = HtmlFormatter(style="friendly").get_style_defs(".highlight")

        font_family = self.settings["font_family"]
        font_css = "'Segoe UI', Arial, sans-serif" if font_family == "system" else f"'{font_family}', serif"
        text_align = self.settings["text_align"]
        font_size = self.settings["font_size"]

        max_width_css = "100%" if for_print else f"{self.settings['max_width']}px"
        padding_css = "0" if for_print else "20px"
        margin_css = "0" if for_print else "0 auto"

        page_css = ""
        if for_print:
            ps = self.pdf_settings
            page_css = f"""
@page {{
    size: {ps['page_size']} {ps['orientation']};
    margin: {ps['margin_top']}mm {ps['margin_right']}mm {ps['margin_bottom']}mm {ps['margin_left']}mm;
"""
            if ps.get("page_numbers", True):
                page_css += """
    @bottom-center { content: counter(page); font-family: Arial, sans-serif; font-size: 10pt; color: #666; }
"""
            page_css += "}\n"

        return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{katex_css}
{pygments_css}
{page_css}

body {{
    font-family: {font_css};
    font-size: {font_size}px;
    line-height: 1.6;
    padding: {padding_css};
    max-width: {max_width_css};
    margin: {margin_css};
    color: #333;
    text-align: {text_align};
}}
pre {{
    background: #f6f8fa;
    padding: 12px;
    border-radius: 6px;
    overflow-x: auto;
    text-align: left;
}}
code {{
    background: #f0f0f0;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Consolas', 'Monaco', monospace;
}}
pre code {{
    background: none;
    padding: 0;
}}
blockquote {{ border-left: 4px solid #ccc; margin: 0; padding-left: 16px; color: #666; }}
table {{ border-collapse: collapse; width: 100%; margin: 16px 0; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background: #f5f5f5; }}
img {{ max-width: 100%; height: auto; }}
.katex-display {{ display: block; text-align: center; margin: 1em 0; }}
.arithmatex {{ display: inline; }}
.arithmatex > .katex-display {{ display: block; text-align: center; margin: 1em 0; }}
</style>
<script>{katex_js}</script>
<script>{auto_render_js}</script>
</head>
<body>
{body_html}
<script>
  document.addEventListener("DOMContentLoaded", function() {{
    renderMathInElement(document.body, {{
      delimiters: [
        {{left: "$$", right: "$$", display: true}},
        {{left: "$", right: "$", display: false}},
        {{left: "\\\\(", right: "\\\\)", display: false}},
        {{left: "\\\\[", right: "\\\\]", display: true}}
      ],
      throwOnError: false
    }});
  }});
</script>
</body>
</html>
"""

    # ------------------------------------------------------------------
    # PDF
    # ------------------------------------------------------------------
    def _page_layout_from_settings(self) -> QPageLayout:
        ps = self.pdf_settings
        size_map = {
            "A4": QPageSize.PageSizeId.A4, "Letter": QPageSize.PageSizeId.Letter,
            "Legal": QPageSize.PageSizeId.Legal, "A3": QPageSize.PageSizeId.A3,
            "A5": QPageSize.PageSizeId.A5,
        }
        page_size = QPageSize(size_map.get(ps["page_size"], QPageSize.PageSizeId.A4))
        orientation = (
            QPageLayout.Orientation.Landscape
            if ps["orientation"] == "landscape"
            else QPageLayout.Orientation.Portrait
        )
        margins = QMarginsF(ps["margin_left"], ps["margin_top"], ps["margin_right"], ps["margin_bottom"])
        return QPageLayout(page_size, orientation, margins, QPageLayout.Unit.Millimeter)

    def _export_pdf(self):
        tab = self.current_tab()
        if tab is None or not tab.editor.toPlainText().strip():
            QMessageBox.warning(
                self, tr(self.lang, "export_empty_title"),
                tr(self.lang, "export_empty_text")
            )
            return
        dlg = PdfExportDialog(self, self.pdf_settings, self.lang)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        self.pdf_settings = dlg.get_settings()
        save_settings(self.settings, self.pdf_settings)

        body = self._convert_markdown_to_html(tab.editor.toPlainText())
        html = self._wrap_html(body, for_print=True)
        base_url = QUrl.fromLocalFile(KATEX_DIR + os.sep)

        self._printer_page = QWebEnginePage(tab.preview.page().profile(), self)
        self._printer_page.setHtml(html, base_url)

        def on_load_finished(ok):
            if not ok:
                QMessageBox.critical(
                    self, tr(self.lang, "error"),
                    tr(self.lang, "error_load_export")
                )
                self._printer_page.deleteLater()
                return
            QTimer.singleShot(500, lambda: self._render_pdf_preview(self._printer_page))

        self._printer_page.loadFinished.connect(on_load_finished)

    def _render_pdf_preview(self, page: QWebEnginePage):
        def on_pdf_ready(pdf_data: bytes):
            page.deleteLater()
            if not pdf_data:
                QMessageBox.critical(
                    self, tr(self.lang, "error"),
                    tr(self.lang, "error_generate_pdf")
                )
                return
            tab = self.current_tab()
            if tab and tab.current_file:
                suggested = os.path.splitext(os.path.basename(tab.current_file))[0] + ".pdf"
            else:
                suggested = "document.pdf"
            dlg = PdfPreviewDialog(pdf_data, self, suggested, self.lang)
            if dlg.exec() == QDialog.DialogCode.Accepted and dlg.saved_path:
                self.status_bar.showMessage(
                    tr(self.lang, "status_pdf_exported", path=dlg.saved_path), 4000
                )
                self._show_pdf_saved_dialog(dlg.saved_path)

        page_layout = self._page_layout_from_settings()
        page.printToPdf(on_pdf_ready, page_layout)

    def _show_pdf_saved_dialog(self, path: str):
        msg = QMessageBox(self)
        msg.setWindowTitle(tr(self.lang, "done_title"))
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(tr(self.lang, "pdf_saved_text", path=path))
        show_btn = msg.addButton(
            tr(self.lang, "btn_show_in_folder"), QMessageBox.ButtonRole.ActionRole
        )
        ok_btn = msg.addButton(QMessageBox.StandardButton.Ok)
        msg.setDefaultButton(ok_btn)
        msg.exec()
        if msg.clickedButton() is show_btn:
            self._reveal_in_explorer(path)

    @staticmethod
    def _reveal_in_explorer(path: str):
        try:
            if sys.platform.startswith("win"):
                import subprocess
                subprocess.Popen(["explorer", "/select,", os.path.normpath(path)])
            elif sys.platform == "darwin":
                import subprocess
                subprocess.Popen(["open", "-R", path])
            else:
                import subprocess
                try:
                    subprocess.Popen([
                        "dbus-send", "--session", "--dest=org.freedesktop.FileManager1",
                        "--type=method_call", "/org/freedesktop/FileManager1",
                        "org.freedesktop.FileManager1.ShowItems",
                        f"array:string:file://{os.path.abspath(path)}", "string:"
                    ])
                except Exception:
                    subprocess.Popen(["xdg-open", os.path.dirname(path)])
        except Exception as e:
            QMessageBox.warning(
                None, "Error", f"Failed to open folder:\n{e}"
            )

    def _show_about(self):
        QMessageBox.about(
            self, tr(self.lang, "about_title"),
            tr(self.lang, "about_text", version=APP_VERSION)
        )


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    editor = MarkdownEditor()
    editor.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()