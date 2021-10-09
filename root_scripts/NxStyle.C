{
  auto nvdex = new TStyle("Nx","Nx style");

  nvdex->SetCanvasBorderMode(0);
  nvdex->SetPadBorderMode(0);
  nvdex->SetPadColor(0);
  nvdex->SetCanvasColor(0);
  nvdex->SetPadRightMargin(0.05);
  nvdex->SetPadTopMargin(0.05);
  nvdex->SetPadLeftMargin(0.1);
//   nvdex->SetTitleColor(0);
  nvdex->SetStatColor(0);
  nvdex->SetOptTitle(0);
  nvdex->SetOptStat(0);
  nvdex->SetOptFit(1111);
  nvdex->SetLegendBorderSize(0);
//   nvdex->SetHistFillStyle(0);
//   nvdex->SetHistFillColor(2);
  nvdex->SetFillStyle(0);
  nvdex->SetLineWidth(1);
  nvdex->SetHistLineWidth(2);
  nvdex->SetMarkerStyle(4);
//   nvdex->SetNdivisions(506, "XYZ");
  nvdex->SetNdivisions(507, "XYZ");
  nvdex->SetPalette(55);

  nvdex->SetPadTickX(1);
  nvdex->SetPadTickY(1);
  gROOT->SetStyle("Nx");
  gROOT->ForceStyle();

  cout << "-------------------------------------" << endl;  
  cout << "Using Nx style"                        << endl;
  cout << "-------------------------------------" << endl;  
 
  return 0;
}
