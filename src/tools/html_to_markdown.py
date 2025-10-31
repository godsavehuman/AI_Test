import os
from markdownify import markdownify as md

def convert_html_to_markdown(html_path):
    # Read the HTML file
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Convert to markdown
    markdown_output = md(html_content)
    
    # Create markdown filename (same name, different extension)
    markdown_path = os.path.splitext(html_path)[0] + '.md'
    
    # Write the markdown file
    with open(markdown_path, 'w', encoding='utf-8') as f:
        f.write(markdown_output)
    
    print(f"Converted {os.path.basename(html_path)} to markdown")

def convert_papers_folder():
    # Get the absolute path to the papers folder
    papers_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'papers')
    
    # Find all HTML files in the papers directory
    html_files = [f for f in os.listdir(papers_dir) if f.endswith('.html')]
    
    if not html_files:
        print("No HTML files found in the papers folder")
        return
    
    # Convert each HTML file to markdown
    for html_file in html_files:
        html_path = os.path.join(papers_dir, html_file)
        convert_html_to_markdown(html_path)

if __name__ == '__main__':
    convert_papers_folder()
