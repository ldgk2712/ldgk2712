import requests
import os

# Cấu hình
USERNAME = "ldgk2712"
# API lấy danh sách public repo, sắp xếp theo thời gian tạo mới nhất
URL = f"https://api.github.com/users/{USERNAME}/repos?sort=created&direction=desc"

def fetch_repos():
    response = requests.get(URL)
    if response.status_code == 200:
        repos = response.json()
        # Chỉ lấy 5 dự án mới nhất và không phải là repo profile này
        return [r for r in repos if r['name'] != USERNAME][:5]
    return []

def update_readme():
    repos = fetch_repos()
    project_html = ""
    
    # Tạo mã HTML theo phong cách "cute hồng" đã thống nhất
    for repo in repos:
        name = repo['name']
        desc = repo['description'] or "No description provided ✨"
        url = repo['html_url']
        project_html += f"""
<p align="center">
  <a href="{url}">
    <img src="https://github-readme-stats.vercel.app/api/pin/?username={USERNAME}&repo={name}&bg_color=ffe4e1&title_color=ff1493&text_color=c71585&icon_color=ff69b4&border_color=ffb6c1" />
  </a>
</p>
"""

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # Thay thế nội dung giữa 2 thẻ anchor
    start_tag = ""
    end_tag = ""
    
    start_idx = content.find(start_tag) + len(start_tag)
    end_idx = content.find(end_tag)
    
    new_content = content[:start_idx] + "\n" + project_html + "\n" + content[end_idx:]

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    update_readme()