from cv_creator import CV_Creator
from resume_creator import Resume_Creator


resume = Resume_Creator("resume");
resume.add_header("blah");
resume.save_resume();
