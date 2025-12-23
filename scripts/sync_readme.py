import os
import re
import urllib.parse

# Configuration
LAB_ROOT_DIR = 'The First Cloud Journey'
README_FILENAME = 'README.md'
TABLE_START_MARKER = '<!-- TABLE_START -->'
TABLE_END_MARKER = '<!-- TABLE_END -->'


FOOTER_START_MARKER = '<!-- FOOTER_START -->'
FOOTER_END_MARKER = '<!-- FOOTER_END -->'

FOOTER_TEMPLATE = f"""
{FOOTER_START_MARKER}
<br>
<div align="center">
  <b>AWS Cloud Journey</b>
  <br>
  <i>"Hành trình từ Zero đến Hero với AWS Cloud & DevOps"</i>
  <br><br>
  <a href="https://www.facebook.com/XueYongFu"><img src="https://img.shields.io/badge/Facebook-%231877F2.svg?style=for-the-badge&logo=Facebook&logoColor=white" alt="Facebook"></a>
  <a href="https://www.linkedin.com/in/tiet-vinh-phu-609173155/"><img src="https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="https://github.com/tietvinhphu/AWS-Journey"><img src="https://img.shields.io/badge/Github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
</div>
{FOOTER_END_MARKER}
"""

def update_lab_footer(readme_path, next_folder_name=None):
    """Updates the README footer with Next Lesson link, Global Footer, and Back to Top."""
    if not os.path.exists(readme_path):
        return

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False
    
    # 1. Ensure Top Anchor
    if TOP_ANCHOR not in content:
        content = TOP_ANCHOR + "\n\n" + content
        modified = True
        
    # 2. Logic to construct the new Footer
    # Order: [Content] -> [Next Lesson] -> [Global Footer] -> [Back to Top]
    
    # 2a. Strip OLD auto-generated content
    # Remove old Next Lesson lines
    content = re.sub(r'> ⏩ \*\*Next Lesson:\*\* .*', '', content)
    
    # Remove old Global Footer (if exists between markers)
    pattern_footer = re.compile(f"{re.escape(FOOTER_START_MARKER)}.*?{re.escape(FOOTER_END_MARKER)}", re.DOTALL)
    content = pattern_footer.sub('', content)
    
    # Remove existing Back to Top link
    content = content.replace(BACK_TO_TOP_LINK, '').strip()
    
    # Also remove trailing newlines to ensure clean append
    content = content.strip()
    
    # 3. Append New Content
    
    # Append Next Lesson Link if exists
    if next_folder_name:
        encoded_next_folder = urllib.parse.quote(next_folder_name)
        # Relative link: ../Next%20Folder
        next_link = f"../{encoded_next_folder}"
        next_nav_line = f"\n\n> ⏩ **Next Lesson:** [{next_folder_name}]({next_link})"
        content += next_nav_line
        
    # Append Global Footer
    content += "\n" + FOOTER_TEMPLATE
        
    # Append Back to Top Link
    content += f"\n{BACK_TO_TOP_LINK}\n"
    modified = True 

    if modified:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)

def get_session_overview(readme_path):
    """Extracts the content between '## 📌 Overview' and the next header."""
    if not os.path.exists(readme_path):
        return None
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Improved regex: Stops at the next line starting with # (any level header)
    match = re.search(r'### 📌 Overview\s*\n(.*?)\n\s*#', content, re.DOTALL)
    # Fallback for H2 if H3 not found (legacy support)
    if not match:
        match = re.search(r'## 📌 Overview\s*\n(.*?)\n\s*#', content, re.DOTALL)
        
    if match:
        return match.group(1).strip()
    return None

def format_as_html_list(markdown_text):
    """Converts markdown content to HTML list, handling both bullet points and plain lines."""
    if not markdown_text:
        return "<ul><li><em>Updating...</em></li></ul>"
        
    lines = markdown_text.split('\n')
    html_items = []
    
    for line in lines:
        line = line.strip()
        if not line: continue 
        
        # Remove bullet point if exists
        if line.startswith('- ') or line.startswith('* '):
            item_content = line[2:].strip()
        else:
            item_content = line
            
        # Basic bold formatting conversion **text** -> <strong>text</strong>
        item_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', item_content)
        html_items.append(f'<li>{item_content}</li>')
            
    if html_items:
        return '<ul>' + ''.join(html_items) + '</ul>'
    return markdown_text

def get_existing_table_data(readme_content):
    """Parses existing table to preserve manual Status and Resources columns."""
    data = {} # Key: Lab Folder Name, Value: (Status Col, Resources Col)
    
    # Regex to capture: | **[Lab Name](path)** | Topics | Status | Resources |
    # We strictly look for the Link structure in the first column
    pattern = r'\|\s*\*\*\[(.*?)\]\((.*?)\)\*\*\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|'
    
    for line in readme_content.split('\n'):
        match = re.search(pattern, line)
        if match:
            # We derive the folder name from the decoded path to be the unique key
            # path is usually: ./Hành%20trình%20lên%20mây/Lab-01...
            rel_path = match.group(2)
            decoded_path = urllib.parse.unquote(rel_path)
            # Assuming path is ./Hành trình lên mây/Folder Name
            # We want "Folder Name"
            parts = decoded_path.split('/')
            if len(parts) >= 3:
                folder_name = parts[-1] 
            else:
                folder_name = parts[-1] # Fallback
            
            status_col = match.group(4).strip()
            resources_col = match.group(5).strip()
            
            data[folder_name] = {
                'status': status_col,
                'resources': resources_col
            }
    return data

def update_readme():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main_readme_path = os.path.join(root_dir, README_FILENAME)
    lab_root_full_path = os.path.join(root_dir, LAB_ROOT_DIR)

    if not os.path.exists(main_readme_path):
        print(f"Error: {README_FILENAME} not found.")
        return

    # 1. Read Main README
    with open(main_readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 2. Extract existing data (to preserve Status/Resources)
    existing_data = get_existing_table_data(content)
    
    # 3. Scan for Labs
    lab_rows = []
    if os.path.exists(lab_root_full_path):
        # List directories only
        dirs = [d for d in os.listdir(lab_root_full_path) if os.path.isdir(os.path.join(lab_root_full_path, d))]
        # Sort by name (Lab-01, Lab-02...)
        dirs.sort()
        
        # Filter valid folders first (starts with number)
        valid_dirs = [d for d in dirs if not d.startswith('.') and re.match(r'^\d+\.', d)]

        for i, folder_name in enumerate(valid_dirs):
             lab_readme_path = os.path.join(lab_root_full_path, folder_name, 'README.md')
             
             # --- Determine Next Lab Folder ---
             next_folder = None
             if i + 1 < len(valid_dirs):
                 next_folder = valid_dirs[i + 1]

             # --- Update Footer (Next Link + Back to Top) ---
             update_lab_footer(lab_readme_path, next_folder)
             
             # --- Prepare Table Columns ---
             
             # Col 1: Link
             encoded_folder = urllib.parse.quote(folder_name)
             encoded_root = urllib.parse.quote(LAB_ROOT_DIR)
             link_path = f"./{encoded_root}/{encoded_folder}"
             
             col1 = f"**[{folder_name}]({link_path})**"
             
             # Col 2: Topics (Overview)
             overview_text = get_session_overview(lab_readme_path)
             col2 = format_as_html_list(overview_text)
             
             # Col 3 & 4: Status & Resources
             # Default values
             col3 = "![In Progress](https://img.shields.io/badge/Status-In_Progress-yellow?style=flat-square)"
             col4 = "_Updating..._"
             
             # If exists in old data, use that
             if folder_name in existing_data:
                 col3 = existing_data[folder_name]['status']
                 col4 = existing_data[folder_name]['resources']
             
             # Construct Row
             row = f"| {col1} | {col2} | {col3} | {col4} |"
             lab_rows.append(row)

    # 4. Reconstruct Table
    table_header = "| <div align=\"center\">Bài Lab (Lab)</div> | <div align=\"center\">Chủ đề (Topics)</div> | <div align=\"center\">Trạng thái (Status)</div> | <div align=\"center\">Tài liệu (Resources)</div> |\n| :---: | :--- | :---: | :---: |"
    table_content = "\n".join(lab_rows)
    new_table_section = f"{table_header}\n{table_content}"
    
    # 5. Inject into README
    # Regex to find block between markers
    pattern = re.compile(f"{re.escape(TABLE_START_MARKER)}.*?{re.escape(TABLE_END_MARKER)}", re.DOTALL)
    
    if pattern.search(content):
        new_content = pattern.sub(f"{TABLE_START_MARKER}\n{new_table_section}\n{TABLE_END_MARKER}", content)
        
        with open(main_readme_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("README.md updated successfully with auto-discovery.")
    else:
        print("Error: Table markers not found in README.md")

if __name__ == "__main__":
    update_readme()
