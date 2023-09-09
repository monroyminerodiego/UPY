#Function created to read a '.txt' file
def display_txt(file):
    #open the file
    with open(file) as f:
        contents = f.read()
    print(contents+'\n')

#Function created to count the number of lines from a '.txt' file which is not starting with an alphabet 'T'
def count_lines_T(file,letter):
    #open the file
    with open(file) as f:
        body = list(f.readlines())
    #Create a new list to store the lines that doesn't start with 'letter'
    lines = []
    #Loop to evaluate if the line starts without the given letter 
    for i in body:
        if i[0].upper() != letter.upper():
            lines.append(i[0:-1])
    print(f"There are {len(lines)} lines that doesn't start with letter '{letter}' in the {file} file, and these are {lines}")

#Function created to count the words of a '.txt' file
def count_letters(file):
    #open the file
    with open(file) as f:
        body = list(f.readlines())
    lines = []
    for i in body:
        i = i.replace('\n','')
        i = i.replace(',','')
        lines.append(i)
    words = []
    for i in range(len(lines)):
        element = lines[i]
        element = element.replace(' ',',')
        temp_words = element.split(',')
        for i in temp_words:
            words.append(i)
    print(f"There are {len(words)} words in {file} and those are: {words}")

#Function created to count the number of apparition of a word in a '.txt' file
def count_words(file, word):
    #open the file
    with open(file) as f:
        body = list(f.readlines())
    lines = []
    for i in body:
        i = i.replace('\n','')
        i = i.replace(',','')
        lines.append(i)
    count = 0
    for i in range(len(lines)):
        element = lines[i]
        element = element.replace(' ',',')
        temp_words = element.split(',')
        for i in temp_words:
            if i.lower() == word.lower():
                count += 1
    print(f"The word '{word}' appears {count} times in {file}")

print('Example 1')
display_txt('story.txt')

print('\nExample 2')
count_lines_T('story.txt','T')

print('\nExample 3')
count_letters('story.txt')

print('\nExample 4')
count_words('story.txt','The')