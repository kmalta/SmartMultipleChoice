1) Download and compile the Glove source code from their website: http://nlp.stanford.edu/projects/glove

2) Download corpus from Wikipedia: http://mattmahoney.net/dc/enwik9.zip

3) Copy and paste the perl script from the bottom of his page and save it to a file. http://mattmahoney.net/dc/textdata.html

4) Run the perl script as specified on his website. It should return a text file that is just plaintext.

5) Run `./vocab_count -min-count 5 -verbose 2 < $CORPUS > $VOCAB_FILE`
   $CORPUS is the file that you got from step 4 and the vocab file the output. It contains all the unique words found in the corpus. Min count is the minimum # of occurrences a word must appear in the corpus to be included in the vocabulary. Verbose 2 outputs debug information.

6) Run `./cooccur -memory $MEMORY -vocab-file $VOCAB_FILE -verbose $VERBOSE -window-size $WINDOW_SIZE < $CORPUS > $COOCCURRENCE_FILE` $MEMORY is the # of gigs RAM your computer has. This command generates a cooccurrence file. $WINDOW_SIZE can be 15.

7) Run `./shuffle -memory $MEMORY -verbose $VERBOSE < $COOCCURRENCE_FILE > $COOCCURRENCE_SHUF_FILE` This shuffles the cooccurrence file. I don't know what this does yet.

8) Run `./glove -save-file $SAVE_FILE -threads $NUM_THREADS -input-file $COOCCURRENCE_SHUF_FILE -x-max $X_MAX -iter $MAX_ITER -vector-size $VECTOR_SIZE -binary $BINARY -vocab-file $VOCAB_FILE -verbose $VERBOSE` This generates the vector file to $SAVE_FILE. Set the num threads to the number of processors in your machine. X_MAX can be set to 10, I don't know what that means yet either. MAX_ITER can be 15, I guess its the number of times glove tries to optimize the model. The more the better? VECTOR_SIZE sets the dimension of the word vectors. BINARY is the output file format, set it to 0 for plaintext output.

9) Once glove finishes running, you should have a vector file with a list of words and their corresponding vector values. Open the file and insert the number of words and the dimension of the vector on the top line seperated by a space.

10) Then run `model = gensim.models.Word2Vec.load_word2vec_format("SAVE_FILE", binary=False)` and once that finishes you should be able to run queries on the data: `model.most_similar(positive=['hello', 'world'], topn=10)`
