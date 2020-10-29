import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import date



def get_papers(term, min_citation = 150):
    
    pmc_query = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=" + term +"&resultType=lite&cursorMark=*&pageSize=1000&sort=CITED%20desc&format=json"

    page = requests.get(pmc_query)
    data = json.loads(page.text)
    df = pd.json_normalize(data['resultList']['result'])
    single_cell_papers = df[['pmid', 'title', 'authorString', 'journalTitle', 'citedByCount', 'pubYear']]
    
    first_authors = single_cell_papers['authorString'].apply(get_first_author)
    single_cell_papers['firstAuthor'] = first_authors
    
    single_cell_papers = single_cell_papers[single_cell_papers['citedByCount']>= min_citation]
    
    return(single_cell_papers)

def get_first_author(string):
    result = string.split(',')[0]
    return(result)

def get_years(pd):
    years = list(set(pd['pubYear']))
    years.sort(reverse = True)
    return(years)
    
    
def get_new_entry(row):
    result = ("* " + row['firstAuthor'] + " et al, " + "[" + row['title'] + "]" + 
         "(" + "https://europepmc.org/article/MED/" + row['pmid'] + ")")
    return(result)
    
    
def add_section_to_md(df, mdFile, last_week_classics):
    df = df.sort_values('firstAuthor')
    years = get_years(df)
    
    for year in years:
        mdFile.new_header(2, year)
        short_df = df[df["pubYear"] == year]
        
        for index,row in short_df.iterrows():
            
            new_entry  = get_new_entry(row)
            print(new_entry)
            
            if row['title'] in last_week_classics[['title']].values:             
                mdFile.new_line(new_entry)
            
            else :
                mdFile.new_line(new_entry + '[NEW]')
            
            
            
        
        mdFile.new_line()
    
    return(mdFile)


def craft_header(mdFile,single_cell_papers):
    mdFile.new_header(level=1, title='Overview')
    mdFile.new_paragraph("Let's start looking for classic citations at the EuropePMC database.Once more, we will use naive definitions of citation classics.") 

    mdFile.new_line()
    mdFile.new_line("* Classics are all cited more than 150 times.")
    mdFile.new_line("* Big classics: more than 500 citations")
    mdFile.new_line("* Medium classics: at least 300 citations, less than 500")
    mdFile.new_line("* Small classics: at least 150 citations, less than 300\n")


    mdFile.new_line("Currently, we have " + str(single_cell_papers.shape[0]) + " classics that meet the criteria above:")
    mdFile.new_line()
    return(mdFile)

def craft_sessions(mdFile, single_cell_papers, last_week_classics):
    mdFile.new_header(1, "Big classics")
    big_classics = single_cell_papers[single_cell_papers['citedByCount'] >= 500]
    mdFile = add_section_to_md(big_classics, mdFile, last_week_classics)

    mdFile.new_header(1, "Medium classics")
    mid_classics = single_cell_papers[(single_cell_papers['citedByCount'] >= 300)
                                      & (single_cell_papers['citedByCount'] < 500)]
    mdFile = add_section_to_md(mid_classics, mdFile, last_week_classics)


    mdFile.new_header(1, "Small classics")
    smol_classics = single_cell_papers[(single_cell_papers['citedByCount'] >= 150)
                                      & (single_cell_papers['citedByCount'] < 300)]
    mdFile = add_section_to_md(smol_classics, mdFile, last_week_classics)
    return(mdFile)

def craft_date(mdFile):
    today = date.today()
    today_long_format = today.strftime("%B %d, %Y")
    mdFile.new_line()
    mdFile.new_header(1, "Last update:")

    mdFile.new_line(today_long_format)
    return(mdFile)