# coding=UTF-8
import os


'''
Multiple sequence alignment of fasta files merged with uniprot and pdb in input_path 
The result is saved to the uniprotId_pdbchain_aln folder with the file name xxx_merge.aln 
Then compare the sequences of pdb and uniprot to find the corresponding position for feature selection.
'''

input_path = '../Datasets/fasta/uniprot_pdbchain_fastas'
output_path = './uniprotId_pdbchain_aln'
input_file_names = os.listdir(input_path)
print(len(input_file_names))
i = 0
# for file_name in input_file_names:
file_name = 'P06241.fasta'
# input_file = input_path + '/' + file_name
input_file = './' + file_name
# output_file = output_path + '/' + file_name.split('.')[0] + '_merge.aln'
output_file = 'P06241_merge.aln'
# cmdr = os.system('clustalo -i %s --seqtype=Proteins_pairs -o %s'% (input_file, output_file))  # linux
cmdr = os.system('clustalo.exe -i %s --seqtype=Proteins_pairs -o %s --force'% (input_file, output_file))  # windows
i += 1
print(i)
if cmdr != 0:  # If there is error printing information
	print(file_name)
	print(i)



