import os
from pathlib import Path
import struct
import unittest

import pefile
from tools.build_classic_complete import hd_fallback, set_ini, FONT_INIT


class ConfigTests(unittest.TestCase):
    def test_nevada_language_preserves_other_sections(self):
        before=b'[sound]\r\nvolume=83\r\n[system]\r\nlanguage=english\r\nmaster_dat=..\\master.dat\r\n'
        after=set_ini(before,'system','language','korean')
        self.assertEqual(after,before.replace(b'language=english',b'language=korean'))

    def test_translation_selection_preserves_mod_settings(self):
        before=b'[Main]\r\nTranslationsINI=./Translations.ini\r\n[Graphics]\r\nMode=4\r\n'
        self.assertEqual(set_ini(before,'Main','TranslationsINI','translations\\korean.ini'),before.replace(b'./Translations.ini',b'translations\\korean.ini'))


@unittest.skipUnless(os.environ.get('NEVADA_NATIVE_HD_EXE'),'Owner HD executable required')
class OwnerHDTests(unittest.TestCase):
    def test_hd_keeps_original_hrp_and_shared_engine_hook(self):
        before=Path(os.environ['NEVADA_NATIVE_HD_EXE']).read_bytes();after=hd_fallback(before)
        self.assertEqual(len(after),len(before))
        self.assertEqual(before[0xd4880:0xd488a],after[0xd4880:0xd488a])
        self.assertEqual(before[0xee5c0:0xee5e7],after[0xee5c0:0xee5e7])
        pe=pefile.PE(data=after);hook=pe.get_offset_from_rva(FONT_INIT-0x400000)
        target=FONT_INIT+5+struct.unpack_from('<i',after,hook+1)[0]
        self.assertEqual(target,0x400000+pe.sections[-1].VirtualAddress+0x800)
        original=pe.get_offset_from_rva(0x4caf22-0x400000)
        self.assertEqual(before[original:original+5],after[original:original+5])
        with self.assertRaisesRegex(ValueError,'Unknown font initializer'):
            hd_fallback(after)
