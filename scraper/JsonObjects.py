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
                 linkedin_url,
                 job_title,
                 company_name,
                 about,
                 location,
                 experiences,
                 educations
                 ):
        self.Name = name
        self.Email = ""
        self.BirthDay = ""
        self.PhoneNumber = ""
        self.Highscool = ""
        self.HighscoolRegion = ""
        self.FinalPaperName = ""
        self.GraduationGrade = ""
        self.UniversityBachelors = ""
        self.FacultyBachelors = ""
        self.BacYear = ""
        self.BachelorsFromYear = ""
        self.LinkedInURL = linkedin_url
        self.JobTitle = job_title
        self.CompanyName = company_name
        self.About = about
        self.Location = location
        self.Experiences = experiences
        self.Educations = educations

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
