import re
import string

grimms = open("grimms.txt", "r")
sw_text = open("stopwords.txt", "r")

#accumulator for line numbers
line_num = 0
#list to store text
text = []
#dictionary to store the words
word_dic = {}
#list to store the stop words
stopwords = []
#variable to store current story title in loop
story_title = ""

story_title_line_numbers = [] 

#create a list of stopwords
for line in sw_text:
    word = line.strip()
    stopwords.append(word)
    
#iterate through fairy tales
for line in grimms:

    line = line.strip()

    #store current line number
    line_num = line_num + 1
    text.append(line)
    
    #make sure to only iterate through story text
    if(line_num > 124 and line_num < 9212):
        #regex to match titles     
        if(text[line_num-3] == '' and text[line_num-1] == ''):
            title = re.search(r'[A-Z]+[A-Z \,\[\]\-]+[A-Z \,\[\]\-]+[A-Z \,\[\]\-]+[A-Z \,\[\]\-]+[A-Z \,\[\]\-]+[A-Z \,\[\]\-]+', text[line_num-2])
            if(title):
                #store current story title in variable
                story_title = title.group()
                story_title_line_numbers.append(line_num-1)

        #split line into list of words
        if((line_num-2) not in story_title_line_numbers and line_num > 126):
            words = text[line_num-3].strip().split()

        #iterate through list of words
            for word in words:
                #convert words to lowercase and remove punctuation
                word = word.lower()
                word = word.strip(string.punctuation + string.whitespace)
                #if word isn't a stop word add it to dictionary
                if(word not in stopwords):
                    #add dictionary of story titles containing list of line numbers to dictionary of words
                    word_dic.setdefault(word, {}).setdefault(story_title,[]).append(line_num-2)




#check to see if word exists as key in the dictionary
def keys_exist(dic, words):
    for word in words:
        value = dic.get(word, 0)
        if value == 0:
            return False
    return True

#get a single word query
def get_output(dic, word):
    if (keys_exist(dic,words)):
        for item in dic[word]:
            print("     " + item)
            for line in dic[word][item]:
                output_line = text[line-1]
                output_line = output_line.replace(word, "**" + word.upper() + "**")
                print("      ", line, output_line)
    else:
        print("     --\n")

#get output for an or query
def get_output_or(dic, words):
    #make sure keys exist in dic
    if (keys_exist(dic,words)):

        titles = []
        #iterate through words list
        for i in range(0,2):
            if(dic.get(words[i]) != None):
                #iterate through stories
                for item in dic[words[i]]:
                    #add story to list of titles
                    if item not in titles:
                        print(item)
                        titles.append(item)
                        #print output
                        for num in range(0,2):            
                            #print output for when one word isn't in story
                            if dic.get(words[num]) == None:
                                print(words[num])
                                print("  --")
                            #print output for when word is in story
                            else:
                                if dic[words[num]].get(item) == None:
                                    print(words[num])
                                    print("  --")
                                else:
                                    print(words[num])
                                    for line in dic[words[num]][item]:
                                        output_line = text[line-1]
                                        output_line = output_line.replace(words[num], "**" + words[num].upper() + "**")
                                        print("      ", line, output_line)
    else:
        print("     --\n")

#get output for a query with multiple words
def get_output_and(dic, words):  
    if (keys_exist(dic,words)):
        #make a list of lists that contains the stories associated with each word
        story_list = []
        for i in range(0,len(words)):
            new_list = []
            for item in dic[words[i]]:
                new_list.append(item)
            story_list.append(new_list)

        #make a list of stories that contain all the words queried 
        output = []    
        for story in story_list[0]:
            for i in range(1, len(story_list)):
                if story in story_list[i]:
                    same = True
                else:
                    same = False
                    break
            if same and story not in output:
                output.append(story)

        #print out the output
        for item in output:
            print(item)
            for word in words:
                print(" ", word)
                for line in dic[word][item]:
                    output_line = text[line-1]
                    output_line = output_line.replace(word, "**" + word.upper() + "**")
                    print("      ", line, output_line)  
    else:
        print("     --\n")

#get output for morethan query
def get_output_morethan(dic, words):
    #make sure word is in dic
    value = dic.get(words[0], 0)    
    if value != 0:
        #iterate through stories with first search term
        for item in dic[words[0]]:
            counter = 0
            for line in dic[words[0]][item]:
                counter += 1
            #check for ints in second search term
            if(words[1] == "0" or
               words[1] == "1" or
               words[1] == "2" or
               words[1] == "3" or
               words[1] == "4" or
               words[1] == "5" or
               words[1] == "6" or
               words[1] == "7" or
               words[1] == "8" or
               words[1] == "9" or
               words[1] == "10"):
                morethan = int(words[1])
            #count uses of second search term if not an int
            else:
                word = dic.get(words[1]).get(item, 0)
                if(word == 0):
                    morethan = 0
                else:
                    morethan = 0
                    for line in dic[words[1]][item]:
                        morethan += 1              
            #print output if it meets morethan criteria
            if(counter > morethan):
                print("     " + item)
                for line in dic[words[0]][item]:
                    output_line = text[line-1]
                    output_line = output_line.replace(words[0], "**" + words[0].upper() + "**")
                    print("      ", line, output_line)
    else:
        print("     --\n")

def get_output_near(dic, words):
    if (keys_exist(dic,words)):

    #make a list of lists that contains the stories associated with each word
        story_list = []
        for i in range(0,len(words)):
            new_list = []
            for item in dic[words[i]]:
                new_list.append(item)
            story_list.append(new_list)

        #make a list of stories that contain all the words queried 
        output = []    
        for story in story_list[0]:
            for i in range(1, len(story_list)):
                if story in story_list[i]:
                    same = True
                else:
                    same = False
                    break
            if same and story not in output:
                output.append(story)

        #iterate through stories that have both words
        for item in output:

            #create list of lines with first search term
            line_list = []
            for line in dic[words[0]][item]:
                line_list.append(line)   

            #create list of line numbers that have both words in proximity
            output_list = []
            for line in dic[words[1]][item]:
                if(line in line_list):
                    output_list.append(line)
                elif((line-1) in line_list):
                    output_list.append(line)
                elif((line+1) in line_list):
                    output_list.append(line)

            #print output
            for line in output_list:    
                print(item)
                output_lines = text[line-2] + "\n " + str(line) + "      " + text[line-1] + "\n " + str(line+1) + "       "  + text[line]
                output_lines = output_lines.replace(words[0], "**" + words[0].upper() + "**")
                output_lines = output_lines.replace(words[1], "**" + words[1].upper() + "**")
                print("", line-1, "      ", output_lines)  

    #output when nothing matches query
    else:
        print("     --\n")

user_query = input("Please enter your query: ")

#loop that continually asks user for input until they quit
while(user_query != 'qquit'):
    print("query =", user_query)
    words = user_query.split()

    #identify which kind of query user is making it and get the right output  
    if(" or " in user_query):
        del words[1]
        get_output_or(word_dic, words)
    elif(len(words) == 1):
        get_output(word_dic, user_query)
    elif(" and " in user_query):
        del words[1]
        get_output_and(word_dic, words)
    elif(" morethan " in user_query):
        del words[1]
        get_output_morethan(word_dic, words)
    elif(" near " in user_query):
        del words[1]
        get_output_near(word_dic, words)
    elif(len(words) > 1):
        get_output_and(word_dic, words)
    
    user_query = input("Please enter your query: ")
    
#close the files
grimms.close()
sw_text.close()
