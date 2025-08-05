import sys
import os
import zlib
import hashlib

def main():
    print("Logs from your program will appear here!", file=sys.stderr)
    
    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    
    elif command =="cat-file" and sys.argv[2] == '-p':
        filename = sys.argv[3]
        with open(f".git/objects/{filename[:2]}/{filename[2:]}",'rb') as f:
            blob = zlib.decompress(f.read()).split(b"\x00")[1]
            print(blob.decode("utf-8"),end="")

    elif command =="hash-object" and sys.argv[2]=='-w':
        filename = sys.argv[3]
        with open(filename,"rb") as f:
            content = f.read()

        header = f"blob {len(content)}".encode()
        full_content = header + b'\x00'+content

        hashed_content = hashlib.sha1(full_content).hexdigest()
        compressed = zlib.compress(full_content)

        dir_path = f".git/objects/{hashed_content[:2]}"
        object_path = f"{dir_path}/{hashed_content[2:]}"
        os.makedirs(dir_path,exist_ok=True)

        with open(object_path,"wb") as f:
            f.write(compressed)

        print(hashed_content)
    
    elif command=="write-tree" :
        index_entries = []

        with open(".index","r")as f:
            for line in f:
                mode,file_name,sha = line.strip().split()
                index_entries.append((mode,file_name,sha))
        
        def write_tree_from_index(index_entries,path_prefix=""):
            entries = []

            folders = {}
            for mode,path,sha in index_entries:
                if path.startswith(path_prefix):
                    continue
                rest = path[len(path_prefix):]
                if "/" in rest:
                    entries.append((mode,rest,sha))
                
                else:
                    folder, subpath = rest.split("/",1)
                    if folder not in folders:
                        folders[folder] = []
                    folders[folder].append((mode,path,sha))

            tree_data = b""
            for mode,filename,sha in entries:
                #"mode <filename>\0<sha>"
                mode_filename = f"{mode} {filename}".encode()
                null = b"\x00"
                raw_sha = bytes.fromhex(sha)
                entry = mode_filename+null+raw_sha
                tree_data += entry

            for folder,folders_entries in folders.items():
                subtree_sha = write_tree_from_index(index_entries,path_prefix+folder+"/")
                folder_entry = f"40000 {folder}".encode() + b"\x00"+ bytes.fromhex(subtree_sha)
                tree_data += folder_entry

            full_tree = f"tree {len(tree_data)}".encode() + b"\x00" + tree_data
            tree_sha = hashlib.sha1(full_tree).hexdigest()
            compressed = zlib.compress(full_tree)
            dir_path = f".git/objects/{tree_sha[:2]}"
            file_path = f"{dir_path}/{tree_sha[2:]}"
            os.makedirs(dir_path, exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(compressed)

            return tree_sha

        root_tree_sha = write_tree_from_index(index_entries)
        print(root_tree_sha)
        
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
