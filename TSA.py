import re
import csv
from sklearn import svm
def Dictionary():
        d={}
        with open("affective_lexicon.tsv","r",encoding="utf8") as f:
            next(f)
            reader = csv.reader(f,delimiter='\t')
            for line in reader:
                    key = line[0]
                    value= line[1]
                    d[key]= value

        return d

lexicon = Dictionary()


def extract_tweet_sentiments(fname): #we return whichever features we want
    def mean(numbers):
        return float(sum((list(map(float,numbers))))) / max(len(numbers), 1)


    def num_tweets(f_name):
        i = 0
        with open(f_name) as f:
            for line in f:
                i+=1 # number of lines
        return i;

    tweet_num = (num_tweets(fname));

    def word_number(f_name):
        with open(f_name) as f:
            j = 0
            for line in f:
                for word in line.split():
                    j+=1
        return j

    tweet_word_number = word_number(fname)

    tweet_words =[[] for _ in range(tweet_num)]
    def word_append(f_name):
        with open(f_name) as f:
            i = 0
            for line in f:
                for word in line.split():
                    tweet_words[i].append(word)
                i+=1
        return 0

    word_append(fname)

    def emoj_finder(f_name):
        eyes, noses, happy = r":;8BX=", r"-~'^", r")DP"
        neutral = r"|"
        sad = r"(/\ "

        list =[[] for _ in range(tweet_num)] # i is #tweets and j = 0 #happy, 1 = #neutral , 2 #sad

        pattern0 = "[%s][%s]?[%s]" % tuple(map(re.escape, [eyes, noses, happy])) # happy pattern
        pattern1 = "[%s][%s]?[%s]" % tuple(map(re.escape, [eyes, noses, neutral])) #neutral pattern
        pattern2 = "[%s][%s]?[%s]" % tuple(map(re.escape, [eyes, noses, sad])) #sad pattern
        i = 0
        with open(f_name) as f:
            for line in f:
                list[i].append(len(re.findall(pattern0, line))/len(tweet_words[i]))
                list[i].append(len(re.findall(pattern1, line))/len(tweet_words[i]))
                list[i].append(len(re.findall(pattern2, line))/len(tweet_words[i]))
                i+=1 # number of lines
        #print(list)
        return list

    tweet_emjs = emoj_finder(fname)

    def punctuation_finder(f_name):
        list = [None]*tweet_num
        i = 0
        pattern = r'[.?\-!",]+'
        with open(fname) as f:
            for line in f:
                list[i] = len(re.findall(pattern, line))/len(tweet_words[i])#punctuation
                i+=1
        return list

    tweet_punct=punctuation_finder(fname)

    def all_upper_finder(f_name):
        list = [None]*tweet_num
        i = 0
        pattern = r'[A-Z]+'
        with open(f_name) as f:
            for line in f:
                list[i] = len(re.findall(pattern, line))/len(tweet_words[i])#all upper
                i+=1
        return list

    tweet_upper = all_upper_finder(fname)

    def hashtag_finder(f_name):
        list = [None]*tweet_num
        i = 0
        pattern = r'[#]+'#r'?<=^|(?<=[^a-zA-Z0-9-_\.]))#([A-Za-z]+[A-Za-z0-9]+'
        with open(f_name) as f:
            for line in f:
                list[i] = len(re.findall(pattern, line))/len(tweet_words[i])
                i+=1
        return list

    tweet_hashes = hashtag_finder(fname)

    def rep_finder(f_name):
        list = [None]*tweet_num
        i = 0
        pattern = r'(\w)\1*?'
        with open(f_name) as f:
            for line in f:
                list[i] = len(re.findall(pattern, line))/len(tweet_words[i])
                i+=1
        return list

    tweet_reps = rep_finder(fname)


    def url_finder(f_name):
        list = [None]*tweet_num
        i = 0
        pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        with open(fname) as f:
            for line in f:
                list[i] = len(re.findall(pattern, line))/len(tweet_words[i])
                i+=1
        return list

    tweet_urls = url_finder(fname)

    def mention_finder(f_name):
        list = [None]*tweet_num
        i = 0
        pattern = r'[@]+'
        with open(f_name) as f:
            for line in f:
                list[i] = len(re.findall(pattern, line))/len(tweet_words[i])#all upper
                i+=1
        return list

    tweet_mentions = mention_finder(fname)
    def word_sentiment(f_name):
            list = [[] for _ in range(tweet_num)] #sentiment list for each tweet
            i = 0 #tweet index
            fail = 0 # number of failures
            with open(f_name) as f:
                line_list=[]
                for line in f:
                    for word in line.split():
                        word = word.lower() #remove lowercase and all previous expressions
                        word = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', "",word)
                        word = re.sub(r'[:)(;|/\.?\-!~^",]+', "",word)
                        line_list.append(word)
                    for j in range(0,len(line_list)-2):
                        try:
                            try:
                                arg = [line_list[j]," ",(line_list[j+1])] #here we are just formatting the argument
                                arg = ''.join(arg)                        #and find its lexicon value
                                value = lexicon[arg]
                                list[i].append(value)
                            except KeyError:
                                if(j==len(line)-3):
                                    list[i].append(lexicon[line_list[j+2]]) # this is the last word
                                list[i].append(lexicon[line_list[j]])       #this is the word which didn't pair with the one after it
                        except KeyError:
                            fail+=1
                            continue
                    i+=1
                    del line_list[:]
            return list


    tweet_word_sentiments = word_sentiment(fname)

#tweet statistics extraction
    tweet_statistics = [[]for _ in range(0,tweet_num)]
    for i in range(0,tweet_num):
            tweet_statistics[i].append(mean(tweet_word_sentiments[i]))# mean
            tweet_statistics[i].append(min(list(map(float,tweet_word_sentiments[i]))))# min
            tweet_statistics[i].append(max((list(map(float,tweet_word_sentiments[i])))))# max
            tweet_statistics[i].extend((tweet_mentions[i],tweet_urls[i],tweet_reps[i],tweet_punct[i],tweet_hashes[i],tweet_reps[i]))
    return tweet_statistics






##############################################################
##################Classification of Tweets####################
##############################################################

def target(fname):
    target_data = []*len(tweet_statistics)
    with open(fname) as f:
        for line in f:
            for word in line.split():
                    target_data.append(word)

    return target_data

tweet_statistics = extract_tweet_sentiments("train.txt")
print(tweet_statistics)
test_statistics = extract_tweet_sentiments("test.txt")
target_data = target("train.sen")
#print(target_data)
clf = svm.SVC(kernel='linear')
clf.fit(tweet_statistics[:-1], target_data[:-1])
print(clf.predict(test_statistics[1:10]))
