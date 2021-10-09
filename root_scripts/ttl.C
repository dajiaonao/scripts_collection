// string getHeader(string filename){
//   /// get first line first
//   ifstream infile(filename.c_str());
// 
//   string sLine;
//   if (infile.good())
//    {
//     getline(infile, sLine);
//     cout << "H:" << sLine << endl;
//    }
//   infile.close();
// 
//   /// we have it now. Next: split it and check it's type
//   string buff="";
//   string hd="";
// 
//   const char c=' ';
//   for(int i=0; i<sLine.length(); i++)
//    {
//     char n = sLine[i];
// 
//     if(n==':') return "";
//     if(n != c) buff+=n; else
//     if(n == c && buff != "") { hd+=":"+buff; buff = ""; }
// //     cout << i << " " << n << " " << hd << endl;
//    }
//   if(buff != "") hd+=":"+buff;
// 
//   return hd;
// }

TTree* ttl(string filename, string treename="", string header="", char delimiter=' ')
{
  static int nT = 0;
//   if(treename=="") treename="t"+std::to_string(nT);
//   TTree* t1 = new TTree(treename.c_str(),"a quick look tree");
  TString trName(treename);
  if(trName == "") trName = TString::Format("t%d", nT); 
  TTree* t1 = new TTree(trName,"a quick look tree");

//   cout << getHeader(filename) << endl;
  t1->ReadFile(filename.c_str(), header.c_str(), delimiter);

  if(nT>0){
    t1->SetLineColor(1+nT);
    t1->SetMarkerColor(1+nT);
    t1->SetMarkerStyle(23+nT);
   }
  nT++;

  std::cout << trName << " is build from " << filename << std::endl;
  std::cout << "Use ttl(string filename, string treename=tN) to open another tree." << std::endl;

  return t1;
}
