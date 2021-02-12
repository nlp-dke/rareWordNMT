
import sys, argparse


class Statistics:

    def __init__(self,source,prefix):
        self.source = source
        self.prefix = prefix
        self.stats = {}
        self.otherTranslation = {}
        self.phrases = {}
        for w in source.keys():
            self.otherTranslation[w] = 0

def main():
    parser = argparse.ArgumentParser(description='Script to train a language model')
    parser.add_argument("--source_corpus", default="../data/epps/EPPS.tiny.en", type=str, help="text file containing the source data")
    parser.add_argument("--target_corpus", default="../data/epps/EPPS.tiny.de", type=str, help="text file containing the source data")
    parser.add_argument("--source_dict", default="../data/wikititels/dict.train", type=str, help="text file containing the list of source words")
    parser.add_argument("--target_dict", default="../data/wikititels/dict.train", type=str, help="text file containing the list of source words")

    args = parser.parse_args()


    dictionary = loadDict(args.source_dict,args.target_dict)


    sf = open(args.source_corpus,encoding="utf8")
    tf = open(args.target_corpus,encoding="utf8")


    slf = open(args.source_corpus+".lemma",encoding="utf8")
    tlf = open(args.target_corpus+".lemma",encoding="utf8")


    sl = sf.readline()
    tl = tf.readline()
    sll = slf.readline()
    tll = tlf.readline()

    while(sl and tl):
        
        sw = sl.strip().split()
        tw = tl.strip().split()
        sl = sll.strip().split()
        tl = tll.strip().split()


        for i in range(len(sw)):

            if(sl[i] in dictionary.source):
                target_start,target_end = findTarget(tl,dictionary.source[sl[i]])
                if (target_start != -1):
                    addStatistic(dictionary,sl[i]," ".join(sw[i:i+1])," ".join(tw[target_start:target_end]))
                else:
                    dictionary.otherTranslation[sl[i]] += 1
                    
            prefix = sl[i]
            j = 1
            while(prefix in dictionary.prefix and i+j < len(sw)):
                prefix += " "+sl[i+j]
                if(prefix in dictionary.source):
                    target_start,target_end = findTarget(tl,dictionary.source[prefix])
                    if (target_start != -1):
                        addStatistic(dictionary,prefix," ".join(sw[i:i+j+1])," ".join(tw[target_start:target_end]))
                    else:
                        dictionary.otherTranslation[prefix] += 1

                j+= 1
                
        

        sl = sf.readline()
        tl = tf.readline()
        sll = slf.readline()
        tll = tlf.readline()

    output(args.source_dict,args.target_dict,dictionary)


def output(sfn,tfn,dictionary):
    sf = open(sfn,encoding="utf8")
    tf = open(tfn,encoding="utf8")


    sl = sf.readline()
    tl = tf.readline()


    while(sl and tl):
        sl = sl.strip()
        tl = tl.strip()
    
        if((sl,tl) in dictionary.stats):
            print (" # ".join([str(i) for i in list(dictionary.stats[(sl,tl)])]),"#",dictionary.otherTranslation[sl],"#",len(dictionary.phrases[(sl,tl)]),"#",sl,"#",tl,"#",dictionary.phrases[(sl,tl)])
        else:
            print ("0 # 0 # 0 # 0 # 0 # 0 #",sl,"#",tl)
        
        sl = sf.readline()
        tl = tf.readline()



def addStatistic(stats,source,sw,tw):

    target = stats.source[source]
    if((source,target) not in stats.stats):
        stats.stats[(source,target)] = [1,0,0,0]
        stats.phrases[(source,target)] = []
    else:
        stats.stats[(source,target)][0] += 1
    if(source == sw):
        stats.stats[(source,target)][1] += 1
    if(target == tw):
        stats.stats[(source,target)][2] += 1
    if(source == sw and target == tw):
        stats.stats[(source,target)][3] += 1

    if((sw,tw) not in stats.phrases[(source,target)]):
        stats.phrases[(source,target)].append((sw,tw))

    


def findTarget(tl,target):
    for i in range(len(tl)):
        if target.startswith(tl[i]):
            if(target == tl[i]):
                return i,i+1
            prefix=tl[i]
            j = 1
            while(target.startswith(prefix) and i+j < len(tl)):
                prefix += " "+tl[i+j]
                if(target == prefix):
                    return i,i+j+1
                j += 1
    return -1,-1

def loadDict(sfn,tfn):


    sf = open(sfn,encoding="utf8")
    tf = open(tfn,encoding="utf8")

    source = {}
    prefix = {}

    sl = sf.readline()
    tl = tf.readline()


    while(sl and tl):
        sl = sl.strip()
        tl = tl.strip()

        if(sl in source and tl != source[sl]):
            print("Problems with:",sl,tl)
            print(sl,source[sl])
            exit()
        source[sl] = tl
        e = sl.strip().split()
        for i in range(len(e) - 1):
            prefix[" ".join(e[:i+1])] = 1


        sl = sf.readline()
        tl = tf.readline()


    return Statistics(source,prefix)


main()
