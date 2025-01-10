import re # library regular expression
import nltk # Menggunakan nltk untuk tokenisasi teks
from collections import Counter # Menggunakan Counter untuk menghitung frekuensi kata

class TextProcessor:
    def __init__(self):
        self.kamus = self.load_kamus() # inisialisasi kata dasar dari kamus.txt
        self.stopwords = self.get_stopwords() # inisialisasi stopword list

    # Memuat kamus kata dasar dari file files/kamuss.txt
    def load_kamus(self):
        try:
            with open('files/kamuss.txt', 'r', encoding='utf-8') as file:
                return {line.strip() for line in file if line.strip()}
        except Exception as e:
            print(f"Error membaca kamus: {e}")
            return set()

    # Memuat daftar stopword dari file dan mengembalikan dalam bentuk set
    def get_stopwords(self):
        try:
            with open('files/stopwordbahasa.xls', 'r', encoding='utf-8') as file:
                stopwords = {line.strip() for line in file if line.strip()}
            return stopwords
        except Exception as e:
            print(f"Error membaca file stopwords: {e}")
            return set()

    # function untuk cleaning teks
    def clean_text(self, text):
        content = text.lower() # ubah setiap karakter menjadi lowercase
        content = ' '.join(content.split())  # Menghapus spasi berlebih
        content = re.sub(r'http\S+|www\S+|\.|\,', '', content) # Menghapus URL, HTTP, koma, dan titik
        content = re.sub(r'[^a-zA-Z\s]', '', content) # mengeliminasi karakter non-huruf
        return content
    
    # function untuk proses tokenisasi
    def tokenizing(self,text):
        try:
            tokens = nltk.word_tokenize(text)
            return tokens
        except Exception as e:
            print(f"Error dalam tokenisasi: {e}")
            return []
    
    # function stopword removal
    def stopword_removal(self, tokens):
        """Remove stopwords from token list"""
        if not isinstance(tokens, list):
            print('oops')
            return []
        return [token for token in tokens if token not in self.stopwords]

    # Mengecek apakah kata ada dalam kamus kata dasar
    def cek_kata_dasar(self, kata):
        if self.kamus is None:
            self.kamus = self.load_kamus()
        return kata in self.kamus

    def hapus_inflection_suffixes(self, kata):
        # Menghapus inflectional suffixes (-lah, -kah, -ku, -mu, atau -nya)
        if kata.endswith(('lah', 'kah')):
            return kata[:-3]
        if kata.endswith(('ku', 'mu')):
            return kata[:-2] 
        if kata.endswith('nya'):
            return kata[:-3] 
        if kata.endswith('tah'):
            return kata[:-3]
        if kata.endswith('pun'):
            return kata[:-3]
        return kata

    def hapus_derivation_suffixes(self, kata):
        # Menghapus derivational suffixes (-i, -an, atau -kan)
        if kata.endswith('i'):
            return kata[:-1]
        if kata.endswith('an'):
            return kata[:-2]
        if kata.endswith('kan'):
            return kata[:-3]
        return kata

    def hapus_derivation_prefix(self, kata):
        # Menghapus derivational prefixes (di-, ke-, se-, me-, be-, pe-, te-)
        if len(kata) <= 4:
            return kata
            
        # Cek awalan di- dan ke-
        if kata.startswith(('di', 'ke')) and len(kata) > 4:
            kata_tanpa_awalan = kata[2:]
            if self.cek_kata_dasar(kata_tanpa_awalan):
                return kata_tanpa_awalan
                
        # Cek awalan se-    
        if kata.startswith('se'):
            kata_tanpa_awalan = kata[2:]
            if self.cek_kata_dasar(kata_tanpa_awalan):
                return kata_tanpa_awalan
                
        # Cek awalan me-
        if kata.startswith('me'):
            kata_tanpa_awalan = kata[2:]
            if kata.startswith('meng'):
                kata_tanpa_awalan = kata[4:]
            elif kata.startswith('meny'):
                kata_tanpa_awalan = 's' + kata[4:]
            elif kata.startswith('men'):
                kata_tanpa_awalan = kata[3:]
            elif kata.startswith('mem'):
                kata_tanpa_awalan = 'p' + kata[3:]
            if self.cek_kata_dasar(kata_tanpa_awalan):
                return kata_tanpa_awalan
                
        # Cek awalan be-
        if kata.startswith('be'):
            kata_tanpa_awalan = kata[2:]
            if kata.startswith('ber'):
                kata_tanpa_awalan = kata[3:]
            if self.cek_kata_dasar(kata_tanpa_awalan):
                return kata_tanpa_awalan
                
        # Cek awalan pe-
        if kata.startswith('pe'):
            kata_tanpa_awalan = kata[2:]
            if kata.startswith('peng'):
                kata_tanpa_awalan = kata[4:]
            elif kata.startswith('peny'):
                kata_tanpa_awalan = 's' + kata[4:]
            elif kata.startswith('pen'):
                kata_tanpa_awalan = kata[3:]
            elif kata.startswith('pem'):
                kata_tanpa_awalan = 'p' + kata[3:]
            if self.cek_kata_dasar(kata_tanpa_awalan):
                return kata_tanpa_awalan
                
        # Cek awalan te-
        if kata.startswith('te'):
            kata_tanpa_awalan = kata[2:]
            if kata.startswith('ter'):
                kata_tanpa_awalan = kata[3:]
            if self.cek_kata_dasar(kata_tanpa_awalan):
                return kata_tanpa_awalan
                
        return kata

    def stem_kata(self, kata):
        # Implementasi algoritma Nazief-Adriani
        if self.cek_kata_dasar(kata):
            return kata
            
        # Hapus inflectional suffixes
        kata_1 = self.hapus_inflection_suffixes(kata)
        if self.cek_kata_dasar(kata_1):
            return kata_1
            
        # Hapus derivational suffix
        kata_2 = self.hapus_derivation_suffixes(kata_1)
        if self.cek_kata_dasar(kata_2):
            return kata_2
            
        # Hapus derivational prefix
        kata_3 = self.hapus_derivation_prefix(kata_2)
        if self.cek_kata_dasar(kata_3):
            return kata_3
            
        return kata

    def stem_text(self, text):
        # Memisahkan teks menjadi kata-kata
        kata_kata = text.split()
        
        # Melakukan stemming untuk setiap kata
        hasil_stemming = []
        for kata in kata_kata:
            kata_dasar = self.stem_kata(kata)
            hasil_stemming.append(kata_dasar)
            
        # Menggabungkan kembali kata-kata yang telah di-stemming
        return ' '.join(hasil_stemming)
    
    def process_text(self, text):
        content = self.clean_text(text) # proses cleaning text
        tokens = self.tokenizing(content) # proses tokenisasi
        print(f"Tokenisasi: {tokens}")
        filtered_tokens = self.stopword_removal(tokens) # proses stopword removal
        print(f'Stopword removal: {filtered_tokens}')
        stemmed_tokens = [self.stem_kata(token) for token in filtered_tokens]  # proses stemming
        print(f'Stemming: {stemmed_tokens}') # menampilkan hasil pre-processing

        return stemmed_tokens