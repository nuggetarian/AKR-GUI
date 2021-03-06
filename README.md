# AKR_Project

# Správce hesel s dvoufaktorovou autentizací

Jednoduchý password manager.
Použité technológie:
- tkinter
- sqlite
- bcrypt
- pycrypto

# Features
- Voľba šifrovacích algoritmov:
  - AES
  - 3DES
  - ChaCha
- Voľba dĺžky kľúčov
- Možnosť viacerých užívateľských účtov
- Dvojfaktorová autentizácia cez e-mail
- Overenie integrity databázového súboru
- Loggovanie

# Screenshots
<img src="images/image1.png" width="463" height="527">
<img src="images/image2.PNG" width="463" height="527">

# Dependencies

bcrypt --> pip install bcrypt

pycrypto --> pip install pycryptodome

Pillow --> pip install Pillow

# Troubleshooting

**Ak nefunguje interpreter vo vscode a nedetekuje knižnice:**

*python -m venv C:\Users\User\Folder\AKR-GUI\venv*

**Ak je problém pri inštalácii Pillow:**

*pip install wheel*
