import numpy as np
from django.shortcuts import render
from django.core.files.base import ContentFile
from .forms import ImageUploadForm
from .models import Upload
from io import BytesIO
import cv2
from .predict_unet import main


def upload_and_process_save(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded = form.cleaned_data['image']

            # 🔥 GARANTIA ABSOLUTA: reposiciona o ponteiro
            uploaded.seek(0)

            file_bytes = uploaded.read()

            if not file_bytes:
                raise ValueError("Upload veio vazio")

            np_bytes = np.frombuffer(file_bytes, dtype=np.uint8)

            outimage = main(np_bytes)

            obj = Upload.objects.create(original=uploaded)

            ok, buffer = cv2.imencode('.png', outimage)
            if not ok:
                raise ValueError("Falha ao salvar imagem resultante")

            obj.result.save(
                f"result_{obj.id}.png",
                ContentFile(buffer.tobytes()),
                save=True
            )

            return render(request, 'imagemproc/result.html', {'obj': obj})

    else:
        form = ImageUploadForm()

    return render(request, 'imagemproc/upload.html', {'form': form})

