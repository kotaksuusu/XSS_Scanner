# XSS_Scanner
REFLECTED XSS SCANNER BY KOTAKSUUSU
**XSS (Cross-Site Scripting)** adalah jenis celah keamanan pada aplikasi web yang memungkinkan penyerang menyisipkan **kode JavaScript berbahaya** ke dalam halaman web yang dilihat oleh pengguna lain. Tujuan utamanya biasanya untuk mencuri data pengguna (seperti cookie, token sesi), melakukan aksi atas nama pengguna, atau merusak tampilan halaman.

---

### Jenis-Jenis XSS:

1. **Reflected XSS**
2. **Stored XSS**
3. **DOM-based XSS**

---

### Reflected XSS (Non-persistent XSS)

Reflected XSS terjadi ketika **input dari pengguna langsung dikembalikan oleh server ke browser tanpa validasi atau encoding**, biasanya melalui URL. Kode berbahaya hanya “terpantul” kembali pada permintaan tersebut saja dan **tidak disimpan di server**.

#### Contoh Sederhana:

Misalnya, ada URL seperti ini:

```
https://example.com/search?q=halo
```

Jika server menampilkan hasilnya langsung seperti:

```html
Hasil pencarian: halo
```

Dan penyerang mengubah URL jadi:

```
https://example.com/search?q=<script>alert('XSS')</script>
```

Jika tidak difilter, browser akan mengeksekusi JavaScript itu, dan muncul alert. Inilah yang disebut **Reflected XSS**.

---

### Ciri-ciri Reflected XSS:

* Kode jahat dikirim melalui parameter URL atau form.
* Tidak disimpan permanen.
* Eksekusi terjadi saat pengguna membuka link khusus dari penyerang.
* Umumnya digunakan dalam **phishing** atau **serangan satu kali**.

---

Mohon digunakan dengan bijak
