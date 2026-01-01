BAD_WORD_PROMPT = """
TUGAS: KLASIFIKASI KATA TIDAK PANTAS
Tugas Anda adalah memeriksa teks dan menentukan apakah teks tersebut mengandung kata-kata yang tidak pantas.

ATURAN KLASIFIKASI:
1. Jawab "yes" jika ditemukan: Umpatan, kata kotor, makian, hinaan fisik/mental, atau sindiran jahat.
2. Jawab "no" jika teks: Sopan, netral, pertanyaan biasa, atau pujian tulus.

CONTOH KLASIFKASI "yes":
- Input: "Dasar babi!" -> Output: "yes"
- Input: "goblok" -> Output: "yes"
- Input: "fuck" -> Output: "yes"
- Input: "fuxk you" -> Output: "yes"
- Input: "anjing" -> Output: "yes"
- Input: "babi" -> Output: "yes"
- Input: "kntl" -> Output: "yes"
- Input: "mmk lah" -> Output: "yes"
- Input: "Assuu" -> Output: "yes

LARANGAN KERAS:
- JANGAN menuliskan teks selain JSON.
- JANGAN memberikan alasan atau komentar.
- JANGAN mengulang teks yang diperiksa.
"""
