#!/usr/bin/env python3
"""
Markdown to PDF Converter
将 Markdown 文件转换为 PDF 文件的工具
"""

import argparse
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    print("错误: 请先安装 markdown 库: pip install markdown")
    sys.exit(1)

try:
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
except ImportError:
    print("错误: 请先安装 weasyprint 库: pip install weasyprint")
    sys.exit(1)


# 默认 CSS 样式 - 使用系统中文字体
DEFAULT_CSS = """
/* 使用系统中文字体 - Heiti SC 在所有 macOS 系统上都有 */
@font-face {
    font-family: "Heiti SC";
    src: local("Heiti SC");
}

@font-face {
    font-family: "STHeiti";
    src: local("STHeiti");
}

@page {
    size: A4;
    margin: 2cm;
}

body {
    font-family: "Heiti SC", "STHeiti", "PingFang SC", "Hiragino Sans GB", sans-serif;
    font-size: 12pt;
    line-height: 1.6;
    color: #333;
    max-width: 100%;
}

h1, h2, h3, h4, h5, h6 {
    color: #2c3e50;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    font-weight: 600;
}

h1 { font-size: 2em; border-bottom: 2px solid #3498db; padding-bottom: 0.3em; }
h2 { font-size: 1.5em; border-bottom: 1px solid #bdc3c7; padding-bottom: 0.2em; }
h3 { font-size: 1.25em; }
h4 { font-size: 1.1em; }

p {
    margin: 1em 0;
    text-align: justify;
}

code {
    font-family: "SF Mono", "Monaco", "Consolas", monospace;
    background-color: #f4f4f4;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-size: 0.9em;
}

pre {
    background-color: #2d2d2d;
    color: #f8f8f2;
    padding: 1em;
    border-radius: 5px;
    overflow-x: auto;
    line-height: 1.4;
}

pre code {
    background-color: transparent;
    padding: 0;
    color: inherit;
}

blockquote {
    border-left: 4px solid #3498db;
    margin: 1em 0;
    padding: 0.5em 1em;
    background-color: #f9f9f9;
    color: #555;
}

ul, ol {
    margin: 1em 0;
    padding-left: 2em;
}

li {
    margin: 0.3em 0;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}

th, td {
    border: 1px solid #ddd;
    padding: 0.5em;
    text-align: left;
}

th {
    background-color: #f5f5f5;
    font-weight: 600;
}

tr:nth-child(even) {
    background-color: #fafafa;
}

a {
    color: #3498db;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

img {
    max-width: 100%;
    height: auto;
}

hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 2em 0;
}
"""


def convert_md_to_pdf(
    input_path: str,
    output_path: str = None,
    css_path: str = None,
    use_default_css: bool = True
):
    """
    将 Markdown 文件转换为 PDF
    
    Args:
        input_path: Markdown 文件路径
        output_path: PDF 输出路径（默认与输入文件同名）
        css_path: 自定义 CSS 文件路径
        use_default_css: 是否使用默认样式
    
    Returns:
        输出文件路径
    """
    input_file = Path(input_path)
    
    if not input_file.exists():
        raise FileNotFoundError(f"找不到文件: {input_path}")
    
    if not input_file.suffix.lower() in ['.md', '.markdown']:
        print(f"警告: 文件 {input_path} 可能不是 Markdown 文件")
    
    # 确定输出路径
    if output_path is None:
        output_path = input_file.with_suffix('.pdf')
    else:
        output_path = Path(output_path)
    
    # 读取 Markdown 内容
    md_content = input_file.read_text(encoding='utf-8')
    
    # 转换为 HTML
    md_extensions = [
        'tables',           # 表格支持
        'fenced_code',      # 围栏代码块
        'codehilite',       # 代码高亮
        'toc',              # 目录
        'nl2br',            # 换行转 <br>
        'sane_lists',       # 更好的列表处理
    ]
    
    html_content = markdown.markdown(
        md_content,
        extensions=md_extensions,
        extension_configs={
            'codehilite': {
                'css_class': 'highlight',
                'guess_lang': True,
            }
        }
    )
    
    # 构建完整 HTML
    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{input_file.stem}</title>
</head>
<body>
{html_content}
</body>
</html>
"""
    
    # 创建字体配置 - 确保字体正确嵌入
    font_config = FontConfiguration()
    
    # 准备 CSS
    stylesheets = []
    
    if use_default_css:
        stylesheets.append(CSS(string=DEFAULT_CSS, font_config=font_config))
    
    if css_path:
        css_file = Path(css_path)
        if css_file.exists():
            stylesheets.append(CSS(filename=str(css_file), font_config=font_config))
        else:
            print(f"警告: 找不到 CSS 文件: {css_path}")
    
    # 生成 PDF（传入 font_config 确保字体嵌入）
    html = HTML(string=full_html, base_url=str(input_file.parent))
    html.write_pdf(str(output_path), stylesheets=stylesheets, font_config=font_config)
    
    return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description='将 Markdown 文件转换为 PDF',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python md2pdf.py document.md                    # 转换为 document.pdf
  python md2pdf.py document.md -o output.pdf     # 指定输出文件名
  python md2pdf.py document.md --css custom.css  # 使用自定义样式
  python md2pdf.py *.md                          # 批量转换
        """
    )
    
    parser.add_argument(
        'input',
        nargs='+',
        help='输入的 Markdown 文件（支持多个文件）'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='输出的 PDF 文件路径（仅在单文件时有效）'
    )
    
    parser.add_argument(
        '--css',
        help='自定义 CSS 样式文件路径'
    )
    
    parser.add_argument(
        '--no-default-css',
        action='store_true',
        help='不使用默认样式'
    )
    
    args = parser.parse_args()
    
    # 如果有多个文件但指定了输出路径，发出警告
    if len(args.input) > 1 and args.output:
        print("警告: 批量转换时忽略 -o 参数")
        args.output = None
    
    success_count = 0
    fail_count = 0
    
    for input_file in args.input:
        try:
            output = None
            if len(args.input) == 1:
                output = args.output
            
            result = convert_md_to_pdf(
                input_file,
                output_path=output,
                css_path=args.css,
                use_default_css=not args.no_default_css
            )
            print(f"✓ 已转换: {input_file} -> {result}")
            success_count += 1
            
        except Exception as e:
            print(f"✗ 转换失败 {input_file}: {e}")
            fail_count += 1
    
    # 打印汇总
    if len(args.input) > 1:
        print(f"\n完成: {success_count} 成功, {fail_count} 失败")
    
    return 0 if fail_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
