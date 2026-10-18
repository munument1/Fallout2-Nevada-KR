"""Build the ready-to-copy Nevada Extended Korean package from owner files.

The shared font DLL stays byte-identical. Only NevadaHD.exe receives a
verified secondary font-initialization entry, retaining its original HRP code.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import zipfile

import pefile

FONT_INIT = 0x4D555C
FONT_INIT_PREFIX = bytes.fromhex('5351525657')
FONT_INIT_HASH = '8bf0be4a1b800412100a596d3bf5302af23dbbd4c7f219e4bf48275270d20304'
SHARED_DLL_HASH = '08e1fc1afe452f3fb727138d14b1856de17f73729960c575f8b09e72ff50893e'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def hd_fallback(raw):
    pe = pefile.PE(data=raw)
    if pe.OPTIONAL_HEADER.ImageBase != 0x400000 or len(pe.sections) != 7:
        raise ValueError('Expected installed native Korean Nevada HD image')
    sec = pe.sections[-1]
    if sec.Name.rstrip(b'\0') != b'.krinit' or sec.SizeOfRawData != 0x1000:
        raise ValueError('Native Korean loader section missing')
    off = pe.get_offset_from_rva(FONT_INIT - 0x400000)
    if sha(raw[off:off + 32]) != FONT_INIT_HASH:
        raise ValueError('Unknown font initializer; refusing patch')
    old_hook = pe.get_offset_from_rva(0x4CAF22 - 0x400000)
    target = 0x4CAF27 + struct.unpack_from('<i', raw, old_hook + 1)[0]
    base = 0x400000 + sec.VirtualAddress
    if raw[old_hook] != 0xE9 or target != base + 0x480:
        raise ValueError('Original native hook does not match')
    if raw[sec.PointerToRawData + 0x600:sec.PointerToRawData + 0x611] != b'fallout2font.dll\0':
        raise ValueError('Unexpected font bridge')
    code = bytearray(b'\x9c\x60')
    code += b'\x68' + struct.pack('<I', base + 0x600)
    code += b'\xff\x15' + struct.pack('<I', 0x6C020C)
    code += b'\x85\xc0'; fail1 = len(code); code += b'\x74\0'
    code += b'\x68' + struct.pack('<I', base + 0x620) + b'\x50'
    code += b'\xff\x15' + struct.pack('<I', 0x6C01FC)
    code += b'\x85\xc0'; fail2 = len(code); code += b'\x74\0'
    code += b'\xff\xd0'; restore = len(code)
    code += b'\x61\x9d' + FONT_INIT_PREFIX
    va = base + 0x800
    code += b'\xe9' + struct.pack('<i', FONT_INIT + 5 - (va + len(code) + 5))
    for n in [fail1, fail2]: code[n + 1] = restore - n - 2
    dest = sec.PointerToRawData + 0x800
    if any(raw[dest:dest + len(code)]):
        raise ValueError('Fallback space is already used')
    result = bytearray(raw)
    result[dest:dest + len(code)] = code
    result[off:off + 5] = b'\xe9' + struct.pack('<i', va - FONT_INIT - 5)
    updated = pefile.PE(data=result)
    struct.pack_into('<I', result, updated.OPTIONAL_HEADER.get_field_absolute_offset('CheckSum'), updated.generate_checksum())
    # Preserve the HRP startup, original Korean loader and all other game code.
    allowed = set(range(off, off + 5)) | set(range(dest, dest + len(code)))
    checksum = updated.OPTIONAL_HEADER.get_field_absolute_offset('CheckSum')
    allowed.update(range(checksum, checksum + 4))
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(raw, result)))
    return bytes(result)


def set_ini(raw, section, key, value):
    lines = raw.splitlines(keepends=True); active = False; found = False
    out = []
    for line in lines:
        if line.strip().startswith(b'['):
            if active and not found: out.append(key.encode() + b'=' + value.encode() + b'\r\n'); found = True
            active = line.strip().lower() == ('[' + section + ']').encode().lower()
        if active and re.match(rb'\s*' + key.encode() + rb'\s*=', line, re.I):
            if not found: out.append(key.encode() + b'=' + value.encode() + b'\r\n'); found = True
        else: out.append(line)
    if not found:
        if not active: out.append(('\r\n[' + section + ']\r\n').encode())
        out.append((key + '=' + value + '\r\n').encode())
    return b''.join(out)


def build(game, translations, output):
    with zipfile.ZipFile(translations) as z:
        payload = {n: z.read(n) for n in z.namelist() if not n.endswith('/')}
    old_manifest = json.loads(payload.pop('translation-manifest.json'))
    original_translations = {n: sha(b) for n,b in payload.items() if n != 'INSTALL_KO.md'}
    for name in ['Nevada.exe','NevadaHD.exe','Nevada.cfg','ddraw.ini','fallout2font.dll','fallout2font.ini']:
        payload[name] = (game/name).read_bytes()
    if sha(payload['fallout2font.dll']) != SHARED_DLL_HASH:
        raise ValueError('Use the verified shared v1.2.3 font DLL')
    payload['NevadaHD.exe'] = hd_fallback(payload['NevadaHD.exe'])
    payload['Nevada.cfg'] = set_ini(payload['Nevada.cfg'], 'system', 'language', 'korean')
    from tools.runtime import sfall_crc
    from tools.install_engine import ensure_sfall_crc
    import tools.runtime as runtime
    table = json.loads((Path(runtime.__file__).resolve().parents[1]/"runtime-manifest.json").read_text(encoding="utf-8"))["crc_table"]
    # This import is not needed by users; release builds load the shared author's
    # runtime utility through --engine-tools during maintainer packaging.
    text = payload['ddraw.ini'].decode('latin-1')
    crcs = [f'0x{sfall_crc(payload[name], table):08X}' for name in ['Nevada.exe','NevadaHD.exe']]
    for crc in crcs: text = ensure_sfall_crc(text, crc)
    payload['ddraw.ini'] = set_ini(text.encode('latin-1'), 'Main', 'TranslationsINI', 'translations\\korean.ini')
    for p in sorted((game/'fonts').glob('*')):
        if p.is_file(): payload['fonts/'+p.name] = p.read_bytes()
    instructions = Path(__file__).resolve().parents[1]/'docs/CLASSIC_COMPLETE_KO.md'
    payload['INSTALL_KO.md'] = instructions.read_bytes()
    assert all(sha(payload[n]) == h for n,h in original_translations.items())
    manifest = {k:v for k,v in old_manifest.items() if k not in ['files','engine_release','engine_repository','engine_minimum_release']}
    manifest.update({'package':'nevada-classic-complete','release':'v2026.10.18-classic-complete.1','engine_mode':'bundled-native-v1.2.3','installation':'copy-overwrite','engine_validation':'standard and HD font registration and wrapping inspected with Nevada bundled sfall','hd_fix':'secondary verified font initialization; shared DLL unchanged','files':{n:sha(b) for n,b in sorted(payload.items())}})
    payload['translation-manifest.json'] = json.dumps(manifest,ensure_ascii=False,indent=2).encode('utf-8')
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for n,b in sorted(payload.items()):
            info=zipfile.ZipInfo(n,date_time=(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,b)
    with zipfile.ZipFile(output) as z:
        assert z.testzip() is None
        for n,h in manifest['files'].items(): assert sha(z.read(n))==h,n
    output.with_suffix('.zip.sha256').write_text(sha(output.read_bytes())+'  '+output.name+'\n',encoding='ascii')
    print(json.dumps({'zip':str(output),'files':len(payload),'translation_files_preserved':len(original_translations),'exe_crcs':crcs,'sha256':sha(output.read_bytes())},ensure_ascii=True))


if __name__ == '__main__':
    import sys
    a=argparse.ArgumentParser();a.add_argument('--game',type=Path,required=True);a.add_argument('--translations',type=Path,required=True);a.add_argument('--output',type=Path,required=True);a.add_argument('--engine-tools',type=Path,required=True)
    args=a.parse_args();sys.path.insert(0,str(args.engine_tools));build(args.game,args.translations,args.output)
