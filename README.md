# NLP-A-more-complex-language-model-
NLP Text Assignment, Task 2 (2018-2019)
# Changes in Task 1 – Vanilla Language Model
In the first task I submitted, I used arrays to store everything that was needed such as all frequencies and all n-grams. Before I implemented task 2, I decided to change the previous code to make use of dictionaries instead of arrays, this should make it more efficient and a less complicated code. I created three dictionaries to store unigrams, bigrams, and trigrams, as keys and the frequencies as their values. I created three more dictionaries containing the same mentioned keys, but this time the values are the probabilities of the n-grams. I also made use of pickle, to save the dictionaries and load them whenever they are needed. Furthermore, in the last submission every time a probability was computed the information was printed on screen. In this task it was decided that nothing is printed on screen to save computational time and make the program faster.

# Task 2 Implementation
For this task I started by changing, the words in the training set which have a frequency of one, equal to a <UNK> token. Then I used the same function that builds the Vanilla Model, to this time build the UNK Model. I passed different ‘.pickle’ filenames from the ones used for the Vanilla Model, so that the UNK dictionaries are stored in new files. After the UNK model is built, linear interpolation was implemented on the trigrams of the UNK model only. The lambdas specified in the assignment description were used. The new trigram probabilities calculated in the linear interpolation, are overwritten over the original trigram probabilities in their respective dictionary.
When all of the above is done, the user gets prompted to type in a word to generate a sentence from. To generate sentences, I followed the Shannon Visualization Method. When generating by unigrams, the words are chosen randomly, and therefore, the sentence is often very long. When generating from bigrams and trigrams, I coded it in a way to choose the next n-gram, sometimes by a roulette wheel selection and sometimes by random selection. This allows a variety of n-grams to be selected instead of choosing just the ones with the highest probabilities.
Last but not least, the probabilities of sentences were calculated. To do so, the program loops through the test set, and uses its sentences to compute their probabilities. For each sentence, three probabilities were calculated, one by using unigrams, one by using bigrams and one by using trigrams. First the sentences are tested on the Vanilla model and then tested on the UNK model. All this information is outputted on screen.

# To Run
Double click on the RunMe.cmd file to run the program.
