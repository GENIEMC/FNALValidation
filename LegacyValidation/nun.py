# fill dag file with neutrino-nucleon cross section splines jobs

import msg
import re, os

nKnots    = "200" # no. of knots for gmkspl
maxEnergy = "150" # maximum energy for gmkspl

# neutrino pdg codes for given job 
nuPDG = {'chm'           : '12,-12,14,-14,16,-16',
         'nue'           : '12,-12,14,-14,16,-16',
         'qel'           : '12,-12,14,-14,16,-16',
         'dis_ebar_cc'   : '-12',
         'dis_ebar_nc'   : '-12',
         'dis_e_cc'      : '12',
         'dis_e_nc'      : '12',
         'dis_mubar_cc'  : '-14',
         'dis_mubar_nc'  : '-14',
         'dis_mu_cc'     : '14',
         'dis_mu_nc'     : '14',
         'dis_taubar_cc' : '-16',
         'dis_taubar_nc' : '-16',
         'dis_tau_cc'    : '16',
         'dis_tau_nc'    : '16',
         'res_ebar_cc'   : '-12',
         'res_ebar_nc'   : '-12',
         'res_e_cc'      : '12',
         'res_e_nc'      : '12',
         'res_mubar_cc'  : '-14',
         'res_mubar_nc'  : '-14',
         'res_mu_cc'     : '14',
         'res_mu_nc'     : '14',
         'res_taubar_cc' : '-16',
         'res_taubar_nc' : '-16',
         'res_tau_cc'    : '16',
         'res_tau_nc'    : '16' }
# for debugging, can use a short set
# nuPDG = {'qel'           : '12,-12,14,-14',
#          'nue'           : '12,-12,14,-14'}
         
# target pdg codes for given job 
targetPDG = {'chm'           : '1000010010,1000000010',
             'nue'           : '1000010010,1000000010',
             'qel'           : '1000010010,1000000010',
             'dis_ebar_cc'   : '1000010010,1000000010',
             'dis_ebar_nc'   : '1000010010,1000000010',
             'dis_e_cc'      : '1000010010,1000000010',
             'dis_e_nc'      : '1000010010,1000000010',
             'dis_mubar_cc'  : '1000010010,1000000010',
             'dis_mubar_nc'  : '1000010010,1000000010',
             'dis_mu_cc'     : '1000010010,1000000010',
             'dis_mu_nc'     : '1000010010,1000000010',
             'dis_taubar_cc' : '1000010010,1000000010',
             'dis_taubar_nc' : '1000010010,1000000010',
             'dis_tau_cc'    : '1000010010,1000000010',
             'dis_tau_nc'    : '1000010010,1000000010',
             'res_ebar_cc'   : '1000010010,1000000010',
             'res_ebar_nc'   : '1000010010,1000000010',
             'res_e_cc'      : '1000010010,1000000010',
             'res_e_nc'      : '1000010010,1000000010',
             'res_mubar_cc'  : '1000010010,1000000010',
             'res_mubar_nc'  : '1000010010,1000000010',
             'res_mu_cc'     : '1000010010,1000000010',
             'res_mu_nc'     : '1000010010,1000000010',
             'res_taubar_cc' : '1000010010,1000000010',
             'res_taubar_nc' : '1000010010,1000000010',
             'res_tau_cc'    : '1000010010,1000000010',
             'res_tau_nc'    : '1000010010,1000000010'}
             
# event generator list for given job 
generatorList = {'chm'           : 'Charm',
                 'nue'           : 'NuE',
                 'qel'           : 'QE',
                 'dis_ebar_cc'   : 'CCDIS',
                 'dis_ebar_nc'   : 'NCDIS',
                 'dis_e_cc'      : 'CCDIS',
                 'dis_e_nc'      : 'NCDIS',
                 'dis_mubar_cc'  : 'CCDIS',
                 'dis_mubar_nc'  : 'NCDIS',
                 'dis_mu_cc'     : 'CCDIS',
                 'dis_mu_nc'     : 'NCDIS',
                 'dis_taubar_cc' : 'CCDIS',
                 'dis_taubar_nc' : 'NCDIS',
                 'dis_tau_cc'    : 'CCDIS',
                 'dis_tau_nc'    : 'NCDIS',
                 'res_ebar_cc'   : 'CCRES',
                 'res_ebar_nc'   : 'NCRES',
                 'res_e_cc'      : 'CCRES',
                 'res_e_nc'      : 'NCRES',
                 'res_mubar_cc'  : 'CCRES',
                 'res_mubar_nc'  : 'NCRES',
                 'res_mu_cc'     : 'CCRES',
                 'res_mu_nc'     : 'NCRES',
                 'res_taubar_cc' : 'CCRES',
                 'res_taubar_nc' : 'NCRES',
                 'res_tau_cc'    : 'CCRES',
                 'res_tau_nc'    : 'NCRES'}

# name of output xml file for given job 
outXML = {'chm'           : 'pgxspl-chm.xml',
          'nue'           : 'pgxspl-nue.xml',
          'qel'           : 'pgxspl-qel.xml',
          'dis_ebar_cc'   : 'pgxspl-dis_ebar_cc.xml',
          'dis_ebar_nc'   : 'pgxspl-dis_ebar_nc.xml',
          'dis_e_cc'      : 'pgxspl-dis_e_cc.xml',
          'dis_e_nc'      : 'pgxspl-dis_e_nc.xml',
          'dis_mubar_cc'  : 'pgxspl-dis_mubar_cc.xml',
          'dis_mubar_nc'  : 'pgxspl-dis_mubar_nc.xml',
          'dis_mu_cc'     : 'pgxspl-dis_mu_cc.xml',
          'dis_mu_nc'     : 'pgxspl-dis_mu_nc.xml',
          'dis_taubar_cc' : 'pgxspl-dis_taubar_cc.xml',
          'dis_taubar_nc' : 'pgxspl-dis_taubar_nc.xml',
          'dis_tau_cc'    : 'pgxspl-dis_tau_cc.xml',
          'dis_tau_nc'    : 'pgxspl-dis_tau_nc.xml',
          'res_ebar_cc'   : 'pgxspl-res_ebar_cc.xml',
          'res_ebar_nc'   : 'pgxspl-res_ebar_nc.xml',
          'res_e_cc'      : 'pgxspl-res_e_cc.xml',
          'res_e_nc'      : 'pgxspl-res_e_nc.xml',
          'res_mubar_cc'  : 'pgxspl-res_mubar_cc.xml',
          'res_mubar_nc'  : 'pgxspl-res_mubar_nc.xml',
          'res_mu_cc'     : 'pgxspl-res_mu_cc.xml',
          'res_mu_nc'     : 'pgxspl-res_mu_nc.xml',
          'res_taubar_cc' : 'pgxspl-res_taubar_cc.xml',
          'res_taubar_nc' : 'pgxspl-res_taubar_nc.xml',
          'res_tau_cc'    : 'pgxspl-res_tau_cc.xml',
          'res_tau_nc'    : 'pgxspl-res_tau_nc.xml'}

def fillDAG (jobsub, tag, paths):
  fillDAGPart (jobsub, tag, paths['xsec_N'])
  fillDAGMerge (jobsub, tag, paths['xsec_N'])

def fillDAGPart (jobsub, tag, out):
  # check if job is done already
  if isDonePart (out):
    msg.warning ("Nucleons splines found in " + out + " ... " + msg.BOLD + "skipping nun:fillDAGPart\n", 1)
    return
  # not done, add jobs to dag
  msg.info ("\tAdding nucleon splines (part) jobs\n")
  # in parallel mode
  jobsub.add ("<parallel>")
  # common options
  inputs = "none"
  # loop over keys and generate proper command
  for key in nuPDG.iterkeys():
    cmd = "gmkspl -p " + nuPDG[key] + " -t " + targetPDG[key] + " -n " + nKnots + " -e " + maxEnergy \
          + " -o " + outXML[key] + " --event-generator-list " + generatorList[key]
    logFile = "gmkspl." + outXML[key] + ".log"
    jobsub.addJob (inputs, out, logFile, cmd)
  # done
  jobsub.add ("</parallel>")
  
def fillDAGMerge (jobsub, tag, out): 
  # check if job is done already
  if isDoneMerge (tag, out):
    msg.warning ("Nucleons merged splines found in " + out + " ... " + msg.BOLD + "skipping nun:fillDAGMerge\n", 1)
    return
  # not done, add jobs to dag
  msg.info ("\tAdding nucleon splines (merge) jobs\n")
  # in serial mode
  jobsub.add ("<serial>")
  # common options
  xmlFile = "gxspl-vN-" + tag + ".xml"  
  # merge splines job
  cmd = "gspladd -d input -o " + xmlFile
  inputs = out + "/*.xml"
  logFile = "gspladd.log"
  jobsub.addJob (inputs, out, logFile, cmd)
  # convert to root job
  rootFile = "xsec-vN-" + tag + ".root"
  cmd = "gspl2root -p 12,-12,14,-14,16,-16 -t 1000010010,1000000010 -o " + rootFile + " -f input/" + xmlFile
  inputs = out + "/" + xmlFile
  logFile = "gspl2root.log"
  jobsub.addJob (inputs, out, logFile, cmd)
  # done
  jobsub.add ("</serial>")

def isDonePart (path):
  # check if given path contains all splines
  for spline in outXML.itervalues():
    if spline not in os.listdir (path): return False
  return True
    
def isDoneMerge (tag, path):
  if "gxspl-vN-" + tag + ".xml" not in os.listdir (path): return False
  if "xsec-vN-" + tag + ".root" not in os.listdir (path): return False
  return True
