from utils import utils
import pandas as pd
from mdutils.mdutils import MdUtils

def main():

    term = "%22single-cell%20RNA-seq%22"

    single_cell_papers = utils.get_papers(term, min_citation = 150)
    single_cell_papers


    last_week_classics = pd.read_csv('current_papers.csv')

    mdFile = MdUtils(file_name='README', title='Classic citations from the Europe PMC database')
    
    mdFile = utils.craft_header(mdFile,single_cell_papers)
    mdFile = utils.craft_sessions(mdFile,single_cell_papers, last_week_classics)


    single_cell_papers.to_csv('current_papers.csv')

    mdFile = utils.craft_date(mdFile)
    mdFile.create_md_file()


if __name__ == "__main__":
    main()