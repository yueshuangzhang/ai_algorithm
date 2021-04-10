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
    vocab = []
    vocab_label = []
    for training_file in training_list:
        with open(training_file) as t_file:
            for line in t_file:
                line=line.strip()
                if not line:continue
                words=line.split(" : ")
                vocab.append(words[:1])
                vocab_label.append(words[1:])

    if  len(vocab)!=len(vocab_label):
        print("words and label doesn't match")
        return
    else:
        print("training start")
        print(len(vocab))
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