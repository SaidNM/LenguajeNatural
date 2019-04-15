'''
Version 2.0
Created on 28/05/2014, tested for Python 2.7
@authors: Juan Pablo Posadas, Grigori Sidorov
Class for obtaining syntactic n-grams from dependency trees using Stanford parser output
NOTE: Input tree should NOT be collapsed: -outputFormat "wordsAndTags, typedDependencies" -outputFormatOptions "basicDependencies"
NOTE: Since ",", "[", "]", and "\" are part of our metalanguage, we add a slash to them when they are part of the sentence (sn-grams), e.g., "\,", "\[", "\\"
This version allows to process separately nodes that have too many children (for a given threshold) and select min and max sizes of sn-grams. Default: 5, 2, 7
'''

from sets import Set
import copy, sys
import codecs

class DepInfo(object):
    '''
    This class represents the dependency information of a sentence
    '''
 
    def __init__(self, lines):
        '''
        Constructor
        '''
        self.word          = {} #Dictionary of original words according to their positions
        self.dep           = {} #Dictionary with dependent words
        self.rel           = {} #Dictionary with dependency relations 
        self.children      = {} #Dictionary with words that are dependent for a (key) word
        self.leaves        = [] #List of indexes of words that are leaves        
        self.root_idx      = -1 #Index of the root

        self.prepare_indices(lines)

    def prepare_indices(self, lines):
        for idx, line in enumerate(lines):
            self.rel[idx + 1] = line[ : line.find("(")]
            line=line[line.find("("):]
                    
            p_idx = int(line [line.find("-") + 1 : line.find(",",line.find("-"))] )
            self.dep [idx + 1]  = p_idx
            self.word[idx + 1]  = line[line.rfind(", ") + 2 : line.rfind("-")]
      
            if self.word[idx+1] == ',':
                self.word[idx+1] = "\,"
            elif self.word[idx+1] == '[':
                self.word[idx+1] = "\["
            elif self.word[idx+1] == ']':
                self.word[idx+1] = "\]"
            elif self.word[idx+1] == '\\':
                self.word[idx+1] = "\\\\"
        
            self.children[p_idx] = self.children.get(p_idx, [])
            self.children[p_idx].append(idx + 1)

            if self.dep [idx + 1] == 0:
                self.root_idx = idx + 1
                self.rel[idx+1] = "root"#Line added because of the FREELING output
      
        #Determine if a word is a leaf
        for i in self.word.keys():
            if i not in self.children.keys():
                self.leaves.append(i)
                                            


class BiSNgrams(object):
    '''
    classdocs
    '''


    def __init__(self, min_size, max_size, max_num_children, option):
        '''
        Constructor
        '''
        self.min_size         = min_size         #The minimum size for the sn-grams
        self.max_size         = max_size         #The maximum size for the sn-grams
        self.max_num_children = max_num_children #The maximum number of children per node
         
        if option in [0,1,2]:
            self.option         = option #Type of sn-grams to be obtained: 0 for WORD sn-grams; 1 for sn-grams of SR Tags ; 2 for both
        else: 
            print "Invalid value for the parameter: option"
            exit(1)
            
        self.subtrees       = [] #List that contains all the nodes that are not leaves
        self.DepNgrams      = []
        self.log            = [] #List that contains the nodes that have more children than the parameter max_num_children        
        #self.dicSRTags      = {}
        #self.dicWordNgrams  = {}
        self.dicSRTags      = []
        self.dicWordNgrams  = []
        
        for i in xrange(min_size, max_size+1):
            self.dicSRTags.append({})
            self.dicWordNgrams.append({})
    
    def reset_vars (self):
        del self.subtrees[:]
        del self.DepNgrams[:] 
        del self.log[:]        
        #self.dicWordNgrams.clear()                   
        #self.dicSRTags.clear()        
    
    def print_parsed_sentence(self, sentence):
        line = "*****Sentence: "
        for i in sorted(sentence.word.keys()):
            line += sentence.word[i]+" "
        print line.rstrip(" ")
        
        '''
        line = ""
        for i in sentence.word.keys():
            line  =     str(i)         + "\t"
            line +=     sentence.word[i]  + "\t"
            line +=     sentence.rel [i]  + "\t"
            line += str(sentence.dep [i]) + "\t"
            if i not in sentence.leaves:
                line += str(sentence.children[i])
            print line

        print "Leaf nodes are:"
        line = ""
        for i in sentence.leaves:
            line += sentence.word[i] + ", "
        print line
        '''
    
    def write_all_sn_grams (self, f2):
        '''
        This method write in a file one kind of sn-gram according with the value of op
        '''
        if self.option == 0 or self.option == 2:
            self.write_WordSngrams(f2)

        if self.option == 1 or self.option == 2:
            self.write_SRSngrams(f2)
    
    def write_WordSngrams(self,f2):
        f2.write("************sn-grams of words/POS tags:\n")
        for idx, dic in enumerate(self.dicWordNgrams):
            f2.write ("\n************Size: " + str(idx + self.min_size) + "\n")
            if len(dic.keys()) > 0:
                for item in dic.keys():
                    f2.write (item + "\t" + str(dic[item]) + "\n")
            else:
                f2.write("EMPTY\n")
        f2.write("\n")
        
    def write_SRSngrams(self,f2):
        f2.write("************sn-grams of tags of syntactic relations (SR tags):\n")
        for idx, dic in enumerate(result.dicSRTags):
            f2.write ("\n************Size: " + str(idx + self.min_size) + "\n")
            if len(dic.keys()) > 0:
                for item in dic.keys():
                    f2.write (item + "\t" + str(dic[item]) + "\n")
            else:
                f2.write("EMPTY\n")
        f2.write("\n")
      
    
    def print_sngrams(self):
        if self.option == 0 or self.option == 2: 
            print "************sn-grams of words/POS tags:"
            for idx, dic in enumerate(self.dicWordNgrams):
                print "\n************Size: " + str(idx + self.min_size)
                if len(dic.keys()) > 0:
                    for item in dic.keys():
                        print  item + "\t"+str(dic[item])
                else:
                    print "EMPTY"
                print "****************************************"
        if self.option == 1 or self.option == 2:
            print "************sn-grams of tags of syntactic relations (SR tags):"
            for idx, dic in enumerate(self.dicSRTags):    
                print "\n************Size: " + str(idx + self.min_size)
                if len(dic.keys()) > 0:
                    for item in dic.keys():
                        print  item + "\t"+str(dic[item])
                else:
                    print "EMPTY"
                print "****************************************"
        
    def process_sentence (self, lines):
        '''
        This method calls the specific methods (general steps) for producing sn-grams according to the parameter "option"
        '''
        self.reset_vars()
        sentence = DepInfo(lines)        
        self.print_parsed_sentence(sentence)
        
        for i in sentence.word.keys():            
            if i in sentence.children.keys():
                self.subtrees.append(i)#Store all the possible roots of the subtrees                
                             
        if self.option in [0,1,2]:
            if self.min_size >= 0:
                if self.max_size >= self.min_size:
                    if self.min_size <= len(sentence.word): 
                        
                        if self.max_size > len(sentence.word):
                            line = "\tMessage: The value of the maximum size exceeds the length of the sentence.\n"
                            #print line                            
                        if self.min_size == 0 or self.max_size == 0:
                            line = "\tMessage: the program will obtain the sn-grams of all possible sizes.\n"
                            #print line                            
                        
                        log = self.get_all_DepNgrams(sentence)
                                                
                        if len(log) > 0:
                            line = "\tThe next words have more than "+ str(self.max_num_children) +" children:\n"
                            print line
                            
                            for item in log:
                                line = "\t\t"+sentence.word[item]+"\n"
                                print line
                                                                                                
                        if self.option in [0,1]:
                            self.store_all_DepNgrams(sentence, self.option)                            
                        else:
                            self.store_all_DepNgrams(sentence, 0)
                            self.store_all_DepNgrams(sentence, 1)
                        
                        #self.show_sngrams(sentence, log) #This method only shows the sn-grams obtained from the sentence
                    
                    else:                        
                        line = "\tERROR: The value of the minimum size exceeds the length of the sentence\n"
                        # print line
                else:                    
                    line = "\tERROR: The maximum size must be greater than the minimum size\n"
                    print line
            else:                
                line = "\tERROR: The value of the minimum size is not allowed\n"
                print line
        else:            
            line = "\tERROR: Invalid value for the parameter option\n"
            print line
        
        
    def prepare_SNgram(self, line, sentence, op):
        '''        
        op=-1 for sn-grams of index
        op=0  for sn-grams of words
        op=1  for sn-grams of sr tags
        '''
        ngram = ""
        for item in line:
            if type(item) is str:
                ngram += item
            elif type(item) is int:
                if op == -1:
                    ngram += str(item)
                elif op == 0:
                    ngram += sentence.word[item]
                else:
                    ngram += sentence.rel[item]            
            else:
                ngram += self.prepare_SNgram(item, sentence, op)
        return ngram

    ######################              
    def is_continuous(self, ngram):
        '''
        This method tests if a sn-gram is continuous or not. It assumes that no punctuation characters are allowed in the sn-gram. Used for testing.
        '''
        answer = ""
        if ngram.count(",") > 0:
            answer = "NO"
        else:
            answer = "YES"                    
        return answer
    
    ######################              
    def len_Ngram(self, ngram):
        n = 1
        n += ngram.count("[")
        n += ngram.count(",")
        n -= ngram.count("\[")
        n -= ngram.count("\,")
        return n

  
    ########################
    def get_all_DepNgrams(self, sentence):
        '''
        This method begins the process of getting all the sn-grams of the dependency tree
        '''                         
        unigrams      = []  #Auxiliar variable that contains all the unigrams
        combinations  = []  #Auxiliar variable that contains all the combinations of a node with its children
        aux           = []
        log           = Set()
        
    
        if sentence.root_idx > 0:
            unigrams, combinations, log = self.get_subtrees (sentence)#Call this method first for obtaining all the posible subtrees                    
            
            if len(unigrams) > 0:
                self.DepNgrams.append([sentence.root_idx])
                self.DepNgrams.extend(unigrams)            #Adds the unigrams to the general container
            for item in combinations:                      #Adds the first sn-grams to the general container
                if self.min_size != 0 or self.max_size != 0:                        
                    size = self.len_Ngram(self.prepare_SNgram(item[0], sentence, -1))
                    if size >= self.min_size and size <= self.max_size:        #Check the size of the new sn-grams                
                        self.DepNgrams.append(copy.deepcopy(item[0]))                        
                    if size < self.max_size:
                        aux.append(item)
                else:
                    self.DepNgrams.append(copy.deepcopy(item[0]))

            if self.min_size != 0 or self.max_size != 0:
                self.compound_sngrams(aux, sentence)   #This function generates the rest of sn-grams
            else:
                self.compound_sngrams(combinations, sentence)
        else:
            line = "\tError, no root found\n"
            print line
        
        return(log)
                    
    
    
    ######################        
    def store_all_DepNgrams(self, sentence, op):
        '''
        This method stores the sn-grams in the container specified by the parameter "op"
        '''
        for item in self.DepNgrams:
            ngram = self.prepare_SNgram (item, sentence, op)            
            if op == 0:                                 #According to the params, the sn-grams are stored in the container
                size = self.len_Ngram(ngram)                
                dic = self.dicWordNgrams[size-self.min_size]
                if dic.has_key(ngram):                  #Update the dictionary of Words sn-grams
                    dic[ngram] += 1                     #If the sn-gram exists in the dictionary, update its frequency
                else:
                    dic[ngram] = 1                      #Otherwise, add the sn-gram to the dictionary                
            else:
                size = self.len_Ngram(ngram)
                dic = self.dicSRTags[size-self.min_size]
                if dic.has_key(ngram):                  #Update the dictionary of sn-grams of SR Tags 
                    dic[ngram] += 1                     #If the sn-gram exists in the dictionary, update its frequency
                else:
                    dic[ngram] = 1                      #Otherwise, add the sn-gram to the dictionary
    
    
    
    ######################    
    def compound_sngrams(self, original, sentence):
        combinations   = []
        candidates    = []    
        
        for combination in original:                     #This cycle initializes the list of combinations and list of candidates 
            if len(combination[1]) > 0:               
                size = self.len_Ngram(self.prepare_SNgram(combination[0], sentence, -1))
                combinations.append([combination[0],combination[1],size])
            if combination[0][0] != sentence.root_idx:
                size = self.len_Ngram(self.prepare_SNgram(combination[0], sentence, -1))       
                candidates.append([combination[0],combination[1],size])
                
        
              
        while len(candidates) > 0:                        #In this cycle, select a sn-gram to be replaced in the rest of combinations            
            candidate = candidates.pop(0)
            value = candidate[0][0]                       #Get the first number of the first candidate sn-gram
                              
            for combination in combinations:
                if value in combination[1]:                
                                        
                    position = combination[0].index(value,2)#First get the position of the element          
          
                    sngram = copy.deepcopy(combination)
                    sngram[0].pop(position)                 #Delete the element in the sn-gram
                    sngram[0].insert(position,candidate[0]) #Insert the new part into the sn-gram
                    sngram[1].remove(value)                 #Update its list of posible combinations
                    sngram[2] = self.len_Ngram(self.prepare_SNgram(sngram[0], sentence, -1))#Obtain the size of the new sngram                                        

                    if (self.min_size > 0) and (self.max_size > 0):            #Case when the user specifies the max and min size of sn-grams                        
                        if sngram[2] in xrange(self.min_size, self.max_size+1):#Case when the sn-grams from the list substitution have to be inserted                            
                            self.DepNgrams.append(copy.deepcopy(sngram[0]))    #Update the list of all sn-grams
                        if sngram[2] < self.max_size:                                                    
                            if sngram[0][0] == sentence.root_idx:
                                if len(sngram[1]) > 0:
                                    combinations.append(copy.deepcopy(sngram))
                            else:
                                if len(sngram[1]) > 0:
                                    combinations.append(copy.deepcopy(sngram))
                                candidates.append(copy.deepcopy(sngram))
                    else:                                                 #Case when there is no restriction on the size of the sn-grams
                        self.DepNgrams.append(copy.deepcopy(sngram[0]))   #Update the list of all sn-grams                                                    
                        if sngram[0][0] == sentence.root_idx:
                            if len(sngram[1]) > 0:
                                combinations.append(copy.deepcopy(sngram))
                        else:
                            if len(sngram[1]) > 0:
                                combinations.append(copy.deepcopy(sngram))
                            candidates.append(copy.deepcopy(sngram))
                                               
    
    ######################              
    def get_subtrees (self, sentence):   # A function that gets all the possible subtrees in the tree
        unigrams     = []    #List of all possible unigrams    
        combinations = []    #List of all possible combinations of nodes and their children
        counter      = 0     #Counts the number of children inserted in the aux list
        aux          = []    #Auxiliar variable that contains the highest number of children allowed
        log          = Set() #Variable that contains IDs of the nodes that have more children than it is allowed
      
        
        for node in self.subtrees:
            if self.max_num_children != 0:                      
                aux = []     #Reset the container for the next iteration
                counter = 0  #Reset the variable for the next iteration
                for child in sentence.children[node]:
                    
                    if self.min_size == 1 or self.min_size == 0 or self.max_size == 0: #This code obtains all unigrams of the sentence                
                        unigrams.append ([child])
                    
                    aux.append(child)
                    counter += 1
                    if counter > self.max_num_children:
                        aux.pop()
                        combinations.extend(self.get_next_combinations(node, aux, sentence))#We save new sn-grams in the global dictionary                    
                        counter = 0
                        aux = []
                        aux.append(child)
                        log.add(node)
                                                                
                if len(aux) > 0:                                                          #Analyze the rest of the children 
                    combinations.extend(self.get_next_combinations(node, aux, sentence))  #We save new sn-grams in the global dictionary
            
            else:            #In this case, there is no limitation on the number of children per node, so all the children are processed                
                combinations.extend(self.get_next_combinations(node, sentence.children[node], sentence))
                
                for child in sentence.children[node]:                
                    if self.min_size == 1 or self.min_size == 0 or self.max_size == 0:#This code obtains all unigrams of the sentence                
                        unigrams.append ([child])                                                                                                                                                        
                                                
        return (unigrams, combinations, log)
    
    
    ######################                  
    def get_next_combinations (self, value, children, sentence):
        ngram         = [] #Auxiliary variable for storing the sn-gram
        options       = [] #Auxiliary variable for storing the all the nodes that can be changed in a sn-gram
        combinations  = [] #Auxiliary variable for generating a combination
        lista         = [] #Auxiliary variable for all sn-grams during analysis of a sub-tree
            
        #Initialize the list of combinations    
        for p in xrange(0, len(children)):
            combinations.append (0)
      
        #Generate sn-grams    
        for r in xrange (1, len(children) + 1):                 
            for j in xrange (1, r + 1):
                combinations [j - 1] = j - 1

        #################### The first combination
            options = []
            ngram   = []
            ngram.append (value)
            ngram.append ("[")
            for z in xrange (0, r):
                ngram.append(children [combinations [z]])

                if children[combinations[z]] not in sentence.leaves:
                    options.append(children [combinations [z]])

                ngram.append (",")
            ngram.pop (len(ngram) - 1)          
            ngram.append ("]")            
            lista.append (copy.deepcopy([ngram,options]))

            ################### The rest
            top = self.Combination (len(children), r)
      
            for j in xrange(2, top + 1):
                m = r
                val_max = len(children)

                while combinations [m - 1] + 1 == val_max:
                    m       -= 1
                    val_max -= 1

                combinations [m - 1] += 1

                for k in xrange (m + 1, r + 1):
                    combinations [k - 1] = combinations [k - 2] + 1
            
                options = []
                ngram   = []
                ngram.append(value)
                ngram.append("[")                
                for z in xrange(0, r):
                    ngram.append (children [combinations [z]])

                    if children[combinations[z]] not in sentence.leaves:
                        options.append(children [combinations [z]])

                    ngram.append (",")
                ngram.pop (len(ngram) - 1)
                ngram.append ("]")
                lista.append (copy.deepcopy([ngram,options]))
              
        return (lista)          
    
    ######################                  
    def Combination (self, sz, r):
        if sz == r:
            numerator = 1
        else:
            numerator = sz
            for i in xrange (1, sz):
                numerator *= sz - i
        
            aux = r
            for i in xrange (1, r):
                aux *= r - i
        
            divisor = sz - r
            for i in xrange (1, sz - r):
                divisor *= sz - r - i
                
            numerator = numerator / (aux * divisor)
      
        return (numerator)

############
def process_one_sentence (result, sent_num, f2):
    print "Sentence " + str(sent_num)
    result.process_sentence (lines)
    #result.print_sngrams()
    result.write_all_sn_grams (f2)
    
    return sent_num + 1 

############### MAIN ################################
if __name__ == '__main__':
        
    if len(sys.argv) < 3:
        print "Usage with at least two parameters:"
        print "python SNGrams_selective.py input output"
        exit(1)

    if len(sys.argv) > 7 or (len(sys.argv) < 7 and len(sys.argv) > 3):
        print "Usage with at least six parameters:"
        print "python SNGrams_selective.py input output min_size max_size max_num_children option"
        exit(1)

    input_file   = sys.argv[1]
    output_file  = sys.argv[2]

    #############These are parameters of configuration for the class BiSNgrams    
    min_size         = 2  #These are the parameters of configuration for the class BiSNgrams 
    max_size         = 7
    max_num_children = 5
    option           = 0  #Type of sn-grams to be obtained: 0 for WORD sn-grams; 1 for sn-grams of SR Tags; 2 for both            

    if len(sys.argv) > 3:
        min_size         = int(sys.argv[3])   #These are the parameters of configuration for the class BiSNgrams 
        max_size         = int(sys.argv[4])
        max_num_children = int(sys.argv[5])
        option           = int(sys.argv[6])   #value 0: for sn-grams of words; 
                                              #value 1: for sn-grams of sr tags; 
                                              #value 2: for sn-grams of words and sr tags (equal to call with option 0 and then with option 1)
                
    encod = 'utf-8'   #'utf-8' or other encoding like '1252'
        
    try:
        f1 = codecs.open (input_file,  "rU", encoding = encod)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        exit(1)
    
    try:
        f2 = codecs.open (output_file, "wb", encoding = encod)  #b - Binary, for Unix line endings
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        exit(1)
 
    sent_num = 1;
    result = BiSNgrams(min_size, max_size, max_num_children, option)
    lines  = []
  
    while True :
        ln = f1.readline ()
        if (not ln) or (ln == ""):
            break;

        ln = ln.strip()
        if ln == "":   #Sentences are separated by EMPTY line
            if len (lines) > 0:
                sent_num = process_one_sentence (result, sent_num, f2)
                del lines [:]
        else:
            lines.append (ln)

    if len(lines) > 0: #Last piece in previous (while)
        sent_num = process_one_sentence (result, sent_num, f2)

    f1.close ()
    f2.close ()
           
    print "Done."