
import sys, argparse

class Statistics:

    def __init__(self,source,s_prefix,target,t_prefix,translation):
        self.source = source
        self.sourcePrefix = s_prefix
        self.target = target
        self.targetPrefix = t_prefix
        self.translation = translation

def main():
    parser = argparse.ArgumentParser(description='Script to train a language model')
    parser.add_argument("--source_corpus", default="../data/epps/EPPS.tiny.en", type=str, help="text file containing the source data")
    parser.add_argument("--target_corpus", default="../data/epps/EPPS.tiny.de", type=str, help="text file containing the source data")
    parser.add_argument("--source_dict", default="../data/wikititels/dict.train", type=str, help="text file containing the list of source words")
    parser.add_argument("--target_dict", default="../data/wikititels/dict.train", type=str, help="text file containing the list of source words")
    parser.add_argument("--split", default="../data/wikititels/dict.train", type=str, help="Split of the dictionary")



    args = parser.parse_args()


    dictionary = loadDict(args.source_dict,args.target_dict,args.split)


    sf = open(args.source_corpus,encoding="utf8")
    tf = open(args.target_corpus,encoding="utf8")


    slf = open(args.source_corpus+".lemma",encoding="utf8")
    tlf = open(args.target_corpus+".lemma",encoding="utf8")


    sl = sf.readline()
    tl = tf.readline()
    sll = slf.readline()
    tll = tlf.readline()

    mixDict = {}
    trainValidSplit = 0


    while(sl and tl):
        
        sw = sl.strip().split()
        tw = tl.strip().split()
        sl = sll.strip().split()
        tl = tll.strip().split()

        foundSource = {}
        foundTarget = {}

        for i in range(len(sw)):

            if(sl[i] in dictionary.source):
                if(sl[i] in foundSource):
                    foundSource[sl[i]] += 1
                else:
                    foundSource[sl[i]] = 1
                    
            prefix = sl[i]
            j = 1
            while(prefix in dictionary.sourcePrefix and i+j < len(sw)):
                prefix += " "+sl[i+j]
                if(prefix in dictionary.source):
                    if(prefix in foundSource):
                        foundSource[prefix] += 1
                    else:
                        foundSource[prefix] = 1

                j+= 1


        for i in range(len(tw)):

            if(tl[i] in dictionary.target):
                if(tl[i] in foundTarget):
                    foundTarget[tl[i]] += 1
                else:
                    foundTarget[tl[i]] = 1
                    
            prefix = tl[i]
            j = 1
            while(prefix in dictionary.targetPrefix and i+j < len(tw)):
                prefix += " "+tl[i+j]
                if(prefix in dictionary.target):
                    if(prefix in foundTarget):
                        foundTarget[prefix] += 1
                    else:
                        foundTarget[prefix] = 1

                j+= 1
                
        if(len(foundTarget) == 0 and len(foundSource) == 0):
            print ("TRAIN 0")
        elif(len(foundTarget) != len(foundSource)):
            print ("IGNORE -1",len(foundTarget),len(foundSource))
        else:
            found=len(foundSource)
            group = "TRAIN"
            mixEntry=""
            for k in foundSource.keys():
                if(dictionary.translation[k] not in foundTarget or foundSource[k] != foundTarget[dictionary.translation[k]]):
                    found = -2
                    break;
                if dictionary.source[k] == "TEST":
                    group = "TEST"
                elif group == "TRAIN" and dictionary.source[k] == "MIX":
                    group = "MIX"
                    mixEntry=k
                    if(k not in mixDict):
                        mixDict[k] = 0
            if(found < 0):
                print("IGNORE",found)
            else:
                if(group == "TEST"):
                    print("TEST",found,"#",list(foundSource.keys()))
                elif(group == "MIX"):
                    if(mixDict[mixEntry] %2 == 0):
                        print("TEST",found,"#",list(foundSource.keys()))
                    else:
                        if(trainValidSplit %2 == 0 and trainValidSplit < 4000):
                            print("VALID",found,"#",list(foundSource.keys()))
                        else:
                            print("TRAIN",found,"#",list(foundSource.keys()))
                        trainValidSplit += 1
                    mixDict[mixEntry] += 1
                else:
                    if(trainValidSplit %2 == 0 and trainValidSplit < 4000):
                        print("VALID",found,"#",list(foundSource.keys()))
                    else:
                        print("TRAIN",found,"#",list(foundSource.keys()))
                    trainValidSplit += 1
                    
                        
                    
                
        sl = sf.readline()
        tl = tf.readline()
        sll = slf.readline()
        tll = tlf.readline()

def loadDict(sfn,tfn,splitfn):


    sf = open(sfn,encoding="utf8")
    tf = open(tfn,encoding="utf8")
    splitf = open(splitfn,encoding="utf8")

    source = {}
    s_prefix = {}
    target = {}
    t_prefix = {}
    translation = {}

    sl = sf.readline()
    tl = tf.readline()
    group = splitf.readline()

    while(sl and tl and group):
        sl = sl.strip()
        tl = tl.strip()
        group = group.strip()

        source[sl] = group
        e = sl.strip().split()
        for i in range(len(e) - 1):
            s_prefix[" ".join(e[:i+1])] = 1

        target[tl] = 1
        e = tl.strip().split()
        for i in range(len(e) - 1):
            t_prefix[" ".join(e[:i+1])] = 1

        translation[sl] = tl

        sl = sf.readline()
        tl = tf.readline()
        group = splitf.readline()


    return Statistics(source,s_prefix,target,t_prefix,translation)



main()
