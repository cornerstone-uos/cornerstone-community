import os
import yaml
import subprocess
from pathlib import Path

PLATFORMS = ["Si_220nm_active", "SiN_300nm"]
SUBFOLDERS = ["components", "ready-made"]
DOCS_DIR = Path("docs")
COMP_REF_DIR = Path("docs/comp_ref")
COMP_DIR_IDX = COMP_REF_DIR / "index.md"
CONTRIB_PATH = DOCS_DIR / "contributor-list.md"



def get_git_info(file_path):
    rel_path = os.path.relpath(file_path)
    try:
        last_modified = subprocess.check_output(
            ["git", "log", "-1", "--pretty=format:%ci", "--", rel_path],
            text=True
        ).strip()
        sha256 = subprocess.check_output(
            ["git", "hash-object", file_path],
            text=True
        ).strip()
        return last_modified, sha256
    except subprocess.CalledProcessError:
        return "Unknown", "Unknown"
def overwrite_after_marker(md_path: Path, new_lines: list[str], marker: str = ":caption: Reference"):
    """
    Overwrites the contents of a Markdown file starting from the line after the marker.
    """
    if not md_path.exists():
        raise FileNotFoundError(f"{md_path} does not exist.")

    with md_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    try:
        eof_index = next(i for i, line in enumerate(lines) if line.strip() == marker)
    except StopIteration:
        raise ValueError(f"Marker '{marker}' not found in {md_path}")

    # Keep everything up to and including the marker
    preserved = lines[:eof_index + 1]

    # Add new content after the marker
    updated = preserved + ["\n"] + [line + "\n" for line in new_lines]

    with md_path.open("w", encoding="utf-8") as f:
        f.writelines(updated)

    print(f"Updated {md_path} after marker '{marker}'")
def generate_docs():
    COMP_REF_DIR.mkdir(parents=True, exist_ok=True)
    unique_authors = set()

    for platform in PLATFORMS:
        folder_path = Path(platform)
        comp_md_path = COMP_REF_DIR / f"{platform}.md"
        sub_md_str = [] 
        with comp_md_path.open("w", encoding="utf-8") as md:
            md.write(f"# Platform information for \"{platform}\"\n\n")
            md.write("```{toctree}\n:maxdepth: 2\n:caption: Platform reference\n\n")
            md.write("[//]: # (EOF) \n")
           
        for subfolder in SUBFOLDERS:
            full_path = folder_path / f"{subfolder}"
            md_path = folder_path / "docs" / "comp-ref" / f"{subfolder}.md"
            md_path.parent.mkdir(parents=True, exist_ok=True)
            
            relative_path = os.path.relpath(md_path,start=comp_md_path.parent)
            sub_md_str.append(relative_path)
            
            with md_path.open("w", encoding="utf-8") as md:
                md.write(f"# Component information for \"{platform}\", subfolder \"{subfolder}\" \n\n")
                
                
                for gds_file in full_path.glob("*.gds"):
                    yaml_file = gds_file.with_suffix(".yaml")
                    authors = []
                    
                    
                    if yaml_file.exists():
                        with yaml_file.open("r", encoding="utf-8") as yf:
                            data = yaml.safe_load(yf)
                        authors = data.get("authors", [])
                        for author in authors:
                            name = author.get("name", "").strip()
                            org = author.get("organisation", "").strip()

                            if name and org and org.lower() != "cornerstone":
                                unique_authors.add((name, org))
                    else:
                        authors = []
                        print(f"YAML file not found for {gds_file.name}. Using default author info.")

                    # Format authors section
                    if not authors:
                        author_lines = ["- Authors: N/A"]
                    else:
                        author_lines = ["- Authors:"]
                        for author in authors:
                            name = author.get("name", "Unknown")
                            org = author.get("organisation", "Unknown")
                            author_lines.append(f"  - {name} ({org})")

                    # Get Git info
                    last_modified, sha256 = get_git_info(gds_file)

                    # Write to Markdown
                    md.write(f"## {gds_file.name}\n")
                    for line in author_lines:
                        md.write(f"{line}\n")
                    md.write(f"- Last Modified: {last_modified}\n")
                    md.write(f"- SHA256 Hash: {sha256}\n\n")
        overwrite_after_marker(md_path=comp_md_path, new_lines = sub_md_str, marker = ":caption: Platform reference")
    compref_appx = [f"{platform}.md" for platform in PLATFORMS]
    overwrite_after_marker(md_path = COMP_DIR_IDX,new_lines = compref_appx, marker = ":caption: Component reference")
    
    
    
    CONTRIB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with CONTRIB_PATH.open("w", encoding="utf-8") as f:
        f.write("# Contributor List\n\n")
        f.write("Many thanks to all the contributors (listed without order):\n\n")
        for name, org in sorted(unique_authors):
            f.write(f"- {name} ({org})\n")


if __name__ == "__main__":
    generate_docs()