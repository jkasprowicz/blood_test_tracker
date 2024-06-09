from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ExamResult
import fitz  # PyMuPDF
import os
from datetime import datetime
import re
    

def tracker_view(request):
    return render(request, 'enter_page.html')


def extract_exam_info(text):
    # Implement logic to handle different PDF structures
    # This function should be able to handle various structures and extract relevant info
    
    # Example: Parsing based on known patterns
    lines = text.split('\n')
    info = {}

    print(info)
    
    try:
        info['name'] = lines[0].strip()
        info['birth_date'] = datetime.strptime(lines[1].strip(), '%Y-%m-%d').date()
        info['data_entrada'] = datetime.strptime(lines[2].strip(), '%Y-%m-%d').date()
        info['material'] = lines[3].strip()
        info['exam_type'] = lines[4].strip()
        info['results'] = lines[5].strip()
        info['method'] = lines[6].strip()
        info['reference_value'] = lines[7].strip()
        info['note'] = lines[8].strip()
    except (IndexError, ValueError):
        # Handle different structure or missing values
        # Use appropriate parsing techniques for different structures
        # You can use regular expressions or other text processing methods
        pass

    return info

@csrf_exempt
def loader_view(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('file')
        print(pdf_file)
        if pdf_file:

        # Open the PDF with fitz
            pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
            print(pdf_document)
            text = ""
            print(text)
            
            # Extract text from all pages
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                text += page.get_text("text") + "\n"
                print(page_num)
                print(page)


            # Extract information using your custom function
            exam_info = extract_exam_info(text)
            print(exam_info)

            if exam_info:
                # Save to the database
                ExamResult.objects.create(
                    name=exam_info.get('name', ''),
                    birth_date=exam_info.get('birth_date', None),
                    data_entrada=exam_info.get('data_entrada', None),
                    material=exam_info.get('material', ''),
                    exam_type=exam_info.get('exam_type', ''),
                    results=exam_info.get('results', ''),
                    method=exam_info.get('method', ''),
                    reference_value=exam_info.get('reference_value', ''),
                    note=exam_info.get('note', ''),
                    uploaded_at=datetime.now()
                )
                return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No file uploaded'})
    return render(request, 'loader_page.html')