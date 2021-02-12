
import sys, argparse




def main():

    parser = argparse.ArgumentParser(description='Script to train a language model')
    parser.add_argument("--source_dict", default="../data/wikititels/dict.train", type=str, help="text file containing the list of source words")
    parser.add_argument("--target_dict", default="../data/wikititels/dict.train", type=str, help="text file containing the list of source words")
    parser.add_argument("--sentenceAnnotation", default="../data/wikititels/dict.train", type=str, help="SentenceAnnotation")



    args = parser.parse_args()


    dict = {}
    group = {}
    sf = open(args.source_dict,encoding="utf8")
    tf = open(args.target_dict,encoding="utf8")


    sl = sf.readline()
    tl = tf.readline()

    while(sl and tl):
        sl = sl.strip()
        tl = tl.strip()
        dict[sl] = tl
        group[sl] = ""
        sl = sf.readline()
        tl = tf.readline()

    sf.close()
    tf.close()


    f = open(args.sentenceAnnotation,encoding="utf8")

    l = f.readline()

    while(l):
    
        l = l.strip().split("#")
        if(len(l) > 1):
            words = eval(l[1])
            g = l[0].split()[0]
        
            for w in words:
                if(g == "TEST"):
                    if(group[w] == "TRAIN"):
                        group[w] = "MIX"
                    elif(group[w] == ""):
                        group[w] = "TEST"
                else:
                    if(group[w] == "TEST"):
                        group[w] = "MIX"
                    elif(group[w] == ""):
                        group[w] = "TRAIN"

        l = f.readline()
    
    f.close()

    sf = open(args.source_dict,encoding="utf8")


    sl = sf.readline()
    while(sl):
        sl = sl.strip()
        print(group[sl])
        sl = sf.readline()

    sf.close()
    tf.close()


main()
