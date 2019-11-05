import csv

fileone = []
filetwo = []
output_ = []
output_fileone = []
output_filetwo = []
with open('website.csv', 'r', encoding='UTF-8', errors='ignore', newline='') as t1:
    reader1 = csv.reader(t1)
    fileone = list(reader1)
    #print(fileone[0])

with open('out.csv', 'r', encoding='UTF-8', errors='ignore', newline='') as t2:
    reader2 = csv.reader(t2)
    filetwo = list(reader2)


with open('test_output.csv', 'w') as outFile:
    writer = csv.writer(outFile, lineterminator='\n')
    writer.writerow(fileone[0] + ['Website Change'])

    i = 1
    x = 1
    missed_one = []
    missed_two = []
    flag = True
    flag2 = True
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
                    writer.writerow(filetwo[x] + ['','','','','','','','',''] + ['INSERT'])
                    missed_two.append(x)
                    x += 1
                    continue
                elif test_text_1 == test_text_2:
                    if set(fileone[i][11]) != set(filetwo[x][11]):
                        writer.writerow(filetwo[x] + ['','','','','','','','',''] + ['UPDATE']) #tags off
                    elif fileone[i][2] != filetwo[x][2]:
                        writer.writerow(filetwo[x] + ['','','','','','','','',''] + ['UPDATE']) #type off
                    elif fileone[i][3] != filetwo[x][3]:
                        writer.writerow(filetwo[x] + ['','','','','','','','',''] + ['UPDATE']) #display off
                    else:
                        writer.writerow(filetwo[x] + ['','','','','','','','','']  + ['UPDATE']) #everything same
                    x += 1
                    i += 1
                elif test_text_1 != test_text_2:
                    writer.writerow(filetwo[x] + ['','','','','','','','',''] + ['UPDATE']) #text off
                    x += 1
                    i += 1
            
        if x < len(filetwo):
            if filetwo[x][6] not in levels1:
                flag2 = False
                writer.writerow(filetwo[x] + ['','','','','','','','',''] + ['INSERT']) #only on drupal
                missed_two.append(x)
                x += 1
                continue
        else:
            break   
        


#with open('test_output.csv', 'w') as outFile:

        
# with open(input_file1) as first:

#     with open(input_file2, newline='\n') as second:
#         read1 = csv.reader(first)
#         print(read1)
#         i = 0

#         read2 = csv.reader(second)
#         x = 0

#         diff_rows = []
#         while i < frist_len or x < second_len:
#             if read1[i] == read2[x]:
#                 i += 1
#                 x += 1
#             elif read1[i] == read2[x+1]:
#                 diff_rows += (x, read2[x])
#                 x += 1
#             elif read1[i+1] == read2[x]:
#                 diff_rows += (i, read1[i])
#                 i += 1
#             else:
#                 diff_rows += (i, read1[i])
#                 diff_rows += (2, read2[x])
#                 i += 1
#                 x += 1
    
# with open(output_path, 'w') as fout:
#     writer = csv.writer(fout)
#     writer.writerows(diff_rows)