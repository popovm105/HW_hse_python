

import bs4
import csv






def get_data_from_token1(token):
    data = {}
    if isinstance(token, bs4.element.Tag):
        data['type'] = 'word'
        data['word'] = token.text.strip()
        data['ana']=[]
        for ana in token.findAll('ana'):
            data['ana'].append(ana.attrs)

    elif len(token.strip())>0:
        data['type'] = 'punct'
        data['punct'] = token.strip()
    else:
        return False
    return data




def get_data_from_token(token):
    data = []
    if isinstance(token, bs4.element.Tag):
        for ana in token.findAll('ana'):
            word_analysis = {'type': 'word', 'word': token.text.strip()}
            word_analysis.update(ana.attrs)
            data.append(word_analysis)
    elif len(token.strip())>0:
        data.append({'type':'punct', 'punct': token.strip()})
    else:
        return False
    return data




def make_list_for_prs(text):
    bs_text = bs4.BeautifulSoup(text, 'html.parser')
    sentences = bs_text.findAll('se')
    list_for_prs = []
    for sent_num, sentence in enumerate(sentences,1):
        #print(sent_num)
        word_num = 0
        for token in sentence:
            data_from_token = get_data_from_token(token)
            if data_from_token:
                if data_from_token[0]['type'] =='word':
                    word_num +=1
                for d in data_from_token:
                    #print(d)
                    d['sentno'] = sent_num
                    if d['type'] == 'word':
                        d['wordno'] = word_num
                    list_for_prs.append(d)
        
    return list_for_prs

        

    
    



def add_hash_to_keys(list_of_dictionaries):
    for item in list_of_dictionaries:
        keys = set(item.keys())
        for key in keys:
            item['#'+key] = item.pop(key)




def add_punct_to_words(list_for_prs):
    
    for index, item in enumerate(list_for_prs):
        if item['type'] == 'word':
            item['punctr'] = ''
        if item['type'] == 'punct' and index > 0:
            list_for_prs[index-1]['punctr'] = item['punct']

    result = [item for item in list_for_prs if item['type']=='word']
    return result

def make_sentences_list(list_from_prs):
    sent_list=[]
    num_of_sent = int(list_from_prs[-1]['#sentno'])
    for sent in range(1,num_of_sent+1):
        sent_list.append([item for item in list_from_prs if item['#sentno'] == str(sent)])

    return sent_list
        



def make_words_list(sentence):
    word_list = []
    num_of_words = int(list_from_prs[-1]['#wordno'])
    for word in range(1,num_of_words+1):
        word_list.append([item for item in sentence if item['#wordno'] == str(word)])

    return word_list




def make_ana_tag_from_word_data(word_data):
    keys = [key for key in word_data.keys() if key not in ['#sentno', '#wordno','#word','#punctr']]
    tag = '      <ana '
    for key in keys:
        tag += key[1:] + '="' + word_data[key] + '" '
    tag += '/>\n'
    return tag




def create_xml_str(list_from_prs):
    xml_str = '<body>\n'
    sentences = make_sentences_list(list_from_prs)
    for sentence in sentences:
        xml_str += '  <se>\n'
        
        words = make_words_list(sentence)
        for word in words:
            xml_str += '    <w>\n'
            for word_data in word:
                xml_str += make_ana_tag_from_word_data(word_data)

            xml_str += '      ' + word_data['#word'] + '\n'
            xml_str += '    </w>\n'
            if word_data['#punctr']:
                xml_str += '    {}\n'.format(word_data['#punctr']) 
        xml_str +='  </se>\n'
    
    xml_str += '</body>'
    return xml_str


if __name__ == "__main__":   
    #делаем из xml_corp new.prs
    with open('xml_corp') as f:
        text = f.read()

    result = make_list_for_prs(text)
    result = add_punct_to_words(result)
    add_hash_to_keys(result)

    with open('new.prs', 'w') as prsfile:
        fieldnames = ['#sentno', '#wordno', '#word'] + sorted([key for key in result[0].keys() if key not in ['#sentno', '#wordno','#word','#type']])

        writer = csv.DictWriter(prsfile, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        for item in result:
            item.pop('#type')
            writer.writerow(item)


    #делаем из new.prs new.xml

    list_from_prs = []
    with open('new.prs') as prsfile:
        reader = csv.DictReader(prsfile, delimiter='\t')
        
        for row in reader:
            list_from_prs.append(row)
    with open('new.xml','w') as f:
        f.write(create_xml_str(list_from_prs))









