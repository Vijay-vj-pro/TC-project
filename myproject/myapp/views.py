from django.shortcuts import render,get_object_or_404
from .models import datab
from PIL import Image
from django.db.models import Q
import pytesseract
from django.contrib import messages


STOP_WORDS = set([
    "i","me","my","myself", "we", "our", "ours", "ourselves", "you", "your", 
    "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", 
    "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", 
    "theirs", "themselves", "what", "which", "who", "whom", "this", "that", 
    "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", 
    "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", 
    "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", 
    "at", "by", "for", "with", "about", "against", "between", "into", "through", 
    "during", "before", "after", "above", "below", "to", "from", "up", "down", 
    "in", "out", "on", "off", "over", "under", "again", "further", "then", 
    "once", "here", "there", "when", "where", "why", "how", "all", "any", 
    "both", "each", "few", "more", "most", "other", "some", "such", "no", 
    "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", 
    "t", "can", "will", "just", "don", "should", "now"
])

def remove_stop_words(text):
    words=text.split()
    filtered_words =[word for word in words if word.lower() not in STOP_WORDS and word.isalnum()]
    return ' '.join(filtered_words)

def imageUpload(request):
    if request.method == 'POST':
        title=request.POST.get('title')
        image=request.FILES.get('image')

        if title and image:
            try:
                doc=datab.objects.create(title=title, image=image)

                image=Image.open(doc.image)

                content=pytesseract.image_to_string(image)

                filtered_text=remove_stop_words(content)

                doc.content=filtered_text
                doc.save()

                messages.success(request,'Uploaded successfully')

            except Exception as e:
                messages.error(request,f'Not Uploaded: {e}')

        else:
            messages.error(request,'Title and image are required')

    return render(request,'upload.html')


def search_view(request):
    query = request.GET.get('q', '')
    if query:
        matches = datab.objects.filter(content__icontains=query)
    else:
        matches = None
    return render(request, 'search.html', {'results': matches, 'query': query})

def image_detail(request, id):
    image = get_object_or_404(datab,id=id)
    return render(request,'image_detail.html',{'image': image})