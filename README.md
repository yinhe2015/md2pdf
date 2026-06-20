# Markdown to PDF Converter (md2pdf)

这是一个简单而强大的 Python 工具，用于将 Markdown 文件转换为 PDF 文件。它支持中文字体，并带有美观的默认样式。

## 功能特点

- ✨ 支持标准的 Markdown 语法
- 🎨 内置美观的 CSS 样式，优化阅读体验
- 🔤 **完美支持中文**（自动使用系统字体：Heiti SC, STHeiti, PingFang SC 等）
- 🚀 支持单个文件或批量转换
- 🛠 支持自定义 CSS 样式
- 📑 支持代码高亮、表格、目录等扩展

## 安装

需要安装 python3 以及以下依赖：

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

转换单个文件：

```bash
python md2pdf.py document.md
```

这将生成 `document.pdf`。

### 指定输出文件名

```bash
python md2pdf.py document.md -o output.pdf
```

### 批量转换

支持通配符批量转换：

```bash
python md2pdf.py *.md
```

### 使用自定义样式

如果你想使用自己的 CSS 样式：

```bash
python md2pdf.py document.md --css custom_style.css
```

### 其它选项

查看所有可用选项：

```bash
python md2pdf.py --help
```

## 依赖说明

- `markdown`: 用于解析 Markdown 文本
- `weasyprint`: 用于将 HTML 渲染为 PDF

## 注意事项

- 请确保你的系统已正确安装 Python 3 环境。
- 工具默认会尝试使用 macOS 系统自带的中文字体。

---

License: MIT
