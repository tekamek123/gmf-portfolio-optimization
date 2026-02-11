import os
import markdown
import shutil
from datetime import datetime
from xhtml2pdf import pisa

def create_pdf_report():
    """Generate a clean PDF report from the final_project_report.md file"""
    
    print("🚀 Generating Final Project Report PDF...")
    
    # Path setup
    root_dir = "d:/My Projects/Kifiya AI Mastery Training/week12"
    artifact_dir = "C:/Users/tekam/.gemini/antigravity/brain/c4692355-0c0d-4c50-98a4-fb3ab3e9e849"
    md_file = os.path.join(artifact_dir, "final_project_report.md")
    output_html = os.path.join(root_dir, "final_report.html")
    output_pdf = os.path.join(root_dir, "Final_Project_Report_Week12.pdf")
    
    if not os.path.exists(md_file):
        print(f"❌ Markdown file not found at {md_file}")
        return
    
    # Step 1: Read Markdown
    with open(md_file, "r", encoding="utf-8") as f:
        md_text = f.read()
        
    # Standardize image paths for the PDF converter (relative to root_dir)
    # The markdown uses ![desc](screenshots/file.png)
    # We want to make sure the script can find them in week12/screenshots/
    
    # Convert Markdown to HTML
    html_content = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])
    
    # Step 2: Wrap in professional HTML Template
    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                size: A4;
                margin: 2cm;
            }}
            body {{
                font-family: 'Helvetica', 'Arial', sans-serif;
                line-height: 1.6;
                color: #2c3e50;
                padding: 20px;
            }}
            h1 {{
                color: #1a5276;
                text-align: center;
                border-bottom: 2px solid #1a5276;
                padding-bottom: 10px;
                margin-top: 0;
            }}
            h2 {{
                color: #2471a3;
                border-bottom: 1px solid #d4e6f1;
                padding-bottom: 5px;
                margin-top: 30px;
            }}
            h3 {{
                color: #2980b9;
                margin-top: 20px;
            }}
            img {{
                display: block;
                margin: 20px auto;
                max-width: 100%;
                border: 1px solid #dee2e6;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }}
            em {{
                display: block;
                text-align: center;
                font-size: 0.9em;
                color: #7f8c8d;
                margin-top: -15px;
                margin-bottom: 20px;
            }}
            code {{
                background-color: #f4f6f7;
                padding: 2px 5px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }}
            pre {{
                background-color: #f4f6f7;
                padding: 15px;
                border-left: 4px solid #3498db;
                overflow-x: auto;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #d5dbdb;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #ebf5fb;
            }}
            .footer {{
                text-align: center;
                font-size: 0.8em;
                color: #95a5a6;
                margin-top: 50px;
                border-top: 1px solid #eee;
                padding-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="header" style="text-align: right; color: #7f8c8d; font-size: 0.9em; margin-bottom: 20px;">
            {datetime.now().strftime('%B %d, %Y')}
        </div>
        {html_content}
        <div class="footer">
            © {datetime.now().year} Tekalegn Mekonen | KAIM 8 - Week 12 Capstone Project
        </div>
    </body>
    </html>
    """
    
    # Save temporary HTML for debugging or manual PDF generation
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(full_html)
        
    # Step 3: Convert HTML to PDF using pisa
    print("🎨 Converting HTML to PDF...")
    with open(output_pdf, "wb") as result_file:
        pisa_status = pisa.CreatePDF(full_html, dest=result_file, path=root_dir)
        
    if pisa_status.err:
        print(f"❌ Error during PDF generation: {pisa_status.err}")
    else:
        print(f"🎉 PDF Report successfully generated at: {output_pdf}")

if __name__ == "__main__":
    create_pdf_report()
