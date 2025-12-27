BAD_WORD_PROMPT = """
TUGAS: KLASIFIKASI KATA TIDAK PANTAS

Tugas Anda adalah memeriksa teks dan menentukan apakah teks tersebut mengandung kata-kata yang tidak pantas (umpatan, hinaan, atau sarkasme merendahkan).

ATURAN KLASIFIKASI:
1. Jawab "yes" jika ditemukan: Umpatan, kata kotor, makian, hinaan fisik/mental, atau sindiran jahat.
2. Jawab "no" jika teks: Sopan, netral, pertanyaan biasa, atau pujian tulus.

CONTOH (IKUTI POLA INI):
- Input: "Selamat pagi semuanya." -> Output: "no"
- Input: "Dasar kau manusia tidak berguna!" -> Output: "yes"
- Input: "What a loser you are." -> Output: "yes"
- Input: "Terima kasih atas bantuannya." -> Output: "no"
- Input: "Bisa diam tidak? Suaramu sampah!" -> Output: "yes"
- Input: "Oh, jadi ini hasil kerja 'hebat' kamu? Jelek banget." -> Output: "yes"
- Input: "I don't care, go to hell." -> Output: "yes"
- Input: "Saya ingin memesan kopi satu gelas." -> Output: "no"
- Input: "Dasar babi, beraninya kamu lewat sini!" -> Output: "yes"
- Input: "Pintar sekali kamu ya, sampai-sampai hal mudah saja salah." -> Output: "yes"

LARANGAN KERAS:
- JANGAN menuliskan teks selain JSON.
- JANGAN memberikan alasan atau komentar.
- JANGAN mengulang teks yang diperiksa.

TEKS YANG HARUS DIPERIKSA:
{text_to_check}

FORMAT OUTPUT WAJIB:
{output_parser_format}
"""
