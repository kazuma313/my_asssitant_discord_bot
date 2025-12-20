# from langchain_yt_dlp.youtube_loader import YoutubeLoaderDL
from typing import Dict, List
import requests
import logging
import string
import json
import re



class YouTubeTranscriptPreprocessor:
    def __init__(self):
        # Daftar kata-kata filler dan interjeksi yang umum dalam bahasa Indonesia
        self.filler_words = {
            "gitu",
            "ya",
            "nih",
            "kan",
            "tuh",
            "sih",
            "loh",
            "dong",
            "deh",
            "kok",
            "kayak",
            "gimana",
            "udah",
            "tapi",
            "terus",
            "nah",
            "jadi",
            "wah",
            "oh",
            "ah",
            "eh",
            "um",
            "uh",
            "hmm",
            "emm",
            "err",
        }

        # Singkatan dan kontraksi umum
        self.contractions = {
            "gua": "saya",
            "lu": "kamu",
            "enggak": "tidak",
            "ngga": "tidak",
            "nggak": "tidak",
            "gak": "tidak",
            "tau": "tahu",
            "udah": "sudah",
            "udh": "sudah",
            "yg": "yang",
            "dgn": "dengan",
            "krn": "karena",
            "sm": "sama",
            "gt": "begitu",
            "bgt": "banget",
        }

    def clean_text(self, text: str) -> str:
        """Membersihkan teks dari karakter yang tidak diperlukan"""
        # Hapus karakter non-printable
        text = "".join(char for char in text if char.isprintable())

        # Hapus multiple spaces
        text = re.sub(r"\s+", " ", text)

        # Hapus spasi di awal dan akhir
        text = text.strip()

        return text

    def normalize_punctuation(self, text: str) -> str:
        """Normalisasi tanda baca"""
        # Hapus tanda baca berlebihan
        text = re.sub(r"[.]{2,}", ".", text)
        text = re.sub(r"[,]{2,}", ",", text)
        text = re.sub(r"[!]{2,}", "!", text)
        text = re.sub(r"[?]{2,}", "?", text)

        # Tambahkan spasi setelah tanda baca jika tidak ada
        text = re.sub(r"([.!?])([A-Za-z])", r"\1 \2", text)
        text = re.sub(r"([,])([A-Za-z])", r"\1 \2", text)

        return text

    def remove_repetitive_words(self, text: str) -> str:
        """Hapus pengulangan kata yang berlebihan"""
        words = text.split()
        cleaned_words = []
        prev_word = None
        repeat_count = 0

        for word in words:
            if word.lower() == prev_word:
                repeat_count += 1
                if repeat_count < 2:  # Izinkan maksimal 1 pengulangan
                    cleaned_words.append(word)
            else:
                cleaned_words.append(word)
                repeat_count = 0
            prev_word = word.lower()

        return " ".join(cleaned_words)

    def expand_contractions(self, text: str) -> str:
        """Ekspansi singkatan dan kontraksi"""
        words = text.split()
        expanded_words = []

        for word in words:
            # Bersihkan tanda baca untuk pencocokan
            clean_word = word.lower().strip(string.punctuation)

            if clean_word in self.contractions:
                # Pertahankan kapitalisasi asli
                if word[0].isupper():
                    replacement = self.contractions[clean_word].capitalize()
                else:
                    replacement = self.contractions[clean_word]

                # Pertahankan tanda baca
                punctuation = "".join(c for c in word if c in string.punctuation)
                expanded_words.append(replacement + punctuation)
            else:
                expanded_words.append(word)

        return " ".join(expanded_words)

    def remove_filler_words(self, text: str, aggressive: bool = False) -> str:
        """Hapus kata-kata filler"""
        words = text.split()
        filtered_words = []

        for i, word in enumerate(words):
            clean_word = word.lower().strip(string.punctuation)

            # Mode aggressive menghapus lebih banyak filler words
            if aggressive:
                if clean_word not in self.filler_words:
                    filtered_words.append(word)
            else:
                # Mode normal, pertahankan beberapa filler words untuk konteks
                if clean_word in self.filler_words:
                    # Pertahankan jika di awal kalimat atau setelah tanda baca
                    if i == 0 or any(p in words[i - 1] for p in ".!?"):
                        filtered_words.append(word)
                    # Skip filler word yang berlebihan
                else:
                    filtered_words.append(word)

        return " ".join(filtered_words)

    def segment_into_sentences(self, text: str) -> List[str]:
        """Segmentasi teks menjadi kalimat-kalimat"""
        # Pisah berdasarkan tanda baca kuat
        sentences = re.split(r"[.!?]+", text)

        # Bersihkan dan filter kalimat kosong
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence.split()) >= 3:  # Minimal 3 kata
                cleaned_sentences.append(sentence + ".")

        return cleaned_sentences

    def fix_common_errors(self, text: str) -> str:
        """Perbaiki kesalahan umum dalam transcript"""
        # Perbaiki spasi sebelum tanda baca
        text = re.sub(r"\s+([,.!?])", r"\1", text)

        # Perbaiki kapitalisasi setelah tanda baca
        text = re.sub(
            r"([.!?])\s*([a-z])", lambda m: m.group(1) + " " + m.group(2).upper(), text
        )

        # Kapitalisasi awal kalimat
        if text and text[0].islower():
            text = text[0].upper() + text[1:]

        return text

    def preprocess(
        self,
        text: str,
        remove_fillers: bool = True,
        aggressive_filler_removal: bool = False,
        expand_contractions: bool = True,
        segment_sentences: bool = False,
    ) -> str:
        """
        Preprocess transcript lengkap

        Args:
            text: Teks transcript asli
            remove_fillers: Hapus kata-kata filler
            aggressive_filler_removal: Mode agresif untuk menghapus filler
            expand_contractions: Ekspansi singkatan
            segment_sentences: Kembalikan sebagai list kalimat terpisah
        """

        # Step 1: Bersihkan teks dasar
        processed_text = self.clean_text(text)

        # Step 2: Normalisasi tanda baca
        processed_text = self.normalize_punctuation(processed_text)

        # Step 3: Hapus pengulangan kata berlebihan
        processed_text = self.remove_repetitive_words(processed_text)

        # Step 4: Ekspansi kontraksi (opsional)
        if expand_contractions:
            processed_text = self.expand_contractions(processed_text)

        # Step 5: Hapus filler words (opsional)
        if remove_fillers:
            processed_text = self.remove_filler_words(
                processed_text, aggressive_filler_removal
            )

        # Step 6: Perbaiki kesalahan umum
        processed_text = self.fix_common_errors(processed_text)

        # Step 7: Segmentasi kalimat (opsional)
        if segment_sentences:
            return self.segment_into_sentences(processed_text) # type: ignore

        return processed_text

    def get_statistics(self, original_text: str, processed_text: str) -> dict:
        """Mendapatkan statistik perbandingan teks asli dan hasil preprocessing"""
        orig_words = len(original_text.split())
        proc_words = len(processed_text.split())

        return {
            "original_word_count": orig_words,
            "processed_word_count": proc_words,
            "words_removed": orig_words - proc_words,
            "reduction_percentage": round(
                ((orig_words - proc_words) / orig_words) * 100, 2
            ),
        }
    
def load_youtube_transcript(url: str, max_attempts: int = 5) -> Dict:
    """
    Load transcript from YouTube video URL with retry mechanism.

    Args:
        url (str): YouTube video URL
        max_attempts (int): Maximum number of retry attempts

    Returns:
        list: List of transcript documents if successful, empty list if failed
    """
    url_hook = "https://bpmn.air.id/webhook/puppeteer"
    attempt = 0
    logging.info(f"Loading YouTube transcript from URL: {url}")
    while attempt < max_attempts:
        url_youtube = url
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "url": url_youtube
        }

        response = requests.post(url_hook, headers=headers, json=data)
        logging.info(f"status request youtube transcipt: {response.status_code} for url: {url}")
        attempt += 1
        if len(response.text) > 1:
            return json.loads(response.text)
        else:
            continue
        
    logging.error(f"Failed to load transcript after {max_attempts} attempts")
    return {}
    
# def get_youtube_metadata(url: str) -> dict:
#     """
#     Get metadata from YouTube video URL.

#     Args:
#         url (str): YouTube video URL

#     Returns:
#         dict: Video metadata if successful, empty dict if failed
#     """
#     try:
#         loader = YoutubeLoaderDL.from_youtube_url(url, add_video_info=True)
#         documents = loader.load()
#         return documents[0].metadata if documents else {}
#     except Exception as e:
#         logging.error(f"Error getting YouTube metadata: {url} ({e})")
#         return {}
# if __name__ == "__main__":
#     # Example usage
#     url = "https://youtu.be/tyN89bZ5MpE?si=PWsGDOjcDzrnqDyx"
#     metadata = get_youtube_metadata(url)
    # print(metadata)

# Contoh penggunaan
if __name__ == "__main__":
    # Inisialisasi preprocessor
    preprocessor = YouTubeTranscriptPreprocessor()

    # Contoh transcript
    sample_transcript = """gitu. Nah ketika sudah jamaah Aristoteles itu berkembang, ekonomi terus berkembang nih teman-teman. ekonomi Islam, ekonomi lain sampai pada akhirnya, long story short, tahun 1775 atau 776, seorang cendikiawan bernama Adam Smith bikin buku yang namanya The World of Nation yang mana itu jadi fondasi dasar ilmu ekonomi modern saat ini gitu. yang dia mengatakan bahwa salah satu faktor penting dalam perputaran ekonomi itu ya produksi ya tenaga kerja gitu. Kalau semua individu itu selalu berpikir bagaimana uangnya lebih baik dan kehidupannya lebih baik, maka masyarakat yang harmonis akan terkumpul. Jadi selama kita berpikir kayak gimana, enggak perlu kita mikirin orang lain, enggak perlu kita mikirin negara, mikirin diri kita aja sendiri."""

    # Preprocessing dengan berbagai opsi
    print("=== ORIGINAL TRANSCRIPT ===")
    print(sample_transcript)
    print("\n")

    # Preprocessing standar
    result_standard = preprocessor.preprocess(
        sample_transcript,
        remove_fillers=True,
        aggressive_filler_removal=False,
        expand_contractions=True,
    )

    print("=== STANDARD PREPROCESSING ===")
    print(result_standard)
    print("\n")

    # Preprocessing agresif
    result_aggressive = preprocessor.preprocess(
        sample_transcript,
        remove_fillers=True,
        aggressive_filler_removal=True,
        expand_contractions=True,
    )

    print("=== AGGRESSIVE PREPROCESSING ===")
    print(result_aggressive)
    print("\n")

    # Segmentasi kalimat
    sentences = preprocessor.preprocess(
        sample_transcript,
        remove_fillers=True,
        expand_contractions=True,
        segment_sentences=True,
    )

    print("=== SENTENCE SEGMENTATION ===")
    for i, sentence in enumerate(sentences, 1):
        print(f"{i}. {sentence}")
    print("\n")

    # Statistik
    stats = preprocessor.get_statistics(sample_transcript, result_standard)
    print("=== STATISTICS ===")
    for key, value in stats.items():
        print(f"{key}: {value}")




