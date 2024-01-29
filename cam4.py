import cv2 as cv
from pyzbar import pyzbar
from datetime import datetime

def salvar_resultado(dados):
    """
    Salva os dados detectados em um arquivo de texto.
    Gera um nome de arquivo com a data e hora atual.
    """
    try:
        nome_arquivo = datetime.now().strftime("%Y-%m-%d_%H.%M.%S%f") + '.txt'
        with open(nome_arquivo, 'w') as arquivo:
            arquivo.write(dados)
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")

def ler_codigos(frame, codigos_detectados):
    """
    Lê os códigos QR e barcodes do frame e retorna o frame modificado.
    Se um novo código for detectado, ele é salvo.
    """
    codigos = pyzbar.decode(frame)
    if not codigos:
        # Calcula a posição para a mensagem no canto superior direito
        texto = "Nenhum codigo detectado!"
        (largura_texto, altura_texto), _ = cv.getTextSize(texto, cv.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        posicao_x = frame.shape[1] - largura_texto - 10  # Subtrai a largura do texto e um pouco mais para margem
        posicao_y = altura_texto + 10  # A altura do texto mais um pouco para margem

        # Exibe mensagem quando nenhum código é detectado
        cv.putText(frame, texto, (posicao_x, posicao_y), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv.LINE_AA)
    
    for codigo in codigos:
        x, y, w, h = codigo.rect
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        dados_codigo = codigo.data.decode('utf-8')
        tipo_codigo = codigo.type
        texto = f'{dados_codigo} ({tipo_codigo})'
        cv.putText(frame, texto, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if dados_codigo not in codigos_detectados:
            codigos_detectados.add(dados_codigo)
            salvar_resultado(dados_codigo)

    return frame


def iniciar_captura():
    """
    Inicia a captura de vídeo e processa os frames para detecção de códigos.
    """
    cap = cv.VideoCapture(1)
    codigos_detectados = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = ler_codigos(frame, codigos_detectados)
        cv.imshow('screen1', frame)
        
        if cv.waitKey(1) & 0xff == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

# Iniciar a captura de vídeo e processamento de códigos
iniciar_captura()
