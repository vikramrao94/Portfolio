import json
from cv_creator import CV_Creator
from resume_creator import Resume_Creator

with open('test.json') as json_file:
    data = json.load(json_file)
resume = Resume_Creator("resume", data);
resume.save_resume();
