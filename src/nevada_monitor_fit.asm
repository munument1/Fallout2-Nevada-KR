; Nevada HRP-specific CP949 text fitting. cdecl(const char*, pixelWidth).
; Uses the game's active whole-string width callback, preserving DBCS pairs.
.386
.model flat
.code
PUBLIC FitKoreanMonitor
FitKoreanMonitor PROC
 push ebp
 mov ebp,esp
 push ebx
 push esi
 push edi
 sub esp,120h
 mov esi,[ebp+8]
 mov ebx,[ebp+12]
 xor edi,edi
 mov dword ptr [ebp-16],-1
 mov dword ptr [ebp-20],0
 test esi,esi
 jz done
 test ebx,ebx
 jle done
next_char:
 cmp edi,252
 jae done
 movzx eax,byte ptr [esi+edi]
 test eax,eax
 jz done
 cmp eax,13
 je newline
 cmp eax,10
 je newline
 mov ecx,1
 cmp eax,81h
 jb copy_char
 cmp eax,0feh
 ja copy_char
 movzx edx,byte ptr [esi+edi+1]
 cmp edx,41h
 jb copy_char
 cmp edx,5ah
 jbe pair_char
 cmp edx,61h
 jb copy_char
 cmp edx,7ah
 jbe pair_char
 cmp edx,81h
 jb copy_char
 cmp edx,0feh
 ja copy_char
pair_char:
 inc ecx
copy_char:
 mov [ebp-24],ecx
 lea edx,[ebp-120h]
 mov al,[esi+edi]
 mov [edx+edi],al
 cmp ecx,2
 jne terminate
 mov al,[esi+edi+1]
 mov [edx+edi+1],al
terminate:
 add ecx,edi
 mov byte ptr [edx+ecx],0
 pushad
 lea eax,[ebp-120h]
 call dword ptr ds:[51e3c0h]
 mov [esp+28],eax
 popad
 cmp eax,ebx
 jg overflow
 cmp byte ptr [esi+edi],20h
 jne accept_char
 mov [ebp-16],edi
accept_char:
 add edi,[ebp-24]
 mov [ebp-20],edi
 jmp next_char
newline:
 inc edi
 cmp eax,13
 jne newline_done
 cmp byte ptr [esi+edi],10
 jne newline_done
 inc edi
newline_done:
 mov [ebp-20],edi
 jmp done
overflow:
 cmp dword ptr [ebp-20],0
 jne use_space
 mov eax,[ebp-24]
 mov [ebp-20],eax
 jmp done
use_space:
 mov eax,[ebp-16]
 test eax,eax
 jle done
 mov [ebp-20],eax
done:
 mov eax,[ebp-20]
 add esp,120h
 pop edi
 pop esi
 pop ebx
 mov esp,ebp
 pop ebp
 ret
FitKoreanMonitor ENDP
END
