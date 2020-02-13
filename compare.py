import csv

fileone = []
filetwo = []
output_ = []
output_fileone = []
output_filetwo = []
initial = False

try:
    myfile = open('cur_website.csv', 'r', encoding='UTF-8', errors='ignore', newline='')
    with myfile as t1:
        reader1 = csv.reader(t1)
        fileone = list(reader1)
except FileNotFoundError:
    initial =  True

with open('output.csv', 'r', encoding='UTF-8', errors='ignore', newline='') as t2:
    reader2 = csv.reader(t2)
    filetwo = list(reader2)


with open('to_test.csv', 'w') as outFile:
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
                            print('a')
                        elif fileone[i][2] != filetwo[x][2]:
                            writer.writerow(filetwo[x] + ['','','','','','','','',''] + ['UPDATE']) #type off
                            print('b')
                        elif fileone[i][3] != filetwo[x][3]:
                            writer.writerow(filetwo[x] + ['','','','','','','','',''] + ['UPDATE']) #display off
                            print('c')
                        else:
                            writer.writerow(filetwo[x] + ['','','','','','','','','']  + ['']) #everything same
                        x += 1
                        i += 1
                    elif test_text_1 != test_text_2:
                        writer.writerow(filetwo[x] + ['','','','','','','','',''] + ['UPDATE']) #text off
                        print("e")
                        x += 1
                        i += 1
                
            if x < len(filetwo):
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

