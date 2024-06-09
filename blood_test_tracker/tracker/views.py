from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ExamResult
import fitz  # PyMuPDF
import os
from datetime import datetime
import re
import spacy

nlp = spacy.load("pt_core_news_sm")


def tracker_view(request):
    return render(request, 'enter_page.html')




def extract_information(text):
    # Perform named entity recognition
    doc = nlp(text)

    # Initialize variables for extracted information
    name = None
    birth_date = None
    data_entrada = None
    material = None
    exam_type = None
    results = None
    method = None
    reference_value = None
    note = None

    # Iterate through named entities
    for ent in doc.ents:
        if ent.label_ == 'PER':
            name = ent.text
        elif ent.label_ == 'DATE' and 'Data de Nascimento' in ent.text:
            birth_date = datetime.strptime(ent.text.split(':')[1].strip(), '%d/%m/%Y').date()
        # Add more conditions to extract other attributes

        print(name)
        print(birth_date)

    # Return extracted information
    return {
        'name': name,
        'birth_date': birth_date,
        'data_entrada': data_entrada,
        'material': material,
        'exam_type': exam_type,
        'results': results,
        'method': method,
        'reference_value': reference_value,
        'note': note,
    }


@csrf_exempt
def loader_view(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('file')
        if pdf_file:
            try:
                # Open the PDF with fitz
                pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
                text = ""

                # Extract text from all pages
                for page_num in range(pdf_document.page_count):
                    page = pdf_document.load_page(page_num)
                    text += page.get_text("text") + "\n"

                # Extract information using spaCy
                extracted_info = extract_information(text)
                print(extracted_info)

                if extracted_info['name'] and extracted_info['birth_date']:
                    # Save to the database
                    ExamResult.objects.create(
                        name=extracted_info['name'],
                        birth_date=extracted_info['birth_date'],
                        data_entrada=extracted_info['data_entrada'],
                        material=extracted_info['material'],
                        exam_type=extracted_info['exam_type'],
                        results=extracted_info['results'],
                        method=extracted_info['method'],
                        reference_value=extracted_info['reference_value'],
                        note=extracted_info['note'],
                        uploaded_at=datetime.now()
                    )
                    return JsonResponse({'status': 'success'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'No entities extracted or incomplete information'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
        else:
            return JsonResponse({'status': 'error', 'message': 'No file uploaded'})
    return render(request, 'loader_page.html')