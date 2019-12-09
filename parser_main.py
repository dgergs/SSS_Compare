#Things break when these aren't here. This is the first reason why you have to run ipython.
#This is also currently running python2.7 and needs to be updated for pip by January 2020. 
#from IPython import get_ipython
#get_ipython().system('pip install opml')


import csv
import opml
import re
import markdown

#md = markdown.markdown()

typenames = ["OVERVIEW","RESOURCES","CHAPTER","VIDEO","EXAMPLES", "EXAMPLES ","EXEMPLARY","CAUTIONARY","#ex.g","#ex.b","goals","ATTITUDES__","__ATTITUDES__","ACQUISITION__","ACQUISITION","APPLICATION__","APPLICATION","ELEMENTS","Readings","Clicker","Discussion","Exercises","Practice","ASSESSMENTS"]


"""
INSTRUCTIONS FOR USE as of 4/21/19

Assign OPML_filename (below) to whatever OPML file you are converting.
Assign desired_CSV_name to the name of the CSV you want to create.

On terminal (for my mac at least), run "ipython OPML_to_CSV.py" in the same directory your OPML file
A CSV will be written to the same directory
"""

OPML_filename = "dynalist.opml" #Make sure this is a string and ends .opml EX: "SSS_04_01_19.opml"
desired_CSV_name = "output.csv" #Make sure this ends .csv

def convert_to_CSV_help(curr_outline, current_topic="", numer="", current_type="", level_list=[], 
                        highest_level=True, nest="", h=0, sp2014=0, answer=0, pp=0, parent='', 
                        depth=0, parent_ht=[], grandparent_ht=[], topic_number=0, arabic=0):
    """ This function helps converts an OPML file to a CSV file. Adjust 
            the file names as necessary to the ones on your desktop. 
        curr_outline = current OPML frame
        current_topic = current topic 
        numer = Roman Numeral of current topic
        current_type = current type (Topic, Overview, etc)
        level_list = simple list of level nestings (big endian)
        highest_level = whether you are at the outermost level
        nest = record of the nested levels data was found (redundant of level_list)
        h, sp2014, answer, pp = default to 0, if included in the hashtags of the line, 1
        parent = name of parent to topic
        depth = current frame level depth
        parent_ht = list of hashtags that parents pass on to children 
        grandparent_ht = list of hashtags that grandparents pass on to children
        topic_number = Ordinal number of topic/data bein looked at
        arabic = 1 if it's child has numbering, 0 if bullets
    
    """

    global line_number
    global declared_refs
    references = []
    dec_refers = []
    dec_refs = ''
    valid = True
    if len(curr_outline) == 0:
        return
    if highest_level:
        for i in range(6, 34): #this can be changed, this makes sure to only through topics as the dynalist is currently written
            startCSV = False
            usetext = curr_outline[i].text
            current_hashtags = [x for x in usetext.split() if x.startswith('#')]
            new_parent_ht = [ht for ht in current_hashtags if ht != '#L1' and ht != '#L2']

            if "#L1" in current_hashtags and len(current_hashtags) > 1: 
                new_topic = (usetext.split("**Topic"))[1].split("**")[0]
                new_numer = (''.join(new_topic.split()[0][:-1]))
                new_topic = (' '.join(new_topic.split()[1:]))   #Just use first words of topic name
                current_type = "Topic"
                startCSV = True
            else:
                new_topic = usetext
            new_nest = str(i-5)
            new_topic_number = i-5
            level_temp = level_list + [i]
            level_updated = level_temp + [-1, -1, -1, -1, -1, -1] #setting up the last columns of the CSV
            
            refs = ''
            for htag in current_hashtags: #adding specific flags for certain hashtags
                if "#h"== htag:
                    h=1
                if "#SP2014" in current_hashtags:
                    sp2014=1
                if '#Answer' == htag or '#Answer:' == htag:
                    answer=1
                    pp=1
                if "#pp" == htag:
                    pp=1
                if "#as" == htag:
                    pp=1
                if re.match(r'(#[A-Z]{2}\.[A-Z]\.\d)', htag):
                    references += [htag]
                    
            refs = ', '.join(references)

            arabic_tag = 0 #taking care of lists being numbered/bulleted
            bullet = abs(arabic-1)
            try:
                if curr_outline[i].listStyle=='arabic':
                    arabic_tag = 1
            except AttributeError:
                pass

            if len(set(typenames).intersection(usetext.split()))==0: 
                for each_hashtag in current_hashtags:
                    usetext = usetext.replace(each_hashtag, "") #removing hashtags from usetext
                curr_hashtags = ', '.join(current_hashtags)
                newtext = re.sub(r'\*{2}([\S\s]+)\*{2}', r'<strong>\1</strong>', usetext)
                newtext = re.sub(r'\_{2}([\S\s]+)\_{2}', r'<strong>\1</strong>', newtext)

                if startCSV and valid: #actually writing to the CSV
                    writer.writerow(['', '', current_type, 'topic', '', '', new_nest, newtext, '', '', '', '']+ [curr_hashtags])
                    line_number += 1

            new_parent = usetext
            new_depth = len(curr_outline[i]) #recursive call
            convert_to_CSV_help(curr_outline[i], new_topic, new_numer, current_type, level_temp, False, 
                                nest=new_nest, parent=new_parent, 
                                depth=new_depth, parent_ht=new_parent_ht, grandparent_ht=parent_ht, 
                                topic_number=new_topic_number, arabic=arabic_tag) 
    else:   
        for i in range(len(curr_outline)): #iterate through current outline
            usetext = curr_outline[i].text
            current_hashtags = [x for x in usetext.split() if x.startswith('#')]
            new_parent_ht = [ht for ht in current_hashtags if ht != '#L1' and ht != '#L2']
            typeset = set(typenames).intersection(usetext.split(" "))
            if typeset: #converting a few tags
                current_type = list(typeset)[0]
                if current_type == '#ex.g':
                    current_type = 'Exemplary Quotes'
                elif current_type == '#ex.b':
                    current_type = 'Cautionary Quotes: Mistakes, Misconceptions, &amp; Misunderstanding'
                else:
                    current_type = re.sub(r'[^a-zA-Z,:& ]+', '', current_type)
                    current_type = current_type.lower().capitalize()


            new_nest = nest + '.' + str(i+1)
            new_topic_number = topic_number
            level_temp = level_list + [i]
            level_updated = level_temp + [-1, -1, -1, -1, -1, -1]
            
            display = '' #changing display values
            if len(nest) <= 2:
                display = 'h2'
            else:
                display = 'snippet'
            
            refs = ''
            ret_hash = []
            references = []
            dec_refers = []
            dec_refs = ''
            for idx in range(len(current_hashtags)):
                if re.match(r'(#[A-Z]{2}\.[A-Z]\.\d)', current_hashtags[idx]):
                    #print(current_hashtags[idx])
                    if "CONCEPT ACQUISITION" in parent:# or "CONCEPT APPLICATION" in parent or "ATTITUDES" in parent:
                        if current_hashtags[idx] not in declared_refs:
                            dec_refers += [current_hashtags[idx]]
                            declared_refs += [current_hashtags[idx]]
                            first = '#' + str(dec_refers[0])
                            valid=True
                            dec_refers = [first] + dec_refers[1:]
                            dec_refs = ', #'.join(dec_refers)
                            
                        else:
                            references += [current_hashtags[idx]]
                    else:
                        references += [current_hashtags[idx]]

                else:#adding hashtag flags
                    if "#h"== current_hashtags[idx]:
                        h=1
                    if "#SP2014"== current_hashtags[idx]:
                        sp2014=1
                    if '#Answer'== current_hashtags[idx] or '#Answer:' == current_hashtags[idx]:
                        answer=1
                        pp=1
                    if "#pp" == current_hashtags[idx]:
                        pp=1
                    if "#as" == current_hashtags[idx]:
                        pp=1
                    updated = re.sub(r'[^#a-zA-Z0-9\.]+', '', current_hashtags[idx])
                    ret_hash.append(updated)
                
            arabic_tag = 0 #taking care of types of lists
            bullet = abs(arabic-1)
            try:
                if curr_outline[i].listStyle=='arabic':
                    arabic_tag = 1
            except AttributeError:
                pass
                    
            refs = ', '.join(references)
            
            if len(typeset) == 1 or len(typeset) == 0 or len(typeset) == 2:
                    for each_hashtag in current_hashtags:
                        usetext = usetext.replace(each_hashtag, "")
                    newtext = re.sub(r'\*{2}([\S\s]+)\*{2}', r'<strong>\1</strong>', usetext)
                    newtext = re.sub(r'\_{2}([\S\s]+)\_{2}', r'<strong>\1</strong>', newtext)
                    steptext = re.sub(r'\&', '&amp;', newtext)
                    fintext = re.sub(r'\[([\S\s]+)\]\((http(\S)+)\)', r'<a href="\2">\1</a>', steptext)
                    print(usetext)
                    ret_parent_ht = list(set(parent_ht + grandparent_ht))
                    current_hashtags_lst = ret_hash + ret_parent_ht

                    curr_hashtags_prime = ', '.join(current_hashtags_lst)
                    curr_hashtags = ''
                    if dec_refs and refs: 
                        curr_hashtags = refs + ', ' + dec_refs + ', ' + curr_hashtags_prime
                    elif dec_refs:
                        curr_hashtags = dec_refs + ', ' + curr_hashtags_prime
                    elif refs:
                        curr_hashtags = refs + ', ' + curr_hashtags_prime
                    
                    else:
                        curr_hashtags = curr_hashtags_prime
                    #ret_hash_parent = ', '.join(ret_parent_ht)
                 
                    if valid: #writing to CSV
                        writer.writerow(['', '', current_type, display, '', '', new_nest, fintext, '', '', '', '']+ [curr_hashtags])
                    line_number += 1

            new_parent = usetext
            new_depth = len(curr_outline[i])
            convert_to_CSV_help(curr_outline[i], current_topic, numer, current_type, level_temp, False, 
                                new_nest, parent=new_parent, 
                                depth=new_depth, parent_ht=new_parent_ht, grandparent_ht=parent_ht, 
                                topic_number=new_topic_number, arabic=arabic_tag) 
    return



#The code to actually call the helper function, be careful putting this in it's own fuction. 
#I ran into issues with nonlocal variables so it's easiest to keep it in the global frame. 
OPML_outline = opml.parse(OPML_filename)
CSVfile = open(desired_CSV_name, 'w', errors='ignore', newline='')
writer = csv.writer(CSVfile)
writer.writerow(['(Numeral)', '(Current Topic)', 'Current Type', 'Display', '(Topic Number)', '(Ordinal Number)', 'Level', 'Text', '(#h)', '(#SP2014)', '(#Answer)', '(#pp)', 'Hashtags', '(Parent)', '(Number of Children)', '(Parent Hashtags)', '(Level 1)', '(Level 2)', '(Level 3)', '(Level 4)', '(Level 5)', '(Level 6)'])
line_number=2
declared_refs = []
#Sometimes you need to run the function below on "OPML_outline[0]" to make sure you're looking at the right outline...
convert_to_CSV_help(OPML_outline)
CSVfile.close()
