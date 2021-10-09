void saveC(TString savename, TVirtualPad* c1=0)
{
  TString dname = gSystem->DirName(savename);
  cout << dname << endl;
  gSystem->Exec("mkdir -p "+dname+"/png");

  if(!c1) c1=(TPad*)gPad;
  c1->SaveAs(savename+".eps");
  c1->SaveAs(savename+".pdf");
  c1->SaveAs(savename+".png");
  gSystem->Exec("mv "+savename+".png "+dname+"/png");

  return;
}
