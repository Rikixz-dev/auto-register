# 🤖 Tretraune Network Auto-Registration Bot

An automated registration bot for Tretraune Network that solves math captchas and creates accounts with 40 free credits each.

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Requests](https://img.shields.io/badge/requests-2.28+-red.svg)](https://requests.readthedocs.io)

## ✨ Features

- 🔢 **Auto Captcha Solving** - Automatically solves math captchas (e.g., "14 - 12 = 2")
- 🍪 **Cookie Management** - Clears cookies between registrations to avoid anti-spam
- 👤 **Random User Generation** - Creates unique usernames, emails, and passwords
- 📦 **Batch Registration** - Register multiple accounts automatically
- 💾 **Account Saving** - Saves all credentials to a text file
- 🎲 **Random Delays** - Variable delays to avoid pattern detection
- 📱 **Mobile User Agents** - Rotates between different mobile device fingerprints
- 💰 **40 Free Credits** - Each account gets 40 free credits upon registration

## 📋 Prerequisites

- Python 3.7 or higher
- `requests` library

## 🚀 Installation

1. **Clone or download this repository**

2. **Install the required dependency:**
```bash
pip install requests
```
3. **Run:**
```bash
python main.py
