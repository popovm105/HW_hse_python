

import csv


# Функция проверяет пересекается ли дата создания с требуемым интервалом


def in_date(min_date, max_date, text_date):
    if '/' not in text_date:    
        if '-' in text_date:
            
            #костыль для даты вида хххх-хххх,хххх
            text_min, text_max = [int(item[0:4]) for item in text_date.split('-')[:2]]
        else:
            text_min, text_max = int(text_date[0:4]),int(text_date[0:4])
        if text_min > max_date or text_max < max_date:
            return False
        else:
            return True
    else:   
        
        text_min, text_max = int(text_date[-4:]),int(text_date[-4:])
        if text_min > max_date or text_max < max_date:
            return False
        else:
            return True


# Функция извлекает сроки из таблицы и делит их согласно требованиям



def make_set_from_csv(path = 'source_post1950_wordcount.csv', delimit='\t'):
    csv_data = []
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimit)
        i=0
        for row in reader:
            if row['words'] == 'none':
                continue
            elif int(row['words']) > 100000:
                part_1 = row.copy()
                part_1['path'] = part_1['path'] + '_1_3'
                part_1['words'] = int(part_1['words'])//2
                part_2 = row.copy()
                part_2['path'] = part_1['path'] + '_2_3'
                part_2['words'] = int(part_1['words'])//2 
                part_3 = row.copy()
                part_3['path'] = part_1['path'] + '_3_3'
                part_3['words'] = int(part_1['words'])//2 + int(part_1['words']) % 3
                csv_data.append(part_1)
                csv_data.append(part_2)
                csv_data.append(part_3)
            elif int(row['words']) > 80000:
                part_1 = row.copy()
                part_1['path'] = part_1['path'] + '_1_2'
                part_1['words'] = int(part_1['words'])//2
                part_2 = row.copy()
                part_2['path'] = part_1['path'] + '_2_2'
                part_2['words'] = int(part_1['words'])//2 + int(part_1['words']) % 2
                csv_data.append(part_1)
                csv_data.append(part_2)
            else:
                csv_data.append(row)
    return csv_data


# Функция возвращает по одному тексту из каждого промежутка если это возможно и объем возвращаемых текстов



def get_one_text_for_each_date(data2):
    data = data2.copy()
    result = []
    volue = 0
    for row in data:
        if in_date(1950, 1960, row['created']):
            result.append(row)
            volue += int(row['words'])
            break
    data = [item for item in data if item not in result]
    for row in data:
        if in_date(1961, 1970, row['created']):
            result.append(row)
            volue += int(row['words'])
            break
    data = [item for item in data if item not in result]
    for row in data:
        if in_date(1971, 1980, row['created']):
            result.append(row)
            volue += int(row['words'])
            break
    data = [item for item in data if item not in result]
    for row in data:
        if in_date(1981, 1990, row['created']):
            result.append(row)
            volue += int(row['words'])
            break
    data = [item for item in data if item not in result]
    for row in data:
        if in_date(1991, 2000, row['created']):
            result.append(row)
            volue += int(row['words'])
            break
    data = [item for item in data if item not in result]
    for row in data:
        if in_date(2001, 2010, row['created']):
            result.append(row)
            volue += int(row['words'])
            break
    data = [item for item in data if item not in result]
    for row in data:
        if in_date(2011, 2015, row['created']):
            result.append(row)
            volue += int(row['words'])
            break
    return result, volue


# Функция возвращает максимально возможно равномерно распределенный по периудам подкорпус указанного жанра и его объем



def get_sphere_for_corp(data, sphere_name, max_volue):
    current_volue = 0
    sphere_set = []
    result_set = []
    i=0
    for row in data:

        
        if sphere_name.lower() == row['sphere'].split(' | ')[0].lower().strip():
            sphere_set.append(row)

    print(sphere_name, len(sphere_set))       
    while current_volue < max_volue:
        
        res, vol = get_one_text_for_each_date(sphere_set)
        #print(res)
        #print(current_volue)
        result_set+=res.copy()
        current_volue += vol
        sphere_set = [item for item in sphere_set if item not in result_set]
        if vol == 0:
            #print('aaaa',sphere_name)
            break
            
    return current_volue, result_set
            
            
            
            




spheres = { 
'Художественная': 40000000,
'Мемуары':11000000, 
'Публицистика':29000000,
'Учебно-научная':12000000, 
'Офиц-деловая':1500000,
'Церковно-богословская':1500000, 
'Бытовая':3600000,
'Производственно-техн': 900000,
'Реклама': 500000
}








data = make_set_from_csv()
res_data = []
cur_vol = 0 
for sphere in spheres.keys():
    
    vol, res_set = get_sphere_for_corp(data, sphere, spheres[sphere])
    
    cur_vol+=vol
    #print(sphere.split(' | ')[0].lower().strip())
    #print(vol)
    res_data += res_set


with open('result.tsv', 'w') as tsvFile:
        fieldNames = res_data[0].keys()
        writer = csv.DictWriter(tsvFile, fieldnames=fieldNames, delimiter='\t')
        writer.writeheader()
        writer.writerows(res_data)
