import os

'''
Read 86 pdbs from RCSB and Alphafold to get the sequence of Pdb chains and save it as pdb_chains_seq.txt
'''

dd = {'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C',
      'GLY': 'G', 'GLN': 'Q', 'GLU': 'E', 'HIS': 'H', 'ILE': 'I',
      'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PRO': 'P', 'PHE': 'F',
      'SER': 'S', 'THR': 'T', 'TYR': 'Y', 'TRP': 'W_Train', 'VAL': 'V'}
standard_amino_acids = ['ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLY', 'GLN', 'GLU', 'HIS', 'ILE',
                        'LEU', 'LYS', 'MET', 'PRO', 'PHE', 'SER', 'THR', 'TRP', 'TYR', 'VAL']

Rcsb_all_pdbs = os.listdir('../Datasets/PDB/RCSB/')
Alphafold_all_pdbs = os.listdir('../Datasets/PDB/Alphafold/')
print(len(Rcsb_all_pdbs), len(Alphafold_all_pdbs))  # 17652

# for pdb in all_pdbs:
#     if len(pdb.split('.')[0]) != 4:
#         print(pdb)

Rcsb_pdbchains = [item.strip('\n') for item in open('../Datasets/PDB/sel_pdbchains.txt', 'r').readlines()]
Alphafold_pdbchains = ['P51451_A', 'Q9UKX2_A', 'P42229_A', 'O75528_A', 'Q05513_A', 'Q9UKI8_A', 'P09769_A', 'O43561_A']  #此处用UniprotId代替pdb，Alphafold中下载的PDB结构文件只有A链

i = 0
# pdb_chain_seq = {}
Rcsb_pdb_path = '../Datasets/PDB/RCSB/'
Alphafold_pdb_path = '../Datasets/PDB/Alphafold/'
pdb_fasta_path = '../Datasets/fasta/pdb_fastas/'


def get_all_pdb_chains(all_pdbs, pdbchains, pdb_path):
    i = 0
    for pdb in all_pdbs:
        # if pdb != '1bcj ':
        # continue
        print(pdb)
        # pdb = '3buw'
        file = pdb_path + '/' + pdb
        chain_seq = {}
        with open(file, 'r') as f:
            for line in f:
                if line[:4] != 'ATOM':
                    continue
                line = line.strip()
                # print(line)
                # break
                chain = line[21]
                sitenum = line[22:28].replace(' ', '')
                residue = line[17:20].replace(' ', '')
                # print(chain, sitenum, residue)
                # break

                if chain == ' ':
                    chain = '-'
                if chain not in chain_seq.keys():
                    chain_seq[chain] = []
                if residue not in standard_amino_acids:
                    continue
                else:
                    value = sitenum + '_' + residue
                    if value not in chain_seq[chain]:
                        chain_seq[chain].append(value)

        # with open('../Datasets/PDB/all_pdb_chain_seq.txt', 'a') as f:
        with open('../Datasets/PDB/all_pdb_chain_seq.txt', 'a') as f:
            for c, seq in chain_seq.items():
                ss = ''
                for s in seq:
                    s = s[-3:]
                    # print(c, s)
                    # print(dd[s])
                    ss += dd[s]
                f.write('>' + pdb.split('.')[0].lower() + '_' + c + ' ' + str(len(ss)) + '\n' + ss + '\n')

        i += 1
        print(i)


get_all_pdb_chains(Rcsb_all_pdbs, Rcsb_pdbchains, Rcsb_pdb_path)
get_all_pdb_chains(Alphafold_all_pdbs, Alphafold_pdbchains, Alphafold_pdb_path)
# get_all_pdb_chains(['6k9l.pdb'], ['6k9l_A'], '../Datasets/PDB/')



