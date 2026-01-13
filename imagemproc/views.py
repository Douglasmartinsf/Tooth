import numpy as np
from django.shortcuts import render
from django.core.files.base import ContentFile
from .forms import ImageUploadForm
from .models import Upload
from io import BytesIO
import cv2
from .predict_unet import main
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    """Página inicial com informações introdutórias"""
    return render(request, 'imagemproc/home.html')


@login_required
def upload_and_process_save(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                uploaded = form.cleaned_data['image']

                # 🔥 GARANTIA ABSOLUTA: reposiciona o ponteiro
                uploaded.seek(0)

                file_bytes = uploaded.read()

                if not file_bytes:
                    form.add_error('image', 'Arquivo de imagem vazio ou corrompido')
                    return render(request, 'imagemproc/upload.html', {'form': form})

                np_bytes = np.frombuffer(file_bytes, dtype=np.uint8)
                
                # Tentar decodificar a imagem para verificar se é válida
                test_img = cv2.imdecode(np_bytes, cv2.IMREAD_COLOR)
                if test_img is None:
                    form.add_error('image', 'Não foi possível processar a imagem. Verifique se o arquivo não está corrompido.')
                    return render(request, 'imagemproc/upload.html', {'form': form})

                outimage = main(np_bytes)

                obj = Upload.objects.create(original=uploaded)

                ok, buffer = cv2.imencode('.png', outimage)
                if not ok:
                    form.add_error('image', 'Erro ao processar a imagem. Tente novamente.')
                    return render(request, 'imagemproc/upload.html', {'form': form})

                obj.result.save(
                    f"result_{obj.id}.png",
                    ContentFile(buffer.tobytes()),
                    save=True
                )

                return render(request, 'imagemproc/result.html', {'obj': obj})
            
            except Exception as e:
                form.add_error('image', f'Erro ao processar a imagem: {str(e)}')
                return render(request, 'imagemproc/upload.html', {'form': form})

    else:
        form = ImageUploadForm()

    return render(request, 'imagemproc/upload.html', {'form': form})
