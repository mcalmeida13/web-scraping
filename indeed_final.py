import csv
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_url(position, location):
    """Generate url from position and location"""
    template = 'https://br.indeed.com/jobs?q={}&l={}'
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    url = template.format(position, location)
    return url

def get_record(card):
    """Extract job data from a single record"""
    job_title = card.find('h2','jobTitle').getText()
    company_tag = card.find('span', 'companyName')
    if company_tag:
        company = company_tag.getText().strip()
    else:
        company = 'Não informado'

    job_location_tag = card.find('div', 'companyLocation')
    if job_location_tag:
        job_location = job_location_tag.getText().split('•')[0]
    else:
        job_location = 'Não informado'
    post_date = card.find('span', 'date').text
    today = datetime.today().strftime('%Y-%m-%d')
    summary = card.find('div', 'job-snippet').text.strip().replace('\n', ' ')

    # this does not exists for all jobs, so handle the exceptions
    salary_tag = card.find('span', 'salary-snippet')
    if salary_tag:
        salary = salary_tag.getText()
    else:
        salary = 'Não informado'

    record = (job_title, company, job_location, post_date, today, summary, salary)

    return record

def main(position,location,filepath):
    records = []
    url = get_url(position, location)
    df = pd.DataFrame()
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', 'job_seen_beacon')

        for card in cards:
            record = get_record(card)
            records.append(record)
        try:
            url = 'https://br.indeed.com/' + soup.find('a', {'aria-label': 'Próxima'}).get('href')
        except AttributeError:
            break

    # save the job data
    path = filepath + '.csv'
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['JobTitle', 'Company', 'Location', 'PostDate', 'ExtractDate', 'Summary', 'Salary'])
        writer.writerows(records)
  # return writer

position = 'business intelligence'
location = 'São paulo'
filepath = 'result_sp'

main(position,localtion,filepath)