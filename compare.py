import csv
import datetime

fileone = []
filetwo = []
output_ = []
output_fileone = []
output_filetwo = []
initial = False

try:
    myfile = open('old_site.csv', 'r', encoding='UTF-8', errors='ignore', newline='')
    with myfile as t1:
        reader1 = csv.reader(t1)
        fileone = list(reader1)
except FileNotFoundError:
    initial =  True

with open('website_data.csv', 'r', encoding='UTF-8', errors='ignore', newline='') as t2:
    reader2 = csv.reader(t2)
    filetwo = list(reader2)

x = datetime.datetime.now()
ret_name = 'upload_' + x.strftime("%Y") + '_' + x.strftime("%m") + '_' + x.strftime("%d") + '.csv'
print(ret_name)
with open(ret_name, 'w') as outFile:
    writer = csv.writer(outFile, lineterminator='\n')
    writer.writerow(filetwo[0] + ['Website Change'])

    i = 1
    x = 1
    missed_one = []
    missed_two = []
    flag = True
    flag2 = True

    if (not initial):
        levels1 = [x[6] for x in fileone]
        levels2 = [x[6] for x in filetwo]

        while True:
            if i < len(fileone):
                if fileone[i][6] not in levels2:
                    writer.writerow(fileone[i] + ['DELETE']) #only on drupal
                    missed_one.append(i)
                    i += 1
                    continue
                elif x < len(filetwo):
                    test_text_1 = fileone[i][7].replace(' ', '')
                    test_text_2 = filetwo[x][7].replace(' ', '')
                    if filetwo[x][6] not in levels1:
                        writer.writerow(filetwo[x] + ['','','','','','','','',''] + ['ADD'])
                        missed_two.append(x)
                        x += 1
                        continue
                    elif test_text_1 == test_text_2:
                        if set(fileone[i][12]) != set(filetwo[x][12]):
                            writer.writerow(filetwo[x] + ['','','','','','','','',''] + ['UPDATE']) #tags off

                        elif fileone[i][2] != filetwo[x][2]:
                            writer.writerow(filetwo[x] + ['','','','','','','','',''] + ['UPDATE']) #type off
               
                        elif fileone[i][3] != filetwo[x][3]:
                            writer.writerow(filetwo[x] + ['','','','','','','','',''] + ['UPDATE']) #display off
                       
                        else:
                            writer.writerow(filetwo[x] + ['','','','','','','','','']  + ['']) #everything same
                        x += 1
                        i += 1
                    elif test_text_1 != test_text_2:
                        writer.writerow(filetwo[x] + ['','','','','','','','',''] + ['UPDATE']) #text off
         
                        x += 1
                        i += 1
                
            elif x < len(filetwo):
                if filetwo[x][6] not in levels1:
                    flag2 = False
                    writer.writerow(filetwo[x] + ['','','','','','','','',''] + ['ADD']) #only on drupal
                    missed_two.append(x)
                    x += 1
                    continue
            else:
                break

    else: 
        while True:
            if x < len(filetwo):
                writer.writerow(filetwo[x] + ['','','','','','','','',''] + ['ADD']) #only on drupal
                x += 1
                continue
            else:
                break

