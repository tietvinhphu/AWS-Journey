import os
import re

# Cấu hình
README_FILE = "README.md"
FOLDER_PATTERN = r"^Session-(\d+)-(.*)$"  # Định dạng folder: Session-01-TenBai
TABLE_HEADER = "| Buổi học (Session) | Chủ đề (Topics) | Trạng thái (Status) | Tài liệu (Resources) |\n| :--- | :--- | :--- | :--- |"
START_MARKER = "<!-- TABLE_START -->"
END_MARKER = "<!-- TABLE_END -->"

def generate_topic_badge(topic_slug):
    """Tạo badge cho topic dựa trên tên bài"""
    topic_name = topic_slug.replace('-', '_')
    return f"![{topic_slug}](https://img.shields.io/badge/AWS-{topic_name}-FF9900?style=flat-square&logo=amazon-aws&logoColor=white)"

def update_readme():
    if not os.path.exists(README_FILE):
        print(f"Không tìm thấy file {README_FILE}")
        return

    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Tìm vị trí bảng cũ
    pattern = f"{re.escape(START_MARKER)}(.*?){re.escape(END_MARKER)}"
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print("Không tìm thấy marker bảng trong README.")
        print(f"Hãy thêm {START_MARKER} và {END_MARKER} vào README.md")
        return

    old_table_content = match.group(1).strip()
    
    # 2. Lưu lại dữ liệu cũ (để giữ lại Link Youtube/Notion bạn đã điền)
    existing_data = {}
    for line in old_table_content.split("\n"):
        if "|" in line and "Session" not in line and "---" not in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                # Key là tên Session (VD: Session 01)
                session_match = re.search(r"\[(Session \d+:.*?)\]", parts[1]) 
                if session_match:
                    existing_data[session_match.group(1)] = line
    
    # 3. Quét thư mục để tìm bài học mới
    new_rows = []
    folders = [f for f in os.listdir(".") if os.path.isdir(f) and f.startswith("Session-")]
    folders.sort()  # Sắp xếp theo tên

    for folder in folders:
        folder_match = re.match(FOLDER_PATTERN, folder)
        if folder_match:
            session_num = folder_match.group(1)
            topic_slug = folder_match.group(2)
            display_name = f"Session {session_num}: {topic_slug.replace('-', ' ')}"
            
            # Nếu bài này đã có trong bảng cũ -> Dùng lại dòng cũ (giữ link)
            if display_name in existing_data:
                new_rows.append(existing_data[display_name])
            else:
                # Nếu là bài mới -> Tạo dòng mới với trạng thái mặc định
                topic_badge = generate_topic_badge(topic_slug)
                status_badge = "![Doing](https://img.shields.io/badge/Status-Learning...-yellow?style=flat-square)"
                link_cell = "_Updating..._"
                
                row = f"| **[{display_name}](./{folder})** | {topic_badge} | {status_badge} | {link_cell} |"
                new_rows.append(row)

    # 4. Ghép bảng mới
    if new_rows:
        new_table = f"{START_MARKER}\n{TABLE_HEADER}\n" + "\n".join(new_rows) + f"\n{END_MARKER}"
    else:
        new_table = f"{START_MARKER}\n{TABLE_HEADER}\n| _Chưa có bài học nào_ | - | - | - |\n{END_MARKER}"
    
    # 5. Ghi đè vào file
    new_content = content.replace(match.group(0), new_table)
    
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print("✅ Đã cập nhật README.md thành công!")
    print(f"📚 Tổng số bài học: {len(new_rows)}")

if __name__ == "__main__":
    update_readme()
