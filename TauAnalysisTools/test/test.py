from samplesHandles import SamplesHandles

import os
import subprocess
import shlex
import shutil

import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

def replaceCommomns(commonName, commonList, singleList):
	if commonName in singleList:
		singleList[:] = [x for x in singleList if x != commonName]
		singleList[:] = commonList + singleList

with open('trainingsets.json') as f:
	ff = json.load(f)

preselections = ff['preselections']
cutDiscriminators = ff['cutDiscriminators']
trainings = ff['trainings']
commonsDict = {
	'commonOtherVariables': ff['commonOtherVariables'],
	'commonSpectatorVariables': ff['commonSpectatorVariables'],
}

for cval in cutDiscriminators.values():
	cval["preselection"] = preselections[cval["preselection"]]

for tval in trainings.values():
	tval["preselection"] = preselections[tval["preselection"]]

	replaceCommomns('commonOtherVariables', commonsDict['commonOtherVariables'], tval["otherVariables"])
	replaceCommomns('commonSpectatorVariables', commonsDict['commonSpectatorVariables'], tval["spectatorVariables"])


# print type(trainings['mvaIsolation3HitsDeltaR03opt1aLTDB'])
# pp.pprint(trainings['mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0'])
mvaDiscriminators = {
    'mvaIsolation3HitsDeltaR03opt1aLTDB': trainings['mvaIsolation3HitsDeltaR03opt1aLTDB'],
    'mvaIsolation3HitsDeltaR03opt2aLTDB': trainings['mvaIsolation3HitsDeltaR03opt2aLTDB'],
    'mvaIsolation3HitsDeltaR03opt2aLTDB_1p0': trainings['mvaIsolation3HitsDeltaR03opt2aLTDB_1p0'],
    'mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0': trainings['mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0']
}

# to ensure the final reweighting root files will be suitable for larger spectra of trainings 
# for value in mvaDiscriminators.values():
#     value["spectatorVariables"] += commonsDict['commonOtherVariables']
# pp.pprint(mvaDiscriminators['mvaIsolation3HitsDeltaR03opt1aLTDB'])

# trainings['mvaIsolation3HitsDeltaR03opt1aLTDB'],
# trainings['mvaIsolation3HitsDeltaR03opt2aLTDB'],
# trainings['mvaIsolation3HitsDeltaR03opt2aLTDB_1p0'],
# trainings['mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0']
#
sh = SamplesHandles("2016")
# pp.pprint(sh.samples)
for i in sh.getDatabeseNames():
	print i
# pp.pprint(sh.getDatabeseNames())

# Printitng the datasets number of events from missing samples
# missing_in_17mcv2 = ["WprimeToTauNu_M-1000_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-1200_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-1400_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-1600_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-1800_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-2000_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-2200_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-2400_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-2600_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-2800_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-3000_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-3200_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-3400_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-3600_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-3800_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-4000_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-400_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-4200_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-4400_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-4600_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-4800_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-5000_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-5200_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-5400_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-5600_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-5800_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"WprimeToTauNu_M-600_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"ZprimeToTauTau_M-1000_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"ZprimeToTauTau_M-1250_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"ZprimeToTauTau_M-1500_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"ZprimeToTauTau_M-1750_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"ZprimeToTauTau_M-2000_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"ZprimeToTauTau_M-2500_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"ZprimeToTauTau_M-3000_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"ZprimeToTauTau_M-3500_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"ZprimeToTauTau_M-4000_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"ZprimeToTauTau_M-500_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"ZprimeToTauTau_M-750_TuneCUETP8M1_13TeV-pythia8-tauola",
# 	"ttHJetToTT_M120_13TeV_amcatnloFXFX_madspin_pythia8",
# 	"ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8",
# 	"ttHJetToTT_M130_13TeV_amcatnloFXFX_madspin_pythia8",
# 	"SUSYGluGluToHToTauTau_M-80_TuneCUETP8M1_13TeV-pythia8",
# 	"SUSYGluGluToHToTauTau_M-90_TuneCUETP8M1_13TeV-pythia8",
# 	"SUSYGluGluToHToTauTau_M-2900_TuneCUETP8M1_13TeV-pythia8",
# 	"SUSYGluGluToHToTauTau_M-1500_TuneCUETP8M1_13TeV-pythia8",
# 	"SUSYGluGluToHToTauTau_M-120_TuneCUETP8M1_13TeV-pythia8",
# 	"SUSYGluGluToHToTauTau_M-130_TuneCUETP8M1_13TeV-pythia8",
# 	"SUSYGluGluToHToTauTau_M-100_TuneCUETP8M1_13TeV-pythia8",
# 	"SUSYGluGluToHToTauTau_M-110_TuneCUETP8M1_13TeV-pythia8",
# 	"SUSYGluGluToBBHToTauTau_M-90_TuneCUETP8M1_13TeV-pythia8",
# 	"SUSYGluGluToBBHToTauTau_M-80_TuneCUETP8M1_13TeV-pythia8",
# 	"SUSYGluGluToBBHToTauTau_M-2900_TuneCUETP8M1_13TeV-pythia8",
# 	"SUSYGluGluToBBHToTauTau_M-1500_TuneCUETP8M1_13TeV-pythia8",
# 	"SUSYGluGluToBBHToTauTau_M-120_TuneCUETP8M1_13TeV-pythia8",
# 	"SUSYGluGluToBBHToTauTau_M-130_TuneCUETP8M1_13TeV-pythia8",
# 	"SUSYGluGluToBBHToTauTau_M-100_TuneCUETP8M1_13TeV-pythia8",
# 	"SUSYGluGluToBBHToTauTau_M-110_TuneCUETP8M1_13TeV-pythia8",
# 	"GluGluHToTauTau_M130_13TeV_powheg_pythia8",
# 	"QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8",
# 	"QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8",
# 	"QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
# 	"QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8",
# 	"GluGluHToTauTau_M130_13TeV_powheg_pythia8"]
# for i in sh.samples.values():
# 	if i['datasetpath'].split('/')[1] in missing_in_17mcv2:
# 		dasCommand = "echo " + i['datasetpath'].split('/')[1] +": ; das_client --query=\"summary dataset=" + i['datasetpath'] + " | grep summary.nevents\" "
# 		subprocess.call(dasCommand, shell = True)




