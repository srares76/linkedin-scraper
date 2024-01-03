from scraper.objects import Education
from typing import List

def studied_at_politehnica(educations: List[Education]):
    for education in educations:
        if "politehnica" in education.institution_name.lower() and ("bucuresti" in education.institution_name.lower() or "bucharest" in education.institution_name.lower()):
            return True
    return False