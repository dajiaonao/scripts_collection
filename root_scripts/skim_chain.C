///////////////////////////
///
/// Contact: Dongliang Zhang <zdl.linqi@gmail.com>
///
/// To-do:
//    * Branch list configuration from cmd line
//    * Status print out
//    * Tree name configuration from cmd line
//
///////////////////////////

#include <iostream>
#include <TChain.h>
#include <TEntryList.h>
#include <TFile.h>
using std::cout;
using std::endl;

int skim_chain(TString chainFiles="", TString selection="", TString outFileName="skimmed.root"){

  if(chainFiles==""){
    cout << "Empty chain -- will do nothing" << endl;
    return -1;
  }

  cout << "Working on chain: " << chainFiles << endl;
  cout << "with selection  : " << selection << endl;
  cout << "and output is   : " << outFileName << endl;

  /// first create the chain
  TChain oldtree;
  oldtree.Add(chainFiles);

  // get entry list
  oldtree.Draw(">>elist",selection, "entrylist");
  TEntryList *elist = (TEntryList*)gDirectory->Get("elist");

  Long64_t listEntries = elist->GetN();
  Long64_t chainEntries = oldtree.GetEntries();
  cout << listEntries << "/" << chainEntries << " will be save in the new tree" << endl;

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

int main(int argc, char *argv[]){
  TString filenames(argc>1?argv[1]:"");
  TString selections(argc>2?argv[2]:"");
  TString outname(argc>3?argv[3]:"mySkimOut.root");

  cout << filenames << " / " << selections << " / " << outname << endl;

  return skim_chain(filenames,selections,outname);
}
