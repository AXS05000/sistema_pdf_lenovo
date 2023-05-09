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
    draw_centered_text(p, 750, f"EXTRATO SIMPLES - POR COLABORADOR – FATO GERADOR", fontsize=10, fontstyle="bold")
    draw_centered_text(p, 725, f"CTO: 21-2021", fontsize=10, fontstyle="bold")
    draw_centered_text(p, 700, f"COMPETÊNCIA: {funcionario.comp}", fontsize=10, fontstyle="bold")
    draw_centered_text(p, 650, f"Matrícula: {funcionario.matricula}")
    draw_centered_text(p, 625, f"Nome: {funcionario.nome}")
    draw_centered_text(p, 600, f"Cargo: {funcionario.cargo}")
    draw_centered_text(p, 575, f"Admissão: 20.11.2021")
    draw_centered_text(p, 550, f"Demissão: __.__.____")
    draw_centered_text(p, 525, f"CPF: 505.695.238-93")
    draw_centered_text(p, 500, f"Local: TECA GUARULHOS")
    draw_centered_text(p, 475, f"Turno: SPM TECA GUARULHOS- TURNO 03")

    draw_centered_text(p, 425, f"IDENTIFICAÇÃO COMPROVANTE/EVIDÊNCIAS:", fontsize=10, fontstyle="bold")
    draw_centered_text(p, 400, f"• AUSÊNCIAS LEGAIS/FÉRIAS/DECIMO TERC./VERBAS RESCISÓRIAS/SAL.MATERN: VIDE AUTENTICAÇÕES E RECIBO.", fontsize=10, fontstyle="bold")
    draw_centered_text(p, 375, f"• FGTS RESCISÓRIO E FGTS SOBRE ACIDENTE TRABALHO: VIDE SEFIP E GRRF.", fontsize=10, fontstyle="bold")





    table_widthxx = 550

    rect_xx = (letter[0] - table_widthxx) / 2

    p.setFont("Helvetica", 10)
    p.drawString(rect_xx, 273, f"_________________________________________________________________________________________________")
    p.drawString(rect_xx, 181, f"_________________________________________________________________________________________________")
    
    

    p.drawString(rect_xx + 275, 150, f"-------")
    p.drawString(rect_xx + 325, 150, f"-------")
    p.drawString(rect_xx + 400, 150, f"-------")

    draw_centered_text(p, 325, f"COMPROVANTE PAGAMENTO - COMPETÊNCIA: {funcionario.comp}", fontsize=12, fontstyle="bold")
    draw_centered_text(p, 300, f"FOLHA/RCT", fontsize=12, fontstyle="bold")

    p.setFont("Helvetica-Bold", 10)
    p.drawString(rect_xx + 10, 275, f"Dados Consultados")
    p.drawString(rect_xx + 10, 166, f"Autenticação")
    p.drawString(rect_xx + 200, 166, f"Data")
    p.drawString(rect_xx + 275, 166, f"Banco")
    p.drawString(rect_xx + 325, 166, f"Agência")
    p.drawString(rect_xx + 400, 166, f"Conta")
    p.drawString(rect_xx + 475, 166, f"Valor R$")


    p.setFont("Helvetica", 8)
    p.drawString(rect_xx + 10, 250, f"Agência:")
    p.drawString(rect_xx + 10, 235, f"Conta:")
    p.drawString(rect_xx + 10, 220, f"Descrição Lote:")
    p.drawString(rect_xx + 10, 205, f"Situação Lote:")
    p.drawString(rect_xx + 10, 190, f"Favorecidos:")
    p.drawString(rect_xx + 10 + 80, 250, f"1195-9 (BANCO DO BRASIL) OU 3380-4 (BRADESCO)")
    p.drawString(rect_xx + 10 + 80, 235, f"106742-7 (BANCO DO BRASIL) OU 15801-1 (BRADESCO)")
    p.drawString(rect_xx + 10 + 80, 220, f"PAG DIVERS DOC – CREDITO CONTA SALÁRIO")
    p.drawString(rect_xx + 10 + 80, 205, f"PROCESSADO - EFETUADO")
    p.drawString(rect_xx + 10 + 80, 190, f"{funcionario.matricula} - {funcionario.nome}")
    p.drawString(rect_xx + 10, 150, f"G331081341857981023 08.02.2022 13.50.39_")
    p.drawString(rect_xx + 200, 150, f"07.02.2022")
    p.drawString(rect_xx + 475, 150, f"R$ 858.00")












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
    rect_y = -24
    # Altura do retangulo
    rect_height = 60
    p.roundRect(rect_x, rect_y + 750, table_width, rect_height, 1, stroke=1, fill=0)
    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 10, rect_y + 750 + 48, f"Código:")
    p.drawString(rect_x + 10, rect_y + 750 + 35, f"{funcionario.matricula}")
    p.drawString(rect_x + 50, rect_y + 750 + 48, f"Nome do Funcionário:")
    p.drawString(rect_x + 50, rect_y + 750 + 35, f"{funcionario.nome}")
    p.drawString(rect_x + 210, rect_y + 750 + 48, f"Função:")
    p.drawString(rect_x + 210, rect_y + 750 + 35, f"{funcionario.cargo}")
    p.drawString(rect_x + 345, rect_y + 750 + 48, f"Admissão:")
    p.drawString(rect_x + 345, rect_y + 750 + 35, f"20.11.2021")
    p.drawString(rect_x + 400, rect_y + 750 + 48, f"Demissão:")
    p.drawString(rect_x + 400, rect_y + 750 + 35, f" __.__.____ ")
    p.drawString(rect_x + 480, rect_y + 750 + 48, f"Competência:")
    p.drawString(rect_x + 480, rect_y + 750 + 35, f"{funcionario.comp}")


    data = [
        ['Cód. Descrição', 'Referência', 'Vencimentos', 'Descontos'],
        ['HORAS NORMAIS', '145.67', '821.58', ' '],
        ['D.S.R. S/HORAS NORMAL', ' ', '60.72', ' '],
        ['HORA EXTRA 100% / HORA EXTRA 100% NOT', '0.00', '0.00 ', ' '],
        ['D.S.R. S/HORA EXTRA 100%', '0.00', '0.00 ', ' '],
        ['HORA EXTRA 50% / HORA EXTRA 50% NOT', '0.00', '0.00 ', ' '],
        ['D.S.R. S/HORA EXTRA 50%', '0.00', '0.00 ', ' '],
        ['ADIC. PERICULOSIDADE', '0.00', '0.00 ', ' '],
        ['ADICIONAL NOTURNO', '0.00', '0.00 ', ' '],
        ['D.S.R. S/ADICIONAL', '0.00', '0.00 ', ' '],
        ['ADICIONAL DE FUNÇÃO 25%', '0.00', '0.00 ', ' '],
        ['SALARIO FAMILIA', '0.00', '0.00 ', ' '],
        ['FALTA ABONADA-PONTO ELETR.', '0.00', '0.00 ', ' '],
        ['LICENÇA GESTANTE (LEI 14.151)', '0.00', '0.00 ', ' '],
        ['ATESTADO HORISTAS', '0.00', '0.00 ', ' '],
        ['SAL. MATERNIDADE', '0.00', '0.00 ', ' '],
        ['AUX. DOENÇA / ACID. TRABALHO (15 DIAS)', '0.00', '0.00 ', ' '],
        ['VERBAS RESCISÓRIAS (Art 7º CF)', '0.00', '0.00 ', ' '],
        ['FERIAS', '0.00', '0.00 ', ' '],
        ['1/3 FERIAS', '0.00', '0.00 ', ' '],
        ['13º SALARIO INDENIZADO E ADICIONAIS', '0.00', '0.00 ', ' '],
        ['ARREDONDAMENTO', '0.00', '0.00 ', ' '],
        ['REEMBOLSO EXAME MEDICO/EPI/UNIF', '0.00', '0.00 ', ' '],
        ['DIF. VR / VA  - DIF. VALE TRANSPORTE', '0.00', '0.00 ', ' '],
        ['SALDO NEGATIVO', '0.00', '0.00 ', ' '],
        ['DESC. FALTAS (DIAS+ATRASOS) E HORAS IND.', '0.00', '0.00 ', ' '],
        ['DESC. D.S.R. S/FALTAS (DIAS)', '0.00', '0.00 ', ' '],
        ['FALTAS ABONADAS', '0.00', '0.00 ', ' '],
        ['DESC. ARREDONDAMENTO', '0.00', '0.00 ', ' '],
        ['DESC. AVISO', '0.00', '0.00 ', ' '],
        ['DESC. I.N.S.S./DESC. I.R.R.F', '0.00', '0.00 ', ' '],
        ['DESC. I.N.S.S. S/13º SALARIO – INSS (Férias)', '0.00', '0.00 ', ' '],
        ['SEGURO VIDA', '0.00', '0.00 ', ' '],
        ['DESC. ASSIST. ODONTOLOGICA', '0.00', '0.00 ', ' '],
        ['DESC. VALE REFEICAO NAO UTILIZADO', '0.00', '0.00 ', ' '],
        ['DESC. VR / VA', '0.00', '0.00 ', ' '],
        ['DESC UNIFORME / EPI', '0.00', '0.00 ', ' '],
        ['DESC. VALE-TRANSPORTE NAO UTILIZADO', '0.00', '0.00 ', ' '],
        ['DESC. VALE-TRANSPORTE', '0.00', '0.00 ', ' '],
        ['DESC. SALDO NEGATIVO', '0.00', '0.00 ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],



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
    table_y = rect_y - rect_height + 120  # Subtrair 2 para diminuir ainda mais o espaço entre a tabela e o retângulo

    table.drawOn(p, table_x, table_y)  #


########################################################################################################
#  QUADRO FINAL DO CONTRA CHEQUE.
########################################################################################################

#################################
# QUADRADO GRANDE
#################################

    # Defina a largura da tabela
    table_width = 550
    # Desenhar um retângulo com informações do funcionário acima da tabela
    rect_x = (letter[0] - table_width) / 2
    # Aqui mexe na altura de onde fica na pagina.
    rect_y = -714
    # Altura do retangulo
    rect_height = 90
    p.roundRect(rect_x, rect_y + 750, table_width, rect_height, 1, stroke=1, fill=0)

#################################
# QUADRADO DE BAIXO PARA ASSINATURA
#################################

    table_width2 = 550
    # Desenhar um retângulo com informações do funcionário acima da tabela
    rect_x2 = (letter[0] - table_width) / 2
    # Aqui mexe na altura de onde fica na pagina.
    rect_y2 = -714
    # Altura do retangulo
    rect_height2 = 40
    p.roundRect(rect_x2, rect_y2 + 750, table_width2, rect_height2, 1, stroke=1, fill=0)

#################################
# QUADRADO GRANDE PARA A DIREITA
#################################

    table_width3 = 275
    # Mexe onde ele fica visando lado
    rect_x3 = 306
    # Aqui mexe na altura de onde fica na pagina.
    rect_y3 = -714
    # Altura do retangulo
    rect_height3 = 90
    p.roundRect(rect_x3, rect_y3 + 750, table_width3, rect_height3, 0, stroke=1, fill=0)

#################################
# LINHA NA DIREITA GRANDE PARA A DIREITA
#################################


#################################
# LINHA NA DIREITA GRANDE PARA A DIREITA
#################################

    table_width3 = 137.5
    # Mexe onde ele fica visando lado
    rect_x3 = 306
    # Aqui mexe na altura de onde fica na pagina.
    rect_y3 = -674
    # Altura do retangulo
    rect_height3 = 50
    p.roundRect(rect_x3, rect_y3 + 750, table_width3, rect_height3, 0, stroke=1, fill=0)

########################################################################################################
    p.drawString(rect_x + 300 + 10, rect_y + 750 + 70, f"Total Vencimentos:")
    p.drawString(rect_x + 300 + 20, rect_y + 750 + 55, f"R$ 1.111.18")
    p.drawString(rect_x + 445 + 10, rect_y + 750 + 70, f"Total Descontos:")
    p.drawString(rect_x + 445 + 20, rect_y + 750 + 55, f"R$ 253.18")
    p.drawString(rect_x + 350, rect_y + 750 + 20, f"Valor Líquido ==== R$ 858.00")
    p.drawString(rect_x + 25, rect_y + 750 + 22, f"__________________________________")
    p.drawString(rect_x + 25, rect_y + 750 + 10, f"Declaro ter recebido a importância líquida discriminada neste recibo")

    p.setFont("Helvetica", 10)
    p.drawString(rect_x + 25, rect_y + 750 + 25, f"{funcionario.nome}")

    # Finalizar a segunda página e começa a 3°.
    p.showPage()











    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'{funcionario.comp} - {funcionario.matricula} - {funcionario.nome}.pdf')

