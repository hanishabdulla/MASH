import os
import cv2
import threading
import serial.tools.list_ports
import serial
from datetime import datetime
from google.cloud import vision

# Set the environment variable for Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"Google Cloud API Keys.json"

# Initialize Google Cloud Vision client
client = vision.ImageAnnotatorClient()

# Arbitrary keyword dictionary for testing purposes
keywords = {"-KBL-": "INVALID ", "-KDH-": "INVALID ", "-OAI-": "INVALID ", "-HME-": "LHRTRA", "-QDI-": "LHRTRA", "-SRE-": "LHRTRA", "-TDD-": "LHRTRA", "-BNX-": "LHRTRA", "-BFA-": "LHRTRA", "-BAF-": "LHRTRA", "-BPC-": "LHRTRA", "-BTA-": "LHRTRA", "-XPA-": "LHRTRA", "-ANF-": "LHRTRA", "-ARI-": "LHRTRA", "-CCP-": "LHRTRA", "-IQQ-": "LHRTRA", "-BUN-": "LHRTRA", "-MZL-": "LHRTRA", "-BKY-": "LHRTRA", "-MNB-": "LHRTRA", "-SCR-": "LHRTRA", "-BRQ-": "LHRTRA", "-OSR-": "LHRTRA", "-STI-": "LHRTRA", "-CUE-": "LHRTRA", "-MCH-": "LHRTRA", "-MZD-": "LHRTRA", "-ALX-": "DXBTRA", "-MPN-": "LHRTRA", "-GHO-": "LHRTRA", "-GTL-": "LHRTRA", "-NKM-": "HKGHUB", "-AKX-": "LHRTRA", "-GUW-": "LHRTRA", "-SCO-": "LHRTRA", "-KGF-": "DXBTRA ", "-PWQ-": "DXBTRA ", "-UKK-": "DXBTRA ", "-TRW-": "HKGHUB", "-TAE-": "HKGHUB", "-MCA-": "HKGHUB", "-MAJ-": "HKGHUB", "-MNI-": "LHRTRA", "-POL-": "LHRTRA", "-TET-": "LHRTRA", "-INU-": "HKGHUB", "-IBA-": "LHRTRA", "-KAD-": "LHRTRA", "-QRW-": "LHRTRA", "-IUE-": "HKGHUB", "-OLA-": "LHRTRA", "-OOS-": "MCTGTW", "-ROR-": "HKGHUB", "-DAV-": "LHRTRA", "-ONX-": "LHRTRA", "-AQP-": "LHRTRA", "-KTW-": "LHRTRA", "-WRO-": "LHRTRA", "-CLJ-": "LHRTRA", "-TSR-": "LHRTRA", "-HLE-": "LHRTRA", "-KSC-": "LHRTRA", "-HGA-": "DXBTRA ", "-XML-": "LHRTRA", "-XVQ-": "LHRTRA", "-XXA-": "LHRTRA", "-XZR-": "LHRTRA", "-SBH-": "LHRTRA", "-EUX-": "LHRTRA", "-HOS-": "DXBTRA ", "-HCU-": "HKGHUB", "-TNN-": "HKGHUB", "-TTT-": "HKGHUB", "-TXG-": "HKGHUB", "-MWZ-": "DXBTRA ", "-BSA-": "LHRTRA", "-ECN-": "LHRTRA", "-IGL-": "LHRTRA", "-GDT-": "LHRTRA", "-FUN-": "HKGHUB", "-DNK-": "LHRTRA", "-RTH-": "LHRTRA", "-TIA-": "LHRTRA", "-AAE-": "LHRTRA", "-ALG-": "LHRTRA", "-ORN-": "LHRTRA", "-PPG-": "LHRTRA", "-ALV-": "LHRTRA", "-CAB-": "LHRTRA", "-LAD-": "LHRTRA", "-SZA-": "LHRTRA", "-AXA-": "LHRTRA", "-ANU-": "LHRTRA", "-BHI-": "LHRTRA", "-BUE-": "LHRTRA", "-COR-": "LHRTRA", "-MDQ-": "LHRTRA", "-MDZ-": "LHRTRA", "-ROS-": "LHRTRA", "-UAQ-": "LHRTRA", "-EVN-": "DXBTRA ", "-AUA-": "LHRTRA", "-ADL-": "HKGHUB", "-BNE-": "HKGHUB", "-CBR-": "HKGHUB", "-CNS-": "HKGHUB", "-DRW-": "HKGHUB", "-MBW-": "HKGHUB", "-MEL-": "HKGHUB", "-NSW-": "HKGHUB", "-PER-": "HKGHUB", "-RQL-": "HKGHUB", "-SYD-": "HKGHUB", "-GRZ-": "LHRTRA", "-INN-": "LHRTRA", "-KLU-": "LHRTRA", "-LNZ-": "LHRTRA", "-SZG-": "LHRTRA", "-VIE-": "LHRTRA", "-BAK-": "LHRTRA", "-FPO-": "LHRTRA", "-BAH-": "DXBTRA / BAH HUB", "-DAC-": "DXBTRA ", "-BGI-": "LHRTRA", "-MSQ-": "DXBTRA ", "-BRU-": "LHRTRA", "-BZE-": "LHRTRA", "-COO-": "LHRTRA", "-BDA-": "LHRTRA", "-PBH-": "HKGHUB", "-CBB-": "LHRTRA", "-LPB-": "LHRTRA", "-SRZ-": "LHRTRA", "-SJJ-": "LHRTRA", "-GBE-": "LHRTRA", "-BEL-": "LHRTRA", "-BHZ-": "LHRTRA", "-BNU-": "LHRTRA", "-BSB-": "LHRTRA", "-CGH-": "LHRTRA", "-CPQ-": "LHRTRA", "-CWB-": "LHRTRA", "-CXJ-": "LHRTRA", "-FOR-": "LHRTRA", "-FRC-": "LHRTRA", "-GRU-": "LHRTRA", "-JOI-": "LHRTRA", "-MAO-": "LHRTRA", "-POA-": "LHRTRA", "-QSB-": "LHRTRA", "-REC-": "LHRTRA", "-RIO-": "LHRTRA", "-SJK-": "LHRTRA", "-SSA-": "LHRTRA", "-SSZ-": "LHRTRA", "-VCP-": "LHRTRA", "-VIX-": "LHRTRA", "-BWN-": "HKGHUB", "-SOF-": "LHRTRA", "-OUA-": "LHRTRA", "-BJM-": "LHRTRA", "-PNH-": "HKGHUB", "-DLA-": "LHRTRA", "-GOU-": "LHRTRA", "-MVR-": "LHRTRA", "-NGE-": "LHRTRA", "-YAO-": "LHRTRA", "-YEG-": "LHRTRA", "-YHM-": "LHRTRA", "-YHZ-": "LHRTRA", "-YLW-": "LHRTRA", "-YMX-": "LHRTRA", "-YOW-": "LHRTRA", "-YQM-": "LHRTRA", "-YQR-": "LHRTRA", "-YUL-": "LHRTRA", "-YVR-": "LHRTRA", "-YWG-": "LHRTRA", "-YXE-": "LHRTRA", "-YYC-": "LHRTRA", "-YYT-": "LHRTRA", "-RAI-": "LHRTRA", "-GCM-": "LHRTRA", "-BGF-": "LHRTRA", "-NDJ-": "LHRTRA", "-GCI-": "LHRTRA", "-JER-": "LHRTRA", "-PUQ-": "LHRTRA", "-SCL-": "LHRTRA", "-VAP-": "LHRTRA", "-BJS-": "HKGHUB", "-CAN-": "HKGHUB", "-CTU-": "HKGHUB", "-DGM-": "HKGHUB", "-DLC-": "HKGHUB", "-FOC-": "HKGHUB", "-HAK-": "HKGHUB", "-HGH-": "HKGHUB", "-PEK-": "HKGHUB", "-PVG-": "HKGHUB", "-SHA-": "HKGHUB", "-SWA-": "HKGHUB", "-SZV-": "HKGHUB", "-SZX-": "HKGHUB", "-TAO-": "HKGHUB", "-TSN-": "HKGHUB", "-WUH-": "HKGHUB", "-XIY-": "HKGHUB", "-XMN-": "HKGHUB", "-ZUH-": "HKGHUB", "-BAQ-": "LHRTRA", "-BGA-": "LHRTRA", "-BOG-": "LHRTRA", "-CLO-": "LHRTRA", "-CTG-": "LHRTRA", "-MDE-": "LHRTRA", "-PEI-": "LHRTRA", "-YVA-": "DXBTRA ", "-FIH-": "LHRTRA", "-FBM-": "DXBGTW", "-BZV-": "LHRTRA", "-PNR-": "LHRTRA", "-RAR-": "HKGHUB", "-ABJ-": "LHRTRA", "-ZAG-": "LHRTRA", "-HAV-": "LHRTRA", "-LCA-": "LHRTRA", "-PRG-": "LHRTRA", "-AAR-": "LHRTRA", "-BLL-": "LHRTRA", "-CPH-": "LHRTRA", "-FAE-": "LHRTRA", "-JIB-": "DXBTRA ", "-DOM-": "LHRTRA", "-SDQ-": "LHRTRA", "-GYE-": "LHRTRA", "-UIO-": "LHRTRA", "-CAI-": "DXBTRA ", "-PSD-": "DXBTRA ", "-SAL-": "LHRTRA", "-SSG-": "LHRTRA", "-ASM-": "DXBTRA ", "-TLL-": "LHRTRA", "-ADD-": "DXBTRA ", "-NAN-": "HKGHUB", "-SUV-": "HKGHUB", "-HEL-": "LHRTRA", "-MHQ-": "LHRTRA", "-OUL-": "LHRTRA", "-TKU-": "LHRTRA", "-TMP-": "LHRTRA", "-VAA-": "LHRTRA", "-BIQ-": "LHRTRA", "-BOD-": "LHRTRA", "-CDG-": "LHRTRA", "-LEH-": "LHRTRA", "-LIL-": "LHRTRA", "-LYS-": "LHRTRA", "-MLH-": "LHRTRA", "-MRS-": "LHRTRA", "-MZM-": "LHRTRA", "-NCE-": "LHRTRA", "-NTE-": "LHRTRA", "-ORE-": "LHRTRA", "-ORY-": "LHRTRA", "-SXB-": "LHRTRA", "-TLS-": "LHRTRA", "-CAY-": "LHRTRA", "-PPT-": "HKGHUB", "-LBV-": "LHRTRA", "-POG-": "LHRTRA", "-BJL-": "LHRTRA", "-TBS-": "LHRTRA", "-BER-": "LHRTRA", "-BFE-": "LHRTRA", "-BRE-": "LHRTRA", "-CGN-": "LHRTRA", "-DRS-": "LHRTRA", "-DTM-": "LHRTRA", "-DUS-": "LHRTRA", "-ERF-": "LHRTRA", "-FNB-": "LHRTRA", "-FRA-": "LHRTRA", "-HAJ-": "LHRTRA", "-HAM-": "LHRTRA", "-HHN-": "LHRTRA", "-KEL-": "LHRTRA", "-KSF-": "LHRTRA", "-LEJ-": "LHRTRA", "-MHN-": "LHRTRA", "-MUC-": "LHRTRA", "-NUE-": "LHRTRA", "-NUM-": "LHRTRA", "-QFB-": "LHRTRA", "-QWU-": "LHRTRA", "-RMS-": "LHRTRA", "-SCN-": "LHRTRA", "-SGE-": "LHRTRA", "-SPM-": "LHRTRA", "-STR-": "LHRTRA", "-ZNJ-": "LHRTRA", "-ZNV-": "LHRTRA", "-ZPE-": "LHRTRA", "-ZPF-": "LHRTRA", "-ZPR-": "LHRTRA", "-ZQL-": "LHRTRA", "-ZTZ-": "LHRTRA", "-ACC-": "LHRTRA", "-GIB-": "LHRTRA", "-ATH-": "LHRTRA", "-HER-": "LHRTRA", "-SKG-": "LHRTRA", "-SFJ-": "LHRTRA", "-GND-": "LHRTRA", "-PTP-": "LHRTRA", "-GUM-": "HKGHUB", "-CKY-": "LHRTRA", "-BXO-": "LHRTRA", "-GEO-": "LHRTRA", "-PAP-": "LHRTRA", "-SAP-": "LHRTRA", "-TGU-": "LHRTRA", "-HKG-": "HKGHUB", "-BUD-": "LHRTRA", "-REK-": "LHRTRA", "-AMD-": "HKGHUB", "-BLR-": "HKGHUB", "-BOM-": "HKGHUB", "-CCU-": "HKGHUB", "-CJB-": "HKGHUB", "-COK-": "HKGHUB", "-DEL-": "HKGHUB", "-HYD-": "HKGHUB", "-IPF-": "HKGHUB", "-JAI-": "HKGHUB", "-MAA-": "HKGHUB", "-PNQ-": "HKGHUB", "-VBA-": "HKGHUB", "-VIF-": "HKGHUB", "-VOM-": "HKGHUB", "-BDO-": "HKGHUB", "-BPN-": "HKGHUB", "-BTH-": "HKGHUB", "-CGK-": "HKGHUB", "-DPS-": "HKGHUB", "-JKT-": "HKGHUB", "-MES-": "HKGHUB", "-SRG-": "HKGHUB", "-SUB-": "HKGHUB", "-TIM-": "HKGHUB", "-UPG-": "HKGHUB", "-IFN-": "INVALID", "-KIH-": "INVALID", "-MHD-": "INVALID", "-SYZ-": "INVALID", "-TBZ-": "INVALID", "-THR-": "INVALID", "-BGW-": "DXBTRA ", "-BSR-": "DXBTRA ", "-EBL-": "DXBTRA ", "-ISU-": "DXBTRA ", "-DUB-": "LHRTRA", "-ORK-": "LHRTRA", "-SNN-": "LHRTRA", "-SXL-": "LHRTRA", "-BEV-": "LHRTRA", "-HFA-": "LHRTRA", "-SDV-": "LHRTRA", "-TLV-": "LHRTRA", "-ZDM-": "LHRTRA", "-AOI-": "LHRTRA", "-BGY-": "LHRTRA", "-BLQ-": "LHRTRA", "-BRI-": "LHRTRA", "-CAG-": "LHRTRA", "-CTA-": "LHRTRA", "-FLR-": "LHRTRA", "-GOA-": "LHRTRA", "-LEG-": "LHRTRA", "-MIL-": "LHRTRA", "-MXP-": "LHRTRA", "-NAP-": "LHRTRA", "-QAL-": "LHRTRA", "-QBS-": "LHRTRA", "-QPG-": "LHRTRA", "-RMI-": "LHRTRA", "-ROM-": "LHRTRA", "-RRO-": "LHRTRA", "-TRN-": "LHRTRA", "-TRS-": "LHRTRA", "-TSF-": "LHRTRA", "-VCE-": "LHRTRA", "-VRN-": "LHRTRA", "-KIN-": "LHRTRA", "-MBJ-": "LHRTRA", "-FUK-": "HKGHUB", "-KIX-": "HKGHUB", "-NGO-": "HKGHUB", "-NRT-": "HKGHUB", "-OSA-": "HKGHUB", "-TYO-": "HKGHUB", "-YOK-": "HKGHUB", "-AMM-": "DXBTRA ", "-AQJ-": "DXBTRA ", "-ALA-": "DXBTRA ", "-TSE-": "DXBTRA ", "-MBA-": "LHRTRA", "-NBO-": "LHRTRA", "-CXI-": "HKGHUB", "-ICN-": "HKGHUB", "-KWI-": "KWIGTW", "-FRU-": "DXBTRA ", "-VTE-": "HKGHUB", "-RIX-": "LHRTRA", "-BEY-": "DXBTRA ", "-MSU-": "LHRTRA", "-TIP-": "LHRTRA", "-VNO-": "LHRTRA", "-LUX-": "LHRTRA", "-SKP-": "LHRTRA", "-TNR-": "LHRTRA", "-BLZ-": "LHRTRA", "-LLW-": "LHRTRA", "-BKI-": "HKGHUB", "-KUL-": "HKGHUB", "-PEN-": "HKGHUB", "-SZB-": "HKGHUB", "-JHB-": "HKGHUB", "-MLE-": "LHRTRA", "-BKO-": "LHRTRA", "-MLA-": "LHRTRA", "-FDF-": "LHRTRA", "-NKC-": "LHRTRA", "-MRU-": "DXBTRA ", "-DZA-": "LHRTRA", "-ACA-": "LHRTRA", "-AGU-": "LHRTRA", "-BJX-": "LHRTRA", "-CEN-": "LHRTRA", "-CJS-": "LHRTRA", "-CLQ-": "LHRTRA", "-CME-": "LHRTRA", "-CUL-": "LHRTRA", "-CUN-": "LHRTRA", "-CUU-": "LHRTRA", "-CVJ-": "LHRTRA", "-CYY-": "LHRTRA", "-DCB-": "LHRTRA", "-DGG-": "LHRTRA", "-FMX-": "LHRTRA", "-GDL-": "LHRTRA", "-HMO-": "LHRTRA", "-HMX-": "LHRTRA", "-HPU-": "LHRTRA", "-JAL-": "LHRTRA", "-JJC-": "LHRTRA", "-JMX-": "LHRTRA", "-LAP-": "LHRTRA", "-LEN-": "LHRTRA", "-LMM-": "LHRTRA", "-MAM-": "LHRTRA", "-MEX-": "LHRTRA", "-MID-": "LHRTRA", "-MLM-": "LHRTRA", "-MTT-": "LHRTRA", "-MTY-": "LHRTRA", "-MXL-": "LHRTRA", "-MZT-": "LHRTRA", "-NLD-": "LHRTRA", "-NLU-": "LHRTRA", "-NMX-": "LHRTRA", "-OAX-": "LHRTRA", "-OMX-": "LHRTRA", "-PAZ-": "LHRTRA", "-PBC-": "LHRTRA", "-PVR-": "LHRTRA", "-QRO-": "LHRTRA", "-REF-": "LHRTRA", "-RMX-": "LHRTRA", "-SLP-": "LHRTRA", "-SLW-": "LHRTRA", "-TAM-": "LHRTRA", "-TAP-": "LHRTRA", "-TGZ-": "LHRTRA", "-TIJ-": "LHRTRA", "-TLC-": "LHRTRA", "-TNY-": "LHRTRA", "-TRC-": "LHRTRA", "-VER-": "LHRTRA", "-VSA-": "LHRTRA", "-ZCL-": "LHRTRA", "-ZIH-": "LHRTRA", "-ZLO-": "LHRTRA", "-PNI-": "HKGHUB", "-KIV-": "LHRTRA", "-ULN-": "HKGHUB", "-TGD-": "LHRTRA", "-CAS-": "LHRTRA", "-RBA-": "LHRTRA", "-TNG-": "LHRTRA", "-BEW-": "LHRTRA", "-MPM-": "LHRTRA", "-RGN-": "HKGHUB", "-WDH-": "LHRTRA", "-KTM-": "DXBTRA ", "-AMS-": "LHRTRA", "-EIN-": "LHRTRA", "-RTM-": "LHRTRA", "-BON-": "LHRTRA", "-CUR-": "LHRTRA", "-SXM-": "LHRTRA", "-NOU-": "HKGHUB", "-AKL-": "HKGHUB", "-CHC-": "HKGHUB", "-WLG-": "HKGHUB", "-XXF-": "HKGHUB", "-MGA-": "LHRTRA", "-NIM-": "LHRTRA", "-ABV-": "LHRTRA", "-LOS-": "LHRTRA", "-PHC-": "LHRTRA", "-FNJ-": "HKGHUB", "-SPN-": "HKGHUB", "-AES-": "LHRTRA", "-BGO-": "LHRTRA", "-KRS-": "LHRTRA", "-OSL-": "LHRTRA", "-SVG-": "LHRTRA", "-TRD-": "LHRTRA", "-TRF-": "LHRTRA", "-MCT-": "MCTGTW", "-SLL-": "MCTGTW", "-ISB-": "DXBTRA ", "-KHI-": "DXBTRA ", "-LHE-": "DXBTRA", "-GZA-": "LHRTRA", "-PTY-": "LHRTRA", "-LAE-": "HKGHUB", "-POM-": "HKGHUB", "-ASU-": "LHRTRA", "-IQT-": "LHRTRA", "-LIM-": "LHRTRA", "-CEB-": "HKGHUB", "-MNL-": "HKGHUB", "-GDN-": "LHRTRA", "-POZ-": "LHRTRA", "-SZZ-": "LHRTRA", "-WAW-": "LHRTRA", "-FNC-": "LHRTRA", "-LIS-": "LHRTRA", "-OPO-": "LHRTRA", "-PDL-": "LHRTRA", "-TER-": "LHRTRA", "-PSE-": "LHRTRA", "-SJU-": "LHRTRA", "-RUN-": "LHRTRA", "-BUH-": "LHRTRA", "-AER-": "LHRTRA", "-ARH-": "LHRTRA", "-CEK-": "LHRTRA", "-DME-": "LHRTRA", "-GDX-": "LHRTRA", "-GOJ-": "LHRTRA", "-IJK-": "LHRTRA", "-IKT-": "LHRTRA", "-KGD-": "LHRTRA", "-KHV-": "LHRTRA", "-KJA-": "LHRTRA", "-KLF-": "LHRTRA", "-KRO-": "LHRTRA", "-KRR-": "LHRTRA", "-KSZ-": "LHRTRA", "-KUF-": "LHRTRA", "-KYZ-": "LHRTRA", "-KZN-": "LHRTRA", "-LED-": "LHRTRA", "-MCX-": "LHRTRA", "-MMK-": "LHRTRA", "-MOW-": "LHRTRA", "-NEF-": "LHRTRA", "-NOI-": "LHRTRA", "-NOZ-": "LHRTRA", "-OKT-": "LHRTRA", "-OMS-": "LHRTRA", "-OVB-": "LHRTRA", "-PEE-": "LHRTRA", "-REN-": "LHRTRA", "-ROV-": "LHRTRA", "-RTW-": "LHRTRA", "-SKX-": "LHRTRA", "-STW-": "LHRTRA", "-SVO-": "LHRTRA", "-SVX-": "LHRTRA", "-SWT-": "LHRTRA", "-TJM-": "LHRTRA", "-TOF-": "LHRTRA", "-TYA-": "LHRTRA", "-UFA-": "LHRTRA", "-ULY-": "LHRTRA", "-UUS-": "LHRTRA", "-VOG-": "LHRTRA", "-VOZ-": "LHRTRA", "-VVO-": "LHRTRA", "-YKS-": "LHRTRA", "-KGL-": "LHRTRA", "-SKB-": "LHRTRA", "-SLU-": "LHRTRA", "-SVD-": "LHRTRA", "-APW-": "HKGHUB", "-TMS-": "LHRTRA", "-ABT-": "DXBTRA ", "-AHB-": "DXBTRA / BAH HUB", "-AJF-": "DXBTRA / BAH HUB", "-AQI-": "DXBTRA / BAH HUB", "-DHA-": "DXBTRA / BAH HUB", "-DMM-": "DXBTRA / BAH HUB", "-EAM-": "DXBTRA / BAH HUB", "-ELQ-": "DXBTRA / BAH HUB", "-GIZ-": "DXBTRA / BAH HUB", "-HAS-": "DXBTRA / BAH HUB", "-HOF-": "DXBTRA / BAH HUB", "-JBL-": "DXBTRA / BAH HUB", "-JED-": "DXBTRA / BAH HUB", "-KHJ-": "DXBTRA / BAH HUB", "-MAC-": "DXBTRA / BAH HUB", "-MED-": "DXBTRA / BAH HUB", "-RAE-": "DXBTRA / BAH HUB", "-RUH-": "DXBTRA ", "-TIF-": "DXBTRA / BAH HUB", "-TUU-": "DXBTRA / BAH HUB", "-YAN-": "DXBTRA / BAH HUB", "-EDI-": "LHRTRA", "-DKR-": "LHRTRA", "-BEG-": "LHRTRA", "-PRN-": "LHRTRA", "-SEZ-": "DXBTRA ", "-FNA-": "LHRTRA", "-SIN-": "HKGHUB", "-BTS-": "LHRTRA", "-LJU-": "LHRTRA", "-HIR-": "HKGHUB", "-MGQ-": "LHRTRA", "-CPT-": "LHRTRA", "-DUR-": "LHRTRA", "-ELS-": "LHRTRA", "-JNB-": "LHRTRA", "-PLZ-": "LHRTRA", "-PRY-": "LHRTRA", "-PZB-": "LHRTRA", "-RCB-": "LHRTRA", "-WVB-": "LHRTRA", "-ZEC-": "LHRTRA", "-PUS-": "HKGHUB", "-SEL-": "HKGHUB", "-JUB-": "LHRTRA", "-BCN-": "LHRTRA", "-MAD-": "LHRTRA", "-OVD-": "LHRTRA", "-PMI-": "LHRTRA", "-SCQ-": "LHRTRA", "-VGO-": "LHRTRA", "-VIT-": "LHRTRA", "-VLC-": "LHRTRA", "-CMB-": "DXBTRA ", "-NEV-": "LHRTRA", "-KRT-": "DXBTRA ", "-PBM-": "LHRTRA", "-MTS-": "LHRTRA", "-ARN-": "LHRTRA", "-GOT-": "LHRTRA", "-MMA-": "LHRTRA", "-STO-": "LHRTRA", "-VST-": "LHRTRA", "-BSL-": "LHRTRA", "-GVA-": "LHRTRA", "-LUG-": "LHRTRA", "-ZRH-": "LHRTRA", "-ALP-": "DXBTRA ", "-DAM-": "DXBTRA ", "-KHH-": "HKGHUB", "-TPE-": "HKGHUB", "-ARK-": "DXBTRA ", "-DAR-": "DXBTRA ", "-TFN-": "LHRTRA", "-BKK-": "HKGHUB", "-HKT-": "HKGHUB", "-NAS-": "LHRTRA", "-DIL-": "HKGHUB", "-LFW-": "LHRTRA", "-TBU-": "HKGHUB", "-POS-": "LHRTRA", "-TUN-": "LHRTRA", "-ADA-": "LHRTRA", "-AYT-": "LHRTRA", "-ESB-": "LHRTRA", "-IST-": "LHRTRA", "-SAW-": "LHRTRA", "-TEQ-": "LHRTRA", "-ASB-": "LHRTRA", "-EBB-": "LHRTRA", "-JIN-": "LHRTRA", "-IEV-": "LHRTRA", "-ODS-": "LHRTRA", "-AUH-": "DXBGTW", "-DXB-": "DXBGTW", "-SHJ-": "DXBGTW", "-ZJF-": "DXBGTW", "-ABZ-": "LHRTRA", "-BFS-": "LHRTRA", "-BHX-": "LHRTRA", "-BRS-": "LHRTRA", "-CBG-": "LHRTRA", "-EMA-": "LHRTRA", "-EXT-": "LHRTRA", "-GLA-": "LHRTRA", "-INV-": "LHRTRA", "-IOM-": "LHRTRA", "-IPW-": "LHRTRA", "-LBA-": "LHRTRA", "-LDY-": "LHRTRA", "-LPL-": "LHRTRA", "-MAN-": "LHRTRA", "-MME-": "LHRTRA", "-NCL-": "LHRTRA", "-LCY-": "LHRHUB", "-LGW-": "LHRHUB", "-LHR-": "LHRHUB", "-LON-": "LHRHUB", "-LTN-": "LHRHUB", "-MSE-": "LHRHUB", "-OXF-": "LHRHUB", "-RED-": "LHRHUB", "-SOU-": "LHRHUB", "-STN-": "LHRHUB", "-SWN-": "LHRHUB", "-ZLS-": "LHRHUB", "-MVD-": "LHRTRA", "-ACY-": "LHRTRA ", "-ALB-": "LHRTRA ", "-ALE-": "LHRTRA ", "-ANC-": "LHRTRA ", "-ATL-": "LHRTRA ", "-AUS-": "LHRTRA ", "-BCT-": "LHRTRA ", "-BFI-": "LHRTRA ", "-BHM-": "LHRTRA ", "-BNA-": "LHRTRA ", "-BOS-": "LHRTRA ", "-BQK-": "LHRTRA ", "-BWI-": "LHRTRA ", "-CHS-": "LHRTRA ", "-CID-": "LHRTRA ", "-CLE-": "LHRTRA ", "-CLT-": "LHRTRA ", "-CLU-": "LHRTRA ", "-COP-": "LHRTRA ", "-CVG-": "LHRTRA ", "-DAY-": "LHRTRA ", "-DCA-": "LHRTRA ", "-DEN-": "LHRTRA ", "-DTW-": "LHRTRA ", "-DWF-": "LHRTRA ", "-ELA-": "LHRTRA ", "-ELP-": "LHRTRA ", "-ELZ-": "LHRTRA ", "-FCH-": "LHRTRA ", "-FFT-": "LHRTRA ", "-FMY-": "LHRTRA ", "-FRG-": "LHRTRA ", "-FTK-": "LHRTRA ", "-FYV-": "LHRTRA ", "-GRR-": "LHRTRA ", "-GSO-": "LHRTRA ", "-GSP-": "LHRTRA ", "-HHH-": "LHRTRA ", "-HNL-": "LHRTRA ", "-HRL-": "LHRTRA ", "-IAH-": "LHRTRA ", "-ICT-": "LHRTRA ", "-JAX-": "LHRTRA ", "-JCC-": "LHRTRA ", "-JFB-": "LHRTRA ", "-JFK-": "LHRTRA ", "-LAS-": "LHRTRA ", "-LAX-": "LHRTRA ", "-LGA-": "LHRTRA ", "-LGB-": "LHRTRA ", "-LIT-": "LHRTRA ", "-LRD-": "LHRTRA ", "-MCI-": "LHRTRA ", "-MDT-": "LHRTRA ", "-MEM-": "LHRTRA ", "-MIA-": "LHRTRA ", "-MKE-": "LHRTRA ", "-MSY-": "LHRTRA ", "-NUQ-": "LHRTRA ", "-NWK-": "LHRTRA ", "-OKC-": "LHRTRA ", "-OMA-": "LHRTRA ", "-ONT-": "LHRTRA ", "-OPF-": "LHRTRA ", "-ORD-": "LHRTRA ", "-ORL-": "LHRTRA ", "-PAO-": "LHRTRA ", "-PDX-": "LHRTRA ", "-PHL-": "LHRTRA ", "-PHX-": "LHRTRA ", "-PIT-": "LHRTRA ", "-RDU-": "LHRTRA ", "-RNH-": "LHRTRA ", "-RNO-": "LHRTRA ", "-ROC-": "LHRTRA ", "-SAT-": "LHRTRA ", "-SAV-": "LHRTRA ", "-SCK-": "LHRTRA ", "-SDF-": "LHRTRA ", "-SDM-": "LHRTRA ", "-SEE-": "LHRTRA ", "-SER-": "LHRTRA ", "-SFO-": "LHRTRA ", "-SGH-": "LHRTRA ", "-SLC-": "LHRTRA ", "-SMF-": "LHRTRA ", "-STL-": "LHRTRA ", "-STP-": "LHRTRA ", "-TMB-": "LHRTRA ", "-TTN-": "LHRTRA ", "-TUL-": "LHRTRA ", "-TUS-": "LHRTRA ", "-TXK-": "LHRTRA ", "-VNY-": "LHRTRA ", "-ZYP-": "LHRTRA ", "-TAS-": "DXBTRA ", "-VLI-": "HKGHUB", "-HAN-": "HKGHUB", "-SGN-": "HKGHUB", "-STT-": "LHRTRA", "-STX-": "LHRTRA", "-ADE-": "DXBTRA ", "-SAH-": "DXBTRA ", "-KIW-": "DXBTRA", "-LUN-": "DXBTRA", "-BUQ-": "DXBTRA", "-HRE-": "DXBTRA"
}

# Function to detect the keywords
def detect_keywords(text):
    found_keywords = []
    for keyword in keywords.keys():
        if keyword in text:
            found_keywords.append(keyword)
    return found_keywords

# Function to process the image
def process_image(image_path):
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts

# Initialize serial communication
def init_serial():
    selected_port = '/dev/tty.usbmodem11101'
    return serial.Serial(selected_port, 9600, timeout=1)

# Monitor serial port
def monitor_serial(serial_conn):
    while True:
        try:
            data = serial_conn.readline().decode().strip()
            if data:
                print(f"Received: {data}")
        except Exception as e:
            print(f"Error reading serial data: {e}")

# Function to capture image from camera
def capture_image():
    cap = cv2.VideoCapture(1)  # Change the index if necessary
    if not cap.isOpened():
        print("Error: Could not open camera.")
        available_cameras = get_available_cameras()
        if available_cameras:
            print(f"Available cameras: {available_cameras}")
        else:
            print("No cameras detected.")
        return None

    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        cap.release()
        return None

    image_path = "captured_image.jpg"
    cv2.imwrite(image_path, frame)
    cap.release()
    return image_path

# Function to get available cameras
def get_available_cameras(max_cameras=10):
    available_cameras = []
    for index in range(max_cameras):
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            available_cameras.append(index)
            cap.release()
    return available_cameras

# Function to send data to Arduino
def send_to_arduino(serial_conn, message):
    try:
        serial_conn.write((message + '\n').encode())
        print(f"Sent to Arduino: {message}")
    except Exception as e:
        print(f"Error sending data to Arduino: {e}")

# Initialize the serial connection
serial_conn = init_serial()

# Start serial monitoring in a separate thread
threading.Thread(target=monitor_serial, args=(serial_conn,)).start()

# Main loop
while True:
    user_input = input("Type 'capture' to capture an image or 'exit' to quit: ").strip().lower()
    if user_input == 'exit':
        break
    elif user_input == 'capture':
        image_path = capture_image()
        if image_path:
            texts = process_image(image_path)
            if not texts:
                print("No text detected in the image.")
                send_to_arduino(serial_conn, "INVALID")
                continue

            text = texts[0].description
            print(f"Detected text: {text}")

            found_keywords = detect_keywords(text)
            if not found_keywords:
                print("No keywords found.")
                send_to_arduino(serial_conn, "INVALID")
            else:
                for keyword in found_keywords:
                    print(f"Keyword {keyword}: {keywords[keyword]}")
                    send_to_arduino(serial_conn, keywords[keyword])
    else:
        print("Invalid input. Please try again.")
