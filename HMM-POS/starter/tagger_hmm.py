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
    # start structure

    # Load data
    training_vocab_list = []
    training_label_list = []
    start_list={}

    # The possibility per dic[label] sum up to 1
    tran_list={}
    emis_list={}

    label_list = []

    label_count = {}
    sentence = []
    sentence_label = []

    for training_file in training_list:
        with open(training_file, encoding='utf-8') as train_file:

            has_quo = False
            # the count of left '
            has_sl_quo = False
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
                if (words[1] not in label_list):
                    label_list.append(words[1])

                if words[0] in ['.','!','?']:
                    sentence_complete = True
                
                if words[0] == '"':
                    if has_quo == True: has_quo = False
                    else:has_quo = True

                if words[0] == '‘':
                    has_sl_quo = True

                if words[0] == '’':
                    has_sl_quo = False

                sentence.append(words[0])
                sentence_labels.append(words[1])
                
                if (sentence_complete and has_quo == False and has_sl_quo == False):
                    training_vocab_list.append(sentence)
                    training_label_list.append(sentence_labels)

                    sentence = []
                    sentence_labels = []
                    sentence_complete = False
                    
            if (len(sentence) != 0):
                training_vocab_list.append(sentence)
                training_label_list.append(sentence_labels)


    # print(training_label_list[-1])
    # return
    # So now the training vocab and label list contains all info

    for label_1 in label_list:

        tran_list[label_1]={}
        for label_2 in label_list:
            # tran_list[previous][current] = 0
            tran_list[label_1][label_2] = 0

        emis_list[label_1]={}
        start_list[label_1] = 0
        label_count[label_1] = 0

    print("training start")

    for i in range (len(training_vocab_list)):
        # each file and its sentences
        training_sentence = training_vocab_list[i]
        traning_label = training_label_list[i]

        # for each words in the range of the sentance
        for n in range(len(training_sentence)):
            # count the # of label that appears in the training set
            label_count[traning_label[n]] += 1

            # if the word exists in the emission list
            if training_sentence[n] in emis_list[traning_label[n]]:
                emis_list[traning_label[n]][training_sentence[n]] += 1
            else:
                emis_list[traning_label[n]][training_sentence[n]] = 1
            if n == 0:
                start_list[traning_label[n]] += 1
            else:
                # previous state's current state ++
                tran_list[traning_label[n-1]][traning_label[n]] += 1

    #calculate possibility
    for curr_label in label_list:
        start_list[curr_label] = start_list[curr_label] / len(training_vocab_list)

        for exist_word in emis_list[curr_label]:
            emis_list[curr_label][exist_word] = emis_list[curr_label][exist_word] / label_count[curr_label]

        for exist_label in tran_list[curr_label]:
            tran_list[curr_label][exist_label] = tran_list[curr_label][exist_label] / label_count[curr_label]

    
    # f.write("emis_list:\n"+str(emis_list) + '\n')
    # f.write("tran_list:\n"+str(tran_list) + '\n')
    # f.write("start_list:\n"+str(start_list) + '\n')
    # f.close()
    # print(start_list)
    # print(tran_list)
    # print(emis_list)
    # ==============================================================================
    # =================================== Testing ==================================
    # ==============================================================================

    print("testing start")
    testing_vocab_list = []
#    testing_vocab_list = test_strs

    with open(test_file, encoding='utf-8') as test_file:
        has_quo = False
        has_sl_quo = False
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
            
            if words[0] in ['.','!','?']:
                    sentence_complete = True
                
            if words[0] == '"':
                if has_quo == True: has_quo = False
                else:has_quo = True

            if words[0] == '‘':
                has_sl_quo = True

            if words[0] == '’':
                has_sl_quo = False

            sentence.append(word)

            if (sentence_complete and has_quo == False and has_sl_quo == False):
                testing_vocab_list.append(sentence)
                sentence = []
                sentence_complete = False

        if (len(sentence) != 0):
            testing_vocab_list.append(sentence)

    # =======================================================
    # ====================== viterbi ========================
    # =======================================================
    f_s = open("structures.txt",'w', encoding='utf-8')
    f_s.write("emis_list:\n"+str(emis_list)+ '\n')
    f_s.close()

    f = open(output_file,'w')
    for sentence in testing_vocab_list:

        previous_lable = ""

        for n in range(len(sentence)):
            convertable = False
            convertable_to_double = False
            convertable_dash = False
            word = sentence[n]
            # " can convert to '
            if word == '"':
                convertable = True
            if word in ['—','-']:
                convertable_dash = True
            if word in ['‘','’']:
                convertable_to_double = True
            # maximum possibility of the current word label
            
            max_label_possibility = 0
            pred_label = label_list[0]
            word_exist = False

            # get the possibility list for this word:
            for curr_label in label_list:
                curr_label_possibility = 0
                # get from emission list that according to usual cases
                # we have trained this words:
                if word in emis_list[curr_label]:
                    word_exist = True
                    # for this word, get the possibility of the label
                    curr_emit_possibility = emis_list[curr_label][word]

                    # get the previous state's next state's max possibility
                    if previous_lable != "":
                        curr_label_possibility = tran_list[previous_lable][curr_label] * curr_emit_possibility

                    elif n == 0: # previous_lable == "", start of sentence
                        curr_label_possibility = start_list[curr_label] * curr_emit_possibility
                    else:
                        curr_label_possibility = curr_emit_possibility

                if curr_label_possibility > max_label_possibility:
                    max_label_possibility = curr_label_possibility
                    pred_label = curr_label

            previous_lable = pred_label

            if not word_exist and (convertable or convertable_to_double or convertable_dash):
                conv_word = ""
                if convertable:
                    conv_word = '‘'
                    conv_word.encode(encoding='utf-8')
                elif convertable_to_double:
                    conv_word = '"'
                    conv_word.encode(encoding='utf-8')
                elif convertable_dash:
                    if word =='—':
                        conv_word = '-'
                    else: conv_word ='—'
                    conv_word.encode(encoding='utf-8')

                word_exist = True
                for curr_label in label_list:
                    if conv_word in emis_list[curr_label]:
                        # for this word, get the possibility of the label
                        curr_emit_possibility = emis_list[curr_label][conv_word]
                        # get the previous state's next state's max possibility
                        if previous_lable != "":
                            #curr_tran_possibility = tran_list[previous_lable][curr_label]
                            curr_label_possibility = tran_list[previous_lable][curr_label] * curr_emit_possibility
                        elif n == 0: # previous_lable == "", start of sentence
                            curr_label_possibility = start_list[curr_label] * curr_emit_possibility
                        else:
                            curr_label_possibility = curr_emit_possibility

                if curr_label_possibility > max_label_possibility:
                    max_label_possibility = curr_label_possibility
                    pred_label = curr_label

                previous_lable = pred_label

            # incase unseen words - try capitalize and lowercase
            else:
                if word.islower():
                    conv_word = word.capitalize()
                    conv_word.encode(encoding='utf-8')
                if word[0].isupper():
                    conv_word = word.lower()
                    conv_word.encode(encoding='utf-8')

                for curr_label in label_list:
                    if conv_word in emis_list[curr_label]:
                        word_exist = True
                        # for this word, get the possibility of the label
                        curr_emit_possibility = emis_list[curr_label][conv_word]

                        # get the previous state's next state's max possibility
                        if previous_lable != "":
                            curr_label_possibility = tran_list[previous_lable][curr_label] * curr_emit_possibility
                        elif n == 0: # previous_lable == "", start of sentence
                            curr_label_possibility = start_list[curr_label] * curr_emit_possibility
                        else:
                            curr_label_possibility = curr_emit_possibility

                if word_exist == False:
                    for curr_label in label_list:
                        if previous_lable != "":
                            curr_label_possibility = tran_list[previous_lable][curr_label]
                        elif n == 0:
                            curr_label_possibility = start_list[curr_label]
                        else:
                            curr_label_possibility = tran_list[previous_lable][curr_label]
                        if curr_label_possibility > max_label_possibility:
                            max_label_possibility = curr_label_possibility
                            pred_label = curr_label       
                previous_lable = ""
            
            f.write(word + " : " + pred_label + '\n')   

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