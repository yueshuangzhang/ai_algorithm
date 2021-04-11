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

    # Load data
    training_vocab_list = []
    label_list = dict()

    label_counter = 1 # 0 is reserved for the start state.
    word_counter = 0

    for training_file in training_list:
        with open(training_file) as train_file:
            for line in train_file:
                line = line.strip()
                if not line:continue
                words = line.split(" : ")
                if len(words) != 2:
                    print("word & label not match")
                    return
                training_vocab_list.append((words[0], words[1]))
                if (words[1] not in label_list):
                    label_list.append(words[1])

    print("training start")




    # ==============================================================================
    # =================================== Testing ==================================
    # ==============================================================================
    testing_vocab_list = []

    with open(test_file) as test_file:
        for line in test_file:
            line = line.strip()
            # each line is a testing words
            testing_vocab_list.append(line)



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