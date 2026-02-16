import os
import markdown
from datetime import datetime
from xhtml2pdf import pisa

def create_pdf(md_filename, pdf_filename, title):
    """Common function to generate PDF from markdown"""
    print(f"🚀 Generating {pdf_filename}...")
    
    root_dir = "d:/My Projects/Kifiya AI Mastery Training/week12"
    artifact_dir = "C:/Users/tekam/.gemini/antigravity/brain/c4692355-0c0d-4c50-98a4-fb3ab3e9e849"
    md_file = os.path.join(artifact_dir, md_filename)
    output_pdf = os.path.join(root_dir, pdf_filename)
    
    if not os.path.exists(md_file):
        print(f"❌ Markdown file not found at {md_file}")
        return False
        
    with open(md_file, "r", encoding="utf-8") as f:
        md_text = f.read()
        
    html_content = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])
    
    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ size: A4; margin: 2cm; }}
            body {{ font-family: 'Helvetica', sans-serif; line-height: 1.6; color: #333; }}
            h1 {{ color: #1a5276; text-align: center; border-bottom: 2px solid #1a5276; }}
            h2 {{ color: #2471a3; border-bottom: 1px solid #eee; margin-top: 30px; }}
            img {{ display: block; margin: 20px auto; max-width: 100%; border: 1px solid #ccc; }}
            .footer {{ text-align: center; font-size: 0.8em; color: #999; margin-top: 50px; border-top: 1px solid #eee; padding-top: 10px; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        {html_content}
        <div class="footer">Generated on {datetime.now().strftime('%Y-%m-%d')} | Tekalegn Mekonen</div>
    </body>
    </html>
    """
    
    with open(output_pdf, "wb") as result_file:
        pisa_status = pisa.CreatePDF(full_html, dest=result_file, path=root_dir)
    
    if not pisa_status.err:
        print(f"🎉 PDF created: {output_pdf}")
        return True
    return False

if __name__ == "__main__":
    create_pdf("progress_report.md", "Progress_Report_Interim_1.pdf", "Week 12 Interim Progress Report")
    create_pdf("final_project_report.md", "Final_Project_Report_Week12.pdf", "Portfolio Management Optimizer - Technical Report")
