# AKR_Project

# Správce hesel s dvoufaktorovou autentizací

Jednoduchý password manager.
Použité technológie:
- tkinter
- sqlite
- bcrypt
- pycrypto

# How to Use
-------------------------------


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

# Dependencies

bcrypt --> pip install bcrypt

pycrypto --> pip install pycryptodome

Pillow --> pip install Pillow

# Troubleshooting

**Ak nefunguje interpreter vo vscode a nedetekuje knižnice:**

*python -m venv C:\Users\User\Folder\AKR-GUI\venv*

**Ak je problém pri inštalácii Pillow:**

*pip install wheel*
