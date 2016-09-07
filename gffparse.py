#!/usr/bin/python3 
import sys
file_gff = sys.argv[1] #'Athaliana_167_gene.gff3'
Outfile = open(sys.argv[2],'w')
for line in open(file_gff):
	if line[0] == '#' or line.strip() == '':
		continue
	cell = line.strip().split('\t')
	strChr = cell[0].replace('scaffold_','s').replace('Scaffold','s')
	strL1	= cell[3]
	strL2	= cell[4]
	strTP	= cell[2]
	if strTP == 'mRNA':
		keys 	= [x.split('=')[0] for x in cell[-1].split(';')]
		values 	= [x.split('=')[1] for x in cell[-1].split(';')]
		dic	= dict(zip(keys,values))
		strTGN 	= dic['ID']
		print(strChr, strTGN, strL1, strL2,sep='\t',file=Outfile)
