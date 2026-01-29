
TOOL_REGISTRY = {
    # --- Information Gathering ---
    "nmap": {
        "category": "Information Gathering",
        "description": "Netzwerk- und Portscanner",
        "command": "nmap -sV {target}"
    },
    "masscan": {
        "category": "Information Gathering",
        "description": "Extrem schneller Portscanner",
        "command": "masscan {target} -p0-65535 --rate=1000"
    },
    "netdiscover": {
        "category": "Information Gathering",
        "description": "ARP-basierte Netzwerkerkennung",
        "command": "netdiscover -r {target}"
    },
    "arp-scan": {
        "category": "Information Gathering",
        "description": "ARP-Scanner für lokale Netze",
        "command": "arp-scan {target}"
    },
    "whois": {
        "category": "Information Gathering",
        "description": "Domain- und IP-Registrierungsabfragen",
        "command": "whois {target}"
    },
    "theharvester": {
        "category": "Information Gathering",
        "description": "OSINT-Sammlung (E-Mails, Hosts)",
        "command": "theHarvester -d {target} -b all"
    },
    "dnsenum": {
        "category": "Information Gathering",
        "description": "DNS-Aufzählung",
        "command": "dnsenum {target}"
    },
    "dnsrecon": {
        "category": "Information Gathering",
        "description": "DNS-Reconnaissance",
        "command": "dnsrecon -d {target}"
    },
    "amass": {
        "category": "Information Gathering",
        "description": "OSINT & Asset Discovery",
        "command": "amass enum -d {target}"
    },
    "maltego": {
        "category": "Information Gathering",
        "description": "Graphbasierte OSINT-Analyse",
        "command": "maltego"
    },

    # --- Vulnerability Analysis ---
    "nikto": {
        "category": "Vulnerability Scanning",
        "description": "Webserver-Schwachstellen-Scanner",
        "command": "nikto -host {target}"
    },
    "openvas": {
        "category": "Vulnerability Scanning",
        "description": "Umfassender Schwachstellen-Scanner",
        "command": "gvm-cli socket --gmp-username admin --gmp-password pass --xml '<get_tasks/>'"
    },
    "nessus": {
        "category": "Vulnerability Scanning",
        "description": "Vulnerability Management Scanner",
        "command": "nessuscli ls"  # Placeholder
    },
    "wpscan": {
        "category": "Vulnerability Scanning",
        "description": "WordPress-Sicherheitsanalyse",
        "command": "wpscan --url http://{target}"
    },
    "sqlmap": {
        "category": "Vulnerability Scanning",
        "description": "Automatisierte SQLi-Erkennung",
        "command": "sqlmap -u http://{target} --batch"
    },

    # --- Web Application Analysis ---
    "burpsuite": {
        "category": "Web Application Testing",
        "description": "Intercepting Proxy & Scanner",
        "command": "burpsuite"  # GUI tool
    },
    "owasp-zap": {
        "category": "Web Application Testing",
        "description": "Webscanner & Proxy",
        "command": "zap.sh"
    },
    "gobuster": {
        "category": "Web Application Testing",
        "description": "Directory/DNS Brute-Force",
        "command": "gobuster dir -u http://{target} -w /usr/share/wordlists/dirb/common.txt"
    },
    "dirsearch": {
        "category": "Web Application Testing",
        "description": "Webpfad-Bruteforce",
        "command": "dirsearch -u http://{target}"
    },
    "ffuf": {
        "category": "Web Application Testing",
        "description": "Fuzzer für Web-Parameter",
        "command": "ffuf -u http://{target}/FUZZ -w /usr/share/wordlists/dirb/common.txt"
    },
    "wfuzz": {
        "category": "Web Application Testing",
        "description": "Web-Fuzzing-Tool",
        "command": "wfuzz -c -z file,/usr/share/wordlists/dirb/common.txt --hc 404 http://{target}/FUZZ"
    },

    # --- Database Assessment ---
    "mdbtools": {
        "category": "Database Assessment",
        "description": "MS Access DB Tools",
        "command": "mdb-tables {target}"  # Placeholder
    },

    # --- Password Attacks ---
    "hydra": {
        "category": "Password Attacks",
        "description": "Online-Bruteforce-Tool",
        "command": "hydra -l admin -P /usr/share/wordlists/rockyou.txt {target} ssh"
    },
    "medusa": {
        "category": "Password Attacks",
        "description": "Login-Bruteforce",
        "command": "medusa -h {target} -u admin -P /usr/share/wordlists/rockyou.txt -M ssh"
    },
    "ncrack": {
        "category": "Password Attacks",
        "description": "Netzwerk-Auth-Bruteforce",
        "command": "ncrack -p 22 {target}"
    },
    "hashcat": {
        "category": "Password Attacks",
        "description": "GPU-Passwort-Cracker",
        "command": "hashcat -I"  # Info only
    },
    "john": {
        "category": "Password Attacks",
        "description": "Passwort-Cracker",
        "command": "john --list=formats"
    },

    # --- Wireless Attacks ---
    "aircrack-ng": {
        "category": "Wireless",
        "description": "WLAN Security Suite",
        "command": "aircrack-ng"
    },
    "airodump-ng": {
        "category": "Wireless",
        "description": "WLAN Paket-Capture",
        "command": "airodump-ng"
    },
    "aireplay-ng": {
        "category": "Wireless",
        "description": "WLAN Paket-Injektion",
        "command": "aireplay-ng"
    },
    "reaver": {
        "category": "Wireless",
        "description": "WPS-Bruteforce",
        "command": "reaver"
    },
    "bully": {
        "category": "Wireless",
        "description": "WPS-Angriffe",
        "command": "bully"
    },
    "kismet": {
        "category": "Wireless",
        "description": "WLAN-Detektion & IDS",
        "command": "kismet"
    },

    # --- Reverse Engineering ---
    "ghidra": {
        "category": "Reverse Engineering",
        "description": "Software-Analyse",
        "command": "ghidraRun"
    },
    "radare2": {
        "category": "Reverse Engineering",
        "description": "Disassembler/Debugger",
        "command": "r2"
    },
    "apktool": {
        "category": "Reverse Engineering",
        "description": "Android APK Analyse",
        "command": "apktool"
    },
    "jadx": {
        "category": "Reverse Engineering",
        "description": "DEX zu Java Decompiler",
        "command": "jadx"
    },

    # --- Exploitation Frameworks ---
    "metasploit-framework": {
        "category": "Exploitation",
        "description": "Exploit-Framework",
        "command": "msfconsole"
    },
    "msfconsole": {
        "category": "Exploitation",
        "description": "Metasploit CLI",
        "command": "msfconsole"
    },
    "searchsploit": {
        "category": "Exploitation",
        "description": "Exploit-DB Suche",
        "command": "searchsploit {target}"
    },

    # --- Sniffing & Spoofing ---
    "wireshark": {
        "category": "Sniffing",
        "description": "Netzwerkprotokoll-Analyse",
        "command": "wireshark"
    },
    "tcpdump": {
        "category": "Sniffing",
        "description": "CLI Packet Capture",
        "command": "tcpdump"
    },
    "ettercap": {
        "category": "MITM",
        "description": "Man-in-the-Middle Tool",
        "command": "ettercap"
    },
    "dsniff": {
        "category": "MITM",
        "description": "Passwort-Sniffing Suite",
        "command": "dsniff"
    },

    # --- Post Exploitation ---
    "empire": {
        "category": "Post Exploitation",
        "description": "C2 Framework",
        "command": "empire"
    },
    "beef-xss": {
        "category": "Post Exploitation",
        "description": "Browser Exploitation",
        "command": "beef-xss"
    },
    "powersploit": {
        "category": "Post Exploitation",
        "description": "PowerShell Post-Exploitation",
        "command": "powershell -ep bypass -File PowerSploit.ps1"
    }
}
