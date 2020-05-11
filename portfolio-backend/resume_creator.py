from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

class Resume_Creator:

    def __init__(self, file_name):
        self.pdf_buffer = BytesIO();
        self.doc = SimpleDocTemplate(self.pdf_buffer);
        self.file_name = file_name;
        self.data = [];

    def get_body_style(self,font_size):
        sample_style_sheet = getSampleStyleSheet();
        print("body style",sample_style_sheet)
        body_style = sample_style_sheet['BodyText'];
        body_style.fontSize = font_size;
        return body_style;

    def add_summary(self, data):
        print("summary")

    def add_experience(self, data):
        print("experience")

    def add_skills(self, data):
        print("skills")

    def add_education(self, data):
        print("education")

    def add_header(self, data):
        body_style = self.get_body_style(100);
        self.data = [
            Paragraph("First paragraph", body_style),
            Paragraph("Second paragraph", body_style)
        ]
        print("header")

    def add_projects(self, data):
        print("projects")

    def save_resume(self):
        self.doc.build(self.data);
        with open(self.file_name + ".pdf", "wb") as f:
            f.write(self.pdf_buffer.getbuffer())
            self.pdf_buffer.close();
        print("save resume")
