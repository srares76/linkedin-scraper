import json


class ExperienceJson():
    def __init__(self, institution_name, linkedin_url, from_date, to_date, description, position_title, duration, location):
        self.InstitutionName = institution_name
        self.LinkedInURL = linkedin_url
        self.FromDate = from_date
        self.ToDate = to_date
        self.Description = description
        self.PositionTitle = position_title
        self.Duration = duration
        self.Location = location

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class EducationJson():
    def __init__(self, institution_name, linkedin_url, from_date, to_date, description, degree):
        self.InstitutionName = institution_name
        self.LinkedInURL = linkedin_url
        self.FromDate = from_date
        self.ToDate = to_date
        self.Description = description
        self.Degree = degree

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class PersonJson():
    def __init__(self,
                 name,
                 location,
                 company_name,
                 linkedin_url,
                 job_title,
                 about,
                 experiences,
                 educations,
                 email = "",
                 birthDay = "",
                 phoneNumber ="",
                 highscool = "",
                 highscoolRegion = "",
                 finalPaperName = "",
                 graduationGrade = "",
                 universityBachelors = "",
                 facultyBachelors = "",
                 bacYear = "",
                 bachelorsFromYear = "",
                 ):
        self.Name = name
        self.Location = location
        self.Email = email
        self.BirthDay = birthDay
        self.PhoneNumber = phoneNumber
        self.Highscool = highscool
        self.HighscoolRegion = highscoolRegion
        self.FinalPaperName = finalPaperName
        self.GraduationGrade = graduationGrade
        self.UniversityBachelors = universityBachelors
        self.FacultyBachelors = facultyBachelors
        self.BacYear = bacYear
        self.BachelorsFromYear = bachelorsFromYear
        self.LinkedInURL = linkedin_url
        self.JobTitle = job_title
        self.CompanyName = company_name
        self.About = about
        self.Experiences = experiences
        self.Educations = educations

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
