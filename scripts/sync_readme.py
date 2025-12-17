import os
import re
import urllib.parse

# Configuration
LAB_ROOT_DIR = 'Hành trình lên mây'
README_FILENAME = 'README.md'
TABLE_START_MARKER = '<!-- TABLE_START -->'
TABLE_END_MARKER = '<!-- TABLE_END -->'

def get_session_overview(readme_path):
    """Extracts the content between '## 📌 Overview' and the next header."""
    if not os.path.exists(readme_path):
        return None
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    match = re.search(r'## 📌 Overview\s*\n(.*?)\n\s*###', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def format_as_html_list(markdown_text):
    """Converts markdown bullet points to HTML list."""
    if not markdown_text:
        return "<ul><li><em>Updating...</em></li></ul>"
        
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

        for folder_name in dirs:
            # Skip hidden folders
            if folder_name.startswith('.'): continue
            
            lab_readme_path = os.path.join(lab_root_full_path, folder_name, 'README.md')
            
            # Prepare Columns
            
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
    table_header = "| Bài Lab (Lab) | Chủ đề (Topics) | Trạng thái (Status) | Tài liệu (Resources) |\n| :--- | :--- | :--- | :--- |"
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
