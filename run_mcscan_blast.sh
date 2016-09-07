Q=pep.fa
T=pep.fa
N=Ca2Ca
blastall -i ${Q} -d ${T} -p blastp -e 1e-10 -b 5 -v 5 -m8 -o ${N}.blast.pre -a 5
