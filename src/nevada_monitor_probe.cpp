#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>
using Width=int(__cdecl*)(const char*);
static Width measure;
static void* widthSlot;
static void* byteSlot;
static void* spaceSlot;
static int __cdecl measureText(const char* s){return measure(s);}
static int __cdecl measureByte(int ch){char s[2]={static_cast<char>(ch),0};return measure(s);}
extern "C" __declspec(naked) void WatcomWidth(){__asm{
 pushad
 push eax
 call measureText
 add esp,4
 mov [esp+28],eax
 popad
 ret
}}
extern "C" __declspec(naked) void WatcomByte(){__asm{
 pushad
 push eax
 call measureByte
 add esp,4
 mov [esp+28],eax
 popad
 ret
}}
extern "C" __declspec(naked) void WatcomSpace(){__asm{
 xor eax,eax
 ret
}}
using Fit=int(__cdecl*)(const char*,int);
static void setup(HMODULE module){
 auto* base=reinterpret_cast<unsigned char*>(module);
 *reinterpret_cast<void**>(base+0x684f8)=&byteSlot;
 *reinterpret_cast<void**>(base+0x68500)=&spaceSlot;
}
int main(int argc,char** argv){
 if(argc!=4)return 2;
 widthSlot=reinterpret_cast<void*>(&WatcomWidth);
 byteSlot=reinterpret_cast<void*>(&WatcomByte);
 spaceSlot=reinterpret_cast<void*>(&WatcomSpace);
 auto font=LoadLibraryA("fallout2font.dll");if(!font)return 4;
 auto init=reinterpret_cast<void(__cdecl*)()>(GetProcAddress(font,"InitFont"));
 auto select=reinterpret_cast<void(__cdecl*)(int)>(GetProcAddress(font,"SelectFont"));
 measure=reinterpret_cast<Width>(GetProcAddress(font,"GetTextWidth"));init();select(101);
 auto before=LoadLibraryExA(argv[1],nullptr,DONT_RESOLVE_DLL_REFERENCES);
 auto after=LoadLibraryExA(argv[2],nullptr,DONT_RESOLVE_DLL_REFERENCES);if(!before||!after)return 5;
 setup(before);setup(after);
 // Redirect the single game callback slot to a local stub only in this
 // isolated probe; no game process is launched or modified by the test.
 auto* patchedBase=reinterpret_cast<unsigned char*>(after);
 auto* headers=reinterpret_cast<IMAGE_NT_HEADERS32*>(patchedBase+reinterpret_cast<IMAGE_DOS_HEADER*>(patchedBase)->e_lfanew);
 auto* section=IMAGE_FIRST_SECTION(headers)+headers->FileHeader.NumberOfSections-1;
 auto* code=patchedBase+section->VirtualAddress;
 DWORD oldProtect;VirtualProtect(code,section->Misc.VirtualSize,PAGE_EXECUTE_READWRITE,&oldProtect);
 int injected=0;
 for(DWORD i=0;i+6<=section->Misc.VirtualSize;++i){
  if(code[i]==0xff&&code[i+1]==0x15&&*reinterpret_cast<DWORD*>(code+i+2)==0x51e3c0){
   *reinterpret_cast<void***>(code+i+2)=&widthSlot;++injected;
  }
 }
 if(injected!=1)return 7;
 FlushInstructionCache(GetCurrentProcess(),code,section->Misc.VirtualSize);

 FILE* f=nullptr;fopen_s(&f,argv[3],"rb");if(!f)return 6;
 std::vector<char> data;char chunk[4096];size_t n;while((n=fread(chunk,1,sizeof(chunk),f)))data.insert(data.end(),chunk,chunk+n);fclose(f);data.push_back(0);
 int badBefore=0,failures=0,lines=0,samples=0;
 for(size_t offset=0;offset+1<data.size();){
  const char* text=data.data()+offset;size_t length=strlen(text);offset+=length+1;if(!length)continue;++samples;
  auto oldFit=reinterpret_cast<Fit>(reinterpret_cast<unsigned char*>(before)+0xf250);
  int taken=oldFit(text,320);if(taken>0&&static_cast<size_t>(taken)<=length){std::string line(text,taken);if(measure(line.c_str())>320)++badBefore;}
  for(int entry:{0xf250,0xf2e0})for(int width:{150,167,280,320,327,500}){
   auto fit=reinterpret_cast<Fit>(reinterpret_cast<unsigned char*>(after)+entry);
   size_t start=0;int guard=0;
   while(start<length&&++guard<1000){
    int count=fit(text+start,width);
    if(count<=0||static_cast<size_t>(count)>length-start){++failures;break;}
    std::string line(text+start,count);
    if(MultiByteToWideChar(949,MB_ERR_INVALID_CHARS,line.data(),static_cast<int>(line.size()),nullptr,0)<=0||measure(line.c_str())>width){++failures;break;}
    start+=count;++lines;
    if(text[start]==' ')++start;
   }
   if(start<length)++failures;
  }
 }
 printf("samples=%d lines=%d pre-fix_overflows=%d fixed_failures=%d\n",samples,lines,badBefore,failures);
 return failures==0&&badBefore>0?0:1;
}
