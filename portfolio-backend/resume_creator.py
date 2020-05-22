import json
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor
from PIL import Image

from line_generator import MCLine
from image import HyperlinkedImage

MARGIN_VERTICAL = 10
MARGIN_HORIZONTAL = 20

class Resume_Creator:

    def __init__(self, file_name, input):
        self.pdf_buffer = BytesIO();
        self.doc = SimpleDocTemplate(
                    self.pdf_buffer,
                    pageSize = letter,
                    rightMargin = MARGIN_HORIZONTAL,
                    leftMargin = MARGIN_HORIZONTAL,
                    topMargin = MARGIN_VERTICAL,
                    bottomMargin = MARGIN_VERTICAL
                    );
        self.file_name = file_name;
        self.data = [];
        self.input = input
        self.bullet_properties = {
        "symbol":"•",
        "indent":10
        };
        self.page_size = letter
        # print("page size: ",self.page_size)

    def get_body_style(self,type,parameters):
        sample_style_sheet = getSampleStyleSheet();
        body_style = sample_style_sheet[type];
        # print(sample_style_sheet.list())
        for key in parameters:
            if key == "fontSize":
                body_style.fontSize = parameters[key]
            if key == "textColor":
                body_style.textColor = parameters[key]
        if type == "Bullet":
            body_style.leftIndent = self.bullet_properties["indent"];
        return body_style;

    def generate_bullet_points(self, font_size, array):
        body_style = self.get_body_style("Bullet",{
        "fontSize": font_size
        });
        for point in array:
            self.data.append(Paragraph(point, body_style, bulletText = self.bullet_properties["symbol"]));

    def generate_heading(self, title):
        body_style = self.get_body_style("Normal",{
        "fontSize": 12,
        "textColor": HexColor("#ff8100")
        });
        self.data.append(Paragraph(title, body_style));
        self.data.append(Spacer(1, 5))
        line = MCLine(self.page_size[0] - (3.5 * MARGIN_HORIZONTAL), 0)
        self.data.append(line)

    def add_summary(self):
        self.generate_heading("<b>EXECUTIVE SUMMARY</b>")
        self.generate_bullet_points(10.5, self.input["executive_summary"])
        self.data.append(Spacer(1, 10))
        print("summary")

    def add_experience(self):
        self.generate_heading("<b>EXPERIENCE</b>")
        # for experience in self.input["experience"]:
        #     print("exp: ",json.dumps(experience))
        print("experience")

    def add_skills(self):
        self.generate_heading("SKILLS")
        print("skills")

    def add_education(self):
        print("education")

    def add_header(self):
        print(self.input["heading"])
        # img = Image.open('images/linkedin.png')
        name_style = self.get_body_style("Normal",{
        "fontSize": 24,
        "textColor": HexColor("#ff8100")
        });
        linkedin = HyperlinkedImage('images/linkedin.png', self.input["heading"]["linkedin"],30,30)
        github = HyperlinkedImage('images/github.png', self.input["heading"]["github"],30,30)
        table_data = [
            [Paragraph("<b>%s</b>" % self.input["heading"]["name"], name_style)],
            [Spacer(1, 10)],
            [github, linkedin]
        ]
        table = Table(table_data)
        self.data.append(table)
        print("header")

    def add_projects(self):
        print("projects")

    def save_resume(self):
        self.add_header();
        self.add_summary();
        # self.add_skills();
        self.add_experience();
        self.doc.build(self.data);
        with open(self.file_name + ".pdf", "wb") as f:
            f.write(self.pdf_buffer.getbuffer())
            self.pdf_buffer.close();
        print("save resume")
