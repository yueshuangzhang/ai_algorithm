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
    initial_list={}
    transport_list={}
    emit_list={}

    label_list = []

    line_count = -1
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
                if (words[1] not in label_list):
                    label_list.append(words[1])
                
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
                    line_count +=1
                    training_vocab_list.append(sentence)
                    training_label_list.append(sentence_labels)
                    sentence = []
                    sentence_labels = []
                    sentence_complete = False

                    
            if (len(sentence) != 0):
                line_count +=1
                training_vocab_list.append(sentence)
                training_label_list.append(sentence_labels)

    # print(training_vocab_list[-1])
    # print(training_label_list[-1])
    # return
    # So now the training vocab and label list contains all info

    for state0 in label_list:
        transport_list[state0]={}
        for state1 in label_list:
            transport_list[state0][state1]=0.0
        emit_list[state0]={}
        initial_list[state0]=0.0

    for curr_label in label_list:
        class_count[curr_label]=0.0

    print("training start")

    for i in range (len(training_vocab_list)):
        # each file and its sentences
        training_sentence = training_vocab_list[i]
        traning_label = training_label_list[i]

        for n in range(0, len(training_sentence)):
            class_count[traning_label[n]]+=1.0
            if training_sentence[n] in emit_list[traning_label[n]]:
                emit_list[traning_label[n]][training_sentence[n]] += 1.0
            else:
                emit_list[traning_label[n]][training_sentence[n]] = 1.0
            if n == 0:
                initial_list[traning_label[n]] += 1.0
            else:
                transport_list[traning_label[n-1]][traning_label[n]] += 1.0

    #calculate possibility
    for curr_label in label_list:
        initial_list[curr_label]=initial_list[curr_label]*1.0/line_count
        for current_word in emit_list[curr_label]:
            emit_list[curr_label][current_word]=emit_list[curr_label][current_word]/class_count[curr_label]
        for current_word in transport_list[curr_label]:
            transport_list[curr_label][current_word]=transport_list[curr_label][current_word]/class_count[curr_label]

    # print(initial_list)
    # print(transport_list)
    # print(emit_list)
    # ==============================================================================
    # =================================== Testing ==================================
    # ==============================================================================


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

    for sentence in testing_vocab_list:
        for n in range(0, len(sentence)):
            
            word = sentence[n]
            max_pos = 0
            pred = ""

            #print(word)
            # get the possibility list for this word:
            for curr_label in label_list:
                if word in emit_list[curr_label]:
                    if emit_list[curr_label][word] > max_pos:
                        max_pos = emit_list[curr_label][word]
                        pred = curr_label

            # incase unseen words
            if max_pos == 0:
                # get the max from state
                for curr_label in label_list:
                    temp = initial_list[curr_label]
                    if temp > max_pos:
                        pred = curr_label
                        max_pos = temp
            f.write(word + " : " + pred + '\n')   


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