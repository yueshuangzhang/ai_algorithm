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

    state_list = []

    label_counter = 1 # 0 is reserved for the start state.
    word_counter = 0

    lineCount = -1#句子总数，为了求出开始概率
    class_count={}
    sentence = []
    sentence_label = []

    for training_file in training_list:
        with open(training_file) as train_file:

            has_quo = False
            sentence_complete = False
            sentence = []
            sentence_labels = []

            for line in train_file:
                line = line.strip()
                if not line:continue

                words = line.split(" : ")
                if len(words) != 2:
                    print("word & label not match")
                    return
                
                #record the existing labels
                if (words[1] not in state_list):
                    state_list.append(words[1])
                
                if words[0] == '"':
                    if has_quo == True: 
                        has_quo = False
                    elif has_quo == False: 
                        has_quo = True
                
                if words[0] in ['.','!','?']:
                    sentence_complete = True

                sentence.append(words[0])
                sentence_labels.append(words[1])
                
                if (sentence_complete and has_quo == False):
                    lineCount +=1
                    training_vocab_list.append(sentence)
                    training_label_list.append(sentence_labels)
                    sentence = []
                    sentence_labels = []
                    sentence_complete = False

                    
            if (len(sentence) != 0):
                lineCount +=1
                training_vocab_list.append(sentence)
                training_label_list.append(sentence_labels)

    # print(training_vocab_list[-1])
    # print(training_label_list[-1])
    # return
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
        # each file and its sentences
        training_sentence = training_vocab_list[i]
        traning_label = training_label_list[i]

        for n in range(0, len(training_sentence)):
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

    # print(start_c)
    # print(transport_c)
    # print(emit_c)
    # ==============================================================================
    # =================================== Testing ==================================
    # ==============================================================================
    # test_strs=["Detective","Chief","Inspector","John","McLeish","gazed","doubtfully","at","the","plate","before","him","."]


    print("testing start")
    testing_vocab_list = []
#    testing_vocab_list = test_strs

    with open(test_file) as test_file:
        has_quo = False
        sentence_complete = False
        sentence = []
        for word in test_file:
            word = word.strip()
            if not word:continue
            
            if word == '"':
                if has_quo == True: 
                    has_quo = False
                elif has_quo == False: 
                    has_quo = True
            
            if word in ['.','!','?']:
                sentence_complete = True

            sentence.append(word)

            if (sentence_complete and has_quo == False):
                testing_vocab_list.append(sentence)
                sentence = []
                sentence_complete = False

        if (len(sentence) != 0):
            testing_vocab_list.append(sentence)

    f = open(output_file,'w')

    count = 0
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
                pp,pat=max([(V[n - 1][j] * transport_c[j].get(k,0) * emit_c[k].get(sentence[n], 0) ,j )for j in state_list])
                V[n][k] = pp
                newpath[k] = path[pat] + [k]
            path = newpath

        (prob, state) = max([(V[len(sentence) - 1][y], y) for y in state_list])

        pred = path[state]

        for index in range (len(sentence)):
            # print(sentence[index])
            # print(pred[index])
            f.write(sentence[index] + " " + pred[index] + '\n')
            # if sentence[index] == ".":
            #     count += 1
            # if count==5:
            #     return
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