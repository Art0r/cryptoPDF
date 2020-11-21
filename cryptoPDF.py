from fpdf import FPDF
from PyPDF2 import PdfFileReader, PdfFileWriter
from cryptography.fernet import Fernet

def get_key():
    with open('secrets.key', 'rb') as fs:
        first_line = fs.readline()
        last_line = ""
        for line in fs:
            last_line = line 

    return last_line.decode('utf8')

def generate_key():
    with open('secrets.key', 'ab') as fs:
        fs.write(bytes("\n", 'utf8'))
        fs.write(Fernet.generate_key())
        fs.close()

def encrypt_file(file):
    generate_key()
    key = get_key()
    f = Fernet(key)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size= 10)

    pdf_read = PdfFileReader(file)

    for page in range(pdf_read.getNumPages()):

        pdf_text = pdf_read.getPage(page).extractText()

        encrypted_text = f.encrypt(bytes(pdf_text.encode())).decode('utf-8')

        text = [encrypted_text[i:i+80] for i in range(0, len(encrypted_text), 80)]
        for i in text:
            pdf.cell(200, 10, txt=i,
                ln=1, align='C')

    pdf.output('output.pdf')

def decrypt_file(file):
    key = get_key()
    f = Fernet(key)
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size= 10)

    pdf_read = PdfFileReader(file)

    pdf_text = ""
    for page in range(pdf_read.getNumPages()):

        pdf_text += pdf_read.getPage(page).extractText()

    decrypted_text = f.decrypt(bytes(pdf_text, 'utf-8')).decode('utf8')

    text = [decrypted_text[i:i+100] for i in range(0, len(decrypted_text), 100)]
    for i in text:
        pdf.cell(200, 10, txt=i,
            ln=1, align='C')

    pdf.output('output.pdf')

loop = True
while(loop):
    escolha = int(input('Deseja encriptar ou desencriptar?'))

    if escolha == 1:
        encrypt_file('input.pdf')

    elif escolha == 0:
        decrypt_file('output.pdf')
    
    elif escolha == 2:
        loop = False
