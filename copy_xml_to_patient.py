import os
import shutil
import xml.etree.ElementTree as ET

# ================================================================================================
#       script para associar anotacoes xml ao paciente
# ================================================================================================


#path to directory were CT scans (*.dcm) are
LIDC_PATH = f"C:/Users/joaob/Documents/LIDC-IDRI/"

#path to directory were xml files are
XML_PATH = f"C:/Users/joaob/Documents/tcia-lidc-xml/" 

#path to store the processed data
SAVE_PATH = f'C:/Users/joaob/Documents/LIDC-IDRI-slices/'

patient_done = set()

for xml_f in sorted(os.listdir(XML_PATH)):
    xml_files = sorted(os.listdir(f"{XML_PATH}{xml_f}"))
    
    for file in xml_files:
        # Load the XML file
        tree = ET.parse(f"{XML_PATH}{xml_f}/{file}")
        root = tree.getroot()

        if root.tag == '{http://www.nih.gov/idri}IdriReadMessage': # true for XRs annotations | we only want CTs so just ignore XRs
            continue

        print(f"XML: {file}")
        done = False
        dicom_stack = None


        #find the patient (path to folder) related to xml file
        study_instance_uid = root.find('.//{*}StudyInstanceUID').text #first folder
        series_instance_uid = root.find('.//{*}SeriesInstanceUid').text #subfolder
        patient = None

        for patient_name in sorted(os.listdir(f'{LIDC_PATH}')):
            if done: break
            for study_uid in sorted(os.listdir(f'{LIDC_PATH}/{patient_name}')):

                if study_uid == study_instance_uid: # .xml file correspond with scans
                    if patient_name in patient_done: break

                    print(f'paciente: {patient_name}')
                    patient_done.add(patient_name)
                    patient = patient_name
                    done = True

                    if os.path.exists(f'{SAVE_PATH}{patient}/'):
                        shutil.copy(f'{XML_PATH}{xml_f}/{file}', f'{SAVE_PATH}{patient}') #copy .xml file to the respective patient folder

                    break