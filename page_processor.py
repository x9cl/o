#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Page Processor
Created: 2025-01-22 21:15:20
Author: x9ci
"""

import os
import logging
from io import BytesIO
from typing import List, Dict, Tuple
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class PageProcessor:
    def __init__(self):
        self.font_name = 'Arabic'
        self.font_size = 14
        self.initialize_fonts()

    def initialize_fonts(self):
        """تهيئة الخطوط العربية"""
        try:
            font_paths = [
                "/usr/share/fonts/truetype/arabic/Amiri-Regular.ttf",
                "./fonts/Amiri-Regular.ttf",
                "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
                "./fonts/FreeSans.ttf"
            ]

            for font_path in font_paths:
                if os.path.exists(font_path):
                    if self.font_name not in pdfmetrics.getRegisteredFontNames():
                        pdfmetrics.registerFont(TTFont(self.font_name, font_path))
                        print(f"تم تحميل الخط: {font_path}")
                        return True

            print("تحذير: لم يتم العثور على خط عربي مناسب")
            return False

        except Exception as e:
            print(f"خطأ في تهيئة الخطوط: {e}")
            return False

    def create_translated_overlay(self, blocks: List[Dict], page_size: Tuple[float, float]) -> BytesIO:
        """إنشاء طبقة الترجمة"""
        try:
            packet = BytesIO()
            c = canvas.Canvas(packet, pagesize=page_size)

            for block in blocks:
                try:
                    text = block['text']
                    if not text:
                        continue

                    # موقع النص
                    bbox = block['bbox']
                    x = bbox[0]
                    y = page_size[1] - bbox[1]

                    # رسم خلفية بيضاء شفافة
                    text_width = c.stringWidth(text, self.font_name, self.font_size)
                    c.saveState()
                    c.setFillColorRGB(1, 1, 1, 0.9)
                    c.rect(x, y - self.font_size, text_width, self.font_size * 1.2, fill=True)
                    c.restoreState()

                    # كتابة النص
                    c.setFont(self.font_name, self.font_size)
                    c.drawString(x, y, text)

                except Exception as e:
                    print(f"خطأ في إضافة نص مترجم: {str(e)}")

            c.save()
            packet.seek(0)
            return packet

        except Exception as e:
            print(f"خطأ في إنشاء طبقة الترجمة: {str(e)}")
            # إنشاء صفحة فارغة في حالة الخطأ
            packet = BytesIO()
            c = canvas.Canvas(packet, pagesize=page_size)
            c.save()
            packet.seek(0)
            return packet

    def process_page(self, blocks: List[Dict], page_size: Tuple[float, float]) -> BytesIO:
        """معالجة صفحة كاملة"""
        return self.create_translated_overlay(blocks, page_size)