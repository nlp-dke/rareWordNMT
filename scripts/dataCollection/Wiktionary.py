import sys, argparse

def main():
    parser = argparse.ArgumentParser(description='Script to train a language model')
    parser.add_argument("--wiktionary", default="../data/wikititels/dict.train", type=str, help="text file containing the list of source words")
    parser.add_argument("--out", default="../data/wikititels/dict.train", type=str, help="text file containing the list of source words")
    parser.add_argument("--source_language", default="English", type=str, help="text file containing the list of source words")
    parser.add_argument("--target_language", default="de", type=str, help="text file containing the list of source words")

    args = parser.parse_args()

    so = open(args.out+".s","w")
    to = open(args.out+".t","w")

    print(args.wiktionary)
    f = open(args.wiktionary,encoding="utf8")

    l = f.readline()
 
    c = 0
    while(l):
        c+= 1
        d = eval(l)
        if(d["lang"] != args.source_language):
            l = f.readline()
            continue
        count = 0
        translation = ""
        if("translations" not in d):
            l = f.readline()
            continue
        for trans in d["translations"]:
            if(trans["lang"] == args.target_language):
                count +=1
                translation= trans
        if(count == 1):
            so.write(d["word"]+"\n")
            to.write(translation["word"]+"\n")
        l = f.readline()
main()
