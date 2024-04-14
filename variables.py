from dotenv import load_dotenv
import os

load_dotenv()

my_username = os.environ['LINKEDIN_USERNAME']
my_password = os.environ['LINKEDIN_PASSWORD']

input_file = 'students/2010.txt'
output_file = 'output/2010.json'

query = 'site:linkedin.com/in/ AND "Web" AND "Javascript"'
