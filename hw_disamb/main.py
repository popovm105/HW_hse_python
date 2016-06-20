
from pymystem3 import Mystem
m = Mystem()


class Parsed_text(object):
    """
    конструктору подается текст, в классе хранится текст и обработанный Mystem текст
    """
    def __init__(self, text):
        self.text = text
        self.parsed_text = m.analyze(text)
        self.num_of_tokens = len(self.parsed_text) 
        
        
class PR_stat(Parsed_text):
    '''
    конструктору подается текст, в классе хранится текст и обработанный Mystem текст и статистика вида (предлог, падеж): количество
    для конструкцию предлог + существительное
    '''
    def __init__(self,text):
        super().__init__(text)
        self.statistics = self.make_statistics()
        
        
    def make_statistics(self):
        statistics = {}
        for index,item in enumerate(self.parsed_text[:-3]):
                if 'analysis' in item and len(item['analysis'])>0 and 'gr' in item['analysis'][0] and item['analysis'][0]['gr'] == 'PR=':
                    if self.parsed_text[index + 1]['text'] == ' ':
                        if 'analysis' in self.parsed_text[index + 2] and len(self.parsed_text[index + 2]['analysis'])>0 and 'gr' in self.parsed_text[index + 2]['analysis'][0] and self.parsed_text[index + 2]['analysis'][0]['gr'].split(',')[0] == 'S':
                            case = self.find_case(self.parsed_text[index + 2]['analysis'][0]['gr'])
                            if case:
                                statistics[(item['text'].lower(), case)] = statistics.get((item['text'].lower(), case), 0) + 1
        return statistics
    def find_case(self, gram):
        cases = ['им', 'род', 'дат', 'вин', 'твор', 'пр', 'парт', 'местн', 'зват']
        if '|' in gram:
            return False
        for case in cases:
            if case in gram:
                return case
        return False

    
class Disamb_text(Parsed_text):
    '''
    конструктору подается текст и статистика полученная на другом или том же тексте,
    в классе хранится текст и обработанный Mystem текст с заменой падежей на наиболее частотные в конструкциях предлог+существительное
    '''
    def __init__(self,text, statistics):
        super().__init__(text)
        self.parsed_text = self.disamb_text(self.parsed_text, statistics)
    
    def disamb_text(self, text, statistics):
        pr_case = self.get_pr_case(statistics)
        #print(pr_case)
        for index,item in enumerate(self.parsed_text[:-3]):
            if 'analysis' in item and len(item['analysis'])>0 and 'gr' in item['analysis'][0] and item['analysis'][0]['gr'] == 'PR=':
                pr = item['text'].lower()
                
                if self.parsed_text[index + 1]['text'] == ' ' and pr in pr_case.keys():
                    if 'analysis' in self.parsed_text[index + 2] and len(self.parsed_text[index + 2]['analysis'])>0 and 'gr' in self.parsed_text[index + 2]['analysis'][0] and self.parsed_text[index + 2]['analysis'][0]['gr'].split(',')[0] == 'S':
                        self.parsed_text[index + 2]['analysis'][0]['gr'] = self.replace_cases(self.parsed_text[index + 2]['analysis'][0]['gr'], pr_case[pr])
        return text            
                    
    def get_pr_case(self,statistics):
        PRs = set([item[0] for item in statistics.keys()])
        #print(PRs)
        sort_stat = sorted(statistics.items(), key = lambda a: a[1])
        pr_case = {}
        for pr in PRs:
            for item in sort_stat:
                if pr in item[0]:
                    pr_case[pr] = item[0][1]
                    break
        return pr_case
    
    
    def replace_cases(self, gram, disamb_case):
        cases = ['им', 'род', 'дат', 'вин', 'твор', 'пр', 'парт', 'местн', 'зват']
        for case in cases:
            if case in gram:
                gram = gram.replace(case, disamb_case)
        return gram
        



if __name__ == "__main__":
    with open('book1.txt') as f:
        text1 = f.read()

    with open('book2.txt') as f:
        text2 = f.read()
    a = PR_stat(text1)



    b = Disamb_text(text2, a.statistics)


    print(b.parsed_text)

