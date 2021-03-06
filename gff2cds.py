from __future__ import print_function
import pandas as pd
import numpy as np
import sys
import kang
def rev_comp(strSeq):
	dicComp = {'A':'T','T':'A','G':'C','C':'G','N':'N'}
	strCseq = ''
	for i in strSeq:
		try:
			strCseq += dicComp[i.upper()]
		except KeyError:
			strCseq += 'N'
	# End of for i
	return(strCseq[::-1])

file_fa = sys.argv[1] #'/ref/analysis/Cre/ref/Creinhardtii_281_v5.0.fa'

bulk = open(file_fa).read()
bulk = bulk.split('>')
dicHD2seq = {}
for each_bulk in bulk:
    if each_bulk.strip() == '':
        continue
    genename = each_bulk.split('\n')[0].strip()
    seq      = ''.join(each_bulk.split('\n')[1:])
    dicHD2seq[genename] = seq
#print(dicHD2seq.keys())
file_gff    = sys.argv[2] #'/ref/analysis/stringtie.addcds/my_csv.csv.addgene.gff3.sort.gff3'
df_gff      = pd.read_csv(file_gff,sep='\t',header=None,comment='#')
mask        = (df_gff[2] == 'gene')
df_gff_gene = df_gff[mask]      
df_gff_gene['genename'] = df_gff[8].apply(lambda x: kang.infoparse(x)['ID'])
mask                    = (df_gff[2] == 'CDS')
df_gff_cds              = df_gff[mask]      
df_gff_cds['genename']  = df_gff_cds[8].apply(lambda x : kang.infoparse(x)['Parent'])
df_gff_cds_index        = df_gff_cds.set_index('genename')
df_gff_cds_index        = df_gff_cds_index.sort([3], ascending=[1])

i = 0
dic = {'transcriptname' : [],
       'strand' : [],
       'CDSloc' : [],
       'CDSseq' : []}
for genename in set(df_gff_cds_index.index):
    
    dic['transcriptname'].append(genename)
    
    edf = df_gff_cds_index.loc[genename]
    if str(type(edf)) == "<class 'pandas.core.frame.DataFrame'>":
        CDS_list = zip(list(edf[3]),list(edf[4]))
        chromosome = edf[0][0]
        strand     = edf[6][0]
    else:
        CDS_list = zip([edf[3]],[edf[4]])
        chromosome = edf[0]
        strand     = edf[6]
    
    dic['strand'].append(strand)
    cdsseq = ''
    for l,r in CDS_list:
        #print l,r
        cdsseq += dicHD2seq[chromosome][l-1:r]
    if strand == '+':
        pass
    else: 
        cdsseq = rev_comp(cdsseq)
    dic['CDSloc'].append(CDS_list)
    dic['CDSseq'].append(cdsseq)

df_cds               = pd.DataFrame(dic)
df_cds['transcript'] = df_cds['transcriptname'].apply(lambda x : x.split('.')[1])
df_cds['gene']       = df_cds['transcriptname'].apply(lambda x : x.split('.')[0])
df_cds_index         = df_cds.set_index(['gene','transcript'])

with open('cds.fa','w') as f:
    for ix in df_cds_index.index:
        sub_df = df_cds_index.loc[ix]
        print(sub_df)
        header = sub_df['transcriptname']
        seq    = sub_df['CDSseq']
        print('>'+header,file=f)
        print(seq,file=f)




