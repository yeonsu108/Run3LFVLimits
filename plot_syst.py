import os
import sys
import ROOT

ROOT.gROOT.SetBatch(ROOT.kTRUE)

input_path = sys.argv[1]

drawNom = True
logy = True
#couplings = ['st_lfv_cs','st_lfv_ct','st_lfv_cv','st_lfv_uv','st_lfv_ut','st_lfv_us']
#couplings = ['st_lfv_cs']
couplings = ['st_lfv_ut']
rootfile_template = 'TOP_LFV_COUPLING_Discriminant_DNN_COUPLING_shapes.root'
process_list_org = ['tt', 'other' ,'singleTop']
#process_list_org = ['tt', 'other' ,'singleTop', 'misID', 'misID_tt']

plot_dir = 'systematics_plots_' + input_path
if drawNom: plot_dir = plot_dir.rstrip('/') + '_nom/'
if not os.path.isdir(plot_dir):
    os.mkdir(plot_dir)


def drawRatio(c, nom, up, dn):
    c.cd()
    ratio_up = up.Clone()
    ratio_up.Divide(nom)
    ratio_up.SetLineColor(ROOT.kRed)
    ratio_dn = dn.Clone()
    ratio_dn.SetLineColor(ROOT.kBlue)
    ratio_dn.Divide(nom)
    legend = ROOT.TLegend(0.25, 0.75, 0.55, 0.9, syst)
    legend.AddEntry(ratio_up, "Up/Nom")
    legend.AddEntry(ratio_dn, "Down/Nom")
    line = ROOT.TLine(-1, 1, 1, 1)
    line.SetLineStyle(2)
    minmax = [ratio_up.GetMaximum(), ratio_up.GetMinimum(), ratio_dn.GetMaximum(), ratio_dn.GetMinimum()]
    tmp_min = min(minmax)
    if tmp_min < 0.01:
        nbins = ratio_up.GetNbinsX()
        contents_org = [ratio_up.GetBinContent(x) for x in range(nbins)]
        contents_org.extend([ratio_dn.GetBinContent(x) for x in range(nbins)])
        contents = contents_org[:]
        #for i in range(len(contents_org)):
        #    if contents_org[i] < 0.1: contents.remove(contents_org[i])
        tmp_min = min(contents)
    ratio_up.GetYaxis().SetRangeUser(tmp_min*0.85, max(minmax)*1.15)
    ratio_up.Draw()
    ratio_dn.Draw('same')
    legend.Draw()
    line.Draw()
    c.Print(os.path.join(plot_dir, plot_name + '.pdf'))
    c.Print(os.path.join(plot_dir, plot_name + '.png'))


def drawComp(c, nom, up, dn, lowstat):

    print("In drawComp")
    c.cd()
    pad1 = ROOT.TPad("pad1", "pad1", 0.0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0.02)
    pad1.Draw()
    c.cd()  # returns to main canvas before defining pad2
    pad2 = ROOT.TPad("pad2", "pad2", 0.0, 0.0, 1, 0.28)
    pad2.SetBottomMargin(0.3)
    pad2.SetTopMargin(0.02)
    pad2.SetGridy()
    pad2.Draw()

    pad1.cd()
    nom_ = nom.Clone()
    up_ = up.Clone()
    dn_ = dn.Clone()
    nom_.SetLineColor(ROOT.kBlack)
    up_.SetLineColor(ROOT.kRed)
    dn_.SetLineColor(ROOT.kBlue)
    max_list = [nom_.GetMaximum(), up_.GetMaximum(), dn_.GetMaximum()]
    if not logy: nom_.GetYaxis().SetRangeUser(0.0, max(max_list) * 1.25)
    else:        nom_.GetYaxis().SetRangeUser(0.1, max(max_list) * 20)

    nom_.GetXaxis().SetTitleSize(0.0)
    nom_.GetYaxis().SetTitle('Events')
    nom_.GetYaxis().SetTitleSize(0.06)
    nom_.GetYaxis().SetTitleOffset(0.7)

    nom_.Draw('hist')
    if lowstat:
      up_.Draw('hist e same')
      dn_.Draw('hist e same')
      nom_.Draw('hist e same')
    else:
      up_.Draw('hist same')
      dn_.Draw('hist same')
    nom_.Draw('hist same')
    legend = ROOT.TLegend(0.1, 0.75, 0.4, 0.9, syst)
    legend.AddEntry(up_, "Up")
    legend.AddEntry(dn_, "Down")
    legend.Draw()
    if logy: pad1.SetLogy()
    pad1.SetLogx()
    pad2.SetLogx()

    pad2.cd()
    ratio_up = up.Clone()
    ratio_up.Divide(nom)
    ratio_dn = dn.Clone()
    ratio_dn.Divide(nom)
    ratio_up.SetLineColor(ROOT.kRed)
    ratio_dn.SetLineColor(ROOT.kBlue)
    line = ROOT.TLine(-1, 1, 1, 1)
    line.SetLineStyle(2)
    minmax = [ratio_up.GetMaximum(), ratio_up.GetMinimum(), ratio_dn.GetMaximum(), ratio_dn.GetMinimum()]
    tmp_min = min(minmax)
    if tmp_min < 0.01:
        nbins = ratio_up.GetNbinsX()
        contents_org = [ratio_up.GetBinContent(x) for x in range(nbins)]
        contents_org.extend([ratio_dn.GetBinContent(x) for x in range(nbins)])
        contents = contents_org[:]
        for i in range(len(contents_org)):
            if contents_org[i] < 0.01: contents.remove(contents_org[i])
        tmp_min = min(contents)
    ratio_up.GetYaxis().SetRangeUser(tmp_min*0.97, max(minmax)*1.03)

    ratio_up.SetStats(0)
    ratio_up.SetTitle('')
    ratio_up.GetXaxis().SetLabelSize(0.1)
    ratio_up.GetXaxis().SetTitleSize(0.13)
    ratio_up.GetYaxis().SetTitle('Up(Dn) / Nominal')
    ratio_up.GetYaxis().SetTitleSize(0.1)
    ratio_up.GetYaxis().SetTitleOffset(0.4)
    ratio_up.GetYaxis().SetLabelSize(0.1)
    ratio_up.Draw('hist e')
    ratio_dn.Draw('hist e same')
    line.Draw()
    c.Print(os.path.join(plot_dir, plot_name + '.pdf'))
    c.Print(os.path.join(plot_dir, plot_name + '.png'))


for coupling in couplings:
    process_list = process_list_org[:]
    process_list.append(coupling)
    rootfile_name = rootfile_template.replace("COUPLING", coupling)
    rootfile_path = os.path.join(input_path, coupling, rootfile_name)
    rootfile = ROOT.TFile(rootfile_path)
    dir_in_rootfile = "DNN"
    rootdir = rootfile.GetDirectory(dir_in_rootfile)
    hist_list_org = [x.GetName() for x in rootdir.GetListOfKeys()]
    syst_list = []
    for it in hist_list_org:
        if 'Up' in it: 
		syst_list.append(it[it.find('_')+1:-2])
    for syst in list(set(syst_list)):
        if 'pdf' in syst and 'pdfalphas' not in syst: continue
        #if not any(s in syst for s in ['tune','hdamp'] ): continue
        syst_name = syst + "_" + coupling
        #syst_name = syst
        for proc in process_list:
            plot_name = syst_name + "_" + proc
            canvas = ROOT.TCanvas(plot_name, plot_name)
            nominal_th1 = rootfile.Get(dir_in_rootfile + "/" + proc)
            shape_up = rootfile.Get(dir_in_rootfile + "/" + proc + "_" + syst + "Up")
            #shape_up = rootfile.Get(dir_in_rootfile + "/" + syst + "Up")
            if not shape_up:
                continue
            shape_dn = rootfile.Get(dir_in_rootfile + "/" + proc + "_" + syst + "Down")
            #shape_dn = rootfile.Get(dir_in_rootfile + "/" + syst + "Down")

            if drawNom: drawComp(canvas, nominal_th1, shape_up, shape_dn, any(s in syst for s in ['tune','hdamp']))
            else: drawRatio(canvas, nominal_th1, shape_up, shape_dn)
            canvas.Clear()
