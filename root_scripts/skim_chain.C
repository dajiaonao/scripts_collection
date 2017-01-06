///////////////////////////
///
/// Contact: Dongliang Zhang <zdl.linqi@gmail.com>
///
///////////////////////////

#include <iostream>
#include <TChain.h>
#include <TEntryList.h>
#include <TFile.h>
// #include <gROOT.h>
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

  ///-- start the copy

  /// first create the chain
  TChain oldtree;
  oldtree.Add(chainFiles);

  cout << oldtree.GetEntries() << endl;
  TFile *newfile = new TFile(outFileName,"recreate");
  TTree *newtree = oldtree.CloneTree(0);
//   newfile->cd();

  // get entry list
  oldtree.Draw(">>elist",selection, "entrylist");
  TEntryList *elist = (TEntryList*)gDirectory->Get("elist");
//   oldtree.SetEntryList(elist);
//   elist->Print("v");
//   oldtree.SetBranchStatus("*", 1);

  Long64_t listEntries = elist->GetN();
  Long64_t chainEntries = oldtree.GetEntries();

  cout << listEntries << "/" << chainEntries << " will be save in the new tree" << endl;

  Int_t treenum=0;
  for(Long64_t el =0;el<listEntries;el++) {
    oldtree.GetEntry(elist->GetEntry(el));
    cout << el << "/" << elist->GetEntry(el) << endl;
//      Long64_t treeEntry = elist->GetEntryAndTree(el,treenum);
//      Long64_t chainEntry = treeEntry+oldtree.GetTreeOffset()[treenum];
//      oldtree.GetEntry(chainEntry);
//      cout << el << " -- " << chainEntry << endl;
//      printf("el=%lld, treeEntry=%lld, chainEntry=%lld, treenum=%d\n",el,treeEntry,chainEntry,treenum);

     newfile->cd();
     newtree->Fill();
     newfile = newtree->GetCurrentFile();
//      printf("el=%lld, treeEntry=%lld, chainEntry=%lld, treenum=%d\n",el,treeEntry,chainEntry,treenum);
   }
// }

//   Int_t treenum=0;
//   for(Long64_t el =0;el<GetEntryAndTree(el,treenum);
//      Long64_t chainEntry = treeEntry+ch->GetTreeOffset()[treenum];
//      printf("el=%lld, treeEntry=%lld, chainEntry=%lld, treenum=%d\n",el,treeEntry,chainEntry,treenum);
//   }
// 
//   Long64_t nentries = 
//   cout << elist->GetN() << endl;
// 
//    Long64_t listEntries=myelist->GetN();
//    Long64_t chainEntries = ch->GetEntries();
//    Int_t treenum=0;
//    ch->SetEntryList(myelist);
// 
//   //Create a new file + a clone of old tree in new file
//    for (Long64_t i=0;i<nentries; i++) {
//       oldtree->GetEntry(i);
//       if (event->GetNtrack() > 605) newtree->Fill();
//       event->Clear();
//     }
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
