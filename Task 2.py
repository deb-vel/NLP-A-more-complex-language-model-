import random
import pickle


#used to build both vanilla and unk models. The paramteres are the training set and the file names to pickle dictionaries into.
def nGramModels(trainingData, pickle_file_name1, pickle_file_name2, pickle_file_name3, pickle_file_name4, pickle_file_name5, pickle_file_name6):
    #declaring all the dictionaries to be used
    dictionary = {}  #will be used to store unigrams and their frequencies
    dictionary2 = {} #will be used to store bigrams and their frequencies
    dictionary3 = {} #will be used to store trigrams and their frequencies

    probabilityDict1 = {} #will store unigrams and their probabilities
    probabilityDict2 = {} #will store bigrams and their probabilities
    probabilityDict3 = {} #will store trigrams and their probabilities

    # -----FOR UNIGRAM------
    wordCount = 0 #will keep the total amount of words in corpus

    # loop through the whole 2D array sentence by sentence word by word
    for i in range(len(trainingData)):
        for j in range(len(trainingData[i])):
            wordCount += 1  # counts number of words in the corpus. Will be used to calculate the unigrams' probabilities
            if (trainingData[i][j] not in dictionary):  # if the unigram is unique
                dictionary[trainingData[i][j]] = 1 #add the word as a key to dictionary and give it the value of 1
            else:  # if unigram already met
                dictionary[trainingData[i][j]] += 1 #increase the key's value by one.  i.e the frequency of the unigram

    # loop through dictionary of unigrams and calculate probability of each
    for x in dictionary:
        probability = dictionary[x] / wordCount #frequncy of unigram x / total number of words
        probabilityDict1[x] = probability #add the unigram as a key to the dictionary of unigrams' probabilities and store the probability as its value



    # -----FOR BIGRAM------

    # loop through 2D array
    for i in range(len(trainingData)):
        w2 = 1  # Counter for the next word
        for j in range(len(trainingData[i])):
            currentWord = trainingData[i][j]  # take first word
            if (j < len(trainingData[i]) - 1):  # to make sure we do not access an index which does not exist
                nextWord = trainingData[i][w2]  # take the next word
            bigram = currentWord + " " + nextWord  # join the two words into one whole bigram

            if bigram not in dictionary2:  # if bigram not met yet
                dictionary2[bigram] = 1 #add the bigram as a key to dictionary and give it the value of 1
            else:  # if bigram already met
                # increment frequency
                dictionary2[bigram] += 1 #increase the key's value by one.  i.e the frequency of the bigram
            w2 += 1  # increment for next iteration

    # loop through all unique bigrams and calculate their probabilities
    for x in dictionary2:
        bigram = x
        splitted = bigram.split() #split the string at each space character
        probability = dictionary2[x] / dictionary[splitted[0]] #frequency of bigram/ frequency of the first word
        probabilityDict2[x] = probability #add bigram and its probability to the dictionary of bigrams' probabilities


    # ------FOR TRIGRAM------
    # loop through all 2D array
    for i in range(len(trainingData)):
        w2 = 1  # Set back to one when iterating through next row
        w3 = 2  # Set back to 2 when iterating through a new row
        for j in range(len(trainingData[i])):
            currentWord = trainingData[i][j]  # take first word
            if (j < len(trainingData[i]) - 2):  # to make sure we do not access an index which does not exist
                secondWord = trainingData[i][w2]  # take the second word
                thirdWord = trainingData[i][w3]  # take the third word
                trigram = currentWord + " " + secondWord + " " + thirdWord  # join all three words into one string

            if trigram not in dictionary3:  # if a new trigram is met
                dictionary3[trigram] = 1 #add trigram to the dictionary of trigrams and give it the value of 1
            else: #if trigram already exists in dictionary
                dictionary3[trigram] = +1 #increment the trigram's frequency
            w2 += 1  # increment for next iteration
            w3 += 1

    # loops through dictionary of trigrams and calculate the probabilities
    for x in dictionary3:
        trigram = x
        splitted = trigram.split() #split the string into 3 separate words
        bigram = splitted[0] + " " + splitted[1] #combine first and second words together
        probability = dictionary3[x] / dictionary2[bigram] #frequency of trigram/ frequency of first two words
        probabilityDict3[x] = probability #add trigram and its probability to the dictionary of trigrams' probabilities


    #pickle all the dictionaries used above to their rispective .pickle file
    pickle_dict1 = open(pickle_file_name1, "wb")
    pickle.dump(dictionary, pickle_dict1)
    pickle_dict1.close()

    pickle_dict2 = open(pickle_file_name2, "wb")
    pickle.dump(dictionary2, pickle_dict2)
    pickle_dict2.close()

    pickle_dict3 = open(pickle_file_name3, "wb")
    pickle.dump(dictionary3, pickle_dict3)
    pickle_dict3.close()

    pickle_prob = open(pickle_file_name4, "wb")
    pickle.dump(probabilityDict1, pickle_prob)
    pickle_prob.close()

    pickle_prob = open(pickle_file_name5, "wb")
    pickle.dump(probabilityDict2, pickle_prob)
    pickle_prob.close()

    pickle_prob = open(pickle_file_name6, "wb")
    pickle.dump(probabilityDict3, pickle_prob)
    pickle_prob.close()




def linearInterpolation(): #computes linear interpolation

    #load dictionary of unigram probabilities of the unk model
    pickle_in1 = open("unk_prob_dict1.pickle", "rb")
    probabilityDict1 = pickle.load(pickle_in1)

    # load dictionary of bigrams' probabilities of the unk model
    pickle_in1 = open("unk_prob_dict2.pickle", "rb")
    probabilityDict2 = pickle.load(pickle_in1)

    # load dictionary of trigrams' probabilities of the unk model
    pickle_in1 = open("unk_prob_dict3.pickle", "rb")
    probabilityDict3 = pickle.load(pickle_in1)

    # loops through dictionary of trigrams and calculates probabilities
    for x in probabilityDict3:
        trigram = x
        splitted = trigram.split() #split the string into 3 separate words
        bigram = splitted[1] + " " + splitted[2] #connect first two words as a bigram
        probability = 0.6* probabilityDict3[x] + 0.3* probabilityDict2[bigram] + 0.1 * probabilityDict1[splitted[2]] #implements the linear interpolation formula using the given weights
        probabilityDict3[x] = probability #overwite the old value with the new calculated probability

    #pickle the updated trigrams' probability dictionary
    pickle_dict1 = open("unk_prob_dict3.pickle", "wb")
    pickle.dump(probabilityDict3, pickle_dict1)
    pickle_dict1.close()


#this function caters for getting the n-grams which start with particular word/s
def getGrams(word, dict, number):

    shannonDict = {} #will store all n-grams that start with the string passed as parameter

    if number == 1: #if only first word needs to be matched with the first word of all n-grams
        for y in dict: #for all n-grams in their rispective dictionary
            splitted = y.split() #split it
            if word == splitted[0]: #if the first word of n-gram matches the word passed as parameter
                shannonDict[y] = dict[y] #add the n-gram to the shannonDict dictionary

    else: #if the first two words of each n-gram need to be matched with the passed string
        for y in dict: #for all n-grams in their rispective dictionary
            splitted = y.split() #split it
            if word == splitted[0] +" "+splitted[1]: #if the string matches the concatenated splitted words
                shannonDict[y] = dict[y] #add the n-gram to the shannonDict dictionary

    return shannonDict #return the dictionary containing all n-grams that start with particular word/s


#generates sentences using bigrams and trigrams.  The vanilla model is used for generating sentences
def generateFromBiorTri(firstWord, dict, number):

    sentence_generation1 = [] #will store the sentence being generated
    word = firstWord #word will be used as the string to be passed to the getGrams function
    word2 = word #word2 variable will be used to append the last word of the n-gram to the array sentence_generation
    coin = [0,1]

    #load the vanilla bigrams probabilities
    pickle_in2 = open('vanilla_prob_dict2.pickle', "rb")
    bi_dict = pickle.load(pickle_in2)

    if number == 2: #we're going to generate from trigrams and we need to first get a bigram
        ngram = getGrams(word, bi_dict, 1) #get the bigrams that start with the word passed, and pass '1' to indicate that we're going to search for bigrams
        ngrams = random.choice(list(ngram.keys())) #choose a bigram randomly from the dictionary of bigrams we got
        words = ngrams.split() #split into 2 separate words
        word = words[0]+" "+words[1] #conactenate
        word2 = word


    while word != "." or word != "!" or word != "?": #loop while no punctuation that denote end of sentence is met.
        sentence_generation1.append(word2)  #append the found string to the previous strings to eventually form a sentence
        ngram = getGrams(word, dict, number) #get the n=grams that start with the word passed, and pass number which will indicate if we're going to search for bigrams or trigrams
        oneor0 = random.choice(coin) #choose a random number from the set containing 1 and 0
        if oneor0 == 1: #if 1 is chosen, choose an n-gram from the dictionary by using roulette selection
            max = sum(ngram.values()) #sum of all probabilities
            pick = random.uniform(0, max) #pick a random number from 0 to max
            current = 0
            for key, value in ngram.items(): #for all keys and values in dictionary
                current += value #add the value to current
                if current > pick:
                    words = key.split() #split the key
                    word2 = words[number]  #word2 to be appended to the array sentence_generation1.  This way the sentence will be built up word by word iteration after the other
                    if number == 1: #if generating from bigrams
                        word = words[number] #set word equal to the last word in bigram. Next iteration this word will be used to get the n-grams that start with it
                    else: #if generating from trigrams
                        word = words[1]+ " "+words[number] #set word equal to the last two words in trigram
        else: #if 0 is randomly chosen, randomly choose a key from the dictionary
            ngrams = random.choice(list(ngram.keys())) #chooses a random n-gram from the dictionary of n-grams
            words = ngrams.split()
            word2 = words[number] #set it to the last word i.e either at index 1 (for bigrams) or at index 2 (for trigrams)
            if number == 1: #if generating from bigrams
                word = words[number]
            else: #if generating from trigrams
                word = words[1]+ " "+words[number]

        if words[number] == "." or words[number] == "!" or words[number] == "?": #break the loop if this condition is met
            sentence_generation1.append(word2) #append the ending punctuation (i.e . or ! or ?) to the array of words
            break

    print(*sentence_generation1) #print the sentence generated


def generateModel(firstWord, dict1, dict2, dict3):

    #stores the built sentence word  by word
    sentence_generation = []

    #load the necessary .pickle files which contain the needed dictionaries
    pickle_in1 = open(dict1, "rb")
    uni_dict = pickle.load(pickle_in1)

    pickle_in2 = open(dict2, "rb")
    bi_dict = pickle.load(pickle_in2)

    pickle_in3 = open(dict3, "rb")
    tri_dict = pickle.load(pickle_in3)


    word =firstWord

    # ----------SENTENCE GENERATION USING UNIGRAMS-----------
    sentence_generation.append(word) #append first word

    #implements the roulette selection method.
    max = sum(uni_dict.values()) #sum of all unigrams' probabilities
    pick = random.uniform(0, max) #pick a random number between 0 and the max
    current = 0
    for key, value in uni_dict.items(): #loop through dictionary of unigrams
        current += value #add the value of the particular key we're on in the loop
        if current > pick: #if current is grater than the random picked number
            word = key
            sentence_generation.append(key) #append the word to the array of words
        if word == '.' or word =='!' or word == '?': #if the sentence has ended break the loop
            break

    sentence_generation.append(word)#appends last ending punctuation
    print("Sentence generation using Unigrams: ")
    print(*sentence_generation) #print the sentence

    # call the method that generates sentences from bigrams or trigrams
    print("\nSentence generation using Bigrams: ")
    generateFromBiorTri(firstWord, bi_dict, 1) #pass the bigram dictionary and the number 1 to generate sentences from bigrams
    print("\nSentence generation using Trigrams: ")
    generateFromBiorTri(firstWord, tri_dict,2) #ass the trigram dictionary and the number 2 to generate sentences from trigrams


#computes probabilities of sentences in the test set
def check_sentence(testingData, dictionary1, dictionary2, dictionary3):

    #load the necessary dictionaries
    pickle_in1 = open(dictionary1, "rb")
    uni_dict = pickle.load(pickle_in1)

    pickle_in3 = open(dictionary2, "rb")
    bi_dict = pickle.load(pickle_in3)

    pickle_in2 = open(dictionary3, "rb")
    tri_dict = pickle.load(pickle_in2)

    sentence = []

    # loop through all 2D array element by element i.e word by word
    for i in range(len(testingData)):
        if i != 0: #if not in the first row i.e first sentence, print the probabilities calculated in the previous iteration
            print("Sentenza: ")
            print(*sentence) #print sentence
            print("Probability using unigrams: ",totalProbability1)
            print("Probability using bigrams: ", totalProbability2)
            print("Probability using trigrams: ", totalProbability3)

        #Declare and initialize variable to store the total probability of each n-gram.  set them all to 1
        totalProbability1 = 1
        totalProbability2 =1
        totalProbability3 = 1
        w2 = 1  # Set back to one when iterating through next row
        w3 = 2  # Set back to 2 when iterating through a new row
        sentence =[] #set it back to an empty array to store the next sentence

        for j in range(len(testingData[i])): #loop through row

            currentWord = testingData[i][j]  # take first word
            sentence.append(testingData[i][j]) #stores the sentence (word by word) whose probability is being calculated.

            if (j < len(testingData[i]) - 2):  # to make sure we do not access an index which does not exist
                secondWord = testingData[i][w2]  # take the next word
                thirdWord = testingData[i][w3]  # take the third word


            if dictionary3 == "vanilla_prob_dict3.pickle": #if the probabilities are being calculated onthe vanilla model
                trigram = currentWord + " " + secondWord + " " + thirdWord # join all three words into one string
                bigram = currentWord + " " + secondWord  #join two words into one string

                if currentWord in uni_dict: #if the unigram exists in the dictionary
                    uni_probability = uni_dict.get(currentWord) #get its value
                    totalProbability1 = totalProbability1 * uni_probability #multiply it  by the previous total probability
                else: #if unigram is not in dictionary
                    totalProbability1 = totalProbability1 * 0 #multiply by zero

                if bigram in bi_dict: #if the bigram exists in the dictionary
                    bi_probability = bi_dict.get(bigram) #get its value
                    totalProbability2 = totalProbability2 * bi_probability #multiply it  by the previous total probability
                else:
                    totalProbability2 = totalProbability2 * 0 #Multiply by 0

                if trigram in tri_dict: #if the bigram exists in the dictionary
                    tri_probability = tri_dict.get(trigram) #get its value
                    totalProbability3 = totalProbability3 * tri_probability #multiply it  by the previous total probability
                else:
                    totalProbability3 = totalProbability3 * 0 #multiply by 0
            else: #if the UNK model is being used

                if currentWord not in uni_dict: #if the current word doesn't exist in training set
                    currentWord = '<UNK>' #set it to unk
                if secondWord not in uni_dict: #if the second word doesn't exist in training set
                    secondWord = '<UNK>' #set it to unk
                if thirdWord not in uni_dict: #if the third word doesn't exist in training set
                    thirdWord = '<UNK>' #set it to unk

                #concatenate words into bigram or trigram accordingly
                bigram = currentWord +" "+ secondWord
                trigram = currentWord + " " + secondWord + " " + thirdWord

                #------FOR UNIGRAMS------
                uni_probability = uni_dict.get(currentWord) #get probability
                totalProbability1 = totalProbability1 * uni_probability #multiply the probability to the total one

                if bigram in bi_dict: #if bigram exists in dict
                    bi_probability = bi_dict.get(bigram) #get value
                    totalProbability2 = totalProbability2 * bi_probability #multiply value by total probability
                else: #if the sequence is not in dictionary
                    totalProbability2 = totalProbability2 * 0 #multiply by zero

                if trigram in tri_dict: #if trigram in dictionary
                    tri_probability = tri_dict.get(trigram) #get the value
                    totalProbability3 = totalProbability3 * tri_probability #multiply value with the total probability
                else: #if trigram not in dictionary
                    totalProbability3 = totalProbability3 * 0 #multiply by 0

            # increment for next iteration
            w2 += 1
            w3 += 1






#-----MAIN-----

with open('malti03.academic.1.txt', 'r') as file:
    # gets first word from each line in text file and decode it using utf8 to recognize maltese characters
    wordlist = [line.encode("windows-1252").decode('utf8').split(None, 1)[0] for line in file]

sentences = []  # stores all sentences


# this creates a 2D array of sentences
for i, word in enumerate(wordlist):
    if word == '<s':
        sentence = []
        index = i + 1
        while wordlist[index] != '</s>':  # start getting the sentence word by word till it meets end of sentence
            sentence.append(wordlist[index])  # append current word
            index += 1  # to access next word
        sentences.append(sentence)  # append to a 2D array of sentences

random.shuffle(sentences)  # randomly shuffle sentences in array
trainingData = sentences[0:round((80 / 100) * len(sentences))]  # get the first 80 percent
testingData = sentences[round((80 / 100) * len(sentences)):len(sentences)]  # get the rest

#the below variables store the .pickle file names used for the vanilla model
vanilla_pickle_file_name1 = 'vanilla_dict1.pickle'
vanilla_pickle_file_name2 = 'vanilla_dict2.pickle'
vanilla_pickle_file_name3 = 'vanilla_dict3.pickle'
vanilla_pickle_file_name4 = 'vanilla_prob_dict1.pickle'
vanilla_pickle_file_name5 = 'vanilla_prob_dict2.pickle'
vanilla_pickle_file_name6 = 'vanilla_prob_dict3.pickle'

#call this function to build the vanilla model, passing training set and the file names to  be able to pickle the dictionaries in the right files
nGramModels(trainingData, vanilla_pickle_file_name1, vanilla_pickle_file_name2, vanilla_pickle_file_name3, vanilla_pickle_file_name4, vanilla_pickle_file_name5, vanilla_pickle_file_name6)


#--------------TASK 2 A MORE COMPLEX LANGUAGE MODEL-----------------

#load the unigram dictionary stored in the previous task by using pickle
pickle_in1 = open("vanilla_dict1.pickle","rb")
dictionary1 = pickle.load(pickle_in1)

#loop through training set
for i in range(len(trainingData)):
    for j in range(len(trainingData[i])):
        word = trainingData[i][j]
        frequency = dictionary1[word] #get the unigram's frequency
        if frequency == 1: #if frequency is one chenge the word into a <UNK> word
            trainingData[i][j] = '<UNK>'

#the below variables store the .pickle file names used for the UNK model
unk_pickle_file_name1 = 'unk_dict1.pickle'
unk_pickle_file_name2 = 'unk_dict2.pickle'
unk_pickle_file_name3 = 'unk_dict3.pickle'
unk_pickle_file_name4 = 'unk_prob_dict1.pickle'
unk_pickle_file_name5 = 'unk_prob_dict2.pickle'
unk_pickle_file_name6 = 'unk_prob_dict3.pickle'

#call this function to build the UNK Model, passing the training set containing <UNK> tokens, and the file names to be able to pickle the dictionaries in the right files
nGramModels(trainingData, unk_pickle_file_name1, unk_pickle_file_name2, unk_pickle_file_name3, unk_pickle_file_name4, unk_pickle_file_name5, unk_pickle_file_name6)
#call the below method to perform linear interpolation
linearInterpolation()


#prompts the user to input a word to generate a sentence from
word = input("Enter a word as a start of sentence: ")
#this function is used to generate the sentences using the vanilla mode. three sentences should be generated, one from unigrams, one from bigrams and one from trigrams
generateModel(word, vanilla_pickle_file_name4, vanilla_pickle_file_name5, vanilla_pickle_file_name6)


print("\n\n\n\n\n------------PROBABILITIES OF SENTENCES ON THE VANILLA MODEL------------")
check_sentence(testingData, vanilla_pickle_file_name4, vanilla_pickle_file_name5, vanilla_pickle_file_name6)#calcultaes the probabilities of the sentences on the test set, using vanilla model
print("\n\n\n\n\n------------PROBABILITIES OF SENTENCES ON THE <UNK> MODEL------------")
check_sentence(testingData, unk_pickle_file_name4, unk_pickle_file_name5, unk_pickle_file_name6) #calcultaes the probabilities of the sentences on the test set, using UNK model


input("Press enter to exit")  # keeps cmd window open