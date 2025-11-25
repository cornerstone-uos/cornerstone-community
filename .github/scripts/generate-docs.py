import os
import yaml
import subprocess
import shutil
from pathlib import Path

PLATFORMS = ["Si_220nm_active", "SiN_300nm","Ge_on_Si","Si_220nm_passive","Si_340nm","Si_500nm","Si_sus_bias","Si_sus_not_bias","SiN_200nm"]
SUBFOLDERS = ["components", "ready-made"]
DOCS_DIR = Path("docs")
COMP_REF_DIR = Path("docs/comp_ref")
COMP_DIR_IDX = COMP_REF_DIR / "index.md"
CONTRIB_PATH = DOCS_DIR / "contributor-list.md"



def get_git_info(file_path):
    rel_path = os.path.relpath(file_path)
    try:
        sha256 = subprocess.check_output(
            ["git", "hash-object", file_path],
            text=True
        ).strip()
        return sha256
    except subprocess.CalledProcessError:
        return "Unknown"
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
        comp_md_dir = COMP_REF_DIR / f"{platform}"
        comp_md_dir.mkdir(parents=True, exist_ok= True)
        comp_md_path = comp_md_dir / "index.md"
        sub_md_str = [] 
        with comp_md_path.open("w", encoding="utf-8") as md:
            md.write(f"# Platform information for \"{platform}\"\n\n")
            md.write("```{toctree}\n:maxdepth: 2\n:caption: Platform reference\n\n")
            md.write("[//]: # (EOF) \n")
           
        for subfolder in SUBFOLDERS:
            full_path = folder_path / f"{subfolder}"
            md_path = folder_path / "docs" / "comp-ref" / f"{subfolder}.md"
            md_path.parent.mkdir(parents=True, exist_ok=True)
            
            sub_md_str.append(f"{subfolder}.md")
            
            with md_path.open("w", encoding="utf-8") as md:
                md.write(f"# Component information for \"{platform}\", subfolder \"{subfolder}\" \n\n")
                
                
                for gds_file in sorted(full_path.glob("*.gds")):
                    yaml_file = gds_file.with_suffix(".yaml")
                    authors = []
                    component_md_path = comp_md_dir / f"{gds_file.stem}.md"
                    component_md_path.parent.mkdir(parents=True, exist_ok=True)
                    component_md=component_md_path.open("w", encoding="utf-8")
                    

                    
                    
                    if yaml_file.exists():
                        with yaml_file.open("r", encoding="utf-8") as yf:
                            data = yaml.safe_load(yf)
                        authors = data.get("authors", [])
                        last_updated = data.get("last_updated",[]).strip()
                        for author in authors:
                            name = author.get("name", "").strip()
                            org = author.get("organisation", "").strip()

                            if name and org and org.lower() != "cornerstone":
                                unique_authors.add((name, org))
                    else:
                        authors = []
                        last_updated=["Unknown"]
                        print(f"YAML file not found for {gds_file.stem}. Using default author info.")

                    # Format authors section
                    if not authors:
                        #author_lines = ["- Authors: N/A"]
                        author_cell = "N/A"
                    else:
                        
                        authors_list = [f"{author.get('name', 'Unknown')} ({author.get('organisation', 'Unknown')})"
                                        for author in authors]
                        authors_cell = "<br>".join(authors_list)

                    # Get Git info
                    sha256 = get_git_info(gds_file)

                    # write to component md file
                    component_md.write(f"# {gds_file.stem}\n")

                    
                    # Markdown table header
                    component_md.write("| Field | Value |\n")
                    component_md.write("|:---------|:-----|\n")
                    # Write authors and file info
                    component_md.write(f"| Authors|{authors_cell}|\n")
                    component_md.write(f"| Last Updated | {last_updated} |\n")
                    component_md.write(f"| SHA256 Hash | `{sha256}` |\n")
                    # Import plot
                    component_md.write("## Preview\n")
                    component_md.write(f"![Preview](./birdseye/{gds_file.stem}.jpg)\n")

                    # Write to Markdown
                    md.write(f"## {gds_file.stem}\n")
                    
            shutil.copy(md_path,comp_md_dir / md_path.name)
        overwrite_after_marker(md_path=comp_md_path, new_lines = sub_md_str, marker = ":caption: Platform reference")
    compref_appx = [f"{platform}/index.md" for platform in PLATFORMS]
    overwrite_after_marker(md_path = COMP_DIR_IDX,new_lines = compref_appx, marker = ":caption: Component reference")
    
    
    
    CONTRIB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with CONTRIB_PATH.open("w", encoding="utf-8") as f:
        f.write("# Contributor List\n\n")
        f.write("Many thanks to all the contributors (listed without order):\n\n")
        for name, org in sorted(unique_authors):
            f.write(f"- {name} ({org})\n")


if __name__ == "__main__":
    generate_docs()