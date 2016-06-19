import os
from bs4 import BeautifulSoup
from difflib import SequenceMatcher



def merge_xml(folder_path):
    xml_files  = sorted(os.listdir(folder_path))
    with open(folder_path+xml_files[0]) as f:
        text = f.read()
        
    result_xml = BeautifulSoup(text,'html.parser')

    for file in xml_files[1:]:

        with open(folder_path+file) as f:
            text = f.read()
        bs_text = BeautifulSoup(text,'html.parser')
        result_xml.body.append(bs_text.body)
    for index, para in enumerate(result_xml.findAll('para')):
        para['id']  = index
    
    with open(folder_path[2:-1]+'.xml','w') as f:
        f.write(result_xml.prettify())


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()



def corrector(standard_file_path, dirty_file_path, R_O_value = 0.85):
    with open(standard_file_path) as f:
        text = f.read()
        
    standard_bs = BeautifulSoup(text,'html.parser')
    
    with open(dirty_file_path) as f:
        text = f.read()
        
    dirty_bs = BeautifulSoup(text,'html.parser')

    for se_standard in standard_bs.findAll('se'):

        if se_standard['lang'] in set(['en', 'uk']):
            for se_dirty in dirty_bs.findAll('se'):
                if se_dirty['lang'] in set(['en', 'uk']):
                    if R_O_value <similar(se_standard.text, se_dirty.text) < 1:
                        print(se_dirty.text)
                        print(se_standard.text)
                        print('='*100)
                        se_dirty.string = se_standard.string
                        
                       
    with open(dirty_file_path,'w') as f:
        f.write(dirty_bs.prettify())



if __name__ == "__main__":  
    merge_xml('./pale_fire_Sharyimov/')
    corrector('./pale_vera.xml','./pale_fire_Sharyimov.xml')




