import os
import re
import urllib.parse

def get_session_overview(readme_path):
    """Extracts the content between '## 📌 Overview' and the next header."""
    if not os.path.exists(readme_path):
        return None
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Regex to find the Overview section
    # Matches ## 📌 Overview, then captures everything until the next header (## or ###)
    match = re.search(r'## 📌 Overview\s*\n(.*?)\n\s*###', content, re.DOTALL)
    if match:
        overview_text = match.group(1).strip()
        return overview_text
    return None

def format_as_html_list(markdown_text):
    """Converts markdown bullet points to HTML list."""
    lines = markdown_text.split('\n')
    html_items = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('- '):
            item_content = line[2:].strip()
            # Basic bold formatting conversion **text** -> <strong>text</strong>
            item_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', item_content)
            html_items.append(f'<li>{item_content}</li>')
            
    if html_items:
        return '<ul>' + ''.join(html_items) + '</ul>'
    return markdown_text

def update_main_readme():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main_readme_path = os.path.join(root_dir, 'README.md')
    
    with open(main_readme_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    for line in lines:
        # Check if line contains a Session or Lab link in the first column
        # Format: | **[Name ...](path)** | ...
        match = re.search(r'\|\s*\*\*\[(.*?)\]\((.*?)\)\*\*\s*\|', line)
        if match:
            session_name = match.group(1)
            relative_path = match.group(2)
            
            # Decode URL path (handling %20, etc.)
            decoded_path = urllib.parse.unquote(relative_path)
            
            # Construct full path to the session README
            session_readme_path = os.path.join(root_dir, decoded_path, 'README.md')
            
            # Extract overview
            overview_md = get_session_overview(session_readme_path)
            
            if overview_md:
                html_list = format_as_html_list(overview_md)
                
                # Replace the second column content
                # Split by |
                parts = line.split('|')
                if len(parts) >= 3:
                    parts[2] = ' ' + html_list + ' '
                    new_line = '|'.join(parts)
                    new_lines.append(new_line)
                    print(f"Updated {session_name}")
                    continue
        
        new_lines.append(line)
        
    with open(main_readme_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    update_main_readme()
