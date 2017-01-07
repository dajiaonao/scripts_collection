///////////////////////////
///
/// Contact: Dongliang Zhang <zdl.linqi@gmail.com>
///
/// To-do:
//    * Branch list configuration from cmd line
//    * Status print out
//    * Tree name configuration from cmd line
//
//  Usage:
//  - compile:
//  g++ -Wno-deprecated -std=c++11 -I/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/x86_64/root/6.04.14-x86_64-slc6-gcc49-opt/include -L/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/x86_64/root/6.04.14-x86_64-slc6-gcc49-opt/lib -lGui -lCore -lRIO -lNet -lHist -lGraf -lGraf3d -lGpad -lTree -lRint -lPostscript -lMatrix -lPhysics -lMathCore -lThread -pthread -lm -ldl -rdynamic -o skim_chain skim_chain.C
//
// Example:
// ./skim_chain -t JPsiTPReco/Trees/IDProbes_JPsi_OC/TPTree_IDProbes_JPsi_OC -s "tag_matched_HLT_mu6_bJpsi_Trkloose==1" -o test1.root -l flist1.list -b branches.conf
//
// Note:
//  * lines in the conf files starting with '#' will be skipped
//
///////////////////////////

#include <unistd.h> //getopt
#include <iostream>
#include <vector>
#include <fstream>
#include <TChain.h>
#include <TEntryList.h>
#include <TFile.h>

using namespace std;

int skim_chain(TChain& oldtree, TString selection="", TString outFileName="skimmed.root", string bListName=""){

  Long64_t chainEntries = oldtree.GetEntries();
  if(chainEntries==0){
    cout << "Empty chain -- will do nothing" << endl;
    return -1;
  }

  cout << "Working on chain: " << oldtree.GetName() << endl;
  cout << "with selection  : " << selection << endl;
  cout << "and output is   : " << outFileName << endl;

  // get entry list
  oldtree.Draw(">>elist",selection, "entrylist");
  TEntryList *elist = (TEntryList*)gDirectory->Get("elist");

  Long64_t listEntries = elist->GetN();
  cout << listEntries << "/" << chainEntries << " will be save in the new tree" << endl;

  /// set branch names if given
  if(bListName!=""){
    oldtree.SetBranchStatus("*", 0);

    ifstream infile(bListName);
    string brname;
    while(infile >> brname){
      if(brname=="" || brname[0]=='#') continue;
//       cout << brname << endl;
      oldtree.SetBranchStatus(brname.c_str(), 1);
     }
   }

  /// start copying
  TFile *newfile = new TFile(outFileName,"recreate");
  TTree *newtree = oldtree.CloneTree(0);
  for(Long64_t el =0;el<listEntries;el++) {
    oldtree.GetEntry(elist->GetEntry(el));
//     cout << el << "/" << elist->GetEntry(el) << endl;

    newfile->cd();
    newtree->Fill();
    newfile = newtree->GetCurrentFile();
   }

  newtree->Write();

  return 0;
};



int skim_chain1(TString chainFiles="", TString selection="", TString outFileName="skimmed.root"){

  if(chainFiles==""){
    cout << "Empty chain -- will do nothing" << endl;
    return -1;
  }

  cout << "Working on chain: " << chainFiles << endl;

  /// first create the chain
  TChain oldtree;
  oldtree.Add(chainFiles);
  return skim_chain(oldtree, selection, outFileName);
};

int main(int argc, char *argv[]){
//   TString filenames("");
  TString selections("");
  TString outname("mySkimOut.root");
  TChain* ch(nullptr);
  std::string bListName;
  std::vector< TString > fList;

  /// prase the arguments
  int c;
  while((c=getopt(argc,argv,"hb:s:f:l:t:o:d:")) != -1){
    switch(c){
      case 'h':
        std::cout << "Usage: " << argv[0]
          << " [-h]"
          << " [-b branch list]" 
          << " [-f file1,file2...]"
          << " [-l fileList.txt ]"
          << " [-t tree name ]"
          << " [-r runN ]"
          << " [-d dirTag ]"
          << std::endl;
        exit(0);
        break;
      case 'b': // branch list
        bListName = optarg;
        break;
      case 's': // selection cuts
        selections = optarg;
        break;
      case 'o': // output file name
        outname = optarg;
        break;
      case 't': // tree name
        ch = new TChain(optarg);
        break;
      case 'l': // filelist
       {
        std::ifstream infile(optarg);
        std::string filename;
        while(infile >> filename)
         {
          if(filename=="" || filename[0]=='#') continue;
          TString tmp(filename);
          fList.push_back(tmp);
         }
       }
        break;
      case 'd': // files in directory
        cout << "-d not implemented yet!" << endl;
        break;
      case 'f':  // tree patern
       {
        std::string argStr = optarg;
        for(size_t i=0,n; i < argStr.length(); i=n+1){
          n = argStr.find_first_of(',',i);
          if(n == std::string::npos) n = argStr.length();
          TString tmp(argStr.substr(i,n-i));
          fList.push_back(tmp);
         }
       }
        break;
      default: break;
    }
  }

  if(!ch) ch = new TChain();
  for(auto& f: fList) ch->Add(f);
//   cout << filenames << " / " << selections << " / " << outname << endl;

  return skim_chain(*ch,selections,outname,bListName);

}

int main1(int argc, char *argv[]){
  TString filenames(argc>1?argv[1]:"");
  TString selections(argc>2?argv[2]:"");
  TString outname(argc>3?argv[3]:"mySkimOut.root");

  cout << filenames << " / " << selections << " / " << outname << endl;

  return skim_chain1(filenames,selections,outname);

}
