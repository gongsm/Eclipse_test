
echo Generation XML ICDs
set PYDIR=F:/workspace/pythontest/src/python_ICDTOEXCEL_1
set ICDDIR=%~d0%~p0..\xmlFiles

python %PYDIR%/iomGenExcel.py --logfile FDAS-xx-iomgen.log FDAS_L1 FDAS_L3 FDAS_R3 -- "%ICDDIR%"
python %PYDIR%/iomGenExcel.py --logfile DMI-xx-iomgen.log IMA_DM_L4 IMA_DM_L5 IMA_DM_R4 -- "%ICDDIR%"
python %PYDIR%/iomGenExcel.py --logfile IDU-xx-iomgen.log HF_IDUCENTER HF_IDULEFTINBOARD HF_IDULEFTOUTBOARD  HF_IDURIGHTINBOARD HF_IDURIGHTOUTBOARD -- "%ICDDIR%"
python %PYDIR%/iomGenExcel.py --logfile SYN-LL-iomgen.log --merge -o SYNOPTIC_L-icd.xlsx SYNOPTICMENUAPP_L SYNOPTICPAGEAPP_L  -- "%ICDDIR%"
python %PYDIR%/iomGenExcel.py --logfile SYN-RR-iomgen.log --merge -o SYNOPTIC_R-icd.xlsx SYNOPTICMENUAPP_R SYNOPTICPAGEAPP_R  -- "%ICDDIR%"
python %PYDIR%/iomGenExcel.py --logfile SYN-xx-iomgen.log SYNOPTICMENUAPP_L SYNOPTICMENUAPP_R SYNOPTICPAGEAPP_L SYNOPTICPAGEAPP_R -- "%ICDDIR%"

