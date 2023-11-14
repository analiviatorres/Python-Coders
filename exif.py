try:
    with open('/home/livia/Downloads/nos.jpg', 'rb') as image_file: #abrindo o arquivo e adicionando a variável image_file.

        marcador = image_file.read(4) #lendo os primeiros 4 bytes do arquivo para verificar se a imagem possui dados exif.
        if marcador == b'\\xFF\\xD8\\xFF\\xE1':
            print("A imagem possui dados EXIF.")
        else:
            print("A imagem não possui dados EXIF.")

        data = image_file.read()
        app1_data = b'\xFF\xE1'
        app1_find = data.find(app1_data)
        
        if app1_find != -1:
            sofo_frame = b'\xFF\xC0'
            sofo_inicio = data.find(sofo_frame, app1_find)

            if sofo_inicio != -1:
                altura = (data[sofo_inicio + 9] << 8) + data[sofo_inicio + 10]
                largura = (data[sofo_inicio + 7] << 8) + data[sofo_inicio + 8]

                print(f"Altura da imagem: {altura}")
                print(f"Largura da imagem: {largura}")

            else:
                print("Não foi possível encontrar o marcador SOF0 após o APP1.")
        else:
            print("Não foi possível encontrar o marcador APP1 na imagem.")
except IOError:
    print("Erro ao acessar o arquivo de imagem.")