# library untuk gui
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext

import os # baca folder dan file
import math # untuk perhitungan
from collections import Counter # untuk menghitungkan kemunculan kata
from docx import Document # read file docx
from PyPDF2 import PdfReader # read file pdf
import text_processor  # memanggil class TextProcessor

class InformationRetrievalApp:
    def __init__(self, master):
        self.master = master
        
        # inisialisasi variabel untuk memanggil function preprocessing
        self.text_processor = text_processor.TextProcessor()

        self.directory_label = tk.Label(master, text="Select Directory:")
        self.directory_label.pack()

        # kolom nama folder
        self.directory_var = tk.StringVar()
        self.directory_entry = tk.Entry(master, textvariable=self.directory_var, width=50)
        self.directory_entry.pack()

        # tombol pilih folder
        self.browse_button = tk.Button(master, text="Browse", command=self.browse_directory)
        self.browse_button.pack()

        self.query_label = tk.Label(master, text="Enter Query:")
        self.query_label.pack()

        # kolom input query
        self.query_var = tk.StringVar()
        self.query_entry = tk.Entry(master, textvariable=self.query_var, width=50)
        self.query_entry.pack()

        # tombol search
        self.search_button = tk.Button(master, text="Search", command=self.perform_search)
        self.search_button.pack()

        self.files_label = tk.Label(master, text="List Dokumen:")
        self.files_label.pack()

        # kolom list dokumen pada folder yang dipilih
        self.list_file = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=70, height=10)
        self.list_file.pack()

        self.result_label = tk.Label(master, text="Hasil Pencarian  :")
        self.result_label.pack()

        # kolom hasil pencarian, diurutkan berdasarkan skor BM25 dari yang terbesar
        self.result_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=70, height=15)
        self.result_text.pack()

    # function untuk mengurutkan hasil pencarian berdasarkan skor BM25 dari yang terbesar
    def sort_files_by_bm25_scores(self,scores):
        return sorted(scores, key=lambda x: x[1], reverse=True)

    # function untuk mengecek keterkaitan antara teks dokumen dan query
    def filter_document_terms(self, query_terms, document_terms):
        return [term for term in document_terms if term in query_terms]

    # function untuk proses perhitungan skor BM25
    def calculate_bm25(self, query, document, document_length, average_document_length, k1=1.5, b=0.75):
        # Splitting / memecah query dan document menjadi bentuk "terms"
        query_terms = self.text_processor.process_text(text=query)
        document_terms = self.text_processor.process_text(text=document)

        # Menghitung jumlah kemunculan setiap terms
        term_freqs = Counter(document_terms)
        
        for word, count in sorted(term_freqs.items(), key=lambda x: x[1], reverse=True):
            if count > 1:
                print(f"Kata {word} sebanyak {count} kata\n")

        # Proses perhitungan nilai IDF untuk setiap term pada query
        # untuk mengukur seberapa jarang kemunculan suatu term pada dokumen
        idf_values = {}
        for term in query_terms:
            df = sum(1 for doc_terms in document_terms if term in doc_terms)
            idf_values[term] = math.log((len(document_terms) - df + 0.5) / (df + 0.5) + 1.0)

        print(f'Nilai IDF: {idf_values}')

        # Proses perhitungan skor BM25 untuk setiap term
        bm25_scores = []
        for term in query_terms:
            tf = term_freqs[term]
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * (document_length / average_document_length))
            bm25_scores.append(idf_values[term] * numerator / denominator)

        print(f'Skor BM25: {bm25_scores}')

        # Mengembalikan jumlah skor BM25 untuk setiap term,
        # yang mengukur relevansi antara query dan dokumen/file
        return sum(bm25_scores)

    # menghitung skor BM25 untuk masing masing file
    def calculate_bm25_score(self, query, file, average_document_length, k1=1.5, b=0.75):
        document_length = len(self.read_file(file).split()) # panjang dokumen
        print(f'\nNama File: {file}')
        return self.calculate_bm25(query, self.read_file(file), document_length, average_document_length, k1, b)

    # menampung hasil perhitungan skor BM25 untuk setiap file
    def calculate_bm25_scores(self,query, files, average_document_length):
        scores = [(file, self.calculate_bm25_score(query, file, average_document_length)) for file in files]
        return scores

    # Membaca dan mengekstrak teks dari file PDF
    def read_pdf(self,file_path):
        try:
            reader = PdfReader(file_path) 
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error membaca PDF {file_path}: {e}")
            return ""

    # Membaca dan mengekstrak teks dari file DOCX
    def read_docx(self,file_path):
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"Error membaca DOCX {file_path}: {e}")
            return ""

    # Membaca dan mengekstrak teks dari file TXT
    def read_txt(self,file_path):
        # Membaca dan mengekstrak teks dari file TXT
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error membaca TXT {file_path}: {e}")
            return ""

    # membaca dokumen berdasarkan ekstensi/jenis file
    def read_file(self,file_path):
        _, extension = os.path.splitext(file_path) # proses ambil ekstensi file

        # jika jenis file adalah .txt
        if extension == '.txt':
            return self.read_txt(file_path)
        # jika jenis file adalah .docx
        elif extension == '.docx':
            return self.read_docx(file_path)
        # jika jenis file adalah PDF
        elif extension == '.pdf':
            return self.read_pdf(file_path)
        else:
            print('Ekstensi file tidak dikenal')
            return ''

    # function menghitung rata-rata panjang dokumen
    def calculate_average_document_length(self,files):
        total_words = sum(len(self.read_file(file).split()) for file in files)
        return total_words / len(files)

    # function proses temu balik informasi
    def search_files_with_bm25(self, query, files):
        # Hitung rata-rata panjang dokumen/file
        average_document_length = self.calculate_average_document_length(files)
        print(f'Rata-rata panjang dokumen: {average_document_length}')

        # Hitung skor BM25
        scores = self.calculate_bm25_scores(query, files, average_document_length)

        # Urutkan file berdasarkan skor BM25 secara Descending
        sorted_files = self.sort_files_by_bm25_scores(scores)

        return sorted_files

    # function proses pencarian, pembacaan, dan temu balik informasi
    def perform_search(self):
        directory_path = self.directory_var.get() # ambil nama folder
        query = self.query_var.get() # ambil nilai query

        # cek apakah folder valid dan query tidak kosong
        if not directory_path or not query:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Please select a directory and enter a query.")
            return

        # menampung semua file pada folder dalam suatu list
        files = [os.path.join(directory_path, filename) for filename in os.listdir(directory_path) if
                 os.path.isfile(os.path.join(directory_path, filename))]

        self.list_file.insert(tk.END, f"Jumlah dokumen pada folder={len(files)}\n")
        self.list_file.insert(tk.END, "========================================\n")

        for rank, file in enumerate(files, start=1):
            self.list_file.insert(tk.END, f"No.{rank} : {os.path.basename(file)}\n")

        # print(f'Files in directory: {files}')
        print(f'Search query: {self.query_var.get()}')

        # Proses temu balik informasi
        result_files = self.search_files_with_bm25(query, files)

        # membersihkan kolom teks hasil
        self.result_text.delete(1.0, tk.END)

        # Jika terdapat file yang mengandung query, tampilkan
        if result_files:
            self.result_text.insert(tk.END, f"Menampilkan {len(result_files)} hasil\n")
            self.result_text.insert(tk.END, f"=====================================\n")
            for rank, (file, score) in enumerate(result_files, start=1):
                if score > 0:
                    self.result_text.insert(tk.END, f"Rank {rank}: {os.path.basename(file)} (Similarity Score: {score:.4f})\n")
        # jika tidak
        else:
            self.result_text.insert(tk.END, "Tidak ada file yang cocok dengan query.")

    # function untuk pilih directory/folder
    def browse_directory(self):
        print('Browse directory...')
        selected_directory = filedialog.askdirectory()
        print(f'Directory: {selected_directory}')
        self.directory_var.set(selected_directory) # set nama folder ke kolom pertama

# function utama
def main():
    root = tk.Tk()
    app = InformationRetrievalApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
