PDF_Copy_Metadata
=================

Copy PDF Metadata from Original PDF + PDF Page Data from 2nd PDF to Final (and Complete) PDF

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
      FineReader produces PDFs with the metadata from the first PDF file 
      duplicated into every subsequent PDF (bug!). This program was written
      to restore the original metadata to each PDF.
