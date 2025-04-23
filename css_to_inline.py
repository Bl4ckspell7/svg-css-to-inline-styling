import logging
import xml.etree.ElementTree as ET

import cssutils

# Suppress cssutils warnings
cssutils.log.setLevel(logging.ERROR)

# Namespace for SVG
NAMESPACE = {"svg": "http://www.w3.org/2000/svg"}


def parse_css_with_cssutils(style_content):
    """
    Extract CSS class styles from the <style> block using cssutils.
    """
    style_dict = {}
    parser = cssutils.CSSParser()
    stylesheet = parser.parseString(style_content)

    for rule in stylesheet.cssRules:
        if rule.type == rule.STYLE_RULE:  # Only process style rules
            class_name = rule.selectorText.lstrip(".")  # Remove the leading '.'
            fill = rule.style.getPropertyValue("fill")
            if fill:
                style_dict[class_name] = fill.strip()

    return style_dict


def apply_inline_styles(svg_root, styles):
    """
    Applies inline styles based on extracted CSS classes.
    """
    for element in svg_root.findall(".//*[@class]", NAMESPACE):
        class_name = element.attrib.get("class")
        if class_name in styles:
            element.set("fill", styles[class_name])
            del element.attrib["class"]  # Remove class attribute after applying style
        else:
            print(f"Class '{class_name}' not found in styles.")

    # Apply default fill for <path> elements without `fill` or `class` attributes
    for element in svg_root.findall(".//svg:path", NAMESPACE):
        if "fill" not in element.attrib:
            element.set("fill", "#000")  # Default to black


def remove_css_styles_and_empty_defs(svg_root):
    """
    Removes all <style> elements and their parent <defs> elements if empty.
    Also removes <style> elements directly inside the <svg>.
    """
    # Remove all <style> elements within <defs>
    for defs_element in svg_root.findall(".//svg:defs", NAMESPACE):
        for style_element in defs_element.findall(".//svg:style", NAMESPACE):
            defs_element.remove(style_element)

        # If <defs> is empty after removing <style>, remove it as well
        if len(defs_element) == 0:  # Check if there are no child elements
            svg_root.remove(defs_element)

    # Manually find and remove <style> elements directly under the root
    for style_element in list(svg_root):  # Use list() to make a copy of children
        if style_element.tag == f"{{{NAMESPACE['svg']}}}style":
            svg_root.remove(style_element)


def convert_svg_to_inline(input_file, output_file):
    """
    Convert an SVG file to use inline styles instead of CSS classes and remove the <style> block.
    """
    tree = ET.parse(input_file)
    root = tree.getroot()

    styles = {}
    # Find the <style> element
    style_content = None
    for style_element in root.findall(".//svg:style", NAMESPACE):
        style_content = style_element.text
        break  # Assume one <style> block for simplicity

    if style_content:
        print(f"Raw style content:\n{style_content.strip()}")  # Debugging
        styles = parse_css_with_cssutils(style_content)
        print(f"Extracted styles: {styles}")
    else:
        print("No styles found in the <style> block.")

    apply_inline_styles(root, styles)
    remove_css_styles_and_empty_defs(root)  # Remove the <style> block

    # Register default namespace to prevent `ns0:` in output
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    tree.write(output_file, encoding="utf-8", xml_declaration=True)


# Example Usage
INPUT_SVG = "test.svg"  # Replace with the path to your SVG file
OUTPUT_SVG = "test" + "_inlinestyle.svg"


def main():
    convert_svg_to_inline(INPUT_SVG, OUTPUT_SVG)


if __name__ == "__main__":
    main()
