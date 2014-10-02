"""

Purpose:
   - Combines the PDF metadata from one PDF file with the data from 
       another PDF file, producing a 3rd (and complete) PDF file
   - It sets the metadata Producer field in the PDF to ""
   - It fixes capitalization of the metadata Title field
   - It optionally renames the updated file based on the Title field 
       (see code for details)
   - It optionally deletes both the PDF with the metadata and the OCR'd 
       PDF files

 Original Need: when batch processing PDF files using Abbyy FineReader
      FineReader produced PDFs with the metadata from the first PDF file 
      duplicated into every subsequent PDF (bug!). This program was written
      to restore the original metadata to each PDF.
      
 Author: Stephen Genusa
    URL: http://development.genusa.com
   Date: September 2014
   
"""

import sys
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import NameObject, createStringObject
from titlecase import titlecase


# Setup the paths where the PDF files are located
metadata_path = '~/PDFs'
pdf_path = '~/PDFs/OCRd'
updated_pdf_path = '~/PDFs/Updated'

# Delete the two original files when done?
do_old_file_delete = True
# Rename file according to the PDF title field?
do_file_rename = True
# Simple switch to test what proposed file name / title changes will be made
test_mode = False

# Only work on files for which the metadata PDF files exist
metadata_files = os.listdir(metadata_path)

# Short test data
# metadata_files = ['Fuzzing the dotNet Framework.pdf', 'Python Heavy Lifting.pdf']

files_found = len(metadata_files)
if files_found == 0:
    raise Exception("No files found in the PDF metadata directory. No work to be done.")
print "Found", files_found, "files"

# for each metadata PDF
for file_no in range(files_found):
    current_filename = metadata_files[file_no]
    
    # Load the original PDF metadata
    if os.path.isfile(os.path.join(metadata_path,current_filename)):
        pdf_metadata_input = PdfFileReader(open(os.path.join(metadata_path,current_filename), "rb"))
        pdf_metadata = pdf_metadata_input.getDocumentInfo()
        
        # If there is a Title field grab it
        if pdf_metadata.title != None:
            pdf_metadata.update({
                NameObject('/Title'): createStringObject(titlecase(pdf_metadata.title))
            })
            pdf_title = pdf_metadata.title
        else:
            pdf_title = ''
        
        # If there is a Producer field set it to ""
        if pdf_metadata.producer != None:
            pdf_metadata.update({
                NameObject('/Producer'): createStringObject(u'')
            })
        
        # If the same file name exists in the PDF directory load it 
        if os.path.isfile(os.path.join(pdf_path,current_filename)):
            pdf_input =  PdfFileReader(open(os.path.join(pdf_path,current_filename), "rb"))
    
            if not test_mode:
                print "Building new PDF file", current_filename
            
            # if the Title field is long enough, build a new file name
            new_filename = ''
            if do_file_rename and len(pdf_title) > 10:
                new_filename = pdf_title
                new_filename = new_filename.split(':')[0].split('[')[0]
                new_filename = new_filename.replace(',', ' ').replace('.', ' ').replace(';', ' ')            
                while new_filename.find('  ') > - 1:
                    new_filename = new_filename.replace('  ', ' ')
                new_filename += '.pdf'
                print new_filename        

            # Create the final PDF combining the metadata with the OCR'd PDF
            if not test_mode: 
                pdf_output = PdfFileWriter()
                pdf_output.addMetadata(pdf_metadata)
                for page in range(pdf_input.getNumPages()):
                    pdf_output.addPage(pdf_input.getPage(page))
                print "Writing new PDF "
                if do_file_rename and new_filename <> '' and not os.path.isfile(os.path.join(updated_pdf_path,new_filename)):
                    current_filename = new_filename            
                pdf_output.write(file(os.path.join(updated_pdf_path, current_filename), 'wb'))
                # Optionally delete the two original partial PDFs
                if do_old_file_delete:
                    os.remove(os.path.join(metadata_path,metadata_files[file_no]))
                    os.remove(os.path.join(pdf_path,metadata_files[file_no]))
            else:
                print "Warning: Running in Test Mode. New PDF file will not be written."
                
    
print "Job Completed"
