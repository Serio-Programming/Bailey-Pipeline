# Bailey Pipeline
# This program is a processing pipeline for DNA analysis of soil samples
# A program by Tyler Serio
# From April 2021 to Whenever It's Done

# Import relevant tools
import subprocess
import sys
import os
import os.path
from os import path
import numpy
import matplotlib.pyplot
import win32com.client


# Define the Functions

# Pair the reads
# not done
def pair_reads():
    global source_file_name
    global working_file_name
    global world_steps
    ofile = open("input/" + working_file_name, "r")
    outputfilename = source_file_name.replace(".fastq", "_paired_reads_output.fastq")
    outputfilename = ("Step" + str(world_steps) + "_" + outputfilename)
    world_steps += 1
    outputfile = open("output/" + outputfilename, "w")
    working_file_name = outputfilename
    print("we're gunna have to make Python run the PEAR program")
    print("Or run NMERGE or whatever it's called")
    print("radda")

    print("")
    print("Output is: " + working_file_name)


    # Look at this
    # with open("solexa_output.txt", "w") as f:
    #   solexa1 = subprocess.run([SolexaQA++.exe])    
    #   print(megablast1.stdout)

# Remove by Length
def remove_by_length():
    global source_file_name
    global working_file_name
    global world_steps
    ofile = open("input/" + working_file_name, "r")
    outputfilename = source_file_name.replace(".fastq", "_removed_by_length.fastq")
    outputfilename = ("Step" + str(world_steps) + "_" + outputfilename)
    longeroutputfile = open("output/" + "Step" + str(world_steps) + "_longer_" + outputfilename, "w")
    world_steps += 1
    outputfile = open("output/" + outputfilename, "w")
    working_file_name = outputfilename

    linep = 0
    length = 350
    longer = False
    for line in ofile:
        linep += 1
        if linep == 1:
            line1 = line
        if linep == 2:
            line2 = line
            #print(len(line))
            if len(line) > length:
                longer = True
        if linep == 3:
            line3 = line
        if linep == 4:
            line4 = line
            linep = 0
            
            if longer == False:
                outputfile.write(line1)
                outputfile.write(line2)
                outputfile.write(line3)
                outputfile.write(line4)
            if longer == True:
                longeroutputfile.write(line1)
                longeroutputfile.write(line2)
                longeroutputfile.write(line3)
                longeroutputfile.write(line4)
                longer = False

# Deduplicator by Prof. Baechle
# This step works properly
def deduplicator():
    global source_file_name
    global working_file_name
    global world_steps
    ofile = open("output/" + working_file_name, "r")
    outputfilename = source_file_name.replace(".fastq", "_removed_duplicates_output.fastq")
    outputfilename = ("Step" + str(world_steps) + "_" + outputfilename)
    world_steps += 1
    outputfile = open("output/" + outputfilename, "w")
    working_file_name = outputfilename
    print("------------------------------------------")
    print("Deduplicator is running...")
    print("Output is: " + working_file_name)
    #filename = sys.argv[1]

    lut = {'A':'T','T':'A','C':'G','G':'C','N':'N'}

    def complement(sequence):
        sequence = reversed(sequence)
        comp_sequence = [lut[x] for x in sequence]
        return ''.join(comp_sequence)

    hm = {}

    with ofile as f:

        while True:

            header = f.readline().rstrip()
            sequence = f.readline().rstrip()
            plus = f.readline().rstrip()
            quality = f.readline().rstrip()
            if header == '':
                break
            
            csequence = complement(sequence)
            if sequence in hm or csequence in hm:

                if csequence in hm:
                    sequence2 = csequence
                    ofilename = ("output/" + "duplicates-complement.txt")
                else:
                    sequence2 = sequence
                    ofilename = ("output/" + "duplicates-regular.txt")

                with open(ofilename,"a") as fw:
                    fw.write("%s\n%s\n%s\n%s\n" % (header,sequence,plus,quality))
                    fw.write("%s\n%s\n%s\n%s\n" % (hm[sequence2][0],hm[sequence2][1],hm[sequence2][2],hm[sequence2][3]))
                    fw.write("====================================================================\n")

                q1 = sum([ord(x) for x in sequence])
                q2 = sum([ord(x) for x in hm[sequence2][3]])

                if q1 > q2:
                    hm[sequence] = (header,sequence,plus,quality)
            else:
                hm[sequence] = (header,sequence,plus,quality)

    with outputfile as f:
        for key in hm:
            header, sequence, plus, quality = hm[key]
            f.write("%s\n%s\n%s\n%s\n" % (header,sequence,plus,quality))

    print("Deduplicator is done!")

# tFilter Function
# Takes quality scores of the first, second, last, and second to last
# thymine bases and changes them to a lower score 
# Seems to be done 
def tFilter():
    global source_file_name
    global working_file_name
    global world_steps
    ofile = open("output/" + working_file_name, "r")
    outputfilename = source_file_name.replace(".fastq", "_tFilter_output.fastq")
    outputfilename = ("Step" + str(world_steps) + "_" + outputfilename)
    world_steps += 1
    outputfile = open("output/" + outputfilename, "w")
    working_file_name = outputfilename
    print("")
    print("tFilter is running...")
    print("Output is: " + working_file_name)
    #readcount = 0
    #totalreadcount = 0
    #milreadcount = 0
    linecount = 0
    badbasecount = 0
    cutoff = 0
    line1 = "blah"
    line2 = "blah"
    line3 = "blah"
    line4 = "blah"
    opening = 1
    replacing = 1
    while replacing == 1:
        cutoff += 1
        if cutoff == 2:
            ofile.close()
            outputfile.close()
            print("tFilter is done!!")
            replacing = 0
            break
        for line in ofile:
            linecount += 1
            if linecount == 1:
                line1 = str(line)
            if linecount == 2:
                line2 = str(line)
                base_characters = split(line2)
            if linecount == 3:
                line3 = str(line)
            if linecount == 4:
                line4 = str(line)
                quality_characters = split(line4)
                if base_characters[0] == "T":
                    quality_characters[0] = "#"
                if base_characters[1] == "T":
                    quality_characters[1] = "#"
                if base_characters[len(base_characters) - 2] == "T":
                    quality_characters[len(base_characters) - 2] = "#"
                if base_characters[len(base_characters) - 3] == "T":
                    quality_characters[len(base_characters) - 3] = "#"
                line4 = ''.join(quality_characters)

                outputfile.write(line1)
                outputfile.write(line2)
                outputfile.write(line3)
                outputfile.write(line4)

                line1 = "blah"
                line2 = "blah"
                line3 = "blah"
                line4 = "blah"
                linecount = 0    

# Used in tFilter function
# Done
def split(word):
    return[char for char in word]

# Remove Low Quality Reads Function
# Seems to be done
def remove_low_quality_reads():
    global source_file_name
    global working_file_name
    global world_steps
    ofile = open("output/" + working_file_name, "r")
    outputfilename = source_file_name.replace(".fastq", "_removed_low_quality_reads_output.fastq")
    outputfilename = ("Step" + str(world_steps) + "_" + outputfilename)
    outputfilename2 = outputfilename.replace("_removed_low_quality_reads_output.fastq", "_low_quality_reads_list.fastq")
    world_steps += 1
    outputfile = open("output/" + outputfilename, "w")
    outputfile2 = open("output/" + outputfilename2, "w")
    working_file_name = outputfilename
    print("")
    print("Remove Low Quality Reads is running...")
    print("Output is: " + working_file_name)

    linecount = 0
    badbasecount = 0

    #each sequence in a FASTQ file has 4 lines, thus 4 variables are created
    line1 = "blah"
    line2 = "blah"
    line3 = "blah"
    line4 = "blah"
    removing = 1
    cutoff = 0


    #begin removing low quality reads
    while removing == 1:
        cutoff += 1

        #if all lines of the file have been read, end this section of the program
        if cutoff == 2:
            ofile.close()
            outputfile.close()
            outputfile2.close()
            removing = 0
            break

        #step through each line of the file
        for line in ofile:
            linecount += 1
            if linecount == 1:
                line1 = str(line)
            if linecount == 2:
                line2 = str(line)
            if linecount == 3:
                line3 = str(line)
            if linecount == 4:
                line4 = str(line)

                #define low quality scores
                characters = ("!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/")

                #check the fourth line for low quality scores
                for i in line4:
                    if i in characters:
                        badbasecount += 1

                #write better quality reads to a file
                if badbasecount < 5:
                    outputfile.write(line1)
                    outputfile.write(line2)
                    outputfile.write(line3)
                    outputfile.write(line4)

                #write lower quality reads to a different file
                else:
                    outputfile2.write(line1)
                    outputfile2.write(line2)
                    outputfile2.write(line3)
                    outputfile2.write(line4)

                #reset the variables
                badbasecount = 0
                line1 = "blah"
                line2 = "blah"
                line3 = "blah"
                line4 = "blah"
                #line5 = "blah"
                linecount = 0    

    ofile.close()
    outputfile.close()
    outputfile2.close()
    print("Remove Low Quality Reads is done!!")

# SolexaQA++
# MOSTLY DONE
# MAKE SURE TO ADD IN THE ABILITY TO CHECK FOR WHETHER OR NOT STEP 4 FILES (SOLEXA OUTPUT FILES) EXIST
# IF THEY DO, NEW FILES CANNOT BE NAMED AS STEP 4 FILES (SOLEXA OUTPUT FILES)
# THIS WILL CAUSE AN ERROR IF THE SAMPLE NEEDS TO BE RERUN
# CHANGE THE "t" ARGUMENT IF YOU'RE USING ILLUMINA
def solexa_qa_plus_plus():
    global source_file_name
    global working_file_name
    global world_steps
    ofile = open("output/" + working_file_name, "r")
    outputfilename = source_file_name.replace(".fastq", "_solexa_qa_plus_plus.fastq")
    outputfilename = ("Step" + str(world_steps) + "_" + outputfilename)
    world_steps += 1
    #outputfile = open("output/" + outputfilename, "w")
    #print(working_file_name)
    f = working_file_name
    f = "output\\" + f
    #print(f)
    working_file_name = outputfilename
    print(outputfilename)
    #for line in ofile:
    #    outputfile.write(line)
    print("")
    print("SolexaQA++ is running...")
    print("Output is: " + working_file_name + " and " + outputfilename.replace(".fastq", ".segments"))

    result = subprocess.run(["supporting_programs\SolexaQA++_v3.1.7.2\Windows_x64\SolexaQA++.exe", "dynamictrim", f, "-p", "0.05", "-b", "-d", "output"], text= True, shell = True, capture_output = True) # Illumina
    #result = subprocess.run(["supporting_programs\SolexaQA++_v3.1.7.2\Windows_x64\SolexaQA++.exe", "dynamictrim", f, "-p", "0.05", "-b", "-d", "output", "-t"], text= True, shell = True, capture_output = True) # Ion Torrent
    print(result)
    ofile.close()
    print(result)
    #print(outputfilename.replace(".fastq", ".segments"))
    os.rename(f.replace(".fastq", ".fastq_trimmed.segments"), "output\\" + outputfilename.replace(".fastq", ".segments"))
    os.rename(f.replace(".fastq.trimmed", ".trimmed"), "output\\" + outputfilename.replace(".fastq", ".trimmed"))
    
    print("SolexaQA++ is done!!")
    working_file_name = outputfilename.replace(".fastq", ".trimmed")

# FASTQ to FASTA
# Converts a FASTQ file to FASTA format
# Seems to be done
def fastq_to_fasta():
    global source_file_name
    global working_file_name
    global world_steps
    ofile = open("output/" + working_file_name, "r")
    outputfilename = source_file_name.replace(".fastq", "_fastq_to_fasta.fasta")
    outputfilename = ("Step" + str(world_steps) + "_" + outputfilename)
    world_steps += 1
    outputfile = open("output/" + outputfilename, "w")
    working_file_name = outputfilename
    print("")
    print("FASTQ to FASTA is running...")
    print("Output is: " + working_file_name)

   
    #global working_file_name
    #global source_file_name
    # Define important variables
    sID = [] # This variable holds the sequence ID
    s = [] # This variable holds the sequence itself

    #fastqfile = open(working_file_name, "r")
    #fastafilename = source_file_name.replace(".fastq", ".fasta")
    #fastafile = open("output/" + fastafilename, "w")
    #working_file_name = fastafilename
    
    # Go through the FASTQ file and take out the relevant information
    line_place = 0
    for line in ofile:
        line_place += 1
        if line_place == 1:
            sID = ">" + line
        if line_place == 2:
            s = line
        if line_place >= 4:
            outputfile.write(sID)
            outputfile.write(s)
            line_place = 0

    #fastqfile.close()
    #fastafile.close()
    ofile.close()
    outputfile.close()

    print("FASTQ to FASTA is done!!!")

# Count FASTA Lengths Function
# Counts the length of FASTA sequences
# Seems to be done
def count_fasta_lengths():
    global source_file_name
    global working_file_name
    global world_steps
    ofile = open("output/" + working_file_name, "r")
    outputfilename = source_file_name.replace(".fastq", "_fasta_length_counts.txt")
    outputfilename = ("Step" + str(world_steps) + "_" + outputfilename)
    world_steps += 1
    outputfile = open("output/" + outputfilename, "w")
    ############################# LOOK HERE ################working_file_name = outputfilename
    print("")
    print("Count FASTA Lengths is running...")
    print("Output is: " + outputfilename)

    # Define important variables
    linecount = 0 # Holds the number of the line
    linelength = 0 # Holds the length of the FASTA sequence

    # Go through the FASTAofilefasta_file:
    for line in ofile:
        linecount += 1
        if linecount == 1:
            query = line.strip()
        if linecount == 2:
            linelength = len(line) - 1
            outputfile.write(query + "\t" + str(linelength) + "\n")
            outputfile.flush()
            linecount = 0

    #working_file_name = ("output/Step5_" + source_file_name)
    #working_file_name = working_file_name.replace(".fastq", "_fastq_to_fasta.fasta")

    print("Count FASTA Lengths is done!!!")
    ofile.close()
    outputfile.close()

# Megablast
# Seems to be done
def megablast():
    global source_file_name
    global working_file_name
    global world_steps
    ofile = open("output/" + working_file_name, "r") # probably not needed
    outputfilename = source_file_name.replace(".fastq", "_megablast_output.fastq")
    outputfilename = ("Step" + str(world_steps) + "_" + outputfilename)
    world_steps += 1
    #outputfile = open("output/" + outputfilename, "w")
    f = working_file_name
    f = "output/" + f
    working_file_name = outputfilename
    working_file_name = working_file_name.replace(".fastq", ".txt")
    print("")
    print("Megablast is running...")
    print("Output is: " + working_file_name)
    working_file_name = working_file_name

    #f = open("input/skreee.txt", "w")
    #result = subprocess.run(["python.exe", "test_program.py"], input = "b", capture_output = True, text = True)
    #print(result.stdout)
    #f.write(result.stdout)

    print("This may take awhile...")
   # blastn -task megablast -query ../../../output/Step5_bison1_paired_sample_Copy_fastq_to_fasta.fasta -db ../../../database_files/nt/nt -out ../../../output/megablast.txt -num_threads 2 -outfmt 6
    result = subprocess.run([r"supporting_programs\blast-2.11.0+\bin\blastn.exe", "-task", "megablast", "-query", f, "-db", r"database_files/nt/nt", "-out", "output/" + working_file_name, "-num_threads", "9", "-outfmt", "6"], text= True, shell = True, capture_output = True)
    #print(result)
    #print(result.stdout)
    ofile.close() # probably not needed
    print("Megablast is done!!")

# TEMPORARILY CHANGED FOR TESTING, MAKE SURE TO LOOK AT IT
# Best Hits
# Identifies the best hits to DNA from a megablast file
# Seems to be done
def best_hits():  
    global source_file_name
    global working_file_name
    global world_steps

    # TESTING
    #world_steps = 8
    #working_file_name = "Step7_bison1_paired_sample_Copy_megablast_output.txt"
    # TESTING
    
    ofile = open("output/" + working_file_name, "r")
    #print("output/" + working_file_name)
    outputfilename = source_file_name.replace(".fastq", "_best_hits_singles.txt")
    newoutputfilename = outputfilename.replace("_best_hits_singles.txt", "_best_hits_multiples.txt")
    outputfilename = ("Step" + str(world_steps) + "_" + outputfilename)
    newoutputfilename = ("Step" + str(world_steps) + "_" + newoutputfilename)
    #print(outputfilename)
    #print(newoutputfilename)
    world_steps += 1
    #outputfilename = working_file_name
    outputfile = open("output/" + outputfilename, "w")
    newoutputfile = open("output/" + newoutputfilename, "w")
    working_file_name = outputfilename
    print("")
    print("Best Hits is running...")
    print("Output is: " + working_file_name)
    parsing = 1
    cutoff = 0

    #begin parsing the file
    while parsing == 1:
        step = 0
        initial_query = 0
        next_query = 0
        single_best_hit = 0
        multiple_best_hit = 0
        query = 0
        printnumber = 0
        fnumber = 0
        number = 0
        milnumber = 0
        end = 0
        record = 1
        cutoff += 1
        
        #when the entire input file has been read, close the input and output files
        if cutoff == 2:
            ofile.close()
            outputfile.close()
            newoutputfile.close()
            #print ("That's it!")
            #print ("We're done!")
            print("Best Hits is done!!")
            parsing = 0
            break
        
        #print("We are now parsing.")
        for line in ofile:
            number += 1
            printnumber += 1
            #if number == 1000000:
                #number = 0
                #milnumber = milnumber + 1000000
                #milnumberstr = str(milnumber)
                #print (milnumberstr + " lines read.")
            columns = line.split()
            queryinfo = line
            recording = 1
            while recording == 1:
                if step == 0:
                    initial_line = queryinfo
                    initial_query = columns[0]
                    initial_score = columns[11]
                    step = 1
                    recording = 0
                    break
                if step == 1:
                    next_line = queryinfo
                    next_query = columns[0]
                    next_score = columns[11]
                    if initial_query == next_query:
                        if float(initial_score) > float(next_score):
                            single_best_hit = 1
                            multiple_best_hit = 0
                            outputfile.write(initial_line)
                            outputfile.flush()
                            step = 3
                            recording = 0
                            break
                        if float(initial_score) == float(next_score):
                            single_best_hit = 0
                            multiple_best_hit = 1
                            newoutputfile.write(initial_line)
                            newoutputfile.flush()
                            newoutputfile.write(next_line)
                            newoutputfile.flush()
                            step = 2
                            recording = 0
                            break
                    if initial_query != next_query:
                        single_best_hit = 1
                        multiple_best_hit = 0
                        outputfile.write(initial_line)
                        outputfile.flush()
                        initial_line = next_line
                        initial_query = next_query
                        initial_score = next_score
                        step = 1
                        recording = 0
                        break
                if step == 2:
                    next_line = queryinfo
                    next_query = columns[0]
                    next_score = columns[11]
                    if initial_query == next_query:
                        if float(initial_score) == float(next_score):
                            single_best_hit = 0
                            multiple_best_hit = 1
                            newoutputfile.write(next_line)
                            newoutputfile.flush()
                            step = 2
                            recording = 0
                            break
                        if float(initial_score) != float(next_score):
                            single_best_hit = 0
                            multiple_best_hit = 0
                            step = 2
                            recording = 0
                            break
                    if initial_query != next_query:
                        initial_line = next_line
                        initial_query = next_query
                        initial_score = next_score
                        step = 1
                        recording = 0
                        break

                if step == 3:
                    next_line = queryinfo
                    next_query = columns[0]
                    next_score = columns[11]
                    if initial_query == next_query:
                        step = 3
                        recording = 0
                        break
                    if initial_query != next_query:
                        initial_line = next_line
                        initial_query = next_query
                        initial_score = next_score
                        step = 1
                        recording = 0
                        break

# CONDENSE MULTIPLE BEST HITS
# COMBINE BEST HITS FILES

# Count FASTA Lengths Again Function
# Counts the length of FASTA sequences again
# Seems to be done    
def count_fasta_lengths_again():
    global source_file_name
    global working_file_name
    global world_steps
    ofile = open("output/" + working_file_name, "r")
    outputfilename = source_file_name.replace(".fastq", "_fasta_length_counts.txt")
    outputfilename = ("Step" + str(world_steps) + "_" + outputfilename)
    world_steps += 1
    outputfile = open("output/" + outputfilename, "w")
    #working_file_name = outputfilename
    print("")
    print("Count FASTA Lengths is running...")
    print("Output is: " + outputfilename)

    # Define important variables
    linecount = 0 # Holds the number of the line
    linelength = 0 # Holds the length of the FASTA sequence

    # Go through the FASTAofilefasta_file:
    for line in ofile:
        linecount += 1
        if linecount == 1:
            query = line.strip()
        if linecount == 2:
            linelength = len(line) - 1
            outputfile.write(query + "\t" + str(linelength) + "\n")
            outputfile.flush()
            linecount = 0

    print("Count FASTA Lengths is done!!")

# Gather Taxonomic IDs from Best Hits file using Accession2ID file
# Probably not done
# "NewAccession2TaxonID"
def taxonomic_ids():
    global source_file_name
    global working_file_name
    global world_steps

    outputfilename = source_file_name.replace(".fastq", "_singles_taxon_IDs.txt")
    outputfilename = ("Step" + str(world_steps) + "_" + outputfilename)
    outputfilename2 = outputfilename.replace("_singles_taxon_IDs.txt", "multiples_taxon_IDs.txt")
    print("")
    print("Taxonomic IDs is running...")
    print("Output is: " + outputfilename + " and " + outputfilename2)
    
    outputfilename = ("output/" + outputfilename)
    
    ofile_singles = "output/" + working_file_name
    ofile_multiples = ofile_singles.replace("_singles.txt", "_multiples.txt")
    #print(ofile_singles)
    #print(ofile_multiples)
    #outputfilename = source_file_name.replace(".fastq", "_fasta_length_counts.txt")
    taxID_file = outputfilename
    taxID_error_file= taxID_file.replace("_singles_taxon_IDs.txt", "_singles_taxon_error_file.txt")
    taxID_file_multiples = taxID_file.replace("_singles_taxon_IDs.txt", "_multiples_taxon_IDs.txt")
    taxID_error_file_multiples = taxID_file_multiples.replace("_multiples_taxon_IDs.txt", "_multiples_taxon_error_file.txt")
    working_file_name = source_file_name.replace(".fastq", "_singles_taxon_IDs.txt")
    working_file_name = ("Step" + str(world_steps) + "_" + working_file_name)
    #outputfilename = ("Step" + str(world_steps) + "_" + outputfilename)
    world_steps += 1
    #outputfile = open("output/" + outputfilename, "w")
    #print("")
    #print("Output is: " + outputfilename)
    
    # Actually run the function
    Build_Dictionary_TaxID() # Will need this later
    Accession_2_Taxonomy(ofile_singles, taxID_file, taxID_error_file) # This can only be used with enough memory
    Accession_2_Taxonomy(ofile_multiples, taxID_file_multiples, taxID_error_file_multiples) # This can only be used with enough memory
    #New_Accession_2_Taxonomy(ofile_singles, taxID_file, taxID_error_file)
    #New_Accession_2_Taxonomy(ofile_multiples, taxID_file_multiples, taxID_error_file_multiples)
    access2tax.clear()
    print("Taxonomic IDs is done!!")

def New_Accession_2_Taxonomy(ofile, taxID_file, taxID_error_file):
    accession_file = open(ofile, "r")
    taxID_file = open(taxID_file, "w")
    taxID_error_file = open(taxID_error_file, "w")
    
    place = -1
    for line in accession_file:
        place += 1
        columns = line.split()
        letters = split(columns[1])
        #if letters[0] == "A":
            #print("DICKS")
        accession2taxidfile = open("accession2taxid/" + str(letters[0]) + "_access2taxid.txt", "r")
        match = 0
        for line in accession2taxidfile:
            columns2 = line.split()
            #print(columns2[0])
            #print(columns[1])
            if columns2[0] == columns[1]:
                #print("Dicks")
                #print(columns[1])
                #print(columns2)
                taxID_file.write(str(place) + "\t" + str(columns2[1]) + "\t" + str(columns2[0] + "\n"))
                taxID_file.flush()
                match = 1
        if match == 0:
            taxID_error_file.write(str(place) + "\t" + str(columns[1]) + "\t" + repr(columns[1]) + "\n")
            taxID_error_file.flush()
        accession2taxidfile.close()
    taxID_file.close()
    taxID_error_file.close()
    accession_file.close()

# Used in Taxonomic ID function
def Build_Dictionary_TaxID():
    accession2tax_file = open("accession2taxid/nucl_gb.accession2taxid", "r")
    accession_code_place = -1
    cutoff = 0
    file_place = 1
    global access2tax
    if 'access2tax' not in globals():
        access2tax = {}

    for line in accession2tax_file:
        #print(line)
        #file_place += 1
        #print(file_place)
        columns = line.split()
        access2tax[str(columns[1])] = str(columns[2])
        #print(access2tax)
    accession2tax_file.close()

# Used in Taxonomic ID function
def Accession_2_Taxonomy(ofile, taxID_file, taxID_error_file):
    #global access2tax
    accession_file = open(ofile, "r")

    taxID_file = open(taxID_file, "w")
    taxID_error_file = open(taxID_error_file, "w")
    
    #accession_file = open("/home/tserio/accession2taxonomy/latrine_best_hits_alphabetical.txt", "r")
    parsing = 1
    cutoff = 0
    accession_count = 0
    accession_codes = []
    queries = []
    accession_checks = []
    taxIDs = []
    #print(accession_file)
    #print(taxID_file)
    #print(taxID_error_file)
    while parsing == 1:
        cutoff += 1
        if cutoff == 2:
            parsing = 0
            #print("That's it!")
            break
        for line in accession_file:
            accession_count += 1
            columns = line.split()
            accession = str(columns[1])
            accession_codes.append(accession)
            query = str(columns[0])
            queries.append(query)
    accession_file.close()

#taxID_file = open("/home/tserio/accession2taxonomy/taxID_file.txt", "w")
#taxID_error_file = open("/home/tserio/accession2taxonomy/taxID_error_file.txt", "w")

    place = -1
    read_dictionary = 1
    while read_dictionary == 1:
        place += 1
        if place >= len(accession_codes):
            read_diciontary = 0
            #print("That's it! We're done!")
            #taxID_file.write("We are done.")
            taxID_file.close()
            taxID_error_file.close()
            break
        try:
            taxID_file.write(str(place) + "    " + str(access2tax[accession_codes[place]]) + "    " + str(accession_codes[place]) + "    " + queries[place] + "\n")
            taxID_file.flush()
        except KeyError:
            taxID_error_file.write(str(place) + "    " + str(accession_codes[place]) + "    " + repr(accession_codes[place]) + "    " + queries[place] + "\n")
            taxID_file.flush()

# MAYBE DONE
# LOOK AT IT
# MAYBE DONE
# LOOK AT IT
# MAYBE DONE
# LOOK AT IT
# Condense Taxonomic Lineage
# This program takes a file with multiple best hits per query
# And condenses them into their lowest shared taxonomic rank for the query
def condense_taxonomic_lineage():
    global source_file_name
    global working_file_name
    global world_steps
    working_file_name = working_file_name.replace("_singles_get_taxonomy.txt", "_multiples_get_taxonomy.txt")
    ofile = open(working_file_name, "r")
    #outputfilename = source_file_nme.replace(".fastq", "_condensed_best_hits.txt")
    #outputfilename = ("Step" + str(world_steps) + "_" + outputfilename)
    #world_steps += 1
    outputfilename = working_file_name.replace("_multiples_get_taxonomy.txt", "_condensed_best_hits.txt")
    output_file = open(outputfilename, "w")
    print("")
    print("Condense Multiple Best Hits is running...")
    print("Output is: " + outputfilename)
    working_file_name = outputfilename
    
    # Create lists
    superkingdoml = []
    kingdoml = []
    phyluml = []
    classl = []
    orderl = []
    familyl = []
    genusl = []
    speciesl = []

    # Create variables
    superkingdomw = "n" 
    kingdomw = "n"
    phylumw = "n"
    classw = "n"
    orderw = "n"
    familyw = "n"
    genusw = "n"
    speciesw = "n"

    superkingdomc = "n" 
    kingdomc = "n"
    phylumc = "n"
    classc = "n"
    orderc = "n"
    familyc = "n"
    genusc = "n"
    speciesc = "n"

    parsing = 1
    take_first_query = 1
    number = -1
    while parsing == 1:
        for line in ofile:
            columns = line.split("    ")
            theline = line
            if take_first_query == 1:
                query1 = columns[12]
                take_first_query = 0
            if take_first_query != 1:
                #query2 = columns[1]
                try:
                    query2 = columns[12]
                except:
                    compare = 1
                    while compare == 1:
                        if len(speciesl) == speciesl.count(speciesl[0]):
                            superkingdomw = superkingdoml[0]
                            kingdomw = kingdoml[0]
                            phylumw = phyluml[0]
                            classw = classl[0]
                            orderw = orderl[0]
                            familyw = familyl[0]
                            genusw = genusl[0]
                            speciesw = speciesl[0]
                            compare = 0
                            break
                        if len(genusl) == genusl.count(genusl[0]):
                            superkingdomw = superkingdoml[0]
                            kingdomw = kingdoml[0]
                            phylumw = phyluml[0]
                            classw = classl[0]
                            orderw = orderl[0]
                            familyw = familyl[0]
                            genusw = genusl[0]
                            speciesw = "n"
                            compare = 0
                            break
                        if len(familyl) == familyl.count(familyl[0]):
                            superkingdomw = superkingdoml[0]
                            kingdomw = kingdoml[0]
                            phylumw = phyluml[0]
                            classw = classl[0]
                            orderw = orderl[0]
                            familyw = familyl[0]
                            genusw = "n"
                            speciesw = "n"
                            compare = 0
                            break 
                        if len(orderl) == orderl.count(orderl[0]):
                            superkingdomw = superkingdoml[0]
                            kingdomw = kingdoml[0]
                            phylumw = phyluml[0]
                            classw = classl[0]
                            orderw = orderl[0]
                            familyw = "n"
                            genusw = "n"
                            speciesw = "n"
                            compare = 0
                            break
                        if len(classl) == classl.count(classl[0]):
                            superkingdomw = superkingdoml[0]
                            kingdomw = kingdoml[0]
                            phylumw = phyluml[0]
                            classw = classl[0]
                            orderw = "n"
                            familyw = "n"
                            genusw = "n"
                            speciesw = "n"
                            compare = 0
                            break 
                        if len(phyluml) == phyluml.count(phyluml[0]):
                            superkingdomw = superkingdoml[0] 
                            kingdomw = kingdoml[0]
                            phylumw = phyluml[0]
                            classw = "n"
                            orderw = "n"
                            familyw = "n"
                            genusw = "n"
                            speciesw = "n"
                            compare = 0
                            break 
                        if len(kingdoml) == kingdoml.count(kingdoml[0]):
                            superkingdomw = superkingdoml[0]
                            kingdomw = kingdoml[0]
                            phylumw = "n"
                            classw = "n"
                            orderw = "n"
                            familyw = "n"
                            genusw = "n"
                            speciesw = "n"
                            compare = 0
                            break  
                        if len(superkingdoml) == superkingdoml.count(superkingdoml[0]):
                            superkingdomw = superkingdoml[0] 
                            kingdomw = "n"
                            phylumw = "n"
                            classw = "n"
                            orderw = "n"
                            familyw = "n"
                            genusw = "n"
                            speciesw = "n"
                            compare = 0
                            break
                        else:
                            superkingdomw = "n" 
                            kingdomw = "n"
                            phylumw = "n"
                            classw = "n"
                            orderw = "n"
                            familyw = "n"
                            genusw = "n"
                            speciesw = "n"
                            compare = 0
                            break

                    # Write the output file
                    number += 1
                    numbers = str(number)
                    output_file.write(numbers + "\t" + query1.strip("\n") + "\t" + str(len(superkingdoml)) + "\t" + "n" + "\t"
                        + speciesw + "\t" + genusw + "\t" + familyw + "\t" + orderw + "\t" + classw + "\t"
                        + phylumw + "\t" + kingdomw + "\t" + superkingdomw + "\n")                    
                    output_file.flush()

                    # compare
                    query1 = query2
                    superkingdoml = []
                    kingdoml = []
                    phyluml = []
                    classl = []
                    orderl = []
                    familyl = []
                    genusl = []
                    speciesl = []
                    superkingdoml.append(superkingdomc)
                    kingdoml.append(kingdomc)
                    phyluml.append(phylumc)
                    classl.append(classc)
                    orderl.append(orderc)
                    familyl.append(familyc)
                    genusl.append(genusc)
                    speciesl.append(speciesc)
                    parsing = 0
                    break
##                    output_file.write(query1 + "\t" + "taxID" + "\t" + "root" + "\t"
##                           + superkingdomc + "\t" + kingdomc + "\t"
##                           + phylumc + "\t" + classc + "\t" + orderc + "\t"
##                           + familyc + "\t" + genusc + "\t" + speciesc + "\n")
##                    output_file.flush()
##                    break

            taxID = columns[2]
            superkingdomc = columns[11].replace("\n", "")
            kingdomc = columns[10]
            phylumc = columns[9]
            classc = columns[8]
            orderc = columns[7]
            familyc = columns[6]
            genusc = columns[5]
            speciesc = columns[3]

            if take_first_query == 1 or query1 == query2:
                superkingdoml.append(superkingdomc)
                kingdoml.append(kingdomc)
                phyluml.append(phylumc)
                classl.append(classc)
                orderl.append(orderc)
                familyl.append(familyc)
                genusl.append(genusc)
                speciesl.append(speciesc)

            if query1 != query2:
                compare = 1
                while compare == 1:
                    if len(speciesl) == speciesl.count(speciesl[0]):
                        superkingdomw = superkingdoml[0]
                        kingdomw = kingdoml[0]
                        phylumw = phyluml[0]
                        classw = classl[0]
                        orderw = orderl[0]
                        familyw = familyl[0]
                        genusw = genusl[0]
                        speciesw = speciesl[0]
                        compare = 0
                        break
                    if len(genusl) == genusl.count(genusl[0]):
                        superkingdomw = superkingdoml[0]
                        kingdomw = kingdoml[0]
                        phylumw = phyluml[0]
                        classw = classl[0]
                        orderw = orderl[0]
                        familyw = familyl[0]
                        genusw = genusl[0]
                        speciesw = "n"
                        compare = 0
                        break
                    if len(familyl) == familyl.count(familyl[0]):
                        superkingdomw = superkingdoml[0]
                        kingdomw = kingdoml[0]
                        phylumw = phyluml[0]
                        classw = classl[0]
                        orderw = orderl[0]
                        familyw = familyl[0]
                        genusw = "n"
                        speciesw = "n"
                        compare = 0
                        break 
                    if len(orderl) == orderl.count(orderl[0]):
                        superkingdomw = superkingdoml[0]
                        kingdomw = kingdoml[0]
                        phylumw = phyluml[0]
                        classw = classl[0]
                        orderw = orderl[0]
                        familyw = "n"
                        genusw = "n"
                        speciesw = "n"
                        compare = 0
                        break
                    if len(classl) == classl.count(classl[0]):
                        superkingdomw = superkingdoml[0]
                        kingdomw = kingdoml[0]
                        phylumw = phyluml[0]
                        classw = classl[0]
                        orderw = "n"
                        familyw = "n"
                        genusw = "n"
                        speciesw = "n"
                        compare = 0
                        break 
                    if len(phyluml) == phyluml.count(phyluml[0]):
                        superkingdomw = superkingdoml[0] 
                        kingdomw = kingdoml[0]
                        phylumw = phyluml[0]
                        classw = "n"
                        orderw = "n"
                        familyw = "n"
                        genusw = "n"
                        speciesw = "n"
                        compare = 0
                        break 
                    if len(kingdoml) == kingdoml.count(kingdoml[0]):
                        superkingdomw = superkingdoml[0]
                        kingdomw = kingdoml[0]
                        phylumw = "n"
                        classw = "n"
                        orderw = "n"
                        familyw = "n"
                        genusw = "n"
                        speciesw = "n"
                        compare = 0
                        break  
                    if len(superkingdoml) == superkingdoml.count(superkingdoml[0]):
                        superkingdomw = superkingdoml[0] 
                        kingdomw = "n"
                        phylumw = "n"
                        classw = "n"
                        orderw = "n"
                        familyw = "n"
                        genusw = "n"
                        speciesw = "n"
                        compare = 0
                        break
                    else:
                        superkingdomw = "n" 
                        kingdomw = "n"
                        phylumw = "n"
                        classw = "n"
                        orderw = "n"
                        familyw = "n"
                        genusw = "n"
                        speciesw = "n"
                        compare = 0
                        break

##                # Write the output file
##                number += 1
##                numbers = str(number)
##                output_file.write(numbers + "\t" + query1.strip("\n") + "\t" + "2" + "\t" + "n" + "\t"
##                        + speciesw + "\t" + genusw + "\t" + familyw + "\t" + orderw + "\t" + classw + "\t"
##                        + phylumw + "\t" + kingdomw + "\t" + superkingdomw + "\n")            
##                output_file.flush()
##
##                # compare
##                query1 = query2
##                superkingdoml = []
##                kingdoml = []
##                phyluml = []
##                classl = []
##                orderl = []
##                familyl = []
##                genusl = []
##                speciesl = []
##                superkingdoml.append(superkingdomc)
##                kingdoml.append(kingdomc)
##                phyluml.append(phylumc)
##                classl.append(classc)
##                orderl.append(orderc)
##                familyl.append(familyc)
##                genusl.append(genusc)
##                speciesl.append(speciesc)

                # Write the output file
                number += 1
                numbers = str(number)
                output_file.write(numbers + "\t" + query1.strip("\n") + "\t" + str(len(superkingdoml)) + "\t" + "n" + "\t"
                        + speciesw + "\t" + genusw + "\t" + familyw + "\t" + orderw + "\t" + classw + "\t"
                        + phylumw + "\t" + kingdomw + "\t" + superkingdomw + "\n")            
                output_file.flush()

                # compare
                query1 = query2
                superkingdoml = []
                kingdoml = []
                phyluml = []
                classl = []
                orderl = []
                familyl = []
                genusl = []
                speciesl = []
                superkingdoml.append(superkingdomc)
                kingdoml.append(kingdomc)
                phyluml.append(phylumc)
                classl.append(classc)
                orderl.append(orderc)
                familyl.append(familyc)
                genusl.append(genusc)
                speciesl.append(speciesc)

        #print(columns)
        #print(repr(columns))
        #print(query1)
        #print(query2)
        #print("")
        #print(repr(query1))
        #print(repr(query2))

        compare = 1
        while compare == 1:
            if len(speciesl) == speciesl.count(speciesl[0]):
                superkingdomw = superkingdoml[0]
                kingdomw = kingdoml[0]
                phylumw = phyluml[0]
                classw = classl[0]
                orderw = orderl[0]
                familyw = familyl[0]
                genusw = genusl[0]
                speciesw = speciesl[0]
                compare = 0
                break
            if len(genusl) == genusl.count(genusl[0]):
                superkingdomw = superkingdoml[0]
                kingdomw = kingdoml[0]
                phylumw = phyluml[0]
                classw = classl[0]
                orderw = orderl[0]
                familyw = familyl[0]
                genusw = genusl[0]
                speciesw = "n"
                compare = 0
                break
            if len(familyl) == familyl.count(familyl[0]):
                superkingdomw = superkingdoml[0]
                kingdomw = kingdoml[0]
                phylumw = phyluml[0]
                classw = classl[0]
                orderw = orderl[0]
                familyw = familyl[0]
                genusw = "n"
                speciesw = "n"
                compare = 0
                break 
            if len(orderl) == orderl.count(orderl[0]):
                superkingdomw = superkingdoml[0]
                kingdomw = kingdoml[0]
                phylumw = phyluml[0]
                classw = classl[0]
                orderw = orderl[0]
                familyw = "n"
                genusw = "n"
                speciesw = "n"
                compare = 0
                break
            if len(classl) == classl.count(classl[0]):
                superkingdomw = superkingdoml[0]
                kingdomw = kingdoml[0]
                phylumw = phyluml[0]
                classw = classl[0]
                orderw = "n"
                familyw = "n"
                genusw = "n"
                speciesw = "n"
                compare = 0
                break 
            if len(phyluml) == phyluml.count(phyluml[0]):
                superkingdomw = superkingdoml[0] 
                kingdomw = kingdoml[0]
                phylumw = phyluml[0]
                classw = "n"
                orderw = "n"
                familyw = "n"
                genusw = "n"
                speciesw = "n"
                compare = 0
                break 
            if len(kingdoml) == kingdoml.count(kingdoml[0]):
                superkingdomw = superkingdoml[0]
                kingdomw = kingdoml[0]
                phylumw = "n"
                classw = "n"
                orderw = "n"
                familyw = "n"
                genusw = "n"
                speciesw = "n"
                compare = 0
                break  
            if len(superkingdoml) == superkingdoml.count(superkingdoml[0]):
                superkingdomw = superkingdoml[0] 
                kingdomw = "n"
                phylumw = "n"
                classw = "n"
                orderw = "n"
                familyw = "n"
                genusw = "n"
                speciesw = "n"
                compare = 0
                break
            else:
                superkingdomw = "n" 
                kingdomw = "n"
                phylumw = "n"
                classw = "n"
                orderw = "n"
                familyw = "n"
                genusw = "n"
                speciesw = "n"
                compare = 0

        # Write the output file
        number += 1
        numbers = str(number)
        output_file.write(numbers + "\t" + query1.strip("\n") + "\t" + str(len(superkingdoml)) + "\t" + "n" + "\t"
                + speciesw + "\t" + genusw + "\t" + familyw + "\t" + orderw + "\t" + classw + "\t"
                + phylumw + "\t" + kingdomw + "\t" + superkingdomw + "\n")            
        output_file.flush()
                
        output_file.close()
        ofile.close()
        parsing = 0

    print("Condense Multiple Best Hits is done!!!")

    #print(source_file_name)
    #print(working_file_name)
    #print(world_steps)

#   "Get Taxonomy"
def taxonomic_lineage():
    global source_file_name
    global working_file_name
    global world_steps
    #ofile = open("output/" + working_file_name, "r")
    outputfilename = source_file_name.replace(".fastq", "_singles_get_taxonomy.txt")
    outputfilename = ("output/" + "Step" + str(world_steps) + "_" + outputfilename)
    singles_outputfilename = outputfilename
    singles_error_output_filename = outputfilename.replace("singles_get_taxonomy.txt", "singles_get_taxonomy_errors.txt")
    multiples_outputfilename = singles_outputfilename.replace("singles_get_taxonomy.txt", "multiples_get_taxonomy.txt")
    multiples_error_output_filename = multiples_outputfilename.replace("multiples_get_taxonomy.txt", "multiples_get_taxonomy_errors.txt")
    world_steps += 1
    #outputfile = open("output/" + outputfilename, "w")
    print("")
    print("Taxonomic Lineage is running...")
    print("Output is: " + outputfilename)

    Build_Dictionary_TaxLineage()
    Get_Taxonomy(working_file_name, singles_outputfilename, singles_error_output_filename)
    working_file_name = working_file_name.replace("_singles_taxon_IDs.txt", "_multiples_taxon_IDs.txt")
    Get_Taxonomy(working_file_name, multiples_outputfilename, multiples_error_output_filename)
    working_file_name = outputfilename
    taxid2taxonomy
    print("Taxonomic Lineage is done!!!")
    
def Build_Dictionary_TaxLineage():

    taxid2taxonomy_file = open("taxid2taxonomy/new_taxdump/rankedlineage.dmp", "r", encoding = "utf-8")

    id_place = -1
    cutoff = 0
    #file_place = 1
    global taxid2taxonomy
    if 'taxid2taxonomy' not in globals():
        taxid2taxonomy = {}
    for line in taxid2taxonomy_file:
        #file_place += 1
        #print(file_place)
        columns = line.split("|")
        #columns_two = columns[2].split(";")
        #columns_two = [item.strip(" ") for item in columns_two]
        #columns = [item.strip("\n") for item in columns]
        #columns_two = "    ".join([str(elem) for elem in columns_two])
        #del columns[2]
        #columns.append([str(elem) for elem in columns_two])
        #columns.extend(columns_two)
        check_columns = -1
        checking_columns = 1
        while checking_columns == 1:
            check_columns += 1
            if check_columns >= len(columns):
                break

            if columns[1] == "\troot\t":
                columns[1] = "n"
            if columns[2] == "\t\t":
                columns[2] = "n"
            if columns[3] == "\t\t":
                columns[3] = "n"
            if columns[4] == "\t\t":
                columns[4] = "n"
            if columns[5] == "\t\t":
                columns[5] = "n"
            if columns[6] == "\t\t":
                columns[6] = "n"
            if columns[7] == "\t\t":
                columns[7] = "n"
            if columns[8] == "\t\t":
                columns[8] = "n"
            if columns[9] == "\t\t":
                columns[9] = "n"
            #if columns[10] == "\n":
            #    del columns[10]
        cleaning = 1
        cleaning_place = -1
        while cleaning == 1:
            cleaning_place += 1
            if cleaning_place >= len(columns):
                cleaning = 0
                break
            columns[cleaning_place] = columns[cleaning_place].strip("\t")              

        #columsstr = columns
        columnsstr = "    ".join([str(elem).strip("\t") for elem in columns])
        columnsstr = columnsstr.strip("\n")
        columnsstr = columnsstr.strip()
        #if file_place <= 200:
            #print(columnsstr)
            #print(repr(columnsstr))
        #del columnstrim[0]
        taxid2taxonomy[str(columns[0].strip("\t"))] = columnsstr
        #print(columnsstr)
    #print(columnsstr)
    #print(repr(columnsstr))
    taxid2taxonomy_file.close()

def Get_Taxonomy(taxid_file, taxonomy_file, taxonomy_error_file):

    parsing = 1
    cutoff = 0
    taxid_count = 0
    taxIDs = []
    query_numbers = []
    queries = []
    sequence_IDs = []
    taxid_file = open("output/" + taxid_file, "r")
    taxonomy_file = open(taxonomy_file, "w")
    taxonomy_error_file = open(taxonomy_error_file, "w")
    while parsing == 1:
        cutoff += 1
        if cutoff == 2:
            parsing = 0
            #print("That's it!")
            break
        for line in taxid_file:
            taxid_count += 1
            columns = line.split()
            query_place = columns[0]
            query_numbers.append(query_place)
            query = columns[2]
            queries.append(query)
            taxID = str(columns[1].strip("\n"))
            taxIDs.append(taxID)
            sequence_ID = str(columns[3].strip("\n"))
            sequence_ID = str(columns[3].strip("    "))
            sequence_IDs.append(sequence_ID)
    taxid_file.close()

    place = -1
    read_dictionary = 1
    while read_dictionary == 1:
        place += 1
        if place >= len(taxIDs):
            read_diciontary = 0
            #print("That's it! We're done!")
            #taxonomy_file.write("We are done.")
            taxonomy_file.close()
            taxonomy_error_file.close()
            break
        try:
            taxonomy_file.write(query_numbers[place] + "    " + queries[place] + "    " + str(taxid2taxonomy[taxIDs[place]]) + "    " + str(sequence_IDs[place]) + "\n")
        except KeyError:
            taxonomy_error_file.write(query_numbers[place] + "    " + str(taxIDs[place]) + "    " + repr(taxIDs[place]) + "    " + str(sequence_IDs[place]) + "\n")

    taxid_file.close()
    taxonomy_file.close()
    taxonomy_error_file.close()
    taxIDs.clear()

# Not Done
#def galaxy_taxonomy_format():
#    print("radda")
    
#def taxonomic_summary():
    # "Taxonomic Representation"
#    print("radda")

# Convert to Krona Format
# TAXONOMIC SUMMARY + GALAXY TAXONOMIC FORMAT = KRONA
# Not Done

def make_krona_format():
    global source_file_name
    global working_file_name
    global world_steps

    ### TESTING TESTING TESTING ###
    #working_file_name = "output/Step10_bison1_paired_sample_Copy_condensed_best_hits.txt"
    #world_steps = 11
    ### TESTING TESTING TESTING ###
    
    ofile = open(working_file_name, "r")
    outputfilename = source_file_name.replace(".fastq", "_Krona_format.tabular")
    outputfilename = ("Step" + str(world_steps) + "_" + outputfilename)
    world_steps += 1
    #print(ofile)
    outputfile = open("output/" + outputfilename, "w")
    bacteriaoutputfile = open("output/bacteria_" + outputfilename, "w")
    virusoutputfile = open("output/viruses_" + outputfilename, "w")
    archaeaoutput = open("output/archaea_" + outputfilename, "w")
    elseoutput = open("output/others_" + outputfilename, "w")
    print("")
    print("Krona Formatter is running...")
    print("Output is: " + outputfilename)
    #print(world_steps)
    #working_file_name = outputfilename
    #print(working_file_name)
    #print(outputfile)

    # Multiples
    for line in ofile:
        columns = line.split("\t")
        #print("columns:")
        #print(columns)
        #print(columns)
        del columns[0]
        del columns[0]
        del columns[0]
        columns[0] = "1"
        #print("columns deleted:")
        #print(columns)
        reverse_columns = columns.copy()
        reverse_columns.reverse()
        #print(reverse_columns)
        del reverse_columns[-1]
        #print("reverse columns:")
        #print(reverse_columns)
        reverse_columns[0] = reverse_columns[0].replace("\n", "")
        columnsstr = "\t".join([str(elem).strip("\t") for elem in reverse_columns])
        if reverse_columns[0] == "Eukaryota":
            outputfile.write(str(columns[0]) + "\t" + columnsstr + "\n")
        elif reverse_columns[0] == "Bacteria":
            bacteriaoutputfile.write(str(columns[0]) + "\t" + columnsstr + "\n")
        elif reverse_columns[0] == "Viruses":
            virusoutputfile.write(str(columns[0]) + "\t" + columnsstr + "\n")
        elif reverse_columns[0] == "Archaea":
            archaeaoutput.write(str(columns[0]) + "\t" + columnsstr + "\n")
        else:
            elseoutput.write(str(columns[0]) + "\t" + columnsstr + "\n")

    ofile.close()
    working_file_name = working_file_name.replace("condensed_best_hits.txt", "singles_get_taxonomy.txt")
    ofile = open(working_file_name, "r")

    #Singles
    for line in ofile:
        columns = line.split("    ")
        #print("columns:")
        #print(columns)
        del columns[-1]
        del columns[0]
        del columns[0]
        del columns[0]
        #print("columns deleted:")
        #print(columns)
        reverse_columns = columns.copy()
        del reverse_columns[0]
        reverse_columns.reverse()
        #print("reverse columns:")
        #print(reverse_columns)
        columnsstr = "\t".join([str(elem).strip("\t") for elem in reverse_columns])
        if reverse_columns[0] == "Eukaryota":
            outputfile.write("1" + "\t" + columnsstr + "\t" + columns[0] + "\n")
        elif reverse_columns[0] == "Bacteria":
            bacteriaoutputfile.write(str(columns[0]) + "\t" + columnsstr + "\n")
        elif reverse_columns[0] == "Viruses":
            virusoutputfile.write(str(columns[0]) + "\t" + columnsstr + "\n")
        elif reverse_columns[0] == "Archaea":
            archaeaoutput.write(str(columns[0]) + "\t" + columnsstr + "\n")
        else:
            elseoutput.write(str(columns[0]) + "\t" + columnsstr + "\n")
            
    ofile.close()
    outputfile.close()
    working_file_name = "output/" + outputfilename
    print("Krona Formatter is done!!!")


# Krona Chart
# Makes the Krona Chart
def krona_chart():
    global source_file_name
    global working_file_name
    global world_steps

    ofile = open(working_file_name, "r")
    outputfilename = source_file_name.replace(".fastq", "_Krona")
    outputfilename = ("Step" + str(world_steps) + "_" + outputfilename)
    world_steps += 1
    #print(ofile)
    #outputfile = open("output/" + outputfilename, "w")
    #print("")
    #print("Output is: " + outputfilename)
    #print(world_steps)
    working_file_name = outputfilename
    #print(working_file_name)
    print("")
    print("Krona Chart is running...")
    print("Output is: " + outputfilename)


    Dataset = "Organisms"

    xl = win32com.client.Dispatch("Excel.Application")
    xl.Application.visible = False
    xl.DisplayAlerts = False
    #wb = xl.Workbooks.Open(os.path.abspath(r"D:\ExcelwPython\supporting\Krona.xltm"))
    wb = xl.Workbooks.Open(os.path.abspath("supporting_programs\Krona\Krona.xltm"))
    wb.Application.Run(r"clearChart")

    #file = open("data/taxonomy_descent.txt", "r")
    ws = wb.Worksheets("Krona")
    numbery = 3
    numberx = 0

    for line in ofile:
        numbery += 1
        cell = "A" + str(numbery)
        columns = line.split("\t")
        #print(columns)
        ws.Range(cell).Value = "Organisms"
        ws.Range("B" + str(numbery)).Value = columns[0]
        ws.Range("D" + str(numbery)).Value = "Domain: " + columns[1]
        ws.Range("E" + str(numbery)).Value = "Kingdom: " + columns[2]
        ws.Range("F" + str(numbery)).Value = "Phylum:" + columns[3]
        ws.Range("G" + str(numbery)).Value = "Class: " + columns[4]
        ws.Range("H" + str(numbery)).Value = "Order: " + columns[5]
        ws.Range("I" + str(numbery)).Value = "Family: " + columns[6]
        ws.Range("J" + str(numbery)).Value = "Genus: " + columns[7]
        ws.Range("K" + str(numbery)).Value = "Species: " + columns[8]
    ws.Range("D2").Value = "Organisms"
    #outputfilename = outputfilename.replace(".html", "")
    #print(r"C:\Users\tseri\Desktop\Bioinformatics Work\Bioinformatics LLC\Bailey Pipeline\The Bailey Pipeline Program\output\\" + outputfilename)
    #wb.SaveAs(r"C:\Users\tseri\Desktop\Bioinformatics_Work\Bioinformatics_LLC\Bailey_Pipeline\The_Bailey_Pipeline_Program\output\\" + outputfilename)
    wb.SaveAs(r"C:\Users\tseri\Desktop\Bioinformatics Work\Bioinformatics_LLC\Bailey_Pipeline\The_Bailey_Pipeline_Program\output\TheChart")
    wb.Application.Run(r"createChart")
    xl.Application.Quit()
    ofile.close()
    print("Krona chart is done!!")
    print("")

# Open Files Function
# This function is used to choose the file that will be run through the pipeline
# done enough but needs work
def open_files():
    # Clear the screen
    os.system("cls")

    # Begin the function
    open_menu = True
    while open_menu == True:

        # Make a storage directory for input
        try:
            os.makedirs("input/")
            print("Input directory created. Input files should be stored here for use.")
        except FileExistsError:
            print("Input directory exists. Input files should be stored here for use.")

        # Make a storage directory for output
        try:
            os.makedirs("output/")
            print("Output directory created. Output files will be stored here.")
        except FileExistsError:
            print("Output directory exists. Output files will be stored here.")

        # Ask the user for input
        print("")
        print("Please choose two FASTQ files that need to be paired in order to begin the pipeline.")
        print("Or choose a paired file in order to begin processing.")
        print("What would you like to do?")
        print("")
        print("[1] - Begin processing by pairing two files.")
        print("[2] - Begin processing with an already paired file.")
        print("[0] - Exit.")
        print("")
        open_menu_selection = input("Please choose one of the options: ")

        # Handle a selection
        if open_menu_selection == "1":
            file_list = []
            selection_list = []
            os.chdir("input/")
            cwd = os.getcwd()
            for file in os.listdir(str(cwd)):
                if file != ".py":
                    file_list.append(file)
            selection_list.extend(range(1, (len(file_list) + 1)))
            os.chdir("..")
            display_menu_selection = True
            # Clear the screen
            os.system("cls")
            while display_menu_selection == True:
                place = -1
                printing = 1
                print("Which file  would you like to choose?")
                print("If you would like to exit, press [0].")
                print("The available files are listed below:")
                print("")
                while printing == 1:
                    place += 1
                    if place >= len(selection_list):
                          printing = 0
                          print("")
                          print("[0] - Exit")
                          print("")
                          break
                    print("[" + str(selection_list[place]) + "] - " + str(file_list[place]))

                print("Which file would you like to use?")
                file_selection = input("Please choose one from the list: ")

                # Exit the program
                if file_selection == "0":
                    open_menu_selection == "0"
                    exiting = 1
                    display_menu_selection = False
                    # Clear the screen
                    os.system("cls")

        # Handle selection to begin pipeline with an already paired file
        if open_menu_selection == "2":
            file_list = []
            selection_list = []
            os.chdir("input/")
            cwd = os.getcwd()
            for file in os.listdir(str(cwd)):
                if file != ".py":
                    file_list.append(file)
            selection_list.extend(range(1, (len(file_list) + 1)))
            os.chdir("..")
            display_menu_selection = True
            
            # Clear the screen
            os.system("cls")
            
            while display_menu_selection == True:
                place = -1
                printing = 1
                print("Which file  would you like to choose?")
                print("If you would like to exit, press [0].")
                print("The available files are listed below:")
                print("")
                while printing == 1:
                    place += 1
                    if place >= len(selection_list):
                          printing = 0
                          print("")
                          print("[0] - Exit")
                          print("")
                          break
                    print("[" + str(selection_list[place]) + "] - " + str(file_list[place]))

                print("Which file would you like to use?")
                file_selection = input("Please choose one from the list: ")
                print("")
                
                # Clear the screen
                os.system("cls")

                # Exit the program
                if file_selection == "0":
                    open_menu_selection == "0"
                    exiting = 1
                    display_menu_selection = False
                    
                    # Clear the screen
                    os.system("cls")

                # Show user the file selection
                print("You have chosen " + "[" + str(file_selection) + "]" + " " + str(file_list[int(file_selection) - 1]))
                print("Okay then, we will use this file.")
                global source_file_name
                source_file_name = file_list[int(file_selection) - 1]
                global working_file_name
                working_file_name = source_file_name
                global world_steps
                world_steps = 1
                display_menu_selection = False
                open_menu = False
                break


        # Exit the program
        if open_menu_selection == "0":
            exiting = 1

            # Make sure the user really wants to exit the program
            # Clear the screen
            os.system("cls")
            print("You have chosen: [" + str(open_menu_selection) + "]")
            while exiting == 1:
                print("Are you sure you want to exit?")
                print("")
                print("[y] - Yes.")
                print("[n] - No.")
                print("")
                
                # Ask for a selection
                exit_selection = input("Please choose one of the options: ")
                
                # Handle the exit selection
                if exit_selection == "y":
                    exit()
                if exit_selection == "n":
                    os.system("cls")
                    print("You have chosen: [" + str(exit_selection) + "]")
                    print("Oh, nevermind then.")
                    print("We will not exit.")
                    print("")
                    exiting = 0
                if exit_selection != "y" and exit_selection != "n":
                    os.system("cls")
                    print("You have chosen: [" + str(exit_selection) + "]")
                    print("That is not a proper selection.")
                    print("Please choose from the list of options.")
                    print("")

        # Handle an improper selection
        if open_menu_selection != "0" and open_menu_selection != "1" and open_menu_selection != "2":
            print("That is not a proper selection.")
            print("Please choose from the list of options.")
            print("")

def pipeline():
    global source_file_name
    global working_file_name
    global steps
    open_files()
    #pair_reads() #############################
    remove_by_length() # probably okay lol
    deduplicator() # okay
    tFilter() # okay
    #remove_low_quality_reads() # okay
    solexa_qa_plus_plus() # okay # Temporarily removed this step for Ion Torrent FASTQ files
    fastq_to_fasta() # okay
    count_fasta_lengths() # okay
    megablast() # okay
    best_hits() # okay
    #count_fasta_lengths_again() # This is probably not needed
    taxonomic_ids() # okay
    taxonomic_lineage() # okay
    condense_taxonomic_lineage() # okay
    make_krona_format() # okay? minor issue with condensed information species
    krona_chart() # close enough
    #galaxy_taxonomy_format()
    #taxonomic_summary()
    #krona_format()
    # Krona Chart

def main():
    # Clear the screen
    os.system("cls")
    
    running = 1
    while running == 1:
        
        # Display the main menu
        print("---------------")
        print("Bailey Pipeline")
        print("---------------")
        print("")
        print("Hello.")
        print("What would you like to do?")
        print("")
        print("[1] - Process Soil DNA.")
        print("[0] - Exit the Program.")
        print("")

        # Ask for a selection
        menu_selection = input("Please choose one of the options: ")

        # Handle an improper selection
        if menu_selection != "0" and menu_selection != "1":
            # Clear the screen
            os.system("cls")
            
            print("You have chosen: [" + str(menu_selection) + "]")
            print("That is not a proper selection.")
            print("Please choose from the list of options.")
            print("")
            
        # Exit the program if selected
        if menu_selection == "0":
            exiting = 1

            # Make sure the user actually wants to exit
            # Clear the screen
            os.system("cls")
            
            print("You have chosen: [" + str(menu_selection) + "]")
            while exiting == 1:
                print("Are you sure you want to exit?")
                print("")
                print("[y] - Yes.")
                print("[n] - No.")
                print("")

                # Ask for a selection
                exit_selection = input("Please choose one of the options: ")
                print("")

                # Handle the exit selection
                if exit_selection == "y":
                    exit()
                if exit_selection == "n":
                    os.system("cls")
                    print("You have chosen: [" + str(exit_selection) + "]")
                    print("Oh, nevermind then.")
                    print("We will not exit.")
                    print("")
                    exiting = 0
                if exit_selection != "y" and exit_selection != "n":
                    os.system("cls")
                    print("You have chosen: [" + str(exit_selection) + "]")
                    print("That is not a proper selection.")
                    print("Please choose from the list of options.")
                    print("")

        # Start the program
        if menu_selection == "1":
            pipeline()
            
                

if __name__ == "__main__":
    main()
