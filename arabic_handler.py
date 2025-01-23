#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arabic Text Handler Module
Created: 2025-01-23 18:52:06
Author: x9ci
"""
# arabic_handler.py
# import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from pathlib import Path
import shutil
import requests

import arabic_reshaper
from bidi.algorithm import get_display
import logging

class ArabicTextHandler:  # تم تغيير الاسم من ArabicHandler إلى ArabicTextHandler
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def process_text(self, text: str) -> str:
        """معالجة النص العربي وتحسينه للعرض"""
        try:
            # إعادة تشكيل النص العربي
            reshaped_text = arabic_reshaper.reshape(text)
            # تطبيق خوارزمية BIDI
            bidi_text = get_display(reshaped_text)
            return bidi_text
        except Exception as e:
            self.logger.error(f"خطأ في معالجة النص العربي: {str(e)}")
            return text

    def initialize_fonts(self):
        """تهيئة الخطوط العربية"""
        try:
            current_dir = Path(__file__).parent
            fonts_dir = current_dir / "fonts"
            fonts_dir.mkdir(exist_ok=True)

            font_paths = [
                "/usr/share/fonts/truetype/fonts-arabeyes/ae_AlArabiya.ttf",
                "/usr/share/fonts/truetype/fonts-arabeyes/ae_Furat.ttf",
                str(fonts_dir / "ae_AlArabiya.ttf"),
                str(fonts_dir / "Amiri-Regular.ttf")
            ]

            for font_path in font_paths:
                if Path(font_path).exists():
                    try:
                        if self.font_name not in pdfmetrics.getRegisteredFontNames():
                            pdfmetrics.registerFont(TTFont(self.font_name, font_path))
                            print(f"تم تحميل الخط: {font_path}")
                            return True
                    except Exception as e:
                        print(f"فشل تحميل الخط {font_path}: {str(e)}")
                        continue

            # إذا لم يتم العثور على خط، حاول التحميل
            return self.download_arabic_font()

        except Exception as e:
            print(f"خطأ في تهيئة الخطوط: {e}")
            return False

    def download_arabic_font(self):
        """تحميل الخط العربي"""
        try:
            font_url = "https://github.com/google/fonts/raw/main/ofl/amiri/Amiri-Regular.ttf"
            fonts_dir = Path(__file__).parent / "fonts"
            font_path = fonts_dir / "Amiri-Regular.ttf"
            
            response = requests.get(font_url)
            response.raise_for_status()
            
            with open(font_path, 'wb') as f:
                f.write(response.content)
            
            pdfmetrics.registerFont(TTFont(self.font_name, str(font_path)))
            print("تم تحميل الخط العربي بنجاح")
            return True
            
        except Exception as e:
            print(f"خطأ في تحميل الخط العربي: {e}")
            return False

    def process_arabic_text(self, text):
        """معالجة النص العربي"""
        try:
            reshaped_text = arabic_reshaper.reshape(text)
            bidi_text = get_display(reshaped_text)
            return bidi_text
        except Exception as e:
            print(f"خطأ في معالجة النص العربي: {e}")
            return text