#!/usr/bin/env python
'''
In this file as for the dR0p3 cone you can make a choice of training with new or old DM
as well as the choice of the campaighn

for sg and bg only the "tthHiggs%1.0ftoTauTau" and TT_powheg samples are used, through
manipulating of the SamplesHandles class
'''
from samplesHandles import SamplesHandles
import os
import yaml
from string import Template
import pprint
pp = pprint.PrettyPrinter(indent=4)

from submitHelpers import getTrainingSets

config = yaml.load(open("config.yaml", 'r'))
preselections, cutDiscriminatorsAll, trainings, commonsDict = getTrainingSets(trainingsets='trainingsets.json')

inputFilePath = os.path.join(config['nfs_base'], config['workarea_base'] + config['version'], 'ntuples')
outputFilePath = Template(os.path.join(config['nfs_base'], config['workarea_base'] + config['version'], "$trainingtype"))
# version = decaymodes[DM]["version"] #version = 'tauId_dR03' #'tauId_v3_0'
# inputFilePath  = "/nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/ntuples/"
# outputFilePath = "/nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/%s/trainfilesfinal_WIP1_attempt2/" % version


# ---------- Settings to touch ----------------
DM = "old"  # New DM not used for 0.3 cone training
disable_xml_inclusion = True
use_condor = False

traintingVariables = ['recTauPt', 'recTauEta', 'chargedIsoPtSum', 'neutralIsoPtSum_ptGt1.0', 'puCorrPtSum', 'photonPtSumOutsideSignalCone_ptGt1.0', 'recTauDecayMode', 'recTauNphoton_ptGt1.0', 'recTauPtWeightedDetaStrip_ptGt1.0', 'recTauPtWeightedDphiStrip_ptGt1.0', 'recTauPtWeightedDrSignal_ptGt1.0', 'recTauPtWeightedDrIsolation_ptGt1.0', 'recTauEratio', 'recImpactParam', 'recImpactParam', 'recImpactParamSign', 'recImpactParam3D', 'recImpactParam3D', 'recImpactParamSign3D', 'hasRecDecayVertex', 'recDecayDistMag', 'recDecayDistSign', 'recTauGJangleDiff']
# TODO:
prepareTreeOptions = "nTrain_Signal=0:nTrain_Background=0:nTest_Signal=0:nTest_Background=0:SplitMode=Random:NormMode=NumEvents:!V"

decaymodes = {
    "old": {
        "mvaDiscriminators": {
            # 'mvaIsolation3HitsDeltaR05opt2aLTDB_1p0': trainings['mvaIsolation3HitsDeltaR05opt2aLTDB_1p0'], # this one should have different presel input file
            # 'mvaIsolation3HitsDeltaR05opt1aLTDB': trainings['mvaIsolation3HitsDeltaR05opt1aLTDB'], # only untill will be possible to lead the trainings
            # 'mvaIsolation3HitsDeltaR03opt1aLTDB': trainings['mvaIsolation3HitsDeltaR03opt1aLTDB'],  # has no GJ-angle, but unused track Chi2
            'mvaIsolation3HitsDeltaR03opt2aLTDB': trainings['mvaIsolation3HitsDeltaR03opt2aLTDB']
        },
        "cutDiscriminators": {
            # 'rawMVAoldDMwLT': cutDiscriminatorsAll['rawMVAoldDMwLT'],
            # 'rawMVAoldDMwLT2016': cutDiscriminatorsAll['rawMVAoldDMwLT2016']
            'rawMVAoldDMdR03wLT': cutDiscriminatorsAll['rawMVAoldDMdR03wLT'],
            'rawMVAoldDMdR03wLT2017': cutDiscriminatorsAll['rawMVAoldDMdR03wLT2017'],
        },
        "plots": {  # Here you list all the selections(trained or cut-based) that are compared on the plot
            'mvaIsolation_optDeltaR03BDeltaBeta': {
                'graphs': [
                    'mvaIsolation3HitsDeltaR03opt2aLTDB',
                    'rawMVAoldDMdR03wLT',
                    'rawMVAoldDMdR03wLT2017',
                ]
            }
        },
        "version": 'tauId_dR03_old_' + config['version'],
    }
}

datasetDirName = 'dataset_' + DM + "DM_" + decaymodes[DM]["version"]

# OPTIONAL!!!!
# for val in decaymodes[DM]['mvaDiscriminators'].values():
#     val['applyPtDependentPruningSignal'] = False

# Set this to true if you want to compute ROC curves for additional
# discriminators for comparisons on ALL events available in the ntuples
# NB: if pt-dependent pruning is used, this will not result in an
# apples-to-apples comparison!
computeROConAllEvents = False

# ---------- end Settings to touch ----------------

train_option = 'optaDBAll'

version = decaymodes[DM]["version"]
outputFilePath = outputFilePath.substitute(trainingtype=decaymodes[DM]["version"])

samples_key = config['samples_key']['dR0p3']
sh = SamplesHandles(samples_key)
signalSamples = sh.samples_sg.keys()
backgroundSamples = sh.samples_bg.keys()

# DO NOT process isodR03 and isodR05 together! - different input variables
# preselection root-files can be shared only if thew follow the same preselection choice (1 of 4)
mvaDiscriminators = decaymodes[DM]["mvaDiscriminators"]

# to ensure the final reweighting root files will be suitable for larger spectra of trainings
for value in mvaDiscriminators.values():
    value["spectatorVariables"] += commonsDict['commonOtherVariables']

cutDiscriminators = decaymodes[DM]["cutDiscriminators"]
plots = decaymodes[DM]["plots"]
allDiscriminators = {}
allDiscriminators.update(mvaDiscriminators)
allDiscriminators.update(cutDiscriminators)

from runTauIdMVATrainingMiniAOD_common import produceRunScripts
produceRunScripts(
    inputFilePath=inputFilePath,
    signalSamples=signalSamples,
    backgroundSamples=backgroundSamples,
    decaymodes=decaymodes,
    DM=DM,
    train_option=train_option,
    mvaDiscriminators=mvaDiscriminators,
    outputFilePath=outputFilePath,
    disable_xml_inclusion=disable_xml_inclusion,
    computeROConAllEvents=computeROConAllEvents,
    datasetDirName=datasetDirName,
    cutDiscriminators=cutDiscriminators,
    plots=plots,
    traintingVariables=traintingVariables,
    allDiscriminators=allDiscriminators,
    use_condor=use_condor,
)
