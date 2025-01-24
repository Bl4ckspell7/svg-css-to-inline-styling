# SVG CSS-to-Inline Style Converter

This Python script converts SVG files that use CSS styles into an equivalent format with inline styles. It ensures that SVG files render correctly in applications that do not support CSS styles by directly embedding style information into the SVG elements.

## Features

- Extracts style rules from the `<style>` block using the cssutils library.
- Converts `class`-based styles in SVG files into inline `fill` attributes.
- Applies styles to SVG elements based on their `class` attributes.
- Removes `<style>` elements and cleans up empty `<defs>` elements to streamline the SVG.
- Defaults to black fill for `<path>` elements without specified styles.

## Installation

1. Ensure you have Python 3 installed.
2. Install the `cssutils` library:
   ```bash
   pip install cssutils
   ```

## Usage

1. Save the script as `css_to_inline.py`.
2. Prepare an SVG file (e.g., `test.svg`) that uses CSS styles.
3. Run the script:
   ```bash
   python css_to_inline.py
   ```
    By default, the script will:
   - Read the specified input file.
   - Output the result as a new file with `_inlinestyle` appended to the original name. 

## Example
Input ([test.svg](test.svg)):
```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style type="text/css">
      .cls-1 {
        fill: #fff;
      }
      .cls-2 {
        fill: #37474f;
      }
      .cls-3 {
        fill: #46509e;
      }
    </style>
  </defs>
  <path class="cls-1" d="M10 10 H 90 V 90 H 10 Z" />
  <path class="cls-2" d="M20 20 H 80 V 80 H 20 Z" />
  <path class="cls-3" d="M30 30 H 70 V 70 H 30 Z" />
</svg>
```
Output ([test_inlinestyle.svg](test_inlinestyle.svg)):
```xml
<?xml version='1.0' encoding='utf-8'?>
<svg xmlns="http://www.w3.org/2000/svg">
  <path d="M10 10 H 90 V 90 H 10 Z" fill="#fff" />
  <path d="M20 20 H 80 V 80 H 20 Z" fill="#37474f" />
  <path d="M30 30 H 70 V 70 H 30 Z" fill="#46509e" />
</svg>
```

## License

This script is open-source and available under the [MIT License](LICENSE).
