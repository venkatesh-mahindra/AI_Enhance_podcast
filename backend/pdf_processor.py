"""
PDF Processing Module
Extracts text, images, and structure from PDF files
"""

import io
import re
from typing import Dict, List

import fitz  # PyMuPDF
import numpy as np
from PIL import Image


class PDFProcessor:
    def __init__(self):
        self.supported_formats = ["pdf"]

    def extract_content(self, pdf_path: str) -> Dict:
        """
        Extract basic content and metadata from PDF
        Returns preview and basic info
        """
        try:
            doc = fitz.open(pdf_path)

            # Extract first page text as preview
            first_page = doc[0]
            preview_text = first_page.get_text()

            # Check for images
            has_images = False
            for page_num in range(len(doc)):
                page = doc[page_num]
                images = page.get_images()
                if images:
                    has_images = True
                    break

            result = {
                "page_count": len(doc),
                "has_images": has_images,
                "preview": preview_text[:500],
            }

            doc.close()
            return result

        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")

    def extract_full_content(self, pdf_path: str) -> Dict:
        """
        Extract complete content including text, images, and structure
        """
        try:
            doc = fitz.open(pdf_path)

            content = {
                "text_blocks": [],
                "images": [],
                "metadata": {
                    "title": doc.metadata.get("title", ""),
                    "author": doc.metadata.get("author", ""),
                    "page_count": len(doc),
                },
            }

            for page_num in range(len(doc)):
                page = doc[page_num]

                # Extract text with structure
                text_blocks = self._extract_text_blocks(page, page_num)
                content["text_blocks"].extend(text_blocks)

                # Extract images
                images = self._extract_images(page, page_num)
                content["images"].extend(images)

            doc.close()
            return content

        except Exception as e:
            raise Exception(f"Error extracting full content: {str(e)}")

    def _extract_text_blocks(self, page, page_num: int) -> List[Dict]:
        """Extract text blocks with their types (heading, paragraph, list)"""
        blocks = []
        text_dict = page.get_text("dict")

        for block in text_dict["blocks"]:
            if block["type"] == 0:  # Text block
                block_text = ""
                font_sizes = []

                for line in block["lines"]:
                    for span in line["spans"]:
                        block_text += span["text"]
                        font_sizes.append(span["size"])

                # Determine block type based on font size
                avg_font_size = np.mean(font_sizes) if font_sizes else 12
                block_type = "paragraph"

                if avg_font_size > 16:
                    block_type = "heading"
                elif block_text.strip().startswith(("•", "-", "1.", "2.", "3.")):
                    block_type = "list_item"

                if block_text.strip():  # Only add non-empty blocks
                    blocks.append(
                        {
                            "page": page_num + 1,
                            "type": block_type,
                            "text": block_text.strip(),
                            "font_size": avg_font_size,
                        }
                    )

        return blocks

    def _extract_images(self, page, page_num: int) -> List[Dict]:
        """Extract images from page"""
        images = []
        image_list = page.get_images()

        for img_index, img in enumerate(image_list):
            try:
                xref = img[0]
                base_image = page.parent.extract_image(xref)

                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                # Convert to PIL Image
                image = Image.open(io.BytesIO(image_bytes))

                # Get image position
                rects = page.get_image_rects(xref)
                img_rect = rects[0] if rects else page.rect

                images.append(
                    {
                        "page": page_num + 1,
                        "index": img_index,
                        "format": image_ext,
                        "size": image.size,
                        "position": {
                            "x0": img_rect.x0,
                            "y0": img_rect.y0,
                            "x1": img_rect.x1,
                            "y1": img_rect.y1,
                        },
                    }
                )
            except Exception as e:
                print(
                    f"Error extracting image {img_index} from page {page_num}: {str(e)}"
                )
                continue

        return images

    def create_narrative_structure(self, content: Dict) -> str:
        """
        Create a narrative structure from extracted content
        Useful for podcast script generation
        """
        narrative = ""

        # Add title if available
        if content["metadata"]["title"]:
            narrative += f"Title: {content['metadata']['title']}\n\n"

        current_section = ""

        for block in content["text_blocks"]:
            if block["type"] == "heading":
                if current_section:
                    narrative += current_section + "\n\n"
                current_section = f"## {block['text']}\n\n"
            else:
                current_section += block["text"] + " "

        if current_section:
            narrative += current_section

        return narrative
