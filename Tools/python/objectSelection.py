from    tWZ.Tools.helpers import mZ, getVarValue, getObjDict, deltaR

# standard imports
from    math import *
import  numbers
import  textwrap     # for CutBased Ele ID
import  operator

jetVars = ['eta','pt','phi','btagDeepB', 'btagDeepFlavB', 'btagCSVV2', 'jetId', 'area', 'rawFactor', 'corr_JER']

def getJets(c, jetVars=jetVars, jetColl="Jet"):
    return [getObjDict(c, jetColl+'_', jetVars, i) for i in range(int(getVarValue(c, 'n'+jetColl)))]

def isAnalysisJet(j, ptCut=25, absEtaCut=2.4, ptVar='pt', idVar='jetId'):

    # we pass a string
    if  type(ptVar)==type(''):
        j_pt = j[ptVar]
    # we pass a list of strings -> we take the minimum
    elif (type( ptVar )==type([]) or type( ptVar )==type( tuple() )) and len(ptVar)>=1:
        j_pt = max( [ j[v] for v in ptVar ] )
    else:
        raise RuntimeError( "Do n ot know what to do with ptVar %r" % ptVar )

    return j_pt>ptCut and abs(j['eta'])<absEtaCut and ( j[idVar] >= 2 if idVar is not None else True )

def isBJet(j, tagger = 'DeepFlavor', WP='loose', year = 2016):
    if tagger == 'DeepFlavor' or tagger == 'DeepJet':
        if WP == 'tight':
            if year in [2016, "UL2016_preVFP"]:
                #https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16preVFP
                return j['btagDeepFlavB'] > 0.6502 
            elif year in [2016, "UL2016"]:
                #https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16postVFP
                return j['btagDeepFlavB'] > 0.6377
            elif year in [2017, "UL2017"]:
                #https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL17
                return j['btagDeepFlavB'] > 0.7476
            elif year in [2018, "UL2018"]:
                #https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL18
                return j['btagDeepFlavB'] > 0.7100
            else:
                raise (NotImplementedError, "Don't know what cut to use for year %s"%year)
        elif WP == 'medium':
            if year in [2016, "UL2016_preVFP"]:
                #https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16preVFP
                return j['btagDeepFlavB'] > 0.2598
            elif year in [2016, "UL2016"]:
                #https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16postVFP
                return j['btagDeepFlavB'] > 0.2489
            elif year in [2017, "UL2017"]:
                #https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL17
                return j['btagDeepFlavB'] > 0.3040
            elif year in [2018, "UL2018"]:
                #https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL18
                return j['btagDeepFlavB'] > 0.2783
            else:
                raise (NotImplementedError, "Don't know what cut to use for year %s"%year)
        elif WP == 'loose':
            if year in [2016, "UL2016_preVFP"]:
                #https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16preVFP
                return j['btagDeepFlavB'] > 0.0508
            elif year in [2016, "UL2016"]:
                #https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16postVFP
                return j['btagDeepFlavB'] > 0.0480
            elif year in [2017, "UL2017"]:
                #https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL17
                return j['btagDeepFlavB'] > 0.0532
            elif year in [2018, "UL2018"]:
                #https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL18
                return j['btagDeepFlavB'] > 0.0490
            else:
                raise (NotImplementedError, "Don't know what cut to use for year %s"%year)
        elif WP == "noWP":
            if year in [2016, "UL2016_preVFP"]:
                #https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16preVFP
                return j['btagDeepFlavB'] < 0.0508
            elif year in [2016, "UL2016"]:
                #https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16postVFP
                return j['btagDeepFlavB'] < 0.0480
            elif year in [2017, "UL2017"]:
                #https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL17
                return j['btagDeepFlavB'] < 0.0532
            elif year in [2018, "UL2018"]:
                #https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL18
                return j['btagDeepFlavB'] < 0.0490
            else:
                raise (NotImplementedError, "Don't know what cut to use for year %s"%year)
        else:
            raise (NotImplementedError, "Don't know WP %s"%WP)
    elif tagger == 'CSVv2':
        if WP!='medium':
            raise (NotImplementedError, "Don't know WP %s"%WP)
        if year in [2016, "UL2016", "UL2016_preVFP"]:
            # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco
            return j['btagCSVV2'] > 0.8484
        elif year in [2017, "UL2017"] or year in [2018, "UL2018"]:
            # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
            return j['btagCSVV2'] > 0.8838
        else:
            raise (NotImplementedError, "Don't know what cut to use for year %s"%year)
    elif tagger == 'DeepCSV':
        if WP!='medium':
            raise (NotImplementedError, "Don't know WP %s"%WP)
        if year in [2016, "UL2016_preVFP"]:
            #https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16preVFP
            return j['btagDeepB'] > 0.6001
        elif year in [2016, "UL2016"]:
            # https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16postVFP
            return j['btagDeepB'] > 0.5847
        elif year in [2017, "UL2017"]:
            # https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL17
            return j['btagDeepB'] > 0.4506
        elif year in [2018, "UL2018"]:
            # https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL18
            return j['btagDeepB'] > 0.4168
        else:
            raise (NotImplementedError, "Don't know what cut to use for year %s"%year)

def getGenLeps(c):
    return [getObjDict(c, 'genLep_', ['eta','pt','phi','charge', 'pdgId', 'sourceId'], i) for i in range(int(getVarValue(c, 'ngenLep')))]

def getGenParts(c):
    return [getObjDict(c, 'GenPart_', ['eta','pt','phi','charge', 'pdgId', 'motherId', 'grandmotherId'], i) for i in range(int(getVarValue(c, 'nGenPart')))]

genVars = ['eta','pt','phi','mass','charge', 'status', 'pdgId', 'genPartIdxMother', 'statusFlags','index']
def getGenPartsAll(c, genVars=genVars):
    return [getObjDict(c, 'GenPart_', genVars, i) for i in range(int(getVarValue(c, 'nGenPart')))]

def filterGenPhotons( genParts, status=None ):
    photons = list( filter( lambda l: abs(l['pdgId']) == 22 and l['status'] > 0, genParts ) )
    return photons

def genLepFromZ( genParts ):
    ''' get all gen leptons (e,m,tau) from Z
    '''
    try:
        leptons = list( filter( lambda l: abs(l['pdgId']) in [11,13,15] and abs(genParts[l['genPartIdxMother']]['pdgId']) == 23, genParts ) )
    except:
        print "Found no generated leptons"
        leptons = []
    return leptons

def getGenZs(genparts):
  res = []
  for g in genparts:
    if g['pdgId']  != 23:   continue					# pdgId == 23 for Z
    if g['status'] != 62:	continue					# status 62 is last gencopy before it decays into ll/nunu
    res.append(g)
  return res

def getGenPhoton(genparts):
  for g in genparts:								# Type 0: no photon
    if g['pdgId']  != 22:   continue					# pdgId == 22 for photons
    if g['status'] != 23:	continue					# for photons, take status 23
    return g
  return None

def get_index_str( index ):
    if isinstance(index, int):
        index_str = "["+str(index)+"]"
    elif type(index)==type(""):
        if index.startswith('[') and index.endswith(']'):
            index_str = index
        else:
            index_str = '['+index+']'
    elif index is None:
        index_str=""
    else:
        raise ValueError( "Don't know what to do with index %r" % index )
    return index_str

## MVA TOP lepton thresholds ##
# mvaTOP = {'mu':{'VL':-0.45, 'L':0.05, 'M':0.65, 'T':0.90}, 'ele':{'VL':-0.55, 'L':0.00, 'M':0.60, 'T':0.90}} # EOY
mvaTOP = {'mu':{'VL': 0.20, 'L':0.41, 'M':0.64, 'T':0.81}, 'ele':{'VL': 0.20, 'L':0.41, 'M':0.64, 'T':0.81}} # UL
mvaTOPv2 = {'mu':{'VL': 0.59, 'L':0.81, 'M':0.90, 'T':0.94}, 'ele':{'VL': 0.59, 'L':0.81, 'M':0.90, 'T':0.94}} # ULv2

def lepString( eleMu = None, WP = 'VL', idx = None):
    idx_str = "[%s]"%idx if idx is not None else ""
    if eleMu=='ele':
        return "lep_pt{idx_str}>10&&abs(lep_eta{idx_str})<2.5&&abs(lep_pdgId{idx_str})==11&&lep_mvaTOP{idx_str}>{threshold}".format( threshold = mvaTOP['ele'][WP], idx_str=idx_str )
    elif eleMu=='mu':
        return "lep_pt{idx_str}>10&&abs(lep_eta{idx_str})<2.4&&abs(lep_pdgId{idx_str})==13&&lep_mvaTOP{idx_str}>{threshold}".format( threshold = mvaTOP['mu'][WP], idx_str=idx_str )
    else:
        return '('+lepString( 'ele', WP, idx=idx) + ')||(' + lepString( 'mu', WP, idx=idx) + ')'

def lepStringNoMVA(eleMu = None, idx = None):
    idx_str = "[%s]"%idx if idx is not None else ""
    if eleMu=='ele':
        return "lep_pt{idx_str}>10&&abs(lep_eta{idx_str})<2.5&&abs(lep_pdgId{idx_str})==11".format( idx_str=idx_str )
    elif eleMu=='mu':
        return "lep_pt{idx_str}>10&&abs(lep_eta{idx_str})<2.4&&abs(lep_pdgId{idx_str})==13".format( idx_str=idx_str )
    else:
        return '('+lepString( 'ele', WP, idx=idx) + ')||(' + lepString( 'mu', WP, idx=idx) + ')'

## MUONS ##
def muonSelector( lepton_selection, year, ptCut = 10):
    # tigher isolation applied on analysis level
    if lepton_selection == 'loose':
        def func(l):
            return \
                l["pt"]                 >= ptCut \
                and abs(l["eta"])       < 2.4 \
                and abs(l["dxy"])       < 0.05 \
                and abs(l["dz"])        < 0.1 \
                and l['looseId']
    elif lepton_selection == 'medium':
        def func(l):
            return \
                l["pt"]                 >= ptCut \
                and abs(l["eta"])       < 2.4 \
                and abs(l["dxy"])       < 0.05 \
                and abs(l["dz"])        < 0.1 \
                and l['mediumId']
    elif lepton_selection == 'tight':
        def func(l):
            return \
                l["pt"]                 >= ptCut \
                and abs(l["eta"])       < 2.4 \
                and abs(l["dxy"])       < 0.05 \
                and abs(l["dz"])        < 0.1 \
                and l['tightId']
    elif lepton_selection == 'FOmvaTOPT':
        def func(l):
            return \
                l["pt"]                 >= ptCut \
                and abs(l["eta"])       < 2.4 \
                and abs(l["dxy"])       < 0.05 \
                and abs(l["dz"])        < 0.1 \
                and l["sip3d"]          < 8.0 \
                and l['miniPFRelIso_all'] < 0.40 \
                and l['mediumId']\
                and ( (l['mvaTOP'] > 0.64) or ((1/(l['jetRelIso']+1))> 0.45 and (l['jetBTag'] <  0.025 if l['jetIdx'] >= 0 else True)) )

    elif lepton_selection == 'mvaTOPT':
        def func(l):
            return \
                l["pt"]                 >= ptCut \
                and abs(l["eta"])       < 2.4 \
                and abs(l["dxy"])       < 0.05 \
                and abs(l["dz"])        < 0.1 \
                and l["sip3d"]          < 8.0 \
                and l['miniPFRelIso_all'] < 0.40 \
                and l['mediumId']\
                and l['mvaTOP'] > 0.64

    elif lepton_selection == 'presel':
        #L133 to L143 of http://cms.cern.ch/iCMS/jsp/openfile.jsp?tp=draft&files=AN2022_016_v3.pdf
        def func(l):
            return \
                l["pt"]                 >= ptCut \
                and abs(l["eta"])       < 2.4 \
                and abs(l["dxy"])       < 0.05 \
                and abs(l["dz"])        < 0.1 \
                and l["sip3d"]          < 8.0 \
                and l['miniPFRelIso_all'] < 0.40 \
                and l['mediumId']

    return func

#def muonSelectorString(relIso03 = 0.2, ptCut = 20, absEtaCut = 2.4, dxy = 0.05, dz = 0.1, index = "Sum"):
#    idx = None if (index is None) or (type(index)==type("") and index.lower()=="sum") else index
#    index_str = get_index_str( index  = idx)
#    string = [\
#                "Muon_pt"+index_str+">=%s"%ptCut ,
#                "abs(Muon_eta"+index_str+")<%s" % absEtaCut ,
#                "Muon_mediumId"+index_str+">=1" ,
#                "Muon_sip3d"+index_str+"<4.0" ,
#                "abs(Muon_dxy"+index_str+")<%s" % dxy ,
#                "abs(Muon_dz"+index_str+")<%s" % dz ,
#                "Muon_pfRelIso03_all"+index_str+"<%s" % relIso03 ,
#             ]
#    if type(index)==type("") and index.lower()=='sum':
#        return 'Sum$('+'&&'.join(string)+')'
#    else:
#        return '&&'.join(string)

## ELECTRONS ##

# Electron bitmap
# or  https://cms-nanoaod-integration.web.cern.ch/integration/master-102X/mc102X_doc.html
# Attention: only for nanoAOD v94x or higher (in 80x, only 2 bits are used)
vidNestedWPBitMapNamingList = \
    ['GsfEleMissingHitsCut',
     'GsfEleConversionVetoCut',
     'GsfEleRelPFIsoScaledCut',
     'GsfEleEInverseMinusPInverseCut',
     'GsfEleHadronicOverEMEnergyScaledCut',
     'GsfEleFull5x5SigmaIEtaIEtaCut',
     'GsfEleDPhiInCut',
     'GsfEleDEtaInSeedCut',
     'GsfEleSCEtaMultiRangeCut',
     'MinPtCut']
vidNestedWPBitMap           = { 'fail':0, 'veto':1, 'loose':2, 'medium':3, 'tight':4 }  # Bitwise (Electron vidNestedWPBitMap ID flags (3 bits per cut), '000'=0 is fail, '001'=1 is veto, '010'=2 is loose, '011'=3 is medium, '100'=4 is tight)

def cutBasedEleBitmap( integer ):
    return [int( x, 2 ) for x in textwrap.wrap("{0:030b}".format(integer),3) ]

def cbEleSelector( quality, removeCuts = [] ):
    if quality not in vidNestedWPBitMap.keys():
        raise Exception( "Don't know about quality %r" % quality )
    if type( removeCuts ) == str:
        removeCuts = [removeCuts]

    # construct a list of thresholds the electron has to satisfy
    thresholds = []
    for cut in removeCuts:
        if cut not in vidNestedWPBitMapNamingList:
            raise Exception( "Don't know about ele cut %r" % cut )
    for cut in vidNestedWPBitMapNamingList:
        if cut not in removeCuts:
            thresholds.append( vidNestedWPBitMap[quality] )
        else:
            thresholds.append( 0 )

    # construct the selector
    def _selector( integer ):
        return all(map( lambda x: operator.ge(*x), zip( cutBasedEleBitmap(integer), thresholds ) ))
    return _selector


def cbEleIdFlagGetter( flag ):

    position = vidNestedWPBitMapNamingList.index( flag )

    def getter( integer ):
        return int( textwrap.wrap("{0:030b}".format(integer),3)[position] ,2)

    return getter

def passECALGap(e):
    if abs(e['pdgId']) == 11: absEta = abs(e["eta"] + e["deltaEtaSC"])   # eta supercluster
    else:                     absEta = abs(e["eta"])                     # eta
    return ( absEta > 1.566 or absEta < 1.4442 )

vidNestedWPBitMapNamingList = \
    ['GsfEleMissingHitsCut',
     'GsfEleConversionVetoCut',
     'GsfEleRelPFIsoScaledCut',
     'GsfEleEInverseMinusPInverseCut',
     'GsfEleHadronicOverEMEnergyScaledCut',
     'GsfEleFull5x5SigmaIEtaIEtaCut',
     'GsfEleDPhiInCut',
     'GsfEleDEtaInSeedCut',
     'GsfEleSCEtaMultiRangeCut',
     'MinPtCut']
vidNestedWPBitMap           = { 'fail':0, 'veto':1, 'loose':2, 'medium':3, 'tight':4 }  # Bitwise (Electron vidNestedWPBitMap ID flags (3 bits per cut), '000'=0 is fail, '001'=1 is veto, '010'=2 is loose, '011'=3 is medium, '100'=4 is tight)


def vidNestedWPBitMapToDict( val ):
    # convert int of vidNestedWPBitMap ( e.g. val = 611099940 ) to bitmap ( e.g. "100100011011001010010100100100")
    # split vidBitmap string (containing 3 bits per cut) in parts of 3 bits ( e.g. ["100","100","011","011","001","010","010","100","100","100"] )
    # convert 3 bits to int ( e.g. [4, 4, 3, 3, 1, 2, 2, 4, 4, 4])
    # create dictionary
    idList = [ int( x, 2 ) for x in textwrap.wrap( "{0:030b}".format( val ) , 3) ] #use 2 for nanoAOD version 80x
    return dict( zip( vidNestedWPBitMapNamingList, idList ) )

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def electronVIDSelector( l, idVal, removedCuts=[] ):

    vidDict    = vidNestedWPBitMapToDict( l['vidNestedWPBitmap'] )
    if not removedCuts:
        return all( [ cut >= idVal for cut in vidDict.values() ] )

    if ("pt"             in removedCuts):
        vidDict = removekey( vidDict, "MinPtCut" )
    if ("sieie"          in removedCuts):
        vidDict = removekey( vidDict, "GsfEleFull5x5SigmaIEtaIEtaCut" )
    if ("hoe"            in removedCuts):
        vidDict = removekey( vidDict, "GsfEleHadronicOverEMEnergyScaledCut" )
    if ("pfRelIso03_all" in removedCuts):
        vidDict = removekey( vidDict, "GsfEleRelPFIsoScaledCut" )
    if ("SCEta" in removedCuts):
        vidDict = removekey( vidDict, "GsfEleSCEtaMultiRangeCut" )
    if ("dEtaSeed" in removedCuts):
        vidDict = removekey( vidDict, "GsfEleDEtaInSeedCut" )
    if ("dPhiInCut" in removedCuts):
        vidDict = removekey( vidDict, "GsfEleDPhiInCut" )
    if ("EinvMinusPinv" in removedCuts):
        vidDict = removekey( vidDict, "GsfEleEInverseMinusPInverseCut" )
    if ("convVeto" in removedCuts):
        vidDict = removekey( vidDict, "GsfEleConversionVetoCut" )
    if ("lostHits" in removedCuts):
        vidDict = removekey( vidDict, "GsfEleMissingHitsCut" )

    return all( [ cut >= idVal for cut in vidDict.values() ] )

def eleSelector( lepton_selection, year, ptCut = 10):
    # tigher isolation applied on analysis level. cutBased corresponds to Fall17V2 ID for all 2016-2018.
    if lepton_selection == 'CBtight':
        cbEleSelector_ = cbEleSelector( 'tight')
        def func(l):
            return \
                l["pt"]                 >= ptCut \
                and abs(l["eta"])       < 2.4 \
                and passECALGap(l)\
                and abs(l["dxy"])       < 0.05 \
                and abs(l["dz"])        < 0.1 \
                and cbEleSelector_(l['vidNestedWPBitmap'])

    elif lepton_selection == 'CBmedium':
        cbEleSelector_ = cbEleSelector( 'medium')
        def func(l):
            return \
                l["pt"]                 >= ptCut \
                and abs(l["eta"])       < 2.4 \
                and passECALGap(l)\
                and abs(l["dxy"])       < 0.05 \
                and abs(l["dz"])        < 0.1 \
                and cbEleSelector_(l['vidNestedWPBitmap'])

    elif lepton_selection == 'CBloose':
        cbEleSelector_ = cbEleSelector( 'loose')
        def func(l):
            return \
                l["pt"]                 >= ptCut \
                and abs(l["eta"])       < 2.4 \
                and passECALGap(l)\
                and abs(l["dxy"])       < 0.05 \
                and abs(l["dz"])        < 0.1 \
                and cbEleSelector_(l['vidNestedWPBitmap'])

    elif lepton_selection == 'FOmvaTOPT':

        def func(l):
            if year == 2016:
                pt_ratio = 0.5
            elif year == 2017 or year == 2018:
                pt_ratio = 0.4

            return \
                l["pt"]                 >= ptCut \
                and abs(l["eta"])       < 2.5 \
                and passECALGap(l)\
                and abs(l["dxy"])       < 0.05 \
                and abs(l["dz"])        < 0.1 \
                and l["sip3d"]          < 8.0 \
                and l['miniPFRelIso_all'] < 0.40 \
                and ord(l["lostHits"])  < 2 \
                and l['convVeto']\
                and l['tightCharge']    >= 2\
                and ((l['mvaTOP'] > 0.81) or (l['mvaFall17V2noIso_WPL'] and ((1/(l['jetRelIso']+1))> pt_ratio and (l['jetBTag'] <  0.1 if l['jetIdx'] >= 0 else True) ) ))

    elif lepton_selection == 'mvaTOPT':
        def func(l):
            return \
                l["pt"]                 >= ptCut \
                and abs(l["eta"])       < 2.5 \
                and passECALGap(l)\
                and abs(l["dxy"])       < 0.05 \
                and abs(l["dz"])        < 0.1 \
                and l["sip3d"]          < 8.0 \
                and l['miniPFRelIso_all'] < 0.40 \
                and ord(l["lostHits"])  < 2 \
                and l['convVeto']\
                and l['tightCharge']    >= 2\
                and l['mvaTOP'] > 0.81

    elif lepton_selection == 'presel':
        # L133 - 143 of http://cms.cern.ch/iCMS/jsp/openfile.jsp?tp=draft&files=AN2022_016_v3.pdf
        def func(l):
            return \
                l["pt"]                 >= ptCut \
                and abs(l["eta"])       < 2.5 \
                and passECALGap(l)\
                and abs(l["dxy"])       < 0.05 \
                and abs(l["dz"])        < 0.1 \
                and l["sip3d"]          < 8.0 \
                and l['miniPFRelIso_all'] < 0.40 \
                and ord(l["lostHits"])  < 2

    return func


#def eleSelectorString(relIso03 = 0.2, eleId = 4, ptCut = 20, absEtaCut = 2.4, dxy = 0.05, dz = 0.1, index = "Sum", noMissingHits=True):
#    idx = None if (index is None) or (type(index)==type("") and index.lower()=="sum") else index
#    index_str = get_index_str( index  = idx)
#    string = [\
#                "Electron_pt"+index_str+">=%s" % ptCut ,
#                "abs(Electron_eta"+index_str+")<%s" % absEtaCut ,
#                "Electron_convVeto"+index_str+"",
#                "Electron_lostHits"+index_str+"==0" if noMissingHits else "(1)",
#                "Electron_sip3d"+index_str+"<4.0" ,
#                "abs(Electron_dxy"+index_str+")<%s" % dxy ,
#                "abs(Electron_dz"+index_str+")<%s" % dz ,
#                "Electron_pfRelIso03_all"+index_str+"<%s" % relIso03 ,
#                "Electron_cutBased"+index_str+">=%s"%eleId , # Fall17V2 ID
#             ]
#
#    if type(index)==type("") and index.lower()=='sum':
#        return 'Sum$('+'&&'.join(string)+')'
#    else:
#        return '&&'.join(string)


electronVars_data = ['pt','eta','phi','pdgId','cutBased','miniPFRelIso_all','miniPFRelIso_chg','pfRelIso03_all','sip3d','convVeto','dxy','dz','charge','deltaEtaSC', 'mvaFall17V2noIso_WPL', 'jetPtRelv2', 'jetRelIso', 'mvaFall17V2Iso_WP90', 'vidNestedWPBitmap','mvaTTH', 'jetRelIso', 'jetIdx', 'sieie', 'hoe', 'eInvMinusPInv', 'pfRelIso04_all', 'mvaFall17V2noIso', 'mvaFall17V2noIso_WP80', 'lostHits', 'jetNDauCharged', 'jetRelIso', 'tightCharge', 'jetBTag']
electronVars = electronVars_data + []

muonVars_data = ['pt','eta','phi','pdgId','mediumId','miniPFRelIso_all','miniPFRelIso_chg','pfRelIso04_all','segmentComp','sip3d','dxy','dz','charge','mvaTTH', 'looseId', 'jetPtRelv2', 'jetRelIso', 'jetIdx', 'mvaId', 'pfRelIso03_all', 'jetNDauCharged', 'jetRelIso', 'isGlobal', 'isTracker', 'tightId', 'tightCharge' , 'jetBTag']
muonVars = muonVars_data + []

def getMuons(c, collVars=muonVars):
    return [getObjDict(c, 'Muon_', collVars, i) for i in range(int(getVarValue(c, 'nMuon')))]
def getElectrons(c, collVars=electronVars):
    return [getObjDict(c, 'Electron_', collVars, i) for i in range(int(getVarValue(c, 'nElectron')))]

def getGoodMuons(c, collVars=muonVars, mu_selector = None):
    return [l for l in getMuons(c, collVars) if ( mu_selector is None or mu_selector(l))]

def getGoodElectrons(c, collVars=electronVars, ele_selector = None):
    return [l for l in getElectrons(c, collVars) if ( ele_selector is None or ele_selector(l))]


tauVars=['eta','pt','phi','pdgId','charge', 'dxy', 'dz', 'idDecayModeNewDMs', 'idCI3hit', 'idAntiMu','idAntiE','mcMatchId']

def getTaus(c, collVars=tauVars):
    return [getObjDict(c, 'TauGood_', collVars, i) for i in range(int(getVarValue(c, 'nTauGood')))]

def looseTauID(l, ptCut=20, absEtaCut=2.4):
    return \
        l["pt"]>=ptCut\
        and abs(l["eta"])<absEtaCut\
        and l["idDecayModeNewDMs"]>=1\
        and l["idCI3hit"]>=1\
        and l["idAntiMu"]>=1\
        and l["idAntiE"]>=1\

def getGoodTaus(c, collVars=tauVars):
    return [l for l in getTaus(c,collVars=collVars) if looseTauID(l)]

idCutBased={'loose':0 ,'medium':1, 'tight':2}
photonVars=['eta','pt','phi','mass','cutBased']
photonVarsMC = photonVars + ['mcPt']

def getPhotons(c, collVars=None, year=2016):
    if collVars is None:
        collVars = ['eta','pt','phi','mass','cutBased'] if (not (year == 2017 or year == 2018)) else ['eta','pt','phi','mass','cutBasedBitmap']
    return [getObjDict(c, 'Photon_', collVars, i) for i in range(int(getVarValue(c, 'nPhoton')))]

def getGoodPhotons(c, ptCut=20, idLevel="loose", isData=True, collVars=None, year=2016):
    idVar = "cutBased" if (not (year == 2017 or year == 2018)) else "cutBasedBitmap"
    #if collVars is None: collVars = photonVars if isData else photonVarsMC
    collVars = ['eta','pt','phi','mass','cutBased'] if (not (year == 2017 or year == 2018)) else ['eta','pt','phi','mass','cutBasedBitmap']
    return [p for p in getPhotons(c, collVars) if p[idVar] > idCutBased[idLevel] and p['pt'] > ptCut ] # > 2 is tight for 2016, 2017 and 2018

def genPhotonSelector( photon_selection=None ):
    # According to AN-2017/197
    if photon_selection == 'overlapTTGamma':
        # Remove events from ttbar sample, keep ttgamma events
        def func(g):
            if g["pt"]       <= 13:  return False
            if abs(g["eta"]) >= 3.0: return False
            return True
        return func

    elif photon_selection == 'overlapZWGamma':
        # Remove events from DY and W+jets sample, keep Zgamma and Wgamma events
        def func(g):
            if g["pt"]       <= 15:  return False
            if abs(g["eta"]) >= 2.6: return False
            return True
        return func

    elif photon_selection == 'overlapSingleTopTch':
        # Remove events from single top t-channel sample, keep single top + photon events
        def func(g):
            if g["pt"]       <= 10:  return False
            if abs(g["eta"]) >= 2.6: return False
            return True
        return func

    else:
        # general gen-photon selection
        def func(g):
            if g["pt"]       <= 13:    return False
            if abs(g["eta"]) >= 1.479: return False
            return True
        return func
