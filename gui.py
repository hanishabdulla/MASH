import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import cv2
import threading
import serial
import serial.tools.list_ports
import time
from PIL import Image, ImageTk
from google.cloud import vision
import queue # For thread-safe communication with GUI

# --- Global Variables ---
serialInst = serial.Serial()
cap = None  # Video capture object
google_vision_client = None # Google Vision client
is_running = False # Flag to control main loops/threads
camera_active = False # Flag specifically for camera loop
serial_monitor_active = False # Flag for serial monitoring loop
camera_thread = None
serial_thread = None
root = None # Main Tkinter window

# GUI Widgets (declared globally for easy access)
video_label = None
status_text = None # Using ScrolledText for status logging
destination_label = None
diagram_canvas = None
port_entry = None
connect_button = None
start_button = None
stop_button = None
zone_widgets = {} # To store canvas item IDs for highlighting
ocr_output_text = None # To display raw OCR text

# Thread-safe queue for GUI updates from other threads
gui_queue = queue.Queue()

# --- Placeholder for your Keywords Dictionary ---
# PASTE YOUR LARGE keywords DICTIONARY HERE
keywords = {
    "-KBL-": "INVALID ", "-KDH-": "INVALID ", "-OAI-": "INVALID ", "-HME-": "LHRTRA", "-QDI-": "LHRTRA", "-SRE-": "LHRTRA", "-TDD-": "LHRTRA", "-BNX-": "LHRTRA", "-BFA-": "LHRTRA", "-BAF-": "LHRTRA", "-BPC-": "LHRTRA", "-BTA-": "LHRTRA", "-XPA-": "LHRTRA", "-ANF-": "LHRTRA", "-ARI-": "LHRTRA", "-CCP-": "LHRTRA", "-IQQ-": "LHRTRA", "-BUN-": "LHRTRA", "-MZL-": "LHRTRA", "-BKY-": "LHRTRA", "-MNB-": "LHRTRA", "-SCR-": "LHRTRA", "-BRQ-": "LHRTRA", "-OSR-": "LHRTRA", "-STI-": "LHRTRA", "-CUE-": "LHRTRA", "-MCH-": "LHRTRA", "-MZD-": "LHRTRA", "-ALX-": "DXBTRA", "-MPN-": "LHRTRA", "-GHO-": "LHRTRA", "-GTL-": "LHRTRA", "-NKM-": "HKGHUB", "-AKX-": "LHRTRA", "-GUW-": "LHRTRA", "-SCO-": "LHRTRA", "-KGF-": "DXBTRA ", "-PWQ-": "DXBTRA ", "-UKK-": "DXBTRA ", "-TRW-": "HKGHUB", "-TAE-": "HKGHUB", "-MCA-": "HKGHUB", "-MAJ-": "HKGHUB", "-MNI-": "LHRTRA", "-POL-": "LHRTRA", "-TET-": "LHRTRA", "-INU-": "HKGHUB", "-IBA-": "LHRTRA", "-KAD-": "LHRTRA", "-QRW-": "LHRTRA", "-IUE-": "HKGHUB", "-OLA-": "LHRTRA", "-OOS-": "MCTGTW", "-ROR-": "HKGHUB", "-DAV-": "LHRTRA", "-ONX-": "LHRTRA", "-AQP-": "LHRTRA", "-KTW-": "LHRTRA", "-WRO-": "LHRTRA", "-CLJ-": "LHRTRA", "-TSR-": "LHRTRA", "-HLE-": "LHRTRA", "-KSC-": "LHRTRA", "-HGA-": "DXBTRA ", "-XML-": "LHRTRA", "-XVQ-": "LHRTRA", "-XXA-": "LHRTRA", "-XZR-": "LHRTRA", "-SBH-": "LHRTRA", "-EUX-": "LHRTRA", "-HOS-": "DXBTRA ", "-HCU-": "HKGHUB", "-TNN-": "HKGHUB", "-TTT-": "HKGHUB", "-TXG-": "HKGHUB", "-MWZ-": "DXBTRA ", "-BSA-": "LHRTRA", "-ECN-": "LHRTRA", "-IGL-": "LHRTRA", "-GDT-": "LHRTRA", "-FUN-": "HKGHUB", "-DNK-": "LHRTRA", "-RTH-": "LHRTRA", "-TIA-": "LHRTRA", "-AAE-": "LHRTRA", "-ALG-": "LHRTRA", "-ORN-": "LHRTRA", "-PPG-": "LHRTRA", "-ALV-": "LHRTRA", "-CAB-": "LHRTRA", "-LAD-": "LHRTRA", "-SZA-": "LHRTRA", "-AXA-": "LHRTRA", "-ANU-": "LHRTRA", "-BHI-": "LHRTRA", "-BUE-": "LHRTRA", "-COR-": "LHRTRA", "-MDQ-": "LHRTRA", "-MDZ-": "LHRTRA", "-ROS-": "LHRTRA", "-UAQ-": "LHRTRA", "-EVN-": "DXBTRA ", "-AUA-": "LHRTRA", "-ADL-": "HKGHUB", "-BNE-": "HKGHUB", "-CBR-": "HKGHUB", "-CNS-": "HKGHUB", "-DRW-": "HKGHUB", "-MBW-": "HKGHUB", "-MEL-": "HKGHUB", "-NSW-": "HKGHUB", "-PER-": "HKGHUB", "-RQL-": "HKGHUB", "-SYD-": "HKGHUB", "-GRZ-": "LHRTRA", "-INN-": "LHRTRA", "-KLU-": "LHRTRA", "-LNZ-": "LHRTRA", "-SZG-": "LHRTRA", "-VIE-": "LHRTRA", "-BAK-": "LHRTRA", "-FPO-": "LHRTRA", "-BAH-": "DXBTRA / BAH HUB", "-DAC-": "DXBTRA ", "-BGI-": "LHRTRA", "-MSQ-": "DXBTRA ", "-BRU-": "LHRTRA", "-BZE-": "LHRTRA", "-COO-": "LHRTRA", "-BDA-": "LHRTRA", "-PBH-": "HKGHUB", "-CBB-": "LHRTRA", "-LPB-": "LHRTRA", "-SRZ-": "LHRTRA", "-SJJ-": "LHRTRA", "-GBE-": "LHRTRA", "-BEL-": "LHRTRA", "-BHZ-": "LHRTRA", "-BNU-": "LHRTRA", "-BSB-": "LHRTRA", "-CGH-": "LHRTRA", "-CPQ-": "LHRTRA", "-CWB-": "LHRTRA", "-CXJ-": "LHRTRA", "-FOR-": "LHRTRA", "-FRC-": "LHRTRA", "-GRU-": "LHRTRA", "-JOI-": "LHRTRA", "-MAO-": "LHRTRA", "-POA-": "LHRTRA", "-QSB-": "LHRTRA", "-REC-": "LHRTRA", "-RIO-": "LHRTRA", "-SJK-": "LHRTRA", "-SSA-": "LHRTRA", "-SSZ-": "LHRTRA", "-VCP-": "LHRTRA", "-VIX-": "LHRTRA", "-BWN-": "HKGHUB", "-SOF-": "LHRTRA", "-OUA-": "LHRTRA", "-BJM-": "LHRTRA", "-PNH-": "HKGHUB", "-DLA-": "LHRTRA", "-GOU-": "LHRTRA", "-MVR-": "LHRTRA", "-NGE-": "LHRTRA", "-YAO-": "LHRTRA", "-YEG-": "LHRTRA", "-YHM-": "LHRTRA", "-YHZ-": "LHRTRA", "-YLW-": "LHRTRA", "-YMX-": "LHRTRA", "-YOW-": "LHRTRA", "-YQM-": "LHRTRA", "-YQR-": "LHRTRA", "-YUL-": "LHRTRA", "-YVR-": "LHRTRA", "-YWG-": "LHRTRA", "-YXE-": "LHRTRA", "-YYC-": "LHRTRA", "-YYT-": "LHRTRA", "-RAI-": "LHRTRA", "-GCM-": "LHRTRA", "-BGF-": "LHRTRA", "-NDJ-": "LHRTRA", "-GCI-": "LHRTRA", "-JER-": "LHRTRA", "-PUQ-": "LHRTRA", "-SCL-": "LHRTRA", "-VAP-": "LHRTRA", "-BJS-": "HKGHUB", "-CAN-": "HKGHUB", "-CTU-": "HKGHUB", "-DGM-": "HKGHUB", "-DLC-": "HKGHUB", "-FOC-": "HKGHUB", "-HAK-": "HKGHUB", "-HGH-": "HKGHUB", "-PEK-": "HKGHUB", "-PVG-": "HKGHUB", "-SHA-": "HKGHUB", "-SWA-": "HKGHUB", "-SZV-": "HKGHUB", "-SZX-": "HKGHUB", "-TAO-": "HKGHUB", "-TSN-": "HKGHUB", "-WUH-": "HKGHUB", "-XIY-": "HKGHUB", "-XMN-": "HKGHUB", "-ZUH-": "HKGHUB", "-BAQ-": "LHRTRA", "-BGA-": "LHRTRA", "-BOG-": "LHRTRA", "-CLO-": "LHRTRA", "-CTG-": "LHRTRA", "-MDE-": "LHRTRA", "-PEI-": "LHRTRA", "-YVA-": "DXBTRA ", "-FIH-": "LHRTRA", "-FBM-": "DXBGTW", "-BZV-": "LHRTRA", "-PNR-": "LHRTRA", "-RAR-": "HKGHUB", "-ABJ-": "LHRTRA", "-ZAG-": "LHRTRA", "-HAV-": "LHRTRA", "-LCA-": "LHRTRA", "-PRG-": "LHRTRA", "-AAR-": "LHRTRA", "-BLL-": "LHRTRA", "-CPH-": "LHRTRA", "-FAE-": "LHRTRA", "-JIB-": "DXBTRA ", "-DOM-": "LHRTRA", "-SDQ-": "LHRTRA", "-GYE-": "LHRTRA", "-UIO-": "LHRTRA", "-CAI-": "DXBTRA ", "-PSD-": "DXBTRA ", "-SAL-": "LHRTRA", "-SSG-": "LHRTRA", "-ASM-": "DXBTRA ", "-TLL-": "LHRTRA", "-ADD-": "DXBTRA ", "-NAN-": "HKGHUB", "-SUV-": "HKGHUB", "-HEL-": "LHRTRA", "-MHQ-": "LHRTRA", "-OUL-": "LHRTRA", "-TKU-": "LHRTRA", "-TMP-": "LHRTRA", "-VAA-": "LHRTRA", "-BIQ-": "LHRTRA", "-BOD-": "LHRTRA", "-CDG-": "LHRTRA", "-LEH-": "LHRTRA", "-LIL-": "LHRTRA", "-LYS-": "LHRTRA", "-MLH-": "LHRTRA", "-MRS-": "LHRTRA", "-MZM-": "LHRTRA", "-NCE-": "LHRTRA", "-NTE-": "LHRTRA", "-ORE-": "LHRTRA", "-ORY-": "LHRTRA", "-SXB-": "LHRTRA", "-TLS-": "LHRTRA", "-CAY-": "LHRTRA", "-PPT-": "HKGHUB", "-LBV-": "LHRTRA", "-POG-": "LHRTRA", "-BJL-": "LHRTRA", "-TBS-": "LHRTRA", "-BER-": "LHRTRA", "-BFE-": "LHRTRA", "-BRE-": "LHRTRA", "-CGN-": "LHRTRA", "-DRS-": "LHRTRA", "-DTM-": "LHRTRA", "-DUS-": "LHRTRA", "-ERF-": "LHRTRA", "-FNB-": "LHRTRA", "-FRA-": "LHRTRA", "-HAJ-": "LHRTRA", "-HAM-": "LHRTRA", "-HHN-": "LHRTRA", "-KEL-": "LHRTRA", "-KSF-": "LHRTRA", "-LEJ-": "LHRTRA", "-MHN-": "LHRTRA", "-MUC-": "LHRTRA", "-NUE-": "LHRTRA", "-NUM-": "LHRTRA", "-QFB-": "LHRTRA", "-QWU-": "LHRTRA", "-RMS-": "LHRTRA", "-SCN-": "LHRTRA", "-SGE-": "LHRTRA", "-SPM-": "LHRTRA", "-STR-": "LHRTRA", "-ZNJ-": "LHRTRA", "-ZNV-": "LHRTRA", "-ZPE-": "LHRTRA", "-ZPF-": "LHRTRA", "-ZPR-": "LHRTRA", "-ZQL-": "LHRTRA", "-ZTZ-": "LHRTRA", "-ACC-": "LHRTRA", "-GIB-": "LHRTRA", "-ATH-": "LHRTRA", "-HER-": "LHRTRA", "-SKG-": "LHRTRA", "-SFJ-": "LHRTRA", "-GND-": "LHRTRA", "-PTP-": "LHRTRA", "-GUM-": "HKGHUB", "-CKY-": "LHRTRA", "-BXO-": "LHRTRA", "-GEO-": "LHRTRA", "-PAP-": "LHRTRA", "-SAP-": "LHRTRA", "-TGU-": "LHRTRA", "-HKG-": "HKGHUB", "-BUD-": "LHRTRA", "-REK-": "LHRTRA", "-AMD-": "HKGHUB", "-BLR-": "HKGHUB", "-BOM-": "HKGHUB", "-CCU-": "HKGHUB", "-CJB-": "HKGHUB", "-COK-": "HKGHUB", "-DEL-": "HKGHUB", "-HYD-": "HKGHUB", "-IPF-": "HKGHUB", "-JAI-": "HKGHUB", "-MAA-": "HKGHUB", "-PNQ-": "HKGHUB", "-VBA-": "HKGHUB", "-VIF-": "HKGHUB", "-VOM-": "HKGHUB", "-BDO-": "HKGHUB", "-BPN-": "HKGHUB", "-BTH-": "HKGHUB", "-CGK-": "HKGHUB", "-DPS-": "HKGHUB", "-JKT-": "HKGHUB", "-MES-": "HKGHUB", "-SRG-": "HKGHUB", "-SUB-": "HKGHUB", "-TIM-": "HKGHUB", "-UPG-": "HKGHUB", "-IFN-": "INVALID", "-KIH-": "INVALID", "-MHD-": "INVALID", "-SYZ-": "INVALID", "-TBZ-": "INVALID", "-THR-": "INVALID", "-BGW-": "DXBTRA ", "-BSR-": "DXBTRA ", "-EBL-": "DXBTRA ", "-ISU-": "DXBTRA ", "-DUB-": "LHRTRA", "-ORK-": "LHRTRA", "-SNN-": "LHRTRA", "-SXL-": "LHRTRA", "-BEV-": "LHRTRA", "-HFA-": "LHRTRA", "-SDV-": "LHRTRA", "-TLV-": "LHRTRA", "-ZDM-": "LHRTRA", "-AOI-": "LHRTRA", "-BGY-": "LHRTRA", "-BLQ-": "LHRTRA", "-BRI-": "LHRTRA", "-CAG-": "LHRTRA", "-CTA-": "LHRTRA", "-FLR-": "LHRTRA", "-GOA-": "LHRTRA", "-LEG-": "LHRTRA", "-MIL-": "LHRTRA", "-MXP-": "LHRTRA", "-NAP-": "LHRTRA", "-QAL-": "LHRTRA", "-QBS-": "LHRTRA", "-QPG-": "LHRTRA", "-RMI-": "LHRTRA", "-ROM-": "LHRTRA", "-RRO-": "LHRTRA", "-TRN-": "LHRTRA", "-TRS-": "LHRTRA", "-TSF-": "LHRTRA", "-VCE-": "LHRTRA", "-VRN-": "LHRTRA", "-KIN-": "LHRTRA", "-MBJ-": "LHRTRA", "-FUK-": "HKGHUB", "-KIX-": "HKGHUB", "-NGO-": "HKGHUB", "-NRT-": "HKGHUB", "-OSA-": "HKGHUB", "-TYO-": "HKGHUB", "-YOK-": "HKGHUB", "-AMM-": "DXBTRA ", "-AQJ-": "DXBTRA ", "-ALA-": "DXBTRA ", "-TSE-": "DXBTRA ", "-MBA-": "LHRTRA", "-NBO-": "LHRTRA", "-CXI-": "HKGHUB", "-ICN-": "HKGHUB", "-KWI-": "KWIGTW", "-FRU-": "DXBTRA ", "-VTE-": "HKGHUB", "-RIX-": "LHRTRA", "-BEY-": "DXBTRA ", "-MSU-": "LHRTRA", "-TIP-": "LHRTRA", "-VNO-": "LHRTRA", "-LUX-": "LHRTRA", "-SKP-": "LHRTRA", "-TNR-": "LHRTRA", "-BLZ-": "LHRTRA", "-LLW-": "LHRTRA", "-BKI-": "HKGHUB", "-KUL-": "HKGHUB", "-PEN-": "HKGHUB", "-SZB-": "HKGHUB", "-JHB-": "HKGHUB", "-MLE-": "LHRTRA", "-BKO-": "LHRTRA", "-MLA-": "LHRTRA", "-FDF-": "LHRTRA", "-NKC-": "LHRTRA", "-MRU-": "DXBTRA ", "-DZA-": "LHRTRA", "-ACA-": "LHRTRA", "-AGU-": "LHRTRA", "-BJX-": "LHRTRA", "-CEN-": "LHRTRA", "-CJS-": "LHRTRA", "-CLQ-": "LHRTRA", "-CME-": "LHRTRA", "-CUL-": "LHRTRA", "-CUN-": "LHRTRA", "-CUU-": "LHRTRA", "-CVJ-": "LHRTRA", "-CYY-": "LHRTRA", "-DCB-": "LHRTRA", "-DGG-": "LHRTRA", "-FMX-": "LHRTRA", "-GDL-": "LHRTRA", "-HMO-": "LHRTRA", "-HMX-": "LHRTRA", "-HPU-": "LHRTRA", "-JAL-": "LHRTRA", "-JJC-": "LHRTRA", "-JMX-": "LHRTRA", "-LAP-": "LHRTRA", "-LEN-": "LHRTRA", "-LMM-": "LHRTRA", "-MAM-": "LHRTRA", "-MEX-": "LHRTRA", "-MID-": "LHRTRA", "-MLM-": "LHRTRA", "-MTT-": "LHRTRA", "-MTY-": "LHRTRA", "-MXL-": "LHRTRA", "-MZT-": "LHRTRA", "-NLD-": "LHRTRA", "-NLU-": "LHRTRA", "-NMX-": "LHRTRA", "-OAX-": "LHRTRA", "-OMX-": "LHRTRA", "-PAZ-": "LHRTRA", "-PBC-": "LHRTRA", "-PVR-": "LHRTRA", "-QRO-": "LHRTRA", "-REF-": "LHRTRA", "-RMX-": "LHRTRA", "-SLP-": "LHRTRA", "-SLW-": "LHRTRA", "-TAM-": "LHRTRA", "-TAP-": "LHRTRA", "-TGZ-": "LHRTRA", "-TIJ-": "LHRTRA", "-TLC-": "LHRTRA", "-TNY-": "LHRTRA", "-TRC-": "LHRTRA", "-VER-": "LHRTRA", "-VSA-": "LHRTRA", "-ZCL-": "LHRTRA", "-ZIH-": "LHRTRA", "-ZLO-": "LHRTRA", "-PNI-": "HKGHUB", "-KIV-": "LHRTRA", "-ULN-": "HKGHUB", "-TGD-": "LHRTRA", "-CAS-": "LHRTRA", "-RBA-": "LHRTRA", "-TNG-": "LHRTRA", "-BEW-": "LHRTRA", "-MPM-": "LHRTRA", "-RGN-": "HKGHUB", "-WDH-": "LHRTRA", "-KTM-": "DXBTRA ", "-AMS-": "LHRTRA", "-EIN-": "LHRTRA", "-RTM-": "LHRTRA", "-BON-": "LHRTRA", "-CUR-": "LHRTRA", "-SXM-": "LHRTRA", "-NOU-": "HKGHUB", "-AKL-": "HKGHUB", "-CHC-": "HKGHUB", "-WLG-": "HKGHUB", "-XXF-": "HKGHUB", "-MGA-": "LHRTRA", "-NIM-": "LHRTRA", "-ABV-": "LHRTRA", "-LOS-": "LHRTRA", "-PHC-": "LHRTRA", "-FNJ-": "HKGHUB", "-SPN-": "HKGHUB", "-AES-": "LHRTRA", "-BGO-": "LHRTRA", "-KRS-": "LHRTRA", "-OSL-": "LHRTRA", "-SVG-": "LHRTRA", "-TRD-": "LHRTRA", "-TRF-": "LHRTRA", "-MCT-": "MCTGTW", "-SLL-": "MCTGTW", "-ISB-": "DXBTRA ", "-KHI-": "DXBTRA ", "-LHE-": "DXBTRA", "-GZA-": "LHRTRA", "-PTY-": "LHRTRA", "-LAE-": "HKGHUB", "-POM-": "HKGHUB", "-ASU-": "LHRTRA", "-IQT-": "LHRTRA", "-LIM-": "LHRTRA", "-CEB-": "HKGHUB", "-MNL-": "HKGHUB", "-GDN-": "LHRTRA", "-POZ-": "LHRTRA", "-SZZ-": "LHRTRA", "-WAW-": "LHRTRA", "-FNC-": "LHRTRA", "-LIS-": "LHRTRA", "-OPO-": "LHRTRA", "-PDL-": "LHRTRA", "-TER-": "LHRTRA", "-PSE-": "LHRTRA", "-SJU-": "LHRTRA", "-RUN-": "LHRTRA", "-BUH-": "LHRTRA", "-AER-": "LHRTRA", "-ARH-": "LHRTRA", "-CEK-": "LHRTRA", "-DME-": "LHRTRA", "-GDX-": "LHRTRA", "-GOJ-": "LHRTRA", "-IJK-": "LHRTRA", "-IKT-": "LHRTRA", "-KGD-": "LHRTRA", "-KHV-": "LHRTRA", "-KJA-": "LHRTRA", "-KLF-": "LHRTRA", "-KRO-": "LHRTRA", "-KRR-": "LHRTRA", "-KSZ-": "LHRTRA", "-KUF-": "LHRTRA", "-KYZ-": "LHRTRA", "-KZN-": "LHRTRA", "-LED-": "LHRTRA", "-MCX-": "LHRTRA", "-MMK-": "LHRTRA", "-MOW-": "LHRTRA", "-NEF-": "LHRTRA", "-NOI-": "LHRTRA", "-NOZ-": "LHRTRA", "-OKT-": "LHRTRA", "-OMS-": "LHRTRA", "-OVB-": "LHRTRA", "-PEE-": "LHRTRA", "-REN-": "LHRTRA", "-ROV-": "LHRTRA", "-RTW-": "LHRTRA", "-SKX-": "LHRTRA", "-STW-": "LHRTRA", "-SVO-": "LHRTRA", "-SVX-": "LHRTRA", "-SWT-": "LHRTRA", "-TJM-": "LHRTRA", "-TOF-": "LHRTRA", "-TYA-": "LHRTRA", "-UFA-": "LHRTRA", "-ULY-": "LHRTRA", "-UUS-": "LHRTRA", "-VOG-": "LHRTRA", "-VOZ-": "LHRTRA", "-VVO-": "LHRTRA", "-YKS-": "LHRTRA", "-KGL-": "LHRTRA", "-SKB-": "LHRTRA", "-SLU-": "LHRTRA", "-SVD-": "LHRTRA", "-APW-": "HKGHUB", "-TMS-": "LHRTRA", "-ABT-": "DXBTRA ", "-AHB-": "DXBTRA / BAH HUB", "-AJF-": "DXBTRA / BAH HUB", "-AQI-": "DXBTRA / BAH HUB", "-DHA-": "DXBTRA / BAH HUB", "-DMM-": "DXBTRA / BAH HUB", "-EAM-": "DXBTRA / BAH HUB", "-ELQ-": "DXBTRA / BAH HUB", "-GIZ-": "DXBTRA / BAH HUB", "-HAS-": "DXBTRA / BAH HUB", "-HOF-": "DXBTRA / BAH HUB", "-JBL-": "DXBTRA / BAH HUB", "-JED-": "DXBTRA / BAH HUB", "-KHJ-": "DXBTRA / BAH HUB", "-MAC-": "DXBTRA / BAH HUB", "-MED-": "DXBTRA / BAH HUB", "-RAE-": "DXBTRA / BAH HUB", "-RUH-": "DXBTRA ", "-TIF-": "DXBTRA / BAH HUB", "-TUU-": "DXBTRA / BAH HUB", "-YAN-": "DXBTRA / BAH HUB", "-EDI-": "LHRTRA", "-DKR-": "LHRTRA", "-BEG-": "LHRTRA", "-PRN-": "LHRTRA", "-SEZ-": "DXBTRA ", "-FNA-": "LHRTRA", "-SIN-": "HKGHUB", "-BTS-": "LHRTRA", "-LJU-": "LHRTRA", "-HIR-": "HKGHUB", "-MGQ-": "LHRTRA", "-CPT-": "LHRTRA", "-DUR-": "LHRTRA", "-ELS-": "LHRTRA", "-JNB-": "LHRTRA", "-PLZ-": "LHRTRA", "-PRY-": "LHRTRA", "-PZB-": "LHRTRA", "-RCB-": "LHRTRA", "-WVB-": "LHRTRA", "-ZEC-": "LHRTRA", "-PUS-": "HKGHUB", "-SEL-": "HKGHUB", "-JUB-": "LHRTRA", "-BCN-": "LHRTRA", "-MAD-": "LHRTRA", "-OVD-": "LHRTRA", "-PMI-": "LHRTRA", "-SCQ-": "LHRTRA", "-VGO-": "LHRTRA", "-VIT-": "LHRTRA", "-VLC-": "LHRTRA", "-CMB-": "DXBTRA ", "-NEV-": "LHRTRA", "-KRT-": "DXBTRA ", "-PBM-": "LHRTRA", "-MTS-": "LHRTRA", "-ARN-": "LHRTRA", "-GOT-": "LHRTRA", "-MMA-": "LHRTRA", "-STO-": "LHRTRA", "-VST-": "LHRTRA", "-BSL-": "LHRTRA", "-GVA-": "LHRTRA", "-LUG-": "LHRTRA", "-ZRH-": "LHRTRA", "-ALP-": "DXBTRA ", "-DAM-": "DXBTRA ", "-KHH-": "HKGHUB", "-TPE-": "HKGHUB", "-ARK-": "DXBTRA ", "-DAR-": "DXBTRA ", "-TFN-": "LHRTRA", "-BKK-": "HKGHUB", "-HKT-": "HKGHUB", "-NAS-": "LHRTRA", "-DIL-": "HKGHUB", "-LFW-": "LHRTRA", "-TBU-": "HKGHUB", "-POS-": "LHRTRA", "-TUN-": "LHRTRA", "-ADA-": "LHRTRA", "-AYT-": "LHRTRA", "-ESB-": "LHRTRA", "-IST-": "LHRTRA", "-SAW-": "LHRTRA", "-TEQ-": "LHRTRA", "-ASB-": "LHRTRA", "-EBB-": "LHRTRA", "-JIN-": "LHRTRA", "-IEV-": "LHRTRA", "-ODS-": "LHRTRA", "-AUH-": "DXBGTW", "-DXB-": "DXBGTW", "-SHJ-": "DXBGTW", "-ZJF-": "DXBGTW", "-ABZ-": "LHRTRA", "-BFS-": "LHRTRA", "-BHX-": "LHRTRA", "-BRS-": "LHRTRA", "-CBG-": "LHRTRA", "-EMA-": "LHRTRA", "-EXT-": "LHRTRA", "-GLA-": "LHRTRA", "-INV-": "LHRTRA", "-IOM-": "LHRTRA", "-IPW-": "LHRTRA", "-LBA-": "LHRTRA", "-LDY-": "LHRTRA", "-LPL-": "LHRTRA", "-MAN-": "LHRTRA", "-MME-": "LHRTRA", "-NCL-": "LHRTRA", "-LCY-": "LHRHUB", "-LGW-": "LHRHUB", "-LHR-": "LHRHUB", "-LON-": "LHRHUB", "-LTN-": "LHRHUB", "-MSE-": "LHRHUB", "-OXF-": "LHRHUB", "-RED-": "LHRHUB", "-SOU-": "LHRHUB", "-STN-": "LHRHUB", "-SWN-": "LHRHUB", "-ZLS-": "LHRHUB", "-MVD-": "LHRTRA", "-ACY-": "LHRTRA ", "-ALB-": "LHRTRA ", "-ALE-": "LHRTRA ", "-ANC-": "LHRTRA ", "-ATL-": "LHRTRA ", "-AUS-": "LHRTRA ", "-BCT-": "LHRTRA ", "-BFI-": "LHRTRA ", "-BHM-": "LHRTRA ", "-BNA-": "LHRTRA ", "-BOS-": "LHRTRA ", "-BQK-": "LHRTRA ", "-BWI-": "LHRTRA ", "-CHS-": "LHRTRA ", "-CID-": "LHRTRA ", "-CLE-": "LHRTRA ", "-CLT-": "LHRTRA ", "-CLU-": "LHRTRA ", "-COP-": "LHRTRA ", "-CVG-": "LHRTRA ", "-DAY-": "LHRTRA ", "-DCA-": "LHRTRA ", "-DEN-": "LHRTRA ", "-DTW-": "LHRTRA ", "-DWF-": "LHRTRA ", "-ELA-": "LHRTRA ", "-ELP-": "LHRTRA ", "-ELZ-": "LHRTRA ", "-FCH-": "LHRTRA ", "-FFT-": "LHRTRA ", "-FMY-": "LHRTRA ", "-FRG-": "LHRTRA ", "-FTK-": "LHRTRA ", "-FYV-": "LHRTRA ", "-GRR-": "LHRTRA ", "-GSO-": "LHRTRA ", "-GSP-": "LHRTRA ", "-HHH-": "LHRTRA ", "-HNL-": "LHRTRA ", "-HRL-": "LHRTRA ", "-IAH-": "LHRTRA ", "-ICT-": "LHRTRA ", "-JAX-": "LHRTRA ", "-JCC-": "LHRTRA ", "-JFB-": "LHRTRA ", "-JFK-": "LHRTRA ", "-LAS-": "LHRTRA ", "-LAX-": "LHRTRA ", "-LGA-": "LHRTRA ", "-LGB-": "LHRTRA ", "-LIT-": "LHRTRA ", "-LRD-": "LHRTRA ", "-MCI-": "LHRTRA ", "-MDT-": "LHRTRA ", "-MEM-": "LHRTRA ", "-MIA-": "LHRTRA ", "-MKE-": "LHRTRA ", "-MSY-": "LHRTRA ", "-NUQ-": "LHRTRA ", "-NWK-": "LHRTRA ", "-OKC-": "LHRTRA ", "-OMA-": "LHRTRA ", "-ONT-": "LHRTRA ", "-OPF-": "LHRTRA ", "-ORD-": "LHRTRA ", "-ORL-": "LHRTRA ", "-PAO-": "LHRTRA ", "-PDX-": "LHRTRA ", "-PHL-": "LHRTRA ", "-PHX-": "LHRTRA ", "-PIT-": "LHRTRA ", "-RDU-": "LHRTRA ", "-RNH-": "LHRTRA ", "-RNO-": "LHRTRA ", "-ROC-": "LHRTRA ", "-SAT-": "LHRTRA ", "-SAV-": "LHRTRA ", "-SCK-": "LHRTRA ", "-SDF-": "LHRTRA ", "-SDM-": "LHRTRA ", "-SEE-": "LHRTRA ", "-SER-": "LHRTRA ", "-SFO-": "LHRTRA ", "-SGH-": "LHRTRA ", "-SLC-": "LHRTRA ", "-SMF-": "LHRTRA ", "-STL-": "LHRTRA ", "-STP-": "LHRTRA ", "-TMB-": "LHRTRA ", "-TTN-": "LHRTRA ", "-TUL-": "LHRTRA ", "-TUS-": "LHRTRA ", "-TXK-": "LHRTRA ", "-VNY-": "LHRTRA ", "-ZYP-": "LHRTRA ", "-TAS-": "DXBTRA ", "-VLI-": "HKGHUB", "-HAN-": "HKGHUB", "-SGN-": "HKGHUB", "-STT-": "LHRTRA", "-STX-": "LHRTRA", "-ADE-": "DXBTRA ", "-SAH-": "DXBTRA ", "-KIW-": "DXBTRA", "-LUN-": "DXBTRA", "-BUQ-": "DXBTRA", "-HRE-": "DXBTRA"
}
# --- Make sure you have a default or handle cases where no keyword is found ---


# --- Google Cloud Credentials ---
GOOGLE_CRED_PATH = "Google Cloud API Keys.json" # Ensure this path is correct

# --- GUI Update Functions (Called via queue) ---

def update_status(message):
    """Appends a message to the status text box."""
    if status_text:
        timestamp = time.strftime("%H:%M:%S")
        status_text.insert(tk.END, f"{timestamp}: {message}\n")
        status_text.see(tk.END) # Auto-scroll
    print(message) # Also print to console

def update_destination_display(code="-----", raw_ocr=""):
    """Updates the destination label and OCR output."""
    if destination_label:
        destination_label.config(text=f"Detected Destination: [ {code} ]")
    if ocr_output_text:
        ocr_output_text.delete('1.0', tk.END) # Clear previous text
        ocr_output_text.insert(tk.END, raw_ocr)

def reset_highlights():
    """Resets all diagram zones to default color."""
    if diagram_canvas:
        for zone_id in zone_widgets:
            diagram_canvas.itemconfig(zone_widgets[zone_id], fill='lightgrey') # Default color

def highlight_zone(destination_code):
    """Highlights the corresponding zone on the diagram."""
    reset_highlights() # Reset previous highlights first
    zone_to_highlight = None

    # --- Define your Zone Logic Here ---
    # This maps the final destination code (e.g., LHRTRA) to a zone number
    # Adjust this logic based on your actual sorting destinations and diagram
    if destination_code in ["LHRTRA", "LHR LHS", "DRT RDJ", "LHRHUB"]: # Example Zone 1
        zone_to_highlight = 1
    elif destination_code in ["CGWALT", "DXBTRA", "DXBGTW"]: # Example Zone 2
        zone_to_highlight = 2
    elif destination_code in ["KWGCTC", "RNDTRA", "SMRTST", "HKGHUB"]: # Example Zone 3
        zone_to_highlight = 3
    elif destination_code == "KWIGTW": # Example Zone 4
        zone_to_highlight = 4
    elif destination_code == "MCTGTW": # Example Zone 5
        zone_to_highlight = 5
    # Add more elif blocks for other zones/destinations
    elif destination_code == "INVALID":
         zone_to_highlight = 'invalid' # Special case maybe?
    else:
        zone_to_highlight = 'unknown' # Or handle unknown codes

    if diagram_canvas and zone_to_highlight in zone_widgets:
        try:
            diagram_canvas.itemconfig(zone_widgets[zone_to_highlight], fill='yellow') # Highlight color
            update_status(f"Highlighting Zone {zone_to_highlight} for {destination_code}")
        except tk.TclError as e:
            update_status(f"Error highlighting zone {zone_to_highlight}: {e}")
    elif zone_to_highlight:
         update_status(f"Zone '{zone_to_highlight}' not found in diagram widgets for {destination_code}.")


def process_gui_queue():
    """ Process updates from the queue to safely update Tkinter widgets """
    try:
        while True:
            task, args = gui_queue.get_nowait()
            task(*args)
            root.update_idletasks() # Process pending Tkinter updates
    except queue.Empty:
        pass # No updates pending
    finally:
        # Reschedule processing
        if is_running or camera_active or serial_monitor_active: # Only reschedule if something might still be running
             root.after(100, process_gui_queue) # Check queue every 100ms


# --- Core Logic Functions ---

def initialize_vision_client():
    """Initializes the Google Vision client if not already done."""
    global google_vision_client
    if google_vision_client is None:
        try:
            if not os.path.exists(GOOGLE_CRED_PATH):
                 gui_queue.put((update_status, (f"ERROR: Google credentials not found: {GOOGLE_CRED_PATH}",)))
                 return False
            google_vision_client = vision.ImageAnnotatorClient()
            gui_queue.put((update_status, ("Google Vision client initialized.",)))
            return True
        except Exception as e:
            gui_queue.put((update_status, (f"Error initializing Google Vision: {e}",)))
            return False
    return True # Already initialized

def process_image_ocr(image_frame):
    """ Perform OCR and keyword check (runs in thread). """
    global google_vision_client
    if not google_vision_client:
        gui_queue.put((update_status, ("Vision client not ready for OCR.",)))
        return

    gui_queue.put((update_status, ("Processing image with OCR...",)))
    gui_queue.put((update_destination_display, ("PROCESSING...", ""))) # Show processing state
    gui_queue.put((reset_highlights, ())) # Reset diagram

    try:
        # Convert the image to bytes
        ret, img_encoded = cv2.imencode('.jpg', image_frame)
        if not ret:
            gui_queue.put((update_status, ("Error encoding image for OCR.",)))
            return

        content = img_encoded.tobytes()
        vision_image = vision.Image(content=content)

        # Perform text detection
        response = google_vision_client.text_detection(image=vision_image)
        if response.error.message:
             raise Exception(f"Google Vision API Error: {response.error.message}")

        detected_text = ""
        if response.text_annotations:
            detected_text = response.text_annotations[0].description # Full text block

        # Check for keywords
        found_keyword = None
        for keyword_code in keywords:
            # Ensure keyword_code is treated as a string key
            if str(keyword_code).lower() in detected_text.lower():
                found_keyword = keyword_code
                break # Found the first match

        final_destination = "INVALID" # Default
        if found_keyword:
            final_destination = keywords.get(found_keyword, "INVALID").strip() # Get mapped value
        else:
            gui_queue.put((update_status, ("No matching keyword found in OCR text.",)))
            final_destination = "INVALID" # Explicitly set if no keyword found

        gui_queue.put((update_status, (f"OCR Result: Found keyword '{found_keyword}', Destination: '{final_destination}'",)))
        gui_queue.put((update_destination_display, (final_destination, detected_text))) # Update GUI
        gui_queue.put((highlight_zone, (final_destination,))) # Highlight diagram

        # Send to Arduino
        if serialInst.is_open:
            try:
                serialInst.write(f"{final_destination}\n".encode('utf-8')) # Send with newline
                gui_queue.put((update_status, (f"Sent '{final_destination}' to Arduino.",)))
            except serial.SerialException as e:
                gui_queue.put((update_status, (f"Serial write error: {e}",)))
        else:
            gui_queue.put((update_status, ("Cannot send to Arduino: Serial port not open.",)))

    except Exception as e:
        error_msg = f"Error during OCR/Processing: {e}"
        gui_queue.put((update_status, (error_msg,)))
        gui_queue.put((update_destination_display, ("ERROR", error_msg))) # Show error in GUI
        gui_queue.put((highlight_zone, ("INVALID",))) # Highlight invalid zone on error


def capture_and_process(frame):
    """ Starts the OCR processing in a separate thread. """
    if not is_running: # Don't process if stopped
        return
    gui_queue.put((update_status, ("Trigger received, starting image processing thread.",)))
    ocr_thread = threading.Thread(target=process_image_ocr, args=(frame,), daemon=True)
    ocr_thread.start()

def monitor_serial_port():
    """ Reads serial port in a loop (runs in thread). """
    global serial_monitor_active
    last_frame = None # Keep track of the latest frame for capture

    while serial_monitor_active and serialInst.is_open:
        try:
            if serialInst.in_waiting > 0:
                packet = serialInst.readline()
                try:
                    packet_str = packet.decode('utf-8').strip()
                    if packet_str: # Avoid processing empty lines
                        gui_queue.put((update_status, (f"Received from Arduino: {packet_str}",)))
                        if "OMG" in packet_str: # Check for trigger message
                             # Access the latest frame captured by the camera thread
                             current_frame = get_latest_camera_frame()
                             if current_frame is not None:
                                 capture_and_process(current_frame)
                             else:
                                 gui_queue.put((update_status, ("Trigger received, but no camera frame available.",)))

                except UnicodeDecodeError:
                    gui_queue.put((update_status, (f"Received non-UTF8 data: {packet}",)))
                except Exception as e:
                     gui_queue.put((update_status, (f"Error processing serial data: {e}",)))

            time.sleep(0.05) # Small delay to prevent busy-waiting

        except serial.SerialException as e:
            gui_queue.put((update_status, (f"Serial read error: {e}. Stopping monitor.",)))
            serial_monitor_active = False # Stop this thread on error
            # Consider attempting to reconnect or notifying user more prominently
            break
        except Exception as e:
             gui_queue.put((update_status, (f"Unexpected error in serial monitor: {e}",)))
             time.sleep(1) # Avoid rapid error loops

    gui_queue.put((update_status, ("Serial monitoring stopped.",)))


# --- Camera Handling ---
latest_frame = None
frame_lock = threading.Lock()

def camera_loop():
    """ Captures frames from the camera (runs in thread or via root.after). """
    global cap, camera_active, latest_frame
    if not camera_active or not cap or not cap.isOpened():
        gui_queue.put((update_status, ("Camera loop stopping or camera not ready.",)))
        camera_active = False
        return

    ret, frame = cap.read()
    if ret:
        # Store the latest frame thread-safely
        with frame_lock:
            latest_frame = frame.copy()

        # Convert frame for Tkinter display
        try:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            # Resize image to fit the label area if necessary (optional)
            # img = img.resize((width, height), Image.Resampling.LANCZOS)
            imgtk = ImageTk.PhotoImage(image=img)

            if video_label:
                video_label.imgtk = imgtk # Keep reference
                video_label.config(image=imgtk)
        except Exception as e:
            gui_queue.put((update_status, (f"Error updating camera feed: {e}",)))
            camera_active = False # Stop on error

    else:
        gui_queue.put((update_status, ("Error reading frame from camera.",)))
        camera_active = False # Stop if reading fails

    # Reschedule the next frame capture if still active
    if camera_active:
        root.after(30, camera_loop) # Aim for ~30 FPS update rate in GUI

def get_latest_camera_frame():
    """ Safely gets the latest captured frame. """
    with frame_lock:
        return latest_frame

# --- Button Actions ---

def connect_serial():
    """ Attempts to connect to the specified serial port. """
    global serialInst
    port = port_entry.get()
    if not port:
        messagebox.showerror("Error", "Please enter a serial port.")
        return

    if serialInst.is_open:
        gui_queue.put((update_status, ("Already connected. Disconnect first.",)))
        return

    try:
        # Try common baud rates or stick to 9600 if that's fixed
        serialInst.port = port
        serialInst.baudrate = 9600
        serialInst.timeout = 0.1 # Read timeout
        serialInst.write_timeout = 0.5 # Write timeout
        serialInst.open()
        gui_queue.put((update_status, (f"Successfully connected to {port}.",)))
        connect_button.config(text="Disconnect", command=disconnect_serial)
        start_button.config(state=tk.NORMAL) # Enable start button
    except serial.SerialException as e:
        messagebox.showerror("Connection Error", f"Failed to connect to {port}:\n{e}")
        gui_queue.put((update_status, (f"Failed to connect to {port}: {e}",)))
    except Exception as e:
         messagebox.showerror("Connection Error", f"An unexpected error occurred:\n{e}")
         gui_queue.put((update_status, (f"Unexpected error connecting: {e}",)))


def disconnect_serial():
    """ Disconnects from the serial port. """
    global serialInst, serial_monitor_active
    serial_monitor_active = False # Signal monitor thread to stop
    if serialInst.is_open:
        try:
            serialInst.close()
            gui_queue.put((update_status, ("Serial port disconnected.",)))
        except Exception as e:
             gui_queue.put((update_status, (f"Error closing serial port: {e}",)))

    connect_button.config(text="Connect", command=connect_serial)
    start_button.config(state=tk.DISABLED) # Disable start if disconnected
    stop_button.config(state=tk.DISABLED)


def start_sorting():
    """ Starts the camera feed and serial monitoring. """
    global is_running, cap, camera_active, serial_monitor_active, serial_thread

    if not serialInst.is_open:
        messagebox.showwarning("Warning", "Serial port is not connected.")
        gui_queue.put((update_status, ("Start aborted: Serial port not connected.",)))
        return

    if not initialize_vision_client():
         messagebox.showerror("Error", "Could not initialize Google Vision client. Check credentials.")
         gui_queue.put((update_status, ("Start aborted: Google Vision client init failed.",)))
         return

    is_running = True
    camera_active = True
    serial_monitor_active = True

    # Initialize Camera
    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(0) # Use camera index 0, adjust if needed
        if not cap.isOpened():
            messagebox.showerror("Camera Error", "Could not open camera.")
            gui_queue.put((update_status, ("Start aborted: Could not open camera.",)))
            is_running = False
            camera_active = False
            serial_monitor_active = False
            return
        gui_queue.put((update_status, ("Camera opened successfully.",)))

    # Start camera feed update loop (in main thread via root.after)
    root.after(10, camera_loop)

    # Start serial monitoring thread
    if serial_thread is None or not serial_thread.is_alive():
        serial_thread = threading.Thread(target=monitor_serial_port, daemon=True)
        serial_thread.start()
        gui_queue.put((update_status, ("Serial monitoring thread started.",)))

    gui_queue.put((update_status, ("Sorting process started.",)))
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    connect_button.config(state=tk.DISABLED) # Disable connect/disconnect while running
    port_entry.config(state=tk.DISABLED)


def stop_sorting():
    """ Stops the camera, serial monitoring, and processing. """
    global is_running, camera_active, serial_monitor_active, cap

    gui_queue.put((update_status, ("Stopping sorting process...",)))
    is_running = False
    camera_active = False # Signal camera loop to stop
    serial_monitor_active = False # Signal serial monitor to stop

    # Wait briefly for threads to notice the flag (optional but good practice)
    # time.sleep(0.2) # May cause GUI to hang slightly, use with caution

    # Release camera
    if cap and cap.isOpened():
        cap.release()
        gui_queue.put((update_status, ("Camera released.",)))
        # Clear the video label
        if video_label:
             video_label.config(image='')
             video_label.imgtk = None # Remove reference
        cap = None


    # No explicit join needed for daemon threads, but ensure flags are set

    gui_queue.put((update_status, ("Sorting process stopped.",)))
    start_button.config(state=tk.NORMAL if serialInst.is_open else tk.DISABLED)
    stop_button.config(state=tk.DISABLED)
    connect_button.config(state=tk.NORMAL) # Re-enable connect/disconnect
    port_entry.config(state=tk.NORMAL)
    reset_highlights()
    update_destination_display("STOPPED", "")


def on_closing():
    """ Handles window close event. """
    if is_running:
        if messagebox.askokcancel("Quit", "Sorting is running. Stop and quit?"):
            stop_sorting()
            # Ensure serial is closed if connected
            if serialInst.is_open:
                disconnect_serial()
            root.destroy()
        else:
            return # Don't close if user cancels
    else:
        # Ensure serial is closed if connected
        if serialInst.is_open:
            disconnect_serial()
        root.destroy()


# --- GUI Creation ---
def create_gui():
    global root, video_label, status_text, destination_label, diagram_canvas
    global port_entry, connect_button, start_button, stop_button, zone_widgets
    global ocr_output_text

    root = tk.Tk()
    root.title("Package Sorter Control")
    # Adjust size as needed, make it resizable
    # root.geometry("1200x700")
    root.minsize(800, 500)

    # --- Configure Main Grid Layout ---
    root.columnconfigure(0, weight=3) # Camera area gets more weight
    root.columnconfigure(1, weight=2) # Info/Diagram area
    root.rowconfigure(0, weight=1) # Main content row expands
    root.rowconfigure(1, weight=0) # Control row doesn't expand vertically
    root.rowconfigure(2, weight=0) # OCR output row

    # --- Frames ---
    left_frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
    left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    right_frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
    right_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
    right_frame.rowconfigure(0, weight=1) # Diagram canvas expands
    right_frame.rowconfigure(1, weight=0) # Destination label
    right_frame.rowconfigure(2, weight=2) # Status text expands more
    right_frame.columnconfigure(0, weight=1)

    control_frame = tk.Frame(root)
    control_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    ocr_frame = tk.Frame(root)
    ocr_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    ocr_frame.rowconfigure(0, weight=1)
    ocr_frame.columnconfigure(0, weight=1)


    # --- Left Frame Widgets (Camera) ---
    video_label = tk.Label(left_frame, bg='black')
    video_label.pack(expand=True, fill="both")

    # --- Right Frame Widgets (Diagram, Info) ---
    # Diagram Canvas
    diagram_canvas = tk.Canvas(right_frame, bg='white', relief=tk.GROOVE, bd=1)
    diagram_canvas.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    # Destination Display
    destination_label = tk.Label(right_frame, text="Detected Destination: [ ----- ]", font=("Arial", 16, "bold"), anchor="center")
    destination_label.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    # Status Display (Scrolled Text)
    status_label_frame = tk.LabelFrame(right_frame, text="Status Log")
    status_label_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
    status_label_frame.rowconfigure(0, weight=1)
    status_label_frame.columnconfigure(0, weight=1)
    status_text = scrolledtext.ScrolledText(status_label_frame, height=10, wrap=tk.WORD, state=tk.NORMAL) # Read-only via state
    status_text.grid(row=0, column=0, sticky="nsew")
    # status_text.config(state=tk.DISABLED) # Make read-only after inserting

    # --- Control Frame Widgets ---
    port_label = tk.Label(control_frame, text="Serial Port:")
    port_label.pack(side=tk.LEFT, padx=(5,0), pady=5)
    port_entry = tk.Entry(control_frame, width=20)
    port_entry.pack(side=tk.LEFT, padx=5, pady=5)

    connect_button = tk.Button(control_frame, text="Connect", width=10, command=connect_serial)
    connect_button.pack(side=tk.LEFT, padx=5, pady=5)

    start_button = tk.Button(control_frame, text="Start Sorting", width=12, command=start_sorting, state=tk.DISABLED)
    start_button.pack(side=tk.LEFT, padx=5, pady=5)

    stop_button = tk.Button(control_frame, text="Stop Sorting", width=12, command=stop_sorting, state=tk.DISABLED)
    stop_button.pack(side=tk.LEFT, padx=5, pady=5)

    # --- OCR Output Frame ---
    ocr_label_frame = tk.LabelFrame(ocr_frame, text="Raw OCR Output")
    ocr_label_frame.grid(row=0, column=0, sticky="nsew")
    ocr_label_frame.rowconfigure(0, weight=1)
    ocr_label_frame.columnconfigure(0, weight=1)
    ocr_output_text = scrolledtext.ScrolledText(ocr_label_frame, height=5, wrap=tk.WORD, state=tk.NORMAL)
    ocr_output_text.grid(row=0, column=0, sticky="nsew")

    # --- Draw Initial Diagram ---
    # Wait until canvas is drawn to get dimensions
    root.update_idletasks()
    draw_diagram() # Call function to draw shapes

    # --- Set initial status ---
    update_status("GUI Initialized. Select port and connect.")

    # --- Start GUI Queue Processor ---
    root.after(100, process_gui_queue)

    # --- Handle Window Closing ---
    root.protocol("WM_DELETE_WINDOW", on_closing)


def draw_diagram():
    """Draws the sorting zones on the canvas."""
    global zone_widgets
    if not diagram_canvas: return

    # Clear previous drawings if any
    diagram_canvas.delete("all")
    zone_widgets = {}

    # Get canvas dimensions dynamically
    canvas_width = diagram_canvas.winfo_width()
    canvas_height = diagram_canvas.winfo_height()

    if canvas_width < 50 or canvas_height < 20: # Canvas not ready yet
        root.after(50, draw_diagram) # Try again shortly
        return

    # --- Define Zone Layout (Example: 3 zones horizontally) ---
    num_zones = 3 # Adjust as needed
    zone_width = canvas_width / num_zones
    zone_height = canvas_height * 0.8 # Use 80% of height
    y_offset = canvas_height * 0.1

    # Zone 1 (Left)
    x0, y0 = 5, y_offset
    x1, y1 = zone_width - 5, y_offset + zone_height
    zone_widgets[1] = diagram_canvas.create_rectangle(x0, y0, x1, y1, fill='lightgrey', outline='black', width=2)
    diagram_canvas.create_text((x0+x1)/2, (y0+y1)/2, text="Zone 1\n(LHR/DRT)", justify=tk.CENTER)

    # Zone 2 (Middle)
    x0, y0 = zone_width + 5, y_offset
    x1, y1 = 2 * zone_width - 5, y_offset + zone_height
    zone_widgets[2] = diagram_canvas.create_rectangle(x0, y0, x1, y1, fill='lightgrey', outline='black', width=2)
    diagram_canvas.create_text((x0+x1)/2, (y0+y1)/2, text="Zone 2\n(CGW/DXB)", justify=tk.CENTER)

    # Zone 3 (Right)
    x0, y0 = 2 * zone_width + 5, y_offset
    x1, y1 = 3 * zone_width - 5, y_offset + zone_height
    zone_widgets[3] = diagram_canvas.create_rectangle(x0, y0, x1, y1, fill='lightgrey', outline='black', width=2)
    diagram_canvas.create_text((x0+x1)/2, (y0+y1)/2, text="Zone 3\n(KWG/RND/SMR/\nHKG)", justify=tk.CENTER)

    # Add more zones if needed (adjust num_zones and layout)
    # Example Zone 4 below Zone 1
    # x0, y0 = 5, y_offset + zone_height + 10
    # x1, y1 = zone_width - 5, y_offset + 2*zone_height + 10
    # zone_widgets[4] = diagram_canvas.create_rectangle(x0, y0, x1, y1, fill='lightgrey', outline='black', width=2)
    # diagram_canvas.create_text((x0+x1)/2, (y0+y1)/2, text="Zone 4\n(KWI)", justify=tk.CENTER)

    # Add placeholder for invalid/unknown if desired
    # zone_widgets['invalid'] = ... (maybe a red border around the whole thing?)


# --- Main Execution ---
if __name__ == "__main__":
    # List available serial ports in the console for user convenience
    print("Available serial ports:")
    available_ports = serial.tools.list_ports.comports()
    if not available_ports:
        print("  No serial ports found.")
    else:
        for port in available_ports:
            print(f"  {port.device} - {port.description}")

    create_gui()
    root.mainloop()
    print("Application closed.")
