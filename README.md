# Git Internals in Python

A minimal, from-scratch implementation of core Git features using Python.
This project replicates Git's internal object model — without using Git itself — to understand how version control systems work under the hood.

---

## 🚀 Features Implemented

| Command                 | Description                                     |
| ----------------------- | ----------------------------------------------- |
| `init`                  | Initializes a new Git repository (`.git/`)      |
| `hash-object -w <file>` | Hashes and stores file content as a blob object |
| `cat-file -p <sha>`     | Reads and decompresses Git objects              |
| `write-tree`            | Constructs a tree object from a simulated index |
| (More coming soon...)   | commit-tree, HEAD refs, log, checkout, etc.     |

---

## 📦 How It Works

* **Blob storage**: File content is hashed with SHA-1 and compressed with zlib, then stored in `.git/objects/`.
* **Tree construction**: A tree object stores folder structure, built recursively from a `.index` file.
* **Custom Git CLI**: Each command is implemented as a Python CLI that mimics real Git behavior.

---

## 📁 Repository Structure

```bash
.git/                   # Created on init
├── HEAD                # Points to current ref
├── objects/            # Stores all Git objects (blobs, trees, commits)
└── refs/
.index                  # Simulated Git index for tree building
```

---

## 🛠️ Technologies Used

* Python 3
* `hashlib` for SHA-1 hashing
* `zlib` for object compression
* `os`, `sys` for filesystem + CLI operations

---

## 💡 Why This Project

Rebuilding Git internals helped me:

* Understand Git's content-addressable storage model
* Explore how commits, trees, and blobs work together
* Reinforce low-level file and CLI programming in Python

It’s a powerful way to learn what's really going on when you run `git commit`.

---

## 🧪 Sample Usage

```bash
# Step 1: Initialize
python3 git.py init

# Step 2: Create a file
echo "hello world" > a.txt

# Step 3: Hash and store the file as a blob
python3 git.py hash-object -w a.txt
# => e69de29...

# Step 4: Add entry to .index (simulate git add)
echo "100644 a.txt e69de29..." > .index

# Step 5: Create tree from .index
python3 git.py write-tree
# => <tree-sha>
```

---

## 📈 Coming Next

* `commit-tree` and commit object creation
* `.git/HEAD` and branch refs
* `log` traversal of commit history
* `checkout` to restore file trees

---

## 🤝 Contributions

This project is self-learning focused, but feel free to fork, explore, or suggest ideas!

---
