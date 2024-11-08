from PyQt5 import uic,QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

cnn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'cadastro'
)
def excluir_dados():

    linha = segunda_tela.tableWidget.currentRow()
    segunda_tela.tableWidget.removeRow(linha)

    cursor = cnn.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id="+ str(valor_id))
def main_app():
    line1 = cadastro.lineEdit.text()
    line2 = cadastro.lineEdit_2.text()
    line3 = cadastro.lineEdit_3.text()
    line4 = cadastro.lineEdit_4.text()
    line5 = ''

    print(f"Nome: {line1}")
    print(f"Quantidade: {line2}")
    print(f"Preço: ${line3}")
    print(f"Local de Armazenamento: {line4}")
    print (f"Categoria: {line5}")

    cursor = cnn.cursor()

    line1 = cadastro.lineEdit.text()
    line2 = cadastro.lineEdit_2.text()
    line3 = cadastro.lineEdit_3.text()
    line4 = cadastro.lineEdit_4.text()
    line5 = ''

    addproduto = ("""INSERT INTO produtos
    (Nome, Quantidade, Preco, Local, Categoria)
    VALUES (%s, %s, %s, %s, %s)""")
    addvalue = (line1, line2, line3, line4, line5)
    cursor.execute(addproduto, addvalue)
    cnn.commit

    cadastro.lineEdit.setText("")
    cadastro.lineEdit_2.setText("")
    cadastro.lineEdit_3.setText("")
    cadastro.lineEdit_4.setText("")
    

    if cadastro.radioButton.isChecked():
        print ("Categoria: Eletrodoméstico ")
    elif cadastro.radioButton_2.isChecked():
        print ("Categoria: Informática")
    else:
        print("Categoria: Smartphone")
def show2tela():
    segunda_tela.show()
    
    cursor = cnn.cursor()
    ComandoSql = "SELECT * FROM produtos"
    cursor.execute (ComandoSql)
    DadosLidos = cursor.fetchall()
    print (DadosLidos)

    segunda_tela.tableWidget.setRowCount(len(DadosLidos))
    segunda_tela.tableWidget.setColumnCount (5)

    for i in range (0, len(DadosLidos)):
        for j in range(0,5):
            segunda_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(DadosLidos[i][j])))   
def salvar():

    cursor = cnn.cursor()
    LerDados = "SELECT * FROM produtos"
    cursor.execute(LerDados)
    LerDados = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("Lista_Produtos.pdf")
    pdf.setFont("Times-Bold", 12)
    pdf.drawString(200,800, "Produtos cadastrados:")
    pdf.setFont("Times-Bold", 12)

    pdf.drawString(10,750, "Id Produto")
    pdf.drawString(75,750, "Nome")
    pdf.drawString(250,750, "Quantidade")
    pdf.drawString(360,750, "Preço")
    pdf.drawString(460,750, "Local")

    for i in range(0, len(LerDados)):
        y = y + 15
        pdf.drawString(10,750 - y, str(LerDados[i][0]))
        pdf.drawString(75,750 - y, str(LerDados[i][1]))
        pdf.drawString(260,750 - y, str(LerDados[i][2]))
        pdf.drawString(360,750 - y, str(LerDados[i][3]))
        pdf.drawString(460,750 - y, str(LerDados[i][4]))

    pdf.save()
    print("Lista Salva")
    

    
    
app=QtWidgets.QApplication([])
cadastro=uic.loadUi("Cadastro_produto.ui")
segunda_tela=uic.loadUi("segunda_tela.ui")
cadastro.pushButton.clicked.connect(main_app)
cadastro.pushButton_2.clicked.connect(show2tela)
segunda_tela.pushButton_2.clicked.connect(salvar)
segunda_tela.pushButton.clicked.connect(excluir_dados)

cadastro.show()
app.exec()