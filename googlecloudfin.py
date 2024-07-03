import os
from google.cloud import vision

# Set the environment variable for Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'Google Cloud API Keys.json'

def detect_text(path):
    """Detects text in the file and returns it."""
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(f'{response.error.message}')
    
    return texts[0].description if texts else ""

def check_keywords(text, keywords):
    """Checks if any of the keywords are present in the text."""
    for keyword in keywords:
        if keyword in text:
            print(f"{keyword}")
            break
    else:
        print("No keywords found.")

# Keywords list
keywords = [
    "-KBL-", "-KDH-", "-OAI-", "-HME-", "-QDI-", "-SRE-", "-TDD-", "-BNX-", 
    "-BFA-", "-BAF-", "-BPC-", "-BTA-", "-XPA-", "-ANF-", "-ARI-", "-CCP-", 
    "-IQQ-", "-BUN-", "-MZL-", "-BKY-", "-MNB-", "-SCR-", "-BRQ-", "-OSR-", 
    "-STI-", "-CUE-", "-MCH-", "-MZD-", "-ALX-", "-MPN-", "-GHO-", "-GTL-", 
    "-NKM-", "-AKX-", "-GUW-", "-SCO-", "-KGF-", "-PWQ-", "-UKK-", "-TRW-", 
    "-TAE-", "-MCA-", "-MAJ-", "-MNI-", "-POL-", "-TET-", "-INU-", "-IBA-", 
    "-KAD-", "-QRW-", "-IUE-", "-OLA-", "-OOS-", "-ROR-", "-DAV-", "-ONX-", 
    "-AQP-", "-KTW-", "-WRO-", "-CLJ-", "-TSR-", "-HLE-", "-KSC-", "-HGA-", 
    "-XML-", "-XVQ-", "-XXA-", "-XZR-", "-SBH-", "-EUX-", "-HOS-", "-HCU-", 
    "-TNN-", "-TTT-", "-TXG-", "-MWZ-", "-BSA-", "-ECN-", "-IGL-", "-GDT-", 
    "-FUN-", "-DNK-", "-RTH-", "-TIA-", "-AAE-", "-ALG-", "-ORN-", "-PPG-", 
    "-ALV-", "-CAB-", "-LAD-", "-SZA-", "-AXA-", "-ANU-", "-BHI-", "-BUE-", 
    "-COR-", "-MDQ-", "-MDZ-", "-ROS-", "-UAQ-", "-EVN-", "-AUA-", "-ADL-", 
    "-BNE-", "-CBR-", "-CNS-", "-DRW-", "-MBW-", "-MEL-", "-NSW-", "-PER-", 
    "-RQL-", "-SYD-", "-GRZ-", "-INN-", "-KLU-", "-LNZ-", "-SZG-", "-VIE-", 
    "-BAK-", "-FPO-", "-BAH-", "-DAC-", "-BGI-", "-MSQ-", "-BRU-", "-BZE-", 
    "-COO-", "-BDA-", "-PBH-", "-CBB-", "-LPB-", "-SRZ-", "-SJJ-", "-GBE-", 
    "-BEL-", "-BHZ-", "-BNU-", "-BSB-", "-CGH-", "-CPQ-", "-CWB-", "-CXJ-", 
    "-FOR-", "-FRC-", "-GRU-", "-JOI-", "-MAO-", "-POA-", "-QSB-", "-REC-", 
    "-RIO-", "-SJK-", "-SSA-", "-SSZ-", "-VCP-", "-VIX-", "-BWN-", "-SOF-", 
    "-OUA-", "-BJM-", "-PNH-", "-DLA-", "-GOU-", "-MVR-", "-NGE-", "-YAO-", 
    "-YEG-", "-YHM-", "-YHZ-", "-YLW-", "-YMX-", "-YOW-", "-YQM-", "-YQR-", 
    "-YUL-", "-YVR-", "-YWG-", "-YXE-", "-YYC-", "-YYT-", "-RAI-", "-GCM-", 
    "-BGF-", "-NDJ-", "-GCI-", "-JER-", "-PUQ-", "-SCL-", "-VAP-", "-BJS-", 
    "-CAN-", "-CTU-", "-DGM-", "-DLC-", "-FOC-", "-HAK-", "-HGH-", "-PEK-", 
    "-PVG-", "-SHA-", "-SWA-", "-SZV-", "-SZX-", "-TAO-", "-TSN-", "-WUH-", 
    "-XIY-", "-XMN-", "-ZUH-", "-BAQ-", "-BGA-", "-BOG-", "-CLO-", "-CTG-", 
    "-MDE-", "-PEI-", "-YVA-", "-FIH-", "-FBM-", "-BZV-", "-PNR-", "-RAR-", 
    "-ABJ-", "-ZAG-", "-HAV-", "-LCA-", "-PRG-", "-AAR-", "-BLL-", "-CPH-", 
    "-FAE-", "-JIB-", "-DOM-", "-SDQ-", "-GYE-", "-UIO-", "-CAI-", "-PSD-", 
    "-SAL-", "-SSG-", "-ASM-", "-TLL-", "-ADD-", "-NAN-", "-SUV-", "-HEL-", 
    "-MHQ-", "-OUL-", "-TKU-", "-TMP-", "-VAA-", "-BIQ-", "-BOD-", "-CDG-", 
    "-LEH-", "-LIL-", "-LYS-", "-MLH-", "-MRS-", "-MZM-", "-NCE-", "-NTE-", 
    "-ORE-", "-ORY-", "-SXB-", "-TLS-", "-CAY-", "-PPT-", "-LBV-", "-POG-", 
    "-BJL-", "-TBS-", "-BER-", "-BFE-", "-BRE-", "-CGN-", "-DRS-", "-DTM-", 
    "-DUS-", "-ERF-", "-FNB-", "-FRA-", "-HAJ-", "-HAM-", "-HHN-", "-KEL-", 
    "-KSF-", "-LEJ-", "-MHN-", "-MUC-", "-NUE-", "-NUM-", "-QFB-", "-QWU-", 
    "-RMS-", "-SCN-", "-SGE-", "-SPM-", "-STR-", "-ZNJ-", "-ZNV-", "-ZPE-", 
    "-ZPF-", "-ZPR-", "-ZQL-", "-ZTZ-", "-ACC-", "-GIB-", "-ATH-", "-HER-", 
    "-SKG-", "-SFJ-", "-GND-", "-PTP-", "-GUM-", "-CKY-", "-BXO-", "-GEO-", 
    "-PAP-", "-SAP-", "-TGU-", "-HKG-", "-BUD-", "-REK-", "-AMD-", "-BLR-", 
    "-BOM-", "-CCU-", "-CJB-", "-COK-", "-DEL-", "-HYD-", "-IPF-", "-JAI-", 
    "-MAA-", "-PNQ-", "-VBA-", "-VIF-", "-VOM-", "-BDO-", "-BPN-", "-BTH-", 
    "-CGK-", "-DPS-", "-JKT-", "-MES-", "-SRG-", "-SUB-", "-TIM-", "-UPG-", 
    "-IFN-", "-KIH-", "-MHD-", "-SYZ-", "-TBZ-", "-THR-", "-BGW-", "-BSR-", 
    "-EBL-", "-ISU-", "-DUB-", "-ORK-", "-SNN-", "-SXL-", "-BEV-", "-HFA-", 
    "-SDV-", "-TLV-", "-ZDM-", "-AOI-", "-BGY-", "-BLQ-", "-BRI-", "-CAG-", 
    "-CTA-", "-FLR-", "-GOA-", "-LEG-", "-MIL-", "-MXP-", "-NAP-", "-QAL-", 
    "-QBS-", "-QPG-", "-RMI-", "-ROM-", "-RRO-", "-TRN-", "-TRS-", "-TSF-", 
    "-VCE-", "-VRN-", "-KIN-", "-MBJ-", "-FUK-", "-KIX-", "-NGO-", "-NRT-", 
    "-OSA-", "-TYO-", "-YOK-", "-AMM-", "-AQJ-", "-ALA-", "-TSE-", "-MBA-", 
    "-NBO-", "-CXI-", "-ICN-", "-KWI-", "-FRU-", "-VTE-", "-RIX-", "-BEY-", 
    "-MSU-", "-TIP-", "-VNO-", "-LUX-", "-SKP-", "-TNR-", "-BLZ-", "-LLW-", 
    "-BKI-", "-KUL-", "-PEN-", "-SZB-", "-JHB-", "-MLE-", "-BKO-", "-MLA-", 
    "-FDF-", "-NKC-", "-MRU-", "-DZA-", "-ACA-", "-AGU-", "-BJX-", "-CEN-", 
    "-CJS-", "-CLQ-", "-CME-", "-CUL-", "-CUN-", "-CUU-", "-CVJ-", "-CYY-", 
    "-DCB-", "-DGG-", "-FMX-", "-GDL-", "-HMO-", "-HMX-", "-HPU-", "-JAL-", 
    "-JJC-", "-JMX-", "-LAP-", "-LEN-", "-LMM-", "-MAM-", "-MEX-", "-MID-", 
    "-MLM-", "-MTT-", "-MTY-", "-MXL-", "-MZT-", "-NLD-", "-NLU-", "-NMX-", 
    "-OAX-", "-OMX-", "-PAZ-", "-PBC-", "-PVR-", "-QRO-", "-REF-", "-RMX-", 
    "-SLP-", "-SLW-", "-TAM-", "-TAP-", "-TGZ-", "-TIJ-", "-TLC-", "-TNY-", 
    "-TRC-", "-VER-", "-VSA-", "-ZCL-", "-ZIH-", "-ZMM-", "-GYM-", "-KCM-", 
    "-KOO-", "-PTG-", "-SZF-", "-NLV-", "-ODS-", "-ADB-", "-AYT-", "-ESB-", 
    "-IST-", "-SAW-", "-TEQ-", "-ASB-", "-EBB-", "-JIN-", "-IEV-", "-ODS-", 
    "-AUH-", "-DXB-", "-SHJ-", "-ZJF-", "-ABZ-", "-BFS-", "-BHX-", "-BRS-", 
    "-CBG-", "-EMA-", "-EXT-", "-GLA-", "-INV-", "-IOM-", "-IPW-", "-LBA-", 
    "-LDY-", "-LPL-", "-MAN-", "-MME-", "-NCL-", "-LCY-", "-LHR-", "-LON-", 
    "-LGW-", "-LTN-", "-MSE-", "-OXF-", "-RED-", "-SOU-", "-STN-", "-SWN-", 
    "-ZLS-", "-MVD-", "-ACY-", "-ALB-", "-ALE-", "-ANC-", "-ATL-", "-AUS-", 
    "-BCT-", "-BFI-", "-BHM-", "-BNA-", "-BOS-", "-BQK-", "-BWI-", "-CHS-", 
    "-CID-", "-CLE-", "-CLT-", "-CLU-", "-COP-", "-CVG-", "-DAY-", "-DCA-", 
    "-DEN-", "-DTW-", "-DWF-", "-ELA-", "-ELP-", "-ELZ-", "-FCH-", "-FFT-", 
    "-FMY-", "-FRG-", "-FTK-", "-FYV-", "-GRR-", "-GSO-", "-GSP-", "-HHH-", 
    "-HNL-", "-HRL-", "-IAH-", "-ICT-", "-JAX-", "-JCC-", "-JFB-", "-JFK-", 
    "-LAS-", "-LAX-", "-LGA-", "-LGB-", "-LIT-", "-LRD-", "-MCI-", "-MDT-", 
    "-MEM-", "-MIA-", "-MKE-", "-MSY-", "-NUQ-", "-NWK-", "-OKC-", "-OMA-", 
    "-ONT-", "-OPF-", "-ORD-", "-ORL-", "-PAO-", "-PDX-", "-PHL-", "-PHX-", 
    "-PIT-", "-RDU-", "-RNH-", "-RNO-", "-ROC-", "-SAT-", "-SAV-", "-SCK-", 
    "-SDF-", "-SDM-", "-SEE-", "-SER-", "-SFO-", "-SGH-", "-SLC-", "-SMF-", 
    "-STL-", "-STP-", "-TMB-", "-TTN-", "-TUL-", "-TUS-", "-TXK-", "-VNY-", 
    "-ZYP-", "-TAS-", "-VLI-", "-HAN-", "-SGN-", "-STT-", "-STX-", "-ADE-", 
    "-SAH-", "-KIW-", "-LUN-", "-BUQ-", "-HRE-","-RUH-"
]

# Example image path
image_path = 'IMG 4710 from Heic to JPEG.jpg'

# Extract text from the image
extracted_text = detect_text(image_path)
print("Extracted Text:")
print(extracted_text)

# Check for keywords in the extracted text
check_keywords(extracted_text, keywords)
