from django.shortcuts import render,get_object_or_404
from .models import datab 
from PIL import Image
from django.db.models import Q
import pytesseract
from django.contrib import messages
import cv2 # type: ignore 
from pytesseract import Output
from django.conf import settings
from pathlib import Path

#pytesseract.pytesseract.tesseract_cmd = r"C:\Users\RAD 176\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"


def highlight_text_in_image(image_path, keyword, output_path):
    color = (0, 0, 255)  
    padding = 3  

    img = cv2.imread(image_path)
    
    if img is None:
        print(f"Error: Could not load image from path '{image_path}'. Please check the file path.")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    d = pytesseract.image_to_data(thresh, output_type=Output.DICT)
    
    n_boxes = len(d['text'])
    highlighted = False
    
    for i in range(n_boxes):
        if keyword.lower() in d['text'][i].strip().lower(): 
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            x -= padding
            y -= padding
            w += 2 * padding
            h += 2 * padding
            
            img = cv2.rectangle(img, (x, y),(x + w, y + h),color,2) 
            highlighted = True

    cv2.imwrite(output_path, img)

    return output_path

STOP_WORDS = set([
    "i","me","my","myself", "we", "our", "ours", "ourselves", "you", "your", 
    "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", 
    "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", 
    "theirs", "themselves", "what", "which", "who", "whom", "this", "that", 
    "these", "those", "am","is", "are", "was", "were", "be", "been", "being", 
    "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", 
    "the", "and", "but","if", "or","because", "as", "until", "while", "of", 
    "at", "by", "for", "with", "about", "against", "between", "into", "through", 
    "during", "before", "after", "above", "below", "to", "from", "up", "down", 
    "in", "out", "on", "off", "over", "under", "again", "further", "then", 
    "once", "here", "there", "when", "where", "why", "how", "all", "any", 
    "both", "each", "few", "more", "most", "other", "some", "such", "no", 
    "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", 
    "t", "can", "will", "just", "don", "should","now"
])

def remove_stop_words(text):
    words=text.split()
    filtered_words =[word for word in words if word.lower() not in STOP_WORDS and word.isalnum()]
    return ' '.join(filtered_words)

def imageUpload(request):
    if request.method == 'POST':
        title=request.POST.get('title')
        image=request.FILES.get('image')
        jn = request.POST.get('jn')
        vn = request.POST.get('vn')
        sn = request.POST.get('sn')
        my = request.POST.get('my')

        if title and image:
            try:
                doc=datab.objects.create(title=title,image=image,jn=jn,vn=vn,sn=sn,my=my)

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
    keyword = query
    if query:
        matches = datab.objects.filter(content__icontains=query)
    else:
        matches = None
    return render(request, 'search.html', {'results': matches, 'query': query})


def image_detail(request, id):
    image = get_object_or_404(datab, id=id)
    keyword = request.GET.get('keyword', '')

    highlight_path = Path(settings.MEDIA_ROOT) / f"highlighted_images/highlight_img_.jpg"
    
    output_path = highlight_text_in_image(image.image.path,keyword,str(highlight_path))
    
    relative_path = highlight_path.relative_to(settings.MEDIA_ROOT)
    highlighted_image_url = f"{settings.MEDIA_URL}{relative_path}"

    return render(request, 'image_detail.html', {'highlighted_image_url': highlighted_image_url, 'image' : image})


def year_fun(request):
    '''
    year = request.POST.get('year')
    pdf = request.FILES.get('pdf')
    
    if year and pdf:
        try:
            doc2 = datab2.objects.create(year=year,pdf=pdf)
            doc2.save()
            messages.success("Uploaded successfully")    
        except:
            messages.error("Not uploaded")
            
    else:
        messages.error("File not found")
            '''
    return render(request,'upload_year.html')