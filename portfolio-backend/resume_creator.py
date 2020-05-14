from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

from line_generator import MCLine
class Resume_Creator:

    def __init__(self, file_name, input):
        self.pdf_buffer = BytesIO();
        self.doc = SimpleDocTemplate(self.pdf_buffer, pageSize = letter);
        self.file_name = file_name;
        self.data = [];
        self.input = input
        self.bullet_properties = {
        "symbol":"•",
        "indent":10
        };

    def get_body_style(self,type,font_size):
        sample_style_sheet = getSampleStyleSheet();
        # print("body style",sample_style_sheet.list())
        body_style = sample_style_sheet[type];
        body_style.fontSize = font_size;
        if type == "Bullet":
            body_style.leftIndent = self.bullet_properties["indent"];
        return body_style;

    def generate_bullet_points(self, font_size):
        body_style = self.get_body_style("Bullet",font_size);
        for point in self.input:
            self.data.append(Paragraph(point, body_style, bulletText = self.bullet_properties["symbol"]));

    def add_summary(self):
        self.generate_bullet_points(12)
        line = MCLine(500)
        self.data.append(line)
        print("summary")

    def add_experience(self):
        print("experience")

    def add_skills(self):
        print("skills")

    def add_education(self):
        print("education")

    def add_header(self):
        print("header")

    def add_projects(self):
        print("projects")

    def save_resume(self):
        self.add_summary();
        self.doc.build(self.data);
        with open(self.file_name + ".pdf", "wb") as f:
            f.write(self.pdf_buffer.getbuffer())
            self.pdf_buffer.close();
        print("save resume")
