import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
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
GENERAL_FONT_SIZE = 8
HEADING_FONT_SIZE = GENERAL_FONT_SIZE + 2
NAME_FONT_SIZE = GENERAL_FONT_SIZE * 2
SPACER_VALUE = 5
FOOTER_FONT_SIZE = GENERAL_FONT_SIZE

def convert_differnce_to_string(difference):
    years = difference.years
    months = difference.months
    print (difference)
    string = "";
    if years != 0:
        string += '%s Years' % years if years > 1 else '%s Year' % years;
    if months != 0:
        string += ' %s Months' % months if months > 1 else ' %s Month' % months;
    return string.strip();

def get_difference_between_dates(date_range, get_raw = False):
    date_array = [];
    for date_string in date_range.split("-"):
        if date_string.strip() != "Present":
            date_array.append(datetime.strptime(date_string.strip(), "%B %d %Y"))
        else:
            date_array.append(datetime.now())
    difference = relativedelta(date_array[1], date_array[0])
    if get_raw:
        return difference

    add_strix = "*" if "Present" in date_range else ""
    return convert_differnce_to_string(difference) + add_strix

def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFontSize(FOOTER_FONT_SIZE)
    canvas.drawString(letter[0]-110, 25, "*As of %s" % datetime.strftime(datetime.now(), "%m/%d/%Y"))
    canvas.restoreState()

class Resume_Creator:

    def __init__(self, file_name, input):
        self.pdf_buffer = BytesIO();
        self.doc = SimpleDocTemplate(
                    self.pdf_buffer,
                    pageSize = letter,
                    rightMargin = MARGIN_HORIZONTAL,
                    leftMargin = MARGIN_HORIZONTAL,
                    topMargin = MARGIN_VERTICAL,
                    bottomMargin = MARGIN_VERTICAL,
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
        "fontSize": HEADING_FONT_SIZE,
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
        total = relativedelta()
        for experience in self.input["experience"]:
            total += get_difference_between_dates(experience["exact_duration"], True)
        summary_point = self.input["executive_summary"][0].split("%");
        exp = " (<i>%s of development experience*</i>) " % convert_differnce_to_string(total)
        self.input["executive_summary"][0] = summary_point[0].strip() + exp + summary_point[1].strip()
        self.generate_bullet_points(GENERAL_FONT_SIZE, self.input["executive_summary"])
        self.data.append(Spacer(1, SPACER_VALUE))

    def add_experience(self):
        self.generate_heading("<b>WORK EXPERIENCE</b>", "work.png")
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
                self.generate_alignment_style("<b>%s</b>" % experience["duration"], TA_RIGHT, GENERAL_FONT_SIZE)
                ]
            ]
            sub_heading = [
                [
                Paragraph("<b>%s</b>" % experience["company"] + ' , %s' % experience["location"], word_style),
                self.generate_alignment_style('<b>(%s)</b>' % get_difference_between_dates(experience["exact_duration"]), TA_RIGHT, GENERAL_FONT_SIZE)
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

        self.data.append(Spacer(1, SPACER_VALUE))

    def add_skills(self):
        self.generate_heading("<b>SKILLS</b>","code.png")
        word_style = self.get_body_style("Normal", {
        "fontSize":GENERAL_FONT_SIZE,
        })
        points = []
        for sub_skill in self.input["skills"]:
            list = "<b>%s :</b> " % sub_skill["key"]
            for skill in sub_skill["most_used"]:
                list += '<font color = "red"><b><i>%s</i></b></font>, ' % skill
            for skill in sub_skill["list"]:
                list += "%s, " % skill
            list = list[:-2]
            points.append(list)

        self.generate_bullet_points(GENERAL_FONT_SIZE, points)
        self.data.append(Spacer(1, SPACER_VALUE))

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
        self.data.append(Spacer(1, SPACER_VALUE))

    def add_header(self):
        name_style = self.get_body_style("Normal",{
        "fontSize": NAME_FONT_SIZE
        });
        sub_heading_style = self.get_body_style("Normal", {
        "fontSize": GENERAL_FONT_SIZE
        })
        linkedin = HyperlinkedImage('images/linkedin.png', self.input["heading"]["linkedin"],25,20)
        github = HyperlinkedImage('images/github.png', self.input["heading"]["github"],20,20)
        personal_website = HyperlinkedImage('images/me.png', self.input["heading"]["website"],20,20)
        phone_image = HyperlinkedImage('images/phone.png', None, 20,20)
        address_image = HyperlinkedImage('images/address.png', None, 20, 20)
        email_image = HyperlinkedImage('images/mail.png', None, 20, 20)
        profile_picture = HyperlinkedImage('images/profilepic.png', None, 40, 40)
        heading = [
            [self.generate_alignment_style("<b>%s</b>" % self.input["heading"]["name"], TA_LEFT, NAME_FONT_SIZE)]
        ]
        heading_table = Table(heading)
        heading_table_style = [
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]
        heading_table.setStyle(heading_table_style)
        sub_data = []
        sub_data.append(heading_table)
        sub_data.append(Spacer(1, 10))
        phone = Paragraph(self.input["heading"]["phone"], sub_heading_style)
        address = Paragraph(self.input["heading"]["address"],sub_heading_style)
        email = Paragraph('<a href="mailto:%s"><font color="blue">%s</font></a>' % (self.input["heading"]["email"], self.input["heading"]["email"]), sub_heading_style)
        sub_heading = [
        [phone_image ,phone ,address_image ,address ,email_image, email,linkedin, github]
        ]
        sub_heading_table_style = [
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]
        sub_heading_table = Table(sub_heading,[25,100,25,100,25,187,25,25,25])
        sub_heading_table.setStyle(sub_heading_table_style)
        sub_data.append(sub_heading_table)
        full_data = [
            [
                profile_picture,
                sub_data
            ]
        ]
        full_data_table = Table(full_data)
        full_data_table_style = [
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]
        full_data_table.setStyle(full_data_table_style)
        self.data.append(full_data_table)
        self.data.append(Spacer(1, SPACER_VALUE))

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

        self.data.append(Spacer(1, SPACER_VALUE))

    def add_hobbies(self):
        self.generate_heading("<b>HOBBIES</b>","hobby.png")
        self.generate_bullet_points(GENERAL_FONT_SIZE, self.input["hobbies"])
        # self.data.append(Spacer(1, 10))

    def save_resume(self):
        self.add_header();
        self.add_summary();
        self.add_experience();
        self.add_skills();
        self.add_education();
        self.add_hobbies();
        # self.add_projects()
        self.doc.build(self.data, onFirstPage = myFirstPage);
        with open(self.file_name + ".pdf", "wb") as f:
            f.write(self.pdf_buffer.getbuffer())
            self.pdf_buffer.close();
        print("save resume")
