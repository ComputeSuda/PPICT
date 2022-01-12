#  Write the fasta of the protein to the file
#  proteinID    fasta
import os

Inter_proteins_file = '../Proteins/inter_cross_talk_proteins(dul).txt'
Protein_fasta_file_path = './uniprot_fastas/'

Proteins_fasta_files = os.listdir(Protein_fasta_file_path)
Proteins = []
Proteins_fastas = dict()

with open(Inter_proteins_file, 'r', encoding='utf-8') as f1:
    lines = f1.readlines()[1:]
    for line in lines:
        Proteins.append(line.strip('\n'))


def read_fasta(filepath):
    fastas = ''
    with open(filepath, 'r') as f:
        lines = f.readlines()[1:]
        for line in lines:
            fastas += line.strip('\n')
    return fastas


for Protein in Proteins:
    Proteins_fastas[Protein] = read_fasta(Protein_fasta_file_path+Protein+'.fasta')

print(len(Proteins_fastas))

with open('./Protein_fatas_dict.tsv', 'a') as f2:
    for key, value in Proteins_fastas.items():
        f2.write(key+'\t'+value+'\n')