import klayout.db as pya
import yaml
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import matplotlib
import matplotlib.colors as mcolors
from matplotlib.patches import Patch
import xml.etree.ElementTree as ET
import html

ROOT_DIR = Path(".")
FOLDERS = ["Si_220nm_active","SiN_300nm"]
SAVE_ROOT_DIR = Path("docs/comp_ref")


def parse_lyp_file(filepath):
    def parse_source(source_str):
        try:
            layer_str, rest = source_str.split('/')
            datatype_str = rest.split('@')[0]
            return int(layer_str), int(datatype_str)
        except Exception:
            return None

    with open(filepath, 'r', encoding='utf-8') as file:
        raw_content = file.read()

    xml_content = html.unescape(raw_content)
    root = ET.fromstring(xml_content)

    layers = []

    for props in root.findall('properties'):
        source = props.findtext('source')
        name = props.findtext('name')
        frame_color = props.findtext('frame-color')

        parsed_source = parse_source(source)
        if parsed_source:
            layers.append({
                'frame-color': frame_color,
                'name': name,
                'source': parsed_source
            })
        elif source == '*/*@*':
            for group in props.findall('group-members'):
                group_name = group.findtext('name')
                group_color = group.findtext('frame-color')
                group_source = group.findtext('source')
                parsed_group_source = parse_source(group_source)

                if parsed_group_source:
                    layers.append({
                        'frame-color': group_color,
                        'name': group_name,
                        'source': parsed_group_source
                    })

    return layers


#custom precedence from top (drawn last) to bottom (drawn first)
custom_precedence = [
    (6, 0),   # si etch 1 (dark) for SOI220A
    (3, 0),   # si etch 2 (light)
    (4, 0),   # si etch 2 (dark)
    (5, 0),   # si etch 3 (light)
    (204, 0),   #SiN etch, dark
    (203, 0),   #SiN etch, light
    (7, 0),   # low p-type doping (dark)
    (8, 0),     # low n-type, dark
    (9, 0),     # high p-type, dark
    (11, 0),    # high n-type, dark
    (23, 0),    # defect detector, dark
    (39, 0),    # heater filaments, light
    (41, 0),    # heater pads, light
    (12, 0),    # vias, dark
    (13, 0),    # electrodes, light
    (22, 0),    # cladding opening, dark

]

def plot_gds_with_shapes_and_ports(gds_path, yaml_path, output_path,lyp_path, zoom_factor = 0.1):
    # Load GDS file
    layout = pya.Layout()
    layout.read(gds_path)
    top_cell = layout.top_cell()
    dbu = layout.dbu
    
    lyp_layers = parse_lyp_file(lyp_path)
    
    layer_colour_map = {}
    for layer in lyp_layers:
        key = layer['source']  # Already a tuple (layer, datatype)
        colour = layer['frame-color']
        if colour:
            try:
                rgb = mcolors.to_rgb(colour)
                layer_colour_map[key] = rgb
            except ValueError:
                pass  # Skip invalid colours

    
    # Get bounding box
    bbox = top_cell.bbox()
    x_min, y_min = bbox.left * dbu, bbox.bottom * dbu
    x_max, y_max = bbox.right * dbu, bbox.top * dbu
    
    width = x_max - x_min
    height = y_max - y_min
    if width/height>5 or width/height<0.2:
        aspect_ratio = np.sqrt(height/width)
    else:
        aspect_ratio = height/width
    
    x_pad = width * zoom_factor
    y_pad = height * zoom_factor

    x_min_zoomed = x_min - x_pad 
    x_max_zoomed = x_max + x_pad 
    y_min_zoomed = y_min - y_pad
    y_max_zoomed = y_max + y_pad


    # Load ports from YAML
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    ports = data.get("ports", [])

    # Set up plot
    fig, ax = plt.subplots()
    ax.set_title(gds_path.stem)

    ax.set_xlim(x_min_zoomed, x_max_zoomed)
    ax.set_ylim(y_min_zoomed, y_max_zoomed)
    ax.set_box_aspect(aspect_ratio)

    ax.grid(True)

    
    
    # Get all non-empty layers
    layer_indices = [li for li in layout.layer_indexes() if not top_cell.shapes(li).is_empty()]

    # Build a lookup for layer_info
    layer_info_map = {li: layout.get_info(li) for li in layer_indices}

    # Sort using custom precedence
    def precedence_key(li):
        info = layer_info_map[li]
        try:
            # Lower index in custom_precedence means higher priority (drawn later)
            return custom_precedence.index((info.layer, info.datatype))
        except ValueError:
            # If not in custom list, assign lowest priority (drawn first)
            return len(custom_precedence)

    # Sort layer indices by precedence
    layer_indices.sort(key=precedence_key)
    layer_indices.reverse()

    num_layers = len(layer_indices)
    # Assign colours based on .lyp file, fallback to colormap if not found
    default_colour_map = matplotlib.colormaps.get_cmap('tab20')
    layer_to_colour = {}

    for i, layer_index in enumerate(layer_indices):
        info = layout.get_info(layer_index)
        key = (info.layer, info.datatype)
        if key in layer_colour_map:
            layer_to_colour[layer_index] = layer_colour_map[key]
        else:
            layer_to_colour[layer_index] = default_colour_map(i / num_layers)

    legend_entries = []
    


    
    
    # Draw polygons from all layers
    for layer_index in layer_indices:
        
        layer_info = layout.get_info(layer_index)
        layer_num = layer_info.layer
        datatype = layer_info.datatype

        colour = layer_to_colour[layer_index]
        #label = next((l['name'] for l in lyp_layers if l['source'] == (layer_num, datatype)), f"{layer_num}/{datatype}")
        #legend_entries.append((label, colour))

        
        label = f"{layer_num}/{datatype}"
        legend_entries.append((label, colour))
        
        shapes = top_cell.shapes(layer_index)
        for shape in shapes.each():
            if shape.is_box():
                box = shape.box
                x0, y0 = box.left * dbu, box.bottom * dbu
                x1, y1 = box.right * dbu, box.top * dbu
                rect = plt.Rectangle((x0, y0), x1 - x0, y1 - y0, # type: ignore
                                    edgecolor='none', facecolor=colour, linewidth=0.2)
                ax.add_patch(rect)

            elif shape.is_polygon():
                polygon = shape.polygon
                pts = [(pt.x * dbu, pt.y * dbu) for pt in polygon.each_point_hull()]
                if pts and pts[0] != pts[-1]:
                    pts.append(pts[0])
                poly = plt.Polygon(pts, edgecolor='none', facecolor=colour, linewidth=0.2) # type: ignore
                ax.add_patch(poly)

    legend_entries.sort(key=lambda entry: tuple(map(int, entry[0].split('/'))))
    
    
    #ax.legend(handles=handles, loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0., fontsize=8)
            
    # Define colours for port types
    port_colours = {
        "optical": "blue",
        "electrical_dc": "red",
        "electrical_rf": "red",
        "vertical_te": "green",
        "vertical_tm": "green",
        "edge": "green"
    }
# Plot ports as arrows and collect index-name mapping
    index_name_map = []

    for idx, port in enumerate(ports):
        x, y = port["center"]
        marker_size =4
        port_type = port.get("port_type", "unknown")
        port_angle = port.get("orientation",0.0)
        port_angle = int(np.mod(port_angle/90.0,4))
        #offsets = np.round([(x_pad/2,0),(0,y_pad/2),(-x_pad/2,0),(0,-y_pad/2)])
        offsets = [(2*marker_size,0),(0,2*marker_size),(-2*marker_size,0),(0,-2*marker_size)]

        colour = port_colours.get(port_type)
        fcolour = colour if port_type not in ["vertical_te", "vertical_tm"] else 'none'
        ax.plot(x, y, marker='o', markersize=marker_size, markeredgecolor=colour, markerfacecolor=fcolour)
        #ax.text(x+offsets[port_angle][0], y+offsets[port_angle][1], str(idx), fontsize=12, ha='center', va='center', color=colour)
        
        ax.annotate(str(idx), (x, y),
                    textcoords="offset points", xytext=offsets[port_angle], ha='center',va='center',color=colour)

        
    handles = [Patch(facecolor=colour, edgecolor='none', label=label)
            for label, colour in legend_entries]

    # Add legend outside the plot
    
    fig.tight_layout(rect=(0, 0.05, 1, 1))  # Reserve bottom space
    fig.legend(handles=handles, loc='lower center', ncol=min(len(handles), 4))
    


    #plt.show()
    # Save to JPEG
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved layout with shapes and ports to {output_path}")

for folder in FOLDERS:
    lyp_file = ROOT_DIR / folder / "layers.lyp"
    tmp_path = ROOT_DIR / folder / "components"
    output_dir = SAVE_ROOT_DIR / f"{folder}" / "birdseye"
    output_dir.mkdir(parents=True,exist_ok=True)
    for gds_file in sorted(tmp_path.glob("*.gds")):
        yaml_file = gds_file.with_suffix(".yaml")
        output_file = output_dir /  f"{gds_file.stem}.jpg"
        plot_gds_with_shapes_and_ports(gds_path=gds_file, yaml_path=yaml_file,lyp_path=lyp_file, output_path=output_file)
        print(f"{gds_file.stem} is plotted under {SAVE_ROOT_DIR}")
