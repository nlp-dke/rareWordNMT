
import sys, argparse



def main():
    parser = argparse.ArgumentParser(description='Script to train a language model')
    parser.add_argument("--source_dict", default="../data/wikititels/dict.train", type=str, help="text file containing the list of source words")
    parser.add_argument("--target_dict", default="../data/wikititels/dict.train", type=str, help="text file containing the list of source words")

    args = parser.parse_args()
    s,t = loadDict(args.source_dict,args.target_dict)
    
    output(args.source_dict,args.target_dict,s,t)

def output(sfn,tfn,s,t):
    sf = open(sfn,encoding="utf8")
    tf = open(tfn,encoding="utf8")


    sl = sf.readline()
    tl = tf.readline()


    while(sl and tl):
        sl = sl.strip()
        tl = tl.strip()
        if(s[sl] > 1 or t[tl] > 1):
            print ("0")
        else:
            print("1")

        sl = sf.readline()
        tl = tf.readline()


def loadDict(sfn,tfn):


    sf = open(sfn,encoding="utf8")
    tf = open(tfn,encoding="utf8")

    source = {}
    target = {}

    sl = sf.readline()
    tl = tf.readline()
    d_s = {}
    d_t = {}

    while(sl and tl):
        sl = sl.strip()
        tl = tl.strip()

        if(sl in source and (d_s[sl] != tl or d_t[tl] != sl) ):
            source[sl] += 1
        elif(sl not in source):
            source[sl] = 1
            d_s[sl] = tl

        if(tl in target and (d_s[sl] != tl or d_t[tl] != sl)):
            target[tl] += 1
        elif (tl not in target):
            target[tl] = 1
            d_t[tl] = sl

        sl = sf.readline()
        tl = tf.readline()


    return source,target


main()
