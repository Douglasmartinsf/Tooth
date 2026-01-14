from django import forms
from django.core.exceptions import ValidationError
import os


class ImageUploadForm(forms.Form):
    # O campo não pode ter o widget multiple, vamos tratar múltiplos no template
    pass

    def clean_images(self):
        images = self.files.getlist('images')

        if not images:
            raise ValidationError('Nenhuma imagem foi enviada')

        if len(images) > 50:
            raise ValidationError('Máximo de 50 imagens por vez')

        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']

        for image in images:
            # Verificar extensão do arquivo
            ext = os.path.splitext(image.name)[1].lower()

            if ext not in valid_extensions:
                raise ValidationError(
                    f"Formato inválido em '{image.name}'. Formatos aceitos: {', '.join(valid_extensions)}"
                )

            # Verificar tamanho do arquivo (máximo 10MB)
            if image.size > 10 * 1024 * 1024:
                raise ValidationError(
                    f"'{image.name}' é muito grande. Tamanho máximo: 10MB")

        return images
