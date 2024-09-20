# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 02:13:02 2024

@author: Kevin Berney
"""

### a function to pull the html code of a known website
### a function to pull all text from the website using the paragraph <p> marker
### a function to summarize using a call to a google gemini llm account
## NOTE - this requires signing up for gemini account, 
## there is no charge under a threshold number of calls 
## this was an exemplar option only
## cred.json is a json formatted file with


import requests
from bs4 import BeautifulSoup

import json

#### Google gemini specific, trade out for chatgpt or other programmatic solution
#### 
import google.generativeai as genai

def configure_gemini(cred_file):
    ## todo
    ## catch json errors, fail informatively
    ## create alternate sources beyond goole gemini
    GOOGLE_API_KEY=json.load(open(cred_file,))['g']
    genai.configure(api_key=GOOGLE_API_KEY)
    return 
def pull_html_code(url):
    ## to do 
    ## handle errors
    response=requests.get(url.strip())
    return(response)

def collect_paragraphs(response,write_html=1,write_text=1,write_p=1):
    ## to do handle errors
    ## handle different response_codes
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    outtext = ''
    for paragraph in paragraphs:
        outtext = f'{outtext}\n{str(paragraph.get_text())}'
        # print(paragraph.get_text())
    # if write_html: open(f'{outroot}.html','wb').write(html_content.content)
    # if write_text: open(f'{outroot}.txt','w').write(html_content.text)
    # if write_p   : open(f'{outroot}_paragraphs.txt','w').write(outtext)  \
    return(outtext)
def summarize_text_genai(requested_fields, article_text):
    ## todo
    ## catch json errors, fail informatively
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    action = 'extract the information and'
    output_structure = 'return the result as a table with rows for each of the following fields including the relevent source text'
    full_prompt = f"{action} {output_structure} [{requested_fields}] from the following text {article_text}"
    # extract the information in the following text and return the result as a table with rows for each of the following
    # print(f"extract the information in the following text and return the result as a set of key: value pairs where the keys are [{requested_fields}] with the source text appended  {article_text}")
    response = model.generate_content(full_prompt)
    return(response)

url = 'https://www.mysuncoast.com/2024/09/19/water-boil-alert-bradenton/'
requested_fields = "date article reported, date boil notice begins, event intersection, event city, event state, cause of boil notice, source text"
credentials_file = r"C:/Users/U/Boil/cred.json"

configure_gemini('cred.json')

# outroot = r''
response = requests.get(url)
if response.status_code == 200:
    paragraphtext = collect_paragraphs(response)

result = summarize_text_genai(requested_fields, paragraphtext)