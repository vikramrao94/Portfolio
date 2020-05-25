import json
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer, Table
from reportlab.lib.enums import TA_JUSTIFY,TA_LEFT,TA_CENTER,TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor

from line_generator import MCLine
from image import HyperlinkedImage

MARGIN_VERTICAL = 5
MARGIN_HORIZONTAL = 20
HEADING_COLOR = HexColor("#6969e5")
GENERAL_FONT_SIZE = 10

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

    def generate_bullet_points(self, font_size, array, table = None):
        body_style = self.get_body_style("Bullet",{
        "fontSize": font_size
        });
        if table == True:
            result = []
            for point in array:
                result.append(Paragraph(point, body_style, bulletText = self.bullet_properties["symbol"]))
            return result

        for point in array:
            self.data.append(Paragraph(point, body_style, bulletText = self.bullet_properties["symbol"]));

    def generate_alignment_style(self, input, alignment, size):
        style = ParagraphStyle('Normal',
                    alignment = alignment,
                    fontSize = size
                    )
        return Paragraph(input, style)

    def generate_heading(self, title, image):
        body_style = self.get_body_style("Normal",{
        "fontSize": 12,
        "textColor": HEADING_COLOR
        });
        heading = [
            [
                HyperlinkedImage("images/%s"%image,None, 20,20),
                Paragraph(title, body_style)
            ]
        ]
        heading_table = Table(heading, [30, 525])
        heading_table.setStyle(
            [
                ('VALIGN', (0, 0), (-1, -1), "MIDDLE")
            ]
        )
        self.data.append(heading_table,)
        self.data.append(Spacer(1, 5))
        line = MCLine(self.page_size[0] - (3.5 * MARGIN_HORIZONTAL), 0)
        self.data.append(line)

    def add_summary(self):
        self.generate_heading("<b>EXECUTIVE SUMMARY</b>","summary.png")
        self.generate_bullet_points(GENERAL_FONT_SIZE, self.input["executive_summary"])
        self.data.append(Spacer(1, 10))

    def add_experience(self):
        self.generate_heading("<b>EXPERIENCE</b>", "work.png")
        word_style = self.get_body_style("Normal", {
        "fontSize":GENERAL_FONT_SIZE,
        })
        for experience in self.input["experience"]:
            logo = [
                [
                HyperlinkedImage("images/" + experience["logo"],None, 20, 20)
                ]
            ]
            sub_title = ' | %s' % experience["sub_title"] if experience["sub_title"] != None else ''
            heading = [
                [
                Paragraph("<b>%s</b>" % experience["title"] + sub_title ,word_style),
                self.generate_alignment_style("<b>%s</b>"%experience["duration"], TA_RIGHT, GENERAL_FONT_SIZE)
                ]
            ]
            sub_heading = [
                [
                Paragraph("<b>%s</b>" % experience["company"] + ' , %s' % experience["location"], word_style)
                ]
            ]
            summary = [
                [
                    self.generate_bullet_points(GENERAL_FONT_SIZE, experience["summary"],True)
                ]
            ]
            heading_table = Table(heading,[220,298])
            summary_table = Table(summary)
            sub_heading_table = Table(sub_heading)
            combined_table = [
                [
                    heading_table,
                    sub_heading_table,
                    summary_table
                ]
            ]
            logo_table = Table(logo)
            main = [
                [
                logo_table,
                combined_table
                ]
            ]
            main_table = Table(main, [30, 530])
            main_table_style = [
                ('VALIGN', (0, 0), (0, 0), "MIDDLE"),
            ]
            main_table.setStyle(main_table_style)
            self.data.append(main_table)

        self.data.append(Spacer(1, 10))

    def add_skills(self):
        self.generate_heading("<b>SKILLS</b>","code.png")
        word_style = self.get_body_style("Normal", {
        "fontSize":GENERAL_FONT_SIZE,
        })
        points = []
        for sub_skill in self.input["skills"]:
            list = "<b>%s :</b> " % sub_skill["key"]
            for skill in sub_skill["most_used"]:
                list += "<i>%s</i>, " % skill
            for skill in sub_skill["list"]:
                list += "%s, " % skill
            list = list[:-2]
            points.append(list)

        self.generate_bullet_points(GENERAL_FONT_SIZE, points)
        self.data.append(Spacer(1, 10))

    def add_education(self):
        self.generate_heading("<b>EDUCATION</b>","school.png")
        for education in self.input["education"]:
            word_style = self.get_body_style("Normal", {
            "fontSize":GENERAL_FONT_SIZE,
            })
            logo = [
                [
                HyperlinkedImage("images/" + education["logo"],None, 20, 25)
                ]
            ]
            degree = [[
                Paragraph("<b>%s</b>"% education["degree"],word_style),
                Paragraph("<i>%s</i>"% education["course"],word_style)
            ]]
            school = [[
                Paragraph(education["school"],word_style),
                Paragraph(education["location"],word_style)
            ]]

            educate = [
                [Table(degree, [30, 300])],
                [Table(school, [150, 180])]
            ]
            duration = [
                [
                    self.generate_alignment_style("<b>%s</b>"%education["duration"], TA_RIGHT, GENERAL_FONT_SIZE)
                ]
            ]
            logo_table = Table(logo)

            education_table = Table(educate)
            duration_table = Table(duration)
            main = [
                [
                logo_table,
                education_table,
                duration_table
                ]
            ]
            main_table = Table(main, [30,330,200])
            main_table_style = [
                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
            ]
            main_table.setStyle(main_table_style)
            self.data.append(main_table)
        self.data.append(Spacer(1, 10))

    def add_header(self):
        name_style = self.get_body_style("Normal",{
        "fontSize": 24,
        "textColor": HEADING_COLOR
        });
        sub_heading_style = self.get_body_style("Normal", {
        "fontSize": GENERAL_FONT_SIZE
        })
        linkedin = HyperlinkedImage('images/linkedin.png', self.input["heading"]["linkedin"],25,20)
        github = HyperlinkedImage('images/github.png', self.input["heading"]["github"],20,20)
        personal_website = HyperlinkedImage('images/me.png', self.input["heading"]["website"],20,20)
        phone_image = HyperlinkedImage('images/phone.png', None, 20,20)
        address_image = HyperlinkedImage('images/address.png', None, 20, 20)
        heading = [
            [Paragraph("<b>%s</b>" % self.input["heading"]["name"], name_style)],
        ]
        heading_table = Table(heading)
        heading_table_style = [
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TEXTCOLOR', (0,0),(-1,-1), HEADING_COLOR)
        ]
        heading_table.setStyle(heading_table_style)
        self.data.append(heading_table)
        self.data.append(Spacer(1, 20))
        phone = Paragraph(self.input["heading"]["phone"], sub_heading_style)
        address = Paragraph(self.input["heading"]["address"],sub_heading_style)
        sub_heading = [
        [phone_image ,phone ,address_image ,address, personal_website,linkedin, github]
        ]
        sub_heading_table_style = [
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT')
        ]
        sub_heading_table = Table(sub_heading,[25,100,25,312,25,25,25])
        sub_heading_table.setStyle(sub_heading_table_style)
        self.data.append(sub_heading_table)
        self.data.append(Spacer(1, 10))

    def add_projects(self):
        self.generate_heading("<b>PERSONAL PORJECTS</b>","project.png")
        word_style = self.get_body_style("Normal", {
        "fontSize":GENERAL_FONT_SIZE,
        })
        for project in self.input["personal_projects"]:
            logo = [
                [
                HyperlinkedImage("images/" + project["logo"],project["link"], 20, 20)
                ]
            ]
            summary = [
                [
                    self.generate_bullet_points(GENERAL_FONT_SIZE, project["summary"],True)
                ]
            ]
            description = [[Paragraph("<b>%s</b>" % project["project"], word_style)],[Table(summary)]]
            main = [
                [
                    Table(logo),
                    Table(description)
                ]
            ]
            main_table = Table(main, [30,530])
            main_table_style = [
                ('VALIGN', (0, 0), (0, 0), "MIDDLE"),
            ]
            main_table.setStyle(main_table_style)
            self.data.append(main_table)

        self.data.append(Spacer(1, 10))

    def save_resume(self):
        self.add_header();
        self.add_summary();
        self.add_experience();
        self.add_skills();
        self.add_education();
        self.add_projects()
        self.doc.build(self.data);
        with open(self.file_name + ".pdf", "wb") as f:
            f.write(self.pdf_buffer.getbuffer())
            self.pdf_buffer.close();
        print("save resume")
