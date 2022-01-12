library(bio3d)
library(igraph)

files <- dir('../PDB')

for(pdb_name in files)
{
  pdb_file <- paste('../PDB/',pdb_name,sep = "")
  out_file <- paste('./',substring(pdb_name,1,4),'.txt',sep = "")
  if (file.exists(out_file))
  {
    next
  }
  pdb <- read.pdb(pdb_file)
  print(pdb)
  print(pdb_file)
  modes <- nma(pdb)
  cij <- dccm(modes)
  net <- cna(cij, cutoff.cij=0.3)
  # print(net)
  
  bet <- betweenness(net$network)
  clo <- closeness(net$network)
  deg <- degree(net$network)
  clu <- transitivity(net$network,type="local")
  div <- diversity(net$network)
  ecc <- eccentricity(net$network)
  str <- strength(net$network)
  eig <- eigen_centrality(net$network)
  pr <- page_rank(net$network)
  
  #write.table('betweenness', out_file, append=TRUE,row.names=FALSE,col.names=FALSE)
  #write.table(bet, out_file,append=TRUE,col.names=FALSE)
  #write.table('closeness', out_file, append=TRUE,row.names=FALSE,col.names=FALSE)
  #write.table(clo, out_file,append=TRUE,col.names=FALSE)
  #write.table('degree', out_file, append=TRUE,row.names=FALSE,col.names=FALSE)
  #write.table(deg, out_file,append=TRUE,col.names=FALSE)
  #write.table('cluster', out_file, append=TRUE,row.names=FALSE,col.names=FALSE)
  #write.table(clu, out_file,append=TRUE,col.names=FALSE)
  #write.table('diversity', out_file, append=TRUE,row.names=FALSE,col.names=FALSE)
  #write.table(div, out_file,append=TRUE,col.names=FALSE)
  #write.table('eccentricity', out_file, append=TRUE,row.names=FALSE,col.names=FALSE)
  #write.table(ecc, out_file,append=TRUE,col.names=FALSE)
  #write.table('strength', out_file, append=TRUE,row.names=FALSE,col.names=FALSE)
  #write.table(str, out_file,append=TRUE,col.names=FALSE)
  #write.table('eigen_centrality', out_file, append=TRUE,row.names=FALSE,col.names=FALSE)
  #write.table(eig$vector, out_file,append=TRUE,col.names=FALSE)
  #write.table('page_rank', out_file, append=TRUE,row.names=FALSE,col.names=FALSE)
  #write.table(pr$vector, out_file,append=TRUE,col.names=FALSE)
  # break
}
