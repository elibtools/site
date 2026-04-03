import os
import subprocess

# Paths
BASE_PATH = "/home/thurapsha/apk_build"
SITE_PATH = os.path.join(BASE_PATH, "site")
ASSETS_PATH = os.path.join(BASE_PATH, "assets")

TEMPLATE_FILE = os.path.join(SITE_PATH, "temp_site.html")

# Files to process: (Source Text, Target HTML, Page Title)
TASKS = [
    ("policy.txt", "privacy.html", "Privacy Policy"),
    ("terms.txt", "terms.html", "Terms of Use")
]

def format_text_to_html(text):
    """Converts raw text lines into HTML elements."""
    lines = text.split('\n')
    html_output = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith("---"):
            html_output.append("<hr>")
        elif line[0].isdigit() and "." in line[:3]: # Detects "1. Section"
            html_output.append(f"<h2>{line}</h2>")
        elif "Effective Date:" in line:
            html_output.append(f'<p class="effective-date">{line}</p>')
        elif "Email:" in line or "@" in line:
            # Basic link conversion for emails
            html_output.append(f'<p>{line.replace("elibtools@gmail.com", "<a class=\'link\' href=\'mailto:elibtools@gmail.com\'>elibtools@gmail.com</a>")}</p>')
        else:
            html_output.append(f"<p>{line}</p>")
            
    return "\n".join(html_output)

def run():
    # Load Template
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template = f.read()

    for txt_name, html_name, title in TASKS:
        txt_path = os.path.join(ASSETS_PATH, txt_name)
        html_output_path = os.path.join(SITE_PATH, html_name)

        if os.path.exists(txt_path):
            with open(txt_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Format and Inject
            html_content = format_text_to_html(content)
            final_html = template.replace("{{PAGE_TITLE}}", title)
            final_html = final_html.replace("{{MAIN_CONTENT}}", html_content)

            with open(html_output_path, 'w', encoding='utf-8') as f:
                f.write(final_html)
            print(f"Generated: {html_name}")

    # Git Operations
    try:
        os.chdir(SITE_PATH)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Automated update of privacy and terms html"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("Git Push Successful")
    except Exception as e:
        print(f"Git Error: {e}")

if __name__ == "__main__":
    run()