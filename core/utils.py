import io

import openpyxl
from django.http import FileResponse
from reportlab.lib import colors, utils
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from .models import Funcionario


def importar_excel(arquivo):
    workbook = openpyxl.load_workbook(arquivo)
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=2, values_only=True):
        matricula, nome, cargo, comp = row
        Funcionario.objects.create(
            matricula=matricula,
            nome=nome,
            cargo=cargo,
            comp=comp,
        )


def get_image(path, width):
    image = utils.ImageReader(path)
    aspect_ratio = float(image.getSize()[1]) / float(image.getSize()[0])
    height = aspect_ratio * width
    return path, width, height


def draw_centered_text(p, y, text, fontsize=11, fontname="Helvetica", fontstyle="normal"):
    if fontstyle == "bold":
        fontname = f"{fontname}-Bold"

    p.setFont(fontname, fontsize)
    text_width = p.stringWidth(text, fontname, fontsize)
    x = (letter[0] - text_width) / 2.2
    p.drawString(x, y, text)

def draw_info_rect(p, x, y, width, height, text, fontsize=11, fontname="Helvetica", fontstyle="normal"):
    p.rect(x, y, width, height)
    if fontstyle == "bold":
        fontname = f"{fontname}-Bold"
    p.setFont(fontname, fontsize)
    text_width = p.stringWidth(text, fontname, fontsize)
    text_x = x + (width - text_width) / 2
    text_y = y + height / 2 - fontsize / 2
    p.drawString(text_x, text_y, text)


def gerar_pdf(funcionario):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)


    # Configurar o título do arquivo PDF
    p.setTitle(f"{funcionario.comp} - {funcionario.matricula} - {funcionario.nome}.pdf")


    logo_path, logo_width, logo_height = get_image('static/images/go2b3.jpg', 138)
    p.drawImage(logo_path, 210, 780, width=logo_width, height=logo_height)
    # Desenhe as informações do funcionário no PDF
    draw_centered_text(p, 750, f"KIT PARA COMPROVAÇÃO FATURAMENTO – FATO GERADOR", fontsize=10, fontstyle="bold")
    draw_centered_text(p, 725, f"EXTRATO INDIVIDUAL POR COLABORADOR", fontsize=10, fontstyle="bold")
    draw_centered_text(p, 700, f"GOIÁS BUSINESS CONSULTORIA SERVIÇOS LTDA", fontsize=10, fontstyle="bold")
    draw_centered_text(p, 675, f"19 - ECT - LOG SPM - TECA GUARULHOS - TECA GUARULHOS", fontsize=10, fontstyle="bold")
    draw_centered_text(p, 650, f"CTO: 21-2021", fontsize=10, fontstyle="bold")
    draw_centered_text(p, 625, f"COMPETÊNCIA: {funcionario.comp}", fontsize=10, fontstyle="bold")


    draw_centered_text(p, 550, f"Matrícula: {funcionario.matricula}")
    draw_centered_text(p, 525, f"Nome: {funcionario.nome}")
    draw_centered_text(p, 500, f"Cargo: {funcionario.cargo}")
    draw_centered_text(p, 475, f"Admissão: 20.11.2021")
    draw_centered_text(p, 450, f"Demissão: __.__.____")
    draw_centered_text(p, 425, f"CPF: 505.695.238-93")
    draw_centered_text(p, 400, f"Local: TECA GUARULHOS")
    draw_centered_text(p, 375, f"Turno: SPM TECA GUARULHOS- TURNO 03")

    # Finalizar a primeira página e iniciar a segunda página
    p.showPage()



    # Desenhar as informações na segunda página
    draw_centered_text(p, 805, f"Recibo de Pagamento", fontsize=16, fontstyle="bold")
    p.setFont("Helvetica", 6) # Altere o segundo argumento para o tamanho desejado
    p.drawString(465, 787, f"Sofware Responsável http://www.gi.com.br") 
    
    # Defina a largura da tabela
    table_width = 550
    # Desenhar um retângulo com informações do funcionário acima da tabela
    rect_x = (letter[0] - table_width) / 2
    # Aqui mexe na altura de onde fica na pagina.
    rect_y = -44
    # Altura do retangulo
    rect_height = 80
    p.roundRect(rect_x, rect_y + 750, table_width, rect_height, 1, stroke=1, fill=0)
    p.setFont("Helvetica", 8)

    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 10, rect_y + 750 + 65, f"Empresa: GOIAS BUSINESS CONSULTORIA E SERVIÇOS LTDA")


    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 10, rect_y + 750 + 50, f"Cliente: EMPRESA BRASILEIRA DE CORREIOS E TELEGRAFOS ")




    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 400, rect_y + 750 + 65, f"Inscrição:   18.507.752/0001-55")

    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 400, rect_y + 750 + 50, f"Inscrição:   34.028.316/0015-09")




    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 10, rect_y + 750 + 35, f"Código:")

    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 10, rect_y + 750 + 20, f"{funcionario.matricula}")


    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 80, rect_y + 750 + 35, f"Nome do Funcionário:")

    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 80, rect_y + 750 + 20, f"{funcionario.nome}")


    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 220, rect_y + 750 + 35, f"Função:")

    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 220, rect_y + 750 + 20, f"{funcionario.cargo}")


    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 320, rect_y + 750 + 35, f"Admissão:")

    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 320, rect_y + 750 + 20, f"20.11.2021")


    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 400, rect_y + 750 + 35, f"Demissão:")

    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 400, rect_y + 750 + 20, f" __.__.____ ")


    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 480, rect_y + 750 + 35, f"Competência:")

    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 480, rect_y + 750 + 20, f"{funcionario.comp}")



















    data = [
        ['Cód. Descrição', 'Referência', 'Vencimentos', 'Descontos'],
        ['HORAS NORMAIS', '145.67', '821.58', ' '],
        ['D.S.R. S/HORAS NORMAL', ' ', '60.72', ' '],
        ['HORA EXTRA 100%', '0.00', '0.00 ', ' '],
        ['HORA EXTRA 100% - MG (NOT)', '0.00', '0.00 ', ' '],
        ['D.S.R. S/HORA EXTRA 100%', '0.00', '0.00 ', ' '],
        ['HORA EXTRA 50%', '0.00', '0.00 ', ' '],
        ['D.S.R. S/HORA EXTRA 50%', '0.00', '0.00 ', ' '],
        ['ADIC. PERICULOSIDADE', '0.00', '0.00 ', ' '],
        ['ADICIONAL NOTURNO', '0.00', '0.00 ', ' '],
        ['D.S.R. S/ADICIONAL', '0.00', '0.00 ', ' '],
        ['ADICIONAL DE FUNÇÃO 25%', '0.00', '0.00 ', ' '],
        ['ADICIONAL DE ATIVIDADE 30% (CARTEIRO)', '0.00', '0.00 ', ' '],
        ['SALARIO FAMILIA', '0.00', '0.00 ', ' '],
        ['SAL. MAT. / LICENÇA GESTANTE (LEI 14.151)', '0.00', '0.00 ', ' '],
        ['ATESTADO HORISTAS', '0.00', '0.00 ', ' '],
        ['AUX. DOENÇA (15 DIAS)', '0.00', '0.00 ', ' '],
        ['ACIDENTE DE TRABALHO (F.G.T.S.)', '0.00', '0.00 ', ' '],
        ['AVISO PREVIO INDEN + MÉDIAS E LEI 12506', '0.00', '0.00 ', ' '],
        ['INDENIZACAO ARTº 479', '0.00', '0.00 ', ' '],
        ['INDENIZAÇÃO ADICIONAL', '0.00', '0.00 ', ' '],
        ['FERIAS', '0.00', '0.00 ', ' '],
        ['1/3 FERIAS', '0.00', '0.00 ', ' '],
        ['13º SALARIO INDENIZADO E ADICIONAIS', '0.00', '0.00 ', ' '],
        ['ARREDONDAMENTO', '0.00', '0.00 ', ' '],
        ['REEMBOLSO EXAME MEDICO/EPI/UNIF', '0.00', '0.00 ', ' '],
        ['DIF. VR / VA', '0.00', '0.00 ', ' '],
        ['DIF. VALE-TRANSPORTE', '0.00', '0.00 ', ' '],
        ['DESC. FALTAS (DIAS+ATRASOS) E HORAS IND.', '0.00', '0.00 ', ' '],
        ['DESC. D.S.R. S/FALTAS (DIAS)', '0.00', '0.00 ', ' '],
        ['DESC. SALDO NEGATIVO', '0.00', '0.00 ', ' '],
        ['DESC. ARREDONDAMENTO', '0.00', '0.00 ', ' '],
        ['AVISO PREVIO INDENIZADO', '0.00', '0.00 ', ' '],
        ['INDENIZACAO ARTº 480', '0.00', '0.00 ', ' '],
        ['DESC. I.N.S.S. S/13º SALARIO', '0.00', '0.00 ', ' '],
        ['DESC. I.N.S.S./DESC. I.R.R.F..', '0.00', '0.00 ', ' '],
        ['DESC. I.N.S.S. (Ferias)', '0.00', '0.00 ', ' '],
        ['DESC. ACIDENTE DE TRABALHO (F.G.T.S.)', '0.00', '0.00 ', ' '],
        ['DESC. AUXILIO DOENCA', '0.00', '0.00 ', ' '],
        ['SEGURO VIDA', '0.00', '0.00 ', ' '],
        ['DESC. ASSIST. ODONTOLOGICA', '0.00', '0.00 ', ' '],
        ['DESC. VALE REFEICAO NAO UTILIZADO', '0.00', '0.00 ', ' '],
        ['DESC. VR / VA', '0.00', '0.00 ', ' '],
        ['DESC UNIFORME / EPI', '0.00', '0.00 ', ' '],
        ['DESC. VALE-TRANSPORTE NAO UTILIZADO', '0.00', '0.00 ', ' '],
        ['DESC. VALE-TRANSPORTE', '0.00', '0.00 ', ' '],



    ]



    table = Table(data)

    # Definir a largura das colunas
    table._argW[0], table._argW[1], table._argW[2], table._argW[3] = 265, 95, 95, 95

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 6),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),  #Espaçemnto da primeira linha.
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LINEABOVE', (0, 1), (-1, 1), 1, colors.black),  # Adicionado
    ]))


    table.wrapOn(p, letter[0], letter[1])
    table_x = (letter[0] - table_width) / 2
    table_y = rect_y - rect_height + 145  # Subtrair 2 para diminuir ainda mais o espaço entre a tabela e o retângulo

    table.drawOn(p, table_x, table_y)  #



    # Finalizar a segunda página
    p.showPage()



    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'{funcionario.comp} - {funcionario.matricula} - {funcionario.nome}.pdf')

