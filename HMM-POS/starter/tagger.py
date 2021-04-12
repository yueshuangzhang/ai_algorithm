# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys

def tag(training_list, test_file, output_file):
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    print("Tagging the file.")
    #
    # YOUR IMPLEMENTATION GOES HERE

    # ==============================================================================
    # ================================== Training ==================================
    # ==============================================================================
    # Initial structure

    # Load data
    training_vocab_list = []
    training_label_list = []
    start_c={}#开始概率，就是一个字典，state:chance=Word/lines
    transport_c={}#转移概率，是字典：字典，state:{state:num,state:num....}   num=num(state1)/num(statess)
    emit_c={}#发射概率，也是一个字典，state:{word:num,word,num}  num=num(word)/num(words)
    Count_dic = {}  # 一个属性下的所有单词，为了求解emit

    state_list = []

    label_counter = 1 # 0 is reserved for the start state.
    word_counter = 0

    lineCount = -1#句子总数，为了求出开始概率
    class_count={}

    for training_file in training_list:
        with open(training_file, encoding='utf8',errors='replace') as train_file:
            sentence = []
            sentence_label = []
            for line in train_file:
                line = line.strip()
                if not line:continue
                words = line.split(" : ")
                if len(words) != 2:
                    print("word & label not match")
                    return

                if words[0] not in ['.','!','?']:
                    sentence.append(words[0])
                    sentence_label.append(words[1])
                else:
                    sentence.append(words[0])
                    sentence_label.append(words[1])
                    training_vocab_list.append(sentence)
                    training_label_list.append(sentence_label)
                    sentence = []
                    sentence_label = []

                #record the existing labels
                if (words[1] not in state_list):
                    state_list.append(words[1])

    # So now the training vocab and label list contains all info
    for state0 in state_list:
        transport_c[state0]={}
        for state1 in state_list:
            transport_c[state0][state1]=0.0
        emit_c[state0]={}
        start_c[state0]=0.0

    for state in state_list:
        class_count[state]=0.0

    print("training start")

    for i in range (len(training_vocab_list)):
        training_sentence = training_vocab_list[i]
        traning_label = training_label_list[i]
        for n in range(0,len(training_sentence)):
            class_count[traning_label[n]]+=1.0
            if training_sentence[n] in emit_c[traning_label[n]]:
                emit_c[traning_label[n]][training_sentence[n]] += 1.0
            else:
                emit_c[traning_label[n]][training_sentence[n]] = 1.0
            if n == 0:
                start_c[traning_label[n]] += 1.0
            else:
                transport_c[traning_label[n-1]][traning_label[n]] += 1.0

    for state in state_list:
        start_c[state]=start_c[state]*1.0/lineCount
        for li in emit_c[state]:
            emit_c[state][li]=emit_c[state][li]/class_count[state]
        for li in transport_c[state]:
            transport_c[state][li]=transport_c[state][li]/class_count[state]
   
    file0=open('start.txt','w',encoding='utf8')
    file0.write(str(start_c))
    file1=open('tran.txt','w',encoding='utf8')
    file1.write(str(transport_c))
    file2=open('emit.txt','w',encoding='utf8')
    file2.write(str(emit_c))
    file0.close()
    file1.close()
    file2.close()
    # ==============================================================================
    # =================================== Testing ==================================
    # ==============================================================================
    print("Start testing")
    file0=open('start.txt','r')
    start_c=eval(file0.read())
    file1=open('emit.txt','r',encoding='utf8')
    emit_c=eval(file1.read())
    file2=open('tran.txt','r',encoding='utf8')
    trans_c=eval(file2.read())

    testing_vocab_list = []

    with open(test_file) as test_file:
        sentence = []
        for line in test_file:
            word = line.strip()
            if not word:continue
                
            if word not in ['.','!','?']:
                sentence.append(word)
            else:
                sentence.append(word)
                testing_vocab_list.append(sentence)
                sentence = []

    f = open(output_file,'w')

    for sentence in testing_vocab_list:
        path = {}
        V = [{}]  # 记录第几次的概率
        for state in state_list:
            V[0][state] = start_c[state] * emit_c[state].get(sentence[0], 0)
            path[state] = [state]
        for n in range(1, len(sentence)):
            V.append({})
            newpath = {}
            for k in state_list:
                pp,pat=max([(V[n - 1][j] * trans_c[j].get(k,0) * emit_c[k].get(sentence[n], 0) ,j )for j in state_list])
                V[n][k] = pp
                newpath[k] = path[pat] + [k]
            path = newpath

        (prob, state) = max([(V[len(sentence) - 1][y], y) for y in state_list])

        p = prob
        out_list = path[state]
        print(out_list)
        
        pred = path[state]

        for index in range (len(sentence)):
            f.write(sentence[index] + " " + pred[index] + '\n')

    f.close()

    return

if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")

    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"
    parameters = sys.argv
    training_list = parameters[parameters.index("-d")+1:parameters.index("-t")]
    test_file = parameters[parameters.index("-t")+1]
    output_file = parameters[parameters.index("-o")+1]
    print("Training files: " + str(training_list))
    print("Test file: " + test_file)
    print("Ouptut file: " + output_file)

    # Start the training and tagging operation.
    tag (training_list, test_file, output_file)