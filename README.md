# TITAN OBFUSCATOR v 0.0.1 Release

TITAN OBFUSCATOR is a professional Java bytecode-level source code protection tool. It focuses on breaking decompiler logic and making manual analysis nearly impossible through extreme visual and logical obfuscation.

## 🌟 Key Obfuscation Techniques

- **IO-Pattern Renaming**: Core engine components are renamed to repetitive `IO` sequences to confuse human auditors and pattern recognition.
- **Dynamic String Encryption**: Strings are never stored in plain text. They are decrypted at runtime using a polymorphic switch-case engine.
- **Reflection Injection**: Standard API calls are wrapped in Lambda consumers and invoked via Reflection to hide the program's intent.
- **Number Mutation**: Every integer is replaced with an XOR-based mathematical expression.
- **Entropy Bloating**: Injects hundreds of lines of junk methods and classes to overwhelm static analysis tools.

## 🛠 Installation

```bash
git clone https://github.com/Sqweex-lua/TitanObfuscator.git
cd titan-obfuscator
```

## 🚀 Usage

Run the obfuscator by providing your Java file:
Bash

python titan.py MyScript.java

The output will be a randomized Java file (e.g., lI1O0lIlI.java) containing the protected code.

## ⚖️ Legal Disclaimer

The author is not responsible for any misuse. Always ensure you have the rights to the code you are obfuscating.
