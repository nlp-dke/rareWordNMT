import stanza
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description='Preprocess parallel data with stanza')
    parser.add_argument("--input", default="", type=str, help="Input file")
    parser.add_argument("--output", default="", type=str, help="Output")
    parser.add_argument("--lang", default="en", type=str, help="Language")
    parser.add_argument("--pos", default=False, action="store_true" , help="Output POS tags")
    parser.add_argument("--dependency", default=False, action="store_true" , help="Output POS tags")
    
    args = parser.parse_args()

    stanza.download(args.lang) # download English model
    if(args.dependency):
        nlp = stanza.Pipeline(args.lang,use_gpu=True,processors='tokenize,mwt,pos,lemma,depparse') # initialize English neural pipeline
    elif(args.pos):
        nlp = stanza.Pipeline(args.lang,use_gpu=True,processors='tokenize,mwt,pos,lemma') # initialize English neural pipeline
        
    else:
        nlp = stanza.Pipeline(args.lang,use_gpu=True,processors='tokenize,mwt,lemma') # initialize English neural pipeline
        

    file = open(args.input)

    out_w = open(args.output,"w")
    out_l = open (args.output+".lemma","w")
    if(args.pos):
        out_pos = open (args.output+".pos","w")
    if(args.dependency):
        out_dep = open (args.output+".dep","w")
    line = file.readline()

    deps = []
    
    while(line):

        if(len(line.strip()) == 0):
            out_w.write(line)
            out_l.write(line)
            line = file.readline()
            continue
            

        doc = nlp(line) # run annotation over a sentence
        text = [[word.text,word.lemma] for sent in doc.sentences for word in sent.words]
        for i in range(len(text)):
            if (text[i][1][0].islower()):
                text[i][0] = text[i][0][0].lower() + text[i][0][1:]
        out_w.write(" ".join([s[0] for s in text])+"\n")
        out_l.write(" ".join([s[1] for s in text])+"\n")
        if (args.pos):
            text = [word.upos+"_" + (word.feats if word.feats else "_") for sent in doc.sentences for word in sent.words]
            out_pos.write(" ".join(text)+"\n")
        if(args.dependency):
            deps.append([(word.id,word.head,word.deprel) for sent in doc.sentences for word in sent.words])
        line = file.readline()

    if(args.dependency):
         json.dump(deps, out_dep, indent=2)
main()
