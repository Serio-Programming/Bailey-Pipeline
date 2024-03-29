# Bailey-Pipeline
This program takes FASTQ or FASTA files, runs basic quality controls on them, then compares the DNA to an NCBI database to return a Krona pie chart displaying the constituent organisms of the sample. <br>
<br>
IMPORTANT: <br>
This document is incomplete and a work in progress. It is intended to guide you on using this program. Your patience is appreciated. <br>
<br>
BACKGROUND: <br>
This is a bit of story about how the program came to be. Skip this part if you're interested in how it actually works/how to run it. <br>
This is the Bailey Pipeline, created to do DNA analysis of soil samples from the Old Vero Man archaeology site. It's named after my pug. <br>
I began working on DNA analysis at Indian River State College sometime in 2018. I was a paid volunteer at the paleontology lab that was set up by the Old Vero Ice Age Sites Committee. <br>
The Committee paid for several excavations of the site, and Professor Robert Lowery and his students collected DNA samples from the soil strata during one excavation. <br>
At the time, I was working at a warehouse taking a gap year from college. I decided to volunteer my time, and found OVIASC from their archaeological display at the Indian River County Administration Building. <br>
My original job was sorting soil samples with an iron pick under a microscope. We took soil samples from the site, poured them into plastic boats, and separated them grain by grain. <br>
The goal of this was to search for charcoal bits; signs of human activity at the site. <br>
We sorted samples into small piles of sand grains, bits of decayed plant matter, charcoal, and other things you'd excpect to find in dirt. <br>
The highlight of this endeavor was when another volunteer, Marlin, discovered an insect leg under the microscope. We began searching for the other pieces. <br>
I was unlucky enough to find the head. A cockroach. I hate cockroaches and was displeased to know that they had inhabited Florida for at least 11,000 years. <br>
For several months I spent many afternoons at the lab. It is a time in my life that I enjoy remembering. <br>
After volunteering for some time and after mentioning that I had learned programming, the laboratory manager, Dave Hawkins, recommended that I ask Professor Lowery if he needed any help on a project of his. <br>
I accepted. Professor Lowery had Excel spreadsheets with hundreds of thousands of lines of DNA accession codes. These codes related to DNA from organisms in the NCBI database. <br>
These codes came from analysis done by a lab on the DNA samples collected by Professor Lowery and his students. The codes needed to be matched in the database. It was unknown what organisms were at the site. <br>
Professor Lowery was having students match codes to organisms manually. <br>
They would copy and paste the codes into the NCBI database, enter them, copy information about the organism, and then paste it into the Excel spreadsheet. <br>
I pointed out that this process could probably be automated. That was my first project. <br>
I don't remember how long it took me, but I was able to write a program that automatically copied an accession code, pasted it into the NCBI database, retrieved information about the organism, and wrote it down. <br>
One of my proudest moments during this time is when NCBI blocked my IP address and told me to stop, as my program was interrupting their traffic too much. I have saved this email. <br>
Over the years, Professor Lowery and I spoke back and forth. He would ask if it was possible to do one thing or another, and I told him that I would try. <br>
With lots of help from Professor Lowery, Professor Christopher Baechle, and Indian River State College, I got to practice my programming skills and develop scripts that yielded useful results. <br>
We hashed out how to remove duplicated reads, how to feed information from the program into SolexaQA++, and how to make use of the Krona pie charts. Among dozens of other things. <br>
This all eventually culminated in the Bailey Pipeline, something I'm very proud of. <br>
I'm happy to have had the opportunity to work with these people over the years. <br>
I got to eat dinner with millionaires, so that was nice too. <br>
This pipeline also resulted in the formation of a small business, Montrant Software and Analysis LLC, as well as lead authorship of a paper, both things that I am extremely grateful for. <br>
The program has been uploaded to GitHub in the way that I've been using it all of this time. Currently, it is pretty ramshackle, and will not work without the other programs that are required to use it (ie. SolexaQA++, Krona, Blastn). This will, hopefully, all be rectified with time. I haven't been able to devote as much time to this project as I would like. Economic realities have gotten in the way for years now. But I have uploaded it here in hopes that someone might find use for it. <br>
Please forgive the state of the code itself, as it could be better. I had to learn it all along the way. I spent years working on this project with what little time I had to spare between jobs, classes, moving, and all the rest of the turbulence that comes with life. <br>
<br>
STEPS IN THE PROCESS: <br>
The actual step by step process of the DNA analysis pipeline is listed here, along with a brief explanations of each step. <br>
Insert information here. <br>
Steps in the pipeline: <br>
1. Open Files <br>
--The program displays the files in the directory that are available for analysis. <br>
2. Remove reads by length <br>
--Reads that are above a certain length are removed. The longer the DNA, the less likely it is to be ancient. This is a parameter that can be changed in the code itself, the exact number depends on what needs to be done (ie. analysis of DNA that is not ancient). <br>
3. Remove duplicated reads <br>
--Duplicated reads are removed so as not to be counted/analyzed twice.
4. Remove reads based on Thymine on their fronts/ends <br>
--insert explanation <br>
5. SolexaQA++ <br>
--insert explanation <br>
6. FASTQ to FASTA <br>
--Converts from FASTQ format to FASTA format (essentially just removes two lines per read). This allows Megablast to be performed on the reads.
7. Count FASTA lengths <br>
--insert explanation <br>
8. Megablast <br>
--insert explanation <br>
9. Best Hits <br>
--For every read, the best matching organism is catalogued. <br>
10. Match taxonomic IDs to hits <br>
--For every read, a taxonomic ID is catalogued. <br>
11. Retrieve taxonomic lineage of hits based on IDs <br>
--The taxonomic IDs are used to trace the entirety of the organism's taxonomic ranks. <br>
12. For reads with multiple best hits, condense the lineage to lowest common taxonomic rank <br>
--For reads that have matched to multiple most likely organisms, the lowest common taxonomic rank is discerned and used as a placeholder (ie. if a read matches equally to chimpanzee, orangutan, and gorilla DNA, it might simply be recorded as Hominidae DNA, depending on specifics). <br>
13. Convert output file to a format that can be used to produce Krona charts <br>
--insert explanation <br>
14. Produce the Krona chart <br>
--insert explanation <br>

DIRECTORY STRUCTURE: <br>
The file directory must align to a specific structure or the program will not work. It is listed here: <br>
Insert information here. <br>
<br>
PROGRAMS NEEDED: <br>
The Bailey Pipeline relies on a few other programs/files to run. It won't work without them. <br>
Please review the "STEPS IN THE PROCESS" and "DIRECTORY STRUCTURE" sections before downloading everything all at once. <br>
The necessary programns/files are listed here:<br>
SolexaQA++ (https://solexaqa.sourceforge.net/) <br>
NT database files (https://ftp.ncbi.nlm.nih.gov/blast/db/) <br>
Krona pie chart template () <br>
<br>
