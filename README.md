# 🔐 SecureMe – Platform to Secure Your Daily Life

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Security](https://img.shields.io/badge/Security-AES%20%7C%20Fernet-red.svg)

**An offline, lightweight security platform designed to safeguard your sensitive information**

[Features](#-core-modules) • [Installation](#️-installation) • [Usage](#-how-it-works) • [Security](#️-security-features) • [Tech Stack](#️-technology-stack)

</div>

---

## 📖 Overview

**SecureMe** is an offline, lightweight security platform designed to safeguard a user's sensitive information. It consolidates three major modules into a single local-system application:

- 🗂️ **Folder Lock**
- 🔑 **Password Vault**
- 📝 **Secure Notes**

<div align="center">

![Home](https://github.com/Amritanshu-404/SecureMe/blob/main/data/notes/Home.png)

![Dashboard](https://github.com/Amritanshu-404/SecureMe/blob/main/data/notes/Dashboard.png)

</div>

The platform is built using **Python (Flask)** and utilizes **AES & Fernet encryption**. No data is uploaded or synced to any cloud service—everything stays on the local machine.

---

## 🎯 Core Modules

### 🔐 1. User Login

SecureMe uses a **Master Passkey** authentication system to control access to all modules.

**Security Features:**
- ✅ Passkey hashed using **PBKDF2-HMAC-SHA256**
- ✅ Stored with salt & iterations
- ✅ Prevents unauthorized access
- ✅ Locked interface until authenticated

---

### 🗂️ 2. Folder Lock

This module allows users to lock/unlock local folders using OS-level ACL manipulation.

**Key Behaviors:**
- 🚫 Deny or remove user read/execute permissions
- 📋 Log every operation in **LockedFolders.xlsx**
- 🖱️ One-click Lock/Unlock from web UI

<div align="center">

![Folder Locker UI](https://github.com/Amritanshu-404/SecureMe/blob/main/data/notes/Folder%20Lock.png)

</div>

---

### 🔑 3. Password Vault

Stores encrypted credentials inside an offline Excel file.

**Features:**
- 🔒 AES/Fernet-encrypted password entries
- ➕ Add, view, filter, and edit credentials
- 🔐 Secure vault key stored locally
- 📊 Metadata stored in **OPass.xlsx**

<div align="center">

![Password Vault Module](https://github.com/Amritanshu-404/SecureMe/blob/main/data/notes/PassVault.png)

</div>

---

### 📝 4. Secure Notes

Allows users to create encrypted .docx notes.

**Highlights:**
- 📄 Notes saved as Word files
- 🔐 Immediately encrypted using a user-generated 6-character key
- ✏️ Editable only after decryption
- 📋 Metadata logged in **ONotes.xlsx**

<div align="center">

![Notes Module](https://github.com/Amritanshu-404/SecureMe/blob/main/data/notes/Notes.png)

</div>

---

## 🛡️ Security Features

SecureMe implements multiple layers of security to protect your data:

```
┌─────────────────────────────────────────┐
│    Master Passkey (PBKDF2-HMAC-SHA256)  │
├─────────────────────────────────────────┤
│      AES/Fernet Encryption Layer        │
├─────────────────────────────────────────┤
│     Local Storage (No Cloud Sync)       │
├─────────────────────────────────────────┤
│    OS-Level ACL for Folder Protection   │
└─────────────────────────────────────────┘
```

**Key Security Measures:**
- 🔐 **PBKDF2-HMAC-SHA256** – Secure password hashing with salt
- 🔒 **AES/Fernet Encryption** – Industry-standard symmetric encryption
- 💾 **Local Storage Only** – No cloud synchronization
- 🗂️ **OS ACL Commands** – System-level folder locking
- 📊 **Excel Metadata Logging** – Comprehensive operation tracking

---

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Clone the Repository**
```bash
git clone https://github.com/Amritanshu-404/SecureMe.git
cd SecureMe
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the Application**
```bash
python app.py
```

4. **Access in Browser**
```
http://127.0.0.1:5000
```

---

## 📌 How It Works

### 🚀 First Launch

On your first run, you'll be prompted to create a **Master Passkey**. This passkey is hashed using PBKDF2-HMAC-SHA256 and acts as your gateway to all modules.

### 🗂️ Using Folder Lock

1. Navigate to the Folder Lock module
2. Enter the full path of the folder you want to protect
3. Click **Lock** to deny permissions or **Unlock** to restore access
4. All operations are logged in **LockedFolders.xlsx**

### 🔑 Managing Your Password Vault

1. Click **Add Password** to create a new entry
2. Enter credentials (title, username, password, category, URL)
3. All passwords are encrypted using AES/Fernet before storage
4. View, filter, or edit entries anytime
5. Metadata is automatically saved to **OPass.xlsx**

### 📝 Creating Secure Notes

1. Open the Secure Notes module
2. Click **New Note** and write your content
3. Generate a 6-character encryption key
4. Note is saved as an encrypted .docx file
5. Use the key to decrypt and edit later
6. Metadata logged in **ONotes.xlsx**

---

## ⚙️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python Flask |
| **Encryption** | Cryptography (Fernet, AES) |
| **Frontend** | HTML5 + CSS3 (Flask Templates) |
| **Storage** | OpenPyXL (Encrypted Excel) |
| **Document Handling** | python-docx |
| **Folder Security** | OS ACL Commands |
| **Logging** | Excel Metadata |

---

## 🔮 Future Enhancements

We're constantly working to improve SecureMe. Here's what's on the roadmap:

- [ ] 👆 **Biometric Authentication** – Fingerprint/face recognition
- [ ] 👥 **Multi-User Support** – Multiple accounts with separate vaults
- [ ] 🎭 **Role-Based Access** – Different permission levels
- [ ] 💾 **Encrypted Backup** – Optional secure backup functionality
- [ ] 📱 **Mobile Companion App** – Cross-platform support
- [ ] 🌙 **Dark Mode** – Eye-friendly interface
- [ ] 🔔 **Security Alerts** – Breach notifications and warnings
- [ ] 🗜️ **File Compression** – Space-efficient storage

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

SecureMe is designed for personal use and educational purposes. While we implement industry-standard security practices, no system is 100% secure. Always maintain backups of critical data and use strong, unique passphrases.

---

## 👥 Contributors

<div align="center">

### Developed by:

[Amritanshu Kumar](https://github.com/Amritanshu-404) & [Ritesh Singh Kushwaha](https://github.com/Ritesh000001)

</div>

---

## 📞 Contact & Support

Found a bug? Have a suggestion? We'd love to hear from you!

- 🐛 [Report Issues](https://github.com/Amritanshu-404/SecureMe/issues)
- 💡 [Request Features](https://github.com/Amritanshu-404/SecureMe/issues/new)
- ⭐ [Star this Repository](https://github.com/Amritanshu-404/SecureMe)

---

<div align="center">

**If you find SecureMe helpful, please consider giving it a ⭐!**

Made with ❤️ by security enthusiasts for security enthusiasts

</div>
