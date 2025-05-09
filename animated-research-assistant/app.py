from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# ① 允许前端跨域调用
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # 生产环境请替换为具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

message_all = '''
宇茜姐姐的返回：
{"status":"success","code":"Function: mainCRTStartup\n\nvoid mainCRTStartup(undefined8 param_1,undefined8 param_2,undefined8 param_3)\n\n{\n  *(undefined4 *)_refptr_mingw_app_type = 0;
\n  __security_init_cookie();\n  __tmainCRTStartup(param_1,param_2,param_3);\n  return;\n}\n\n\n----------------------------------------\nFunction: atexit\n\nint __cdecl atexit(_func_5
014 *param_1)\n\n{\n  _onexit_t p_Var1;\n  \n  p_Var1 = _onexit((_onexit_t)param_1);\n  return -(uint)(p_Var1 == (_onexit_t)0x0);\n}\n\n\n----------------------------------------\nFunc
tion: vulnerable_function\n\nvoid vulnerable_function(char *param_1)\n\n{\n  char local_12 [10];\n  \n  strcpy(local_12,param_1);\n  return;\n}\n\n\n-----------------------------------
-----\nFunction: main\n\nint __cdecl main(int _Argc,char **_Argv,char **_Env)\n\n{\n  undefined8 local_28;\n  undefined8 local_20;\n  undefined4 local_18;\n  \n  __main();\n  local_28
= 0x4141414141414141;\n  local_20 = 0x4141414141414141;\n  local_18 = 0x41414141;\n  vulnerable_function((char *)&local_28);\n  return 0;\n}\n\n\n--------------------------------------
--\nFunction: fpreset\n\nvoid __cdecl fpreset(void)\n\n{\n  return;\n}\n\n\n----------------------------------------\nFunction: vfprintf\n\nint __cdecl vfprintf(FILE *_File,char *_Form
at,va_list _ArgList)\n\n{\n  int iVar1;\n  \n                    /* WARNING: Could not recover jumptable at 0x00402a70. Too many branches */\n                    /* WARNING: Treating i
ndirect jump as call */\n  iVar1 = vfprintf(_File,_Format,_ArgList);\n  return iVar1;\n}\n\n\n----------------------------------------\nFunction: strncmp\n\nint __cdecl strncmp(char *_
Str1,char *_Str2,size_t _MaxCount)\n\n{\n  int iVar1;\n  \n                    /* WARNING: Could not recover jumptable at 0x00402a78. Too many branches */\n                    /* WARNI
NG: Treating indirect jump as call */\n  iVar1 = strncmp(_Str1,_Str2,_MaxCount);\n  return iVar1;\n}\n\n\n----------------------------------------\nFunction: strlen\n\nsize_t __cdecl s
trlen(char *_Str)\n\n{\n  size_t sVar1;\n  \n                    /* WARNING: Could not recover jumptable at 0x00402a80. Too many branches */\n                    /* WARNING: Treating i
ndirect jump as call */\n  sVar1 = strlen(_Str);\n  return sVar1;\n}\n\n\n----------------------------------------\nFunction: strcpy\n\nchar * __cdecl strcpy(char *_Dest,char *_Source)
\n\n{\n  char *pcVar1;\n  \n                    /* WARNING: Could not recover jumptable at 0x00402a88. Too many branches */\n                    /* WARNING: Treating indirect jump as c
all */\n  pcVar1 = strcpy(_Dest,_Source);\n  return pcVar1;\n}\n\n\n----------------------------------------\nFunction: signal\n\n/* WARNING: Globals starting with '_' overlap smaller
symbols at the same address */\n\nvoid signal(int param_1)\n\n{\n                    /* WARNING: Could not recover jumptable at 0x00402a90. Too many branches */\n                    /*
 WARNING: Treating indirect jump as call */\n  (*___imp_signal)();\n  return;\n}\n\n\n----------------------------------------\nFunction: memcpy\n\nvoid * __cdecl memcpy(void *_Dst,voi
d *_Src,size_t _Size)\n\n{\n  void *pvVar1;\n  \n                    /* WARNING: Could not recover jumptable at 0x00402a98. Too many branches */\n                    /* WARNING: Treati
ng indirect jump as call */\n  pvVar1 = memcpy(_Dst,_Src,_Size);\n  return pvVar1;\n}\n\n\n----------------------------------------\nFunction: malloc\n\nvoid * __cdecl malloc(size_t _S
ize)\n\n{\n  void *pvVar1;\n  \n                    /* WARNING: Could not recover jumptable at 0x00402aa0. Too many branches */\n                    /* WARNING: Treating indirect jump
as call */\n  pvVar1 = malloc(_Size);\n  return pvVar1;\n}\n\n\n----------------------------------------\nFunction: fwrite\n\nsize_t __cdecl fwrite(void *_Str,size_t _Size,size_t _Coun
t,FILE *_File)\n\n{\n  size_t sVar1;\n  \n                    /* WARNING: Could not recover jumptable at 0x00402aa8. Too many branches */\n                    /* WARNING: Treating indi
rect jump as call */\n  sVar1 = fwrite(_Str,_Size,_Count,_File);\n  return sVar1;\n}\n\n\n----------------------------------------\nFunction: free\n\nvoid __cdecl free(void *_Memory)\n
\n{\n                    /* WARNING: Could not recover jumptable at 0x00402ab0. Too many branches */\n                    /* WARNING: Treating indirect jump as call */\n  free(_Memory)
;\n  return;\n}\n\n\n----------------------------------------\nFunction: fprintf\n\nint __cdecl fprintf(FILE *_File,char *_Format,...)\n\n{\n  int iVar1;\n  \n                    /* WA
RNING: Could not recover jumptable at 0x00402ab8. Too many branches */\n                    /* WARNING: Treating indirect jump as call */\n  iVar1 = fprintf(_File,_Format);\n  return i
Var1;\n}\n\n\n----------------------------------------\nFunction: exit\n\nvoid __cdecl exit(int _Code)\n\n{\n                    /* WARNING: Could not recover jumptable at 0x00402ac0.
Too many branches */\n                    /* WARNING: Subroutine does not return */\n                    /* WARNING: Treating indirect jump as call */\n  exit(_Code);\n  return;\n}\n\n
\n----------------------------------------\nFunction: calloc\n\nvoid * __cdecl calloc(size_t _Count,size_t _Size)\n\n{\n  void *pvVar1;\n  \n                    /* WARNING: Could not r
ecover jumptable at 0x00402ac8. Too many branches */\n                    /* WARNING: Treating indirect jump as call */\n  pvVar1 = calloc(_Count,_Size);\n  return pvVar1;\n}\n\n\n----
------------------------------------\nFunction: abort\n\nvoid __cdecl abort(void)\n\n{\n                    /* WARNING: Could not recover jumptable at 0x00402ad0. Too many branches */\
n                    /* WARNING: Subroutine does not return */\n                    /* WARNING: Treating indirect jump as call */\n  abort();\n  return;\n}\n\n\n----------------------------------------\nFunction: VirtualQuery\n\nSIZE_T __stdcall VirtualQuery(LPCVOID lpAddress,PMEMORY_BASIC_INFORMATION lpBuffer,SIZE_T dwLength)\n\n{\n  SIZE_T SVar1;\n  \n
        /* WARNING: Could not recover jumptable at 0x00402b90. Too many branches */\n                    /* WARNING: Treating indirect jump as call */\n  SVar1 = VirtualQuery(lpAddress
,lpBuffer,dwLength);\n  return SVar1;\n}\n\n\n----------------------------------------\nFunction: VirtualProtect\n\nBOOL __stdcall\nVirtualProtect(LPVOID lpAddress,SIZE_T dwSize,DWORD
flNewProtect,PDWORD lpflOldProtect)\n\n{\n  BOOL BVar1;\n  \n                    /* WARNING: Could not recover jumptable at 0x00402b98. Too many branches */\n                    /* WAR
NING: Treating indirect jump as call */\n  BVar1 = VirtualProtect(lpAddress,dwSize,flNewProtect,lpflOldProtect);\n  return BVar1;\n}\n\n\n----------------------------------------\nFunc
tion: UnhandledExceptionFilter\n\nLONG __stdcall UnhandledExceptionFilter(_EXCEPTION_POINTERS *ExceptionInfo)\n\n{\n  LONG LVar1;\n  \n                    /* WARNING: Could not recover
 jumptable at 0x00402ba0. Too many branches */\n                    /* WARNING: Treating indirect jump as call */\n  LVar1 = UnhandledExceptionFilter(ExceptionInfo);\n  return LVar1;\n
}\n\n\n----------------------------------------\nFunction: TlsGetValue\n\nLPVOID __stdcall TlsGetValue(DWORD dwTlsIndex)\n\n{\n  LPVOID pvVar1;\n  \n                    /* WARNING: Cou
ld not recover jumptable at 0x00402ba8. Too many branches */\n                    /* WARNING: Treating indirect jump as call */\n  pvVar1 = TlsGetValue(dwTlsIndex);\n  return pvVar1;\n}\n\n\n----------------------------------------\nFunction: TerminateProcess\n\nBOOL __stdcall TerminateProcess(HANDLE hProcess,UINT uExitCode)\n\n{\n  BOOL BVar1;\n  \n
    /* WARNING: Could not recover jumptable at 0x00402bb0. Too many branches */\n                    /* WARNING: Treating indirect jump as call */\n  BVar1 = TerminateProcess(hProcess,
uExitCode);\n  return BVar1;\n}\n\n\n----------------------------------------\nFunction: Sleep\n\nvoid __stdcall Sleep(DWORD dwMilliseconds)\n\n{\n                    /* WARNING: Could
 not recover jumptable at 0x00402bb8. Too many branches */\n                    /* WARNING: Treating indirect jump as call */\n  Sleep(dwMilliseconds);\n  return;\n}\n\n\n-------------
---------------------------\nFunction: SetUnhandledExceptionFilter\n\nLPTOP_LEVEL_EXCEPTION_FILTER __stdcall\nSetUnhandledExceptionFilter(LPTOP_LEVEL_EXCEPTION_FILTER lpTopLevelExcepti
onFilter)\n\n{\n  LPTOP_LEVEL_EXCEPTION_FILTER pPVar1;\n  \n                    /* WARNING: Could not recover jumptable at 0x00402bc0. Too many branches */\n                    /* WARN
ING: Treating indirect jump as call */\n  pPVar1 = SetUnhandledExceptionFilter(lpTopLevelExceptionFilter);\n  return pPVar1;\n}\n\n\n----------------------------------------\nFunction:
 RtlVirtualUnwind\n\nPEXCEPTION_ROUTINE __stdcall\nRtlVirtualUnwind(DWORD HandlerType,DWORD64 ImageBase,DWORD64 ControlPc,\n                PRUNTIME_FUNCTION FunctionEntry,PCONTEXT Con
textRecord,PVOID *HandlerData,\n                PDWORD64 EstablisherFrame,PKNONVOLATILE_CONTEXT_POINTERS ContextPointers)\n\n{\n  PEXCEPTION_ROUTINE puVar1;\n  \n                    /*
 WARNING: Could not recover jumptable at 0x00402bc8. Too many branches */\n                    /* WARNING: Treating indirect jump as call */\n  puVar1 = RtlVirtualUnwind(HandlerType,Im
ageBase,ControlPc,FunctionEntry,ContextRecord,HandlerData,\n                            EstablisherFrame,ContextPointers);\n  return puVar1;\n}\n\n\n-----------------------------------
-----\nFunction: RtlLookupFunctionEntry\n\nPRUNTIME_FUNCTION __stdcall\nRtlLookupFunctionEntry(DWORD64 ControlPc,PDWORD64 ImageBase,PUNWIND_HISTORY_TABLE HistoryTable)\n\n{\n  PRUNTIME
_FUNCTION p_Var1;\n  \n                    /* WARNING: Could not recover jumptable at 0x00402bd0. Too many branches */\n                    /* WARNING: Treating indirect jump as call *
/\n  p_Var1 = RtlLookupFunctionEntry(ControlPc,ImageBase,HistoryTable);\n  return p_Var1;\n}\n\n\n----------------------------------------\nFunction: RtlAddFunctionTable\n\nBOOLEAN __c
decl\nRtlAddFunctionTable(PRUNTIME_FUNCTION FunctionTable,DWORD EntryCount,DWORD64 BaseAddress)\n\n{\n  BOOLEAN BVar1;\n  \n                    /* WARNING: Could not recover jumptable
at 0x00402be0. Too many branches */\n                    /* WARNING: Treating indirect jump as call */\n  BVar1 = RtlAddFunctionTable(FunctionTable,EntryCount,BaseAddress);\n  return B
Var1;\n}\n\n\n----------------------------------------\nFunction: QueryPerformanceCounter\n\nBOOL __stdcall QueryPerformanceCounter(LARGE_INTEGER *lpPerformanceCount)\n\n{\n  BOOL BVar
1;\n  \n                    /* WARNING: Could not recover jumptable at 0x00402be8. Too many branches */\n                    /* WARNING: Treating indirect jump as call */\n  BVar1 = Qu
eryPerformanceCounter(lpPerformanceCount);\n  return BVar1;\n}\n\n\n----------------------------------------\nFunction: LeaveCriticalSection\n\nvoid __stdcall LeaveCriticalSection(LPCR
ITICAL_SECTION lpCriticalSection)\n\n{\n                    /* WARNING: Could not recover jumptable at 0x00402bf0. Too many branches */\n                    /* WARNING: Treating indire
ct jump as call */\n  LeaveCriticalSection(lpCriticalSection);\n  return;\n}\n\n\n----------------------------------------\nFunction: InitializeCriticalSection\n\nvoid __stdcall Initia
lizeCriticalSection(LPCRITICAL_SECTION lpCriticalSection)\n\n{\n                    /* WARNING: Could not recover jumptable at 0x00402bf8. Too many branches */\n                    /*
WARNING: Treating indirect jump as call */\n  InitializeCriticalSection(lpCriticalSection);\n  return;\n}\n\n\n----------------------------------------\nFunction: GetTickCount\n\nDWORD
 __stdcall GetTickCount(void)\n\n{\n  DWORD DVar1;\n  \n                    /* WARNING: Could not recover jumptable at 0x00402c00. Too many branches */\n                    /* WARNING:
 Treating indirect jump as call */\n  DVar1 = GetTickCount();\n  return DVar1;\n}\n\n\n----------------------------------------\nFunction: GetSystemTimeAsFileTime\n\nvoid __stdcall Get
SystemTimeAsFileTime(LPFILETIME lpSystemTimeAsFileTime)\n\n{\n                    /* WARNING: Could not recover jumptable at 0x00402c08. Too many branches */\n                    /* WA
RNING: Treating indirect jump as call */\n  GetSystemTimeAsFileTime(lpSystemTimeAsFileTime);\n  return;\n}\n\n\n----------------------------------------\nFunction: GetStartupInfoA\n\nv
oid __stdcall GetStartupInfoA(LPSTARTUPINFOA lpStartupInfo)\n\n{\n                    /* WARNING: Could not recover jumptable at 0x00402c10. Too many branches */\n                    /
* WARNING: Treating indirect jump as call */\n  GetStartupInfoA(lpStartupInfo);\n  return;\n}\n\n\n----------------------------------------\nFunction: GetLastError\n\nDWORD __stdcall G
etLastError(void)\n\n{\n  DWORD DVar1;\n  \n                    /* WARNING: Could not recover jumptable at 0x00402c18. Too many branches */\n                    /* WARNING: Treating in
direct jump as call */\n  DVar1 = GetLastError();\n  return DVar1;\n}\n\n\n----------------------------------------\nFunction: GetCurrentThreadId\n\nDWORD __stdcall GetCurrentThreadId(
void)\n\n{\n  DWORD DVar1;\n  \n                    /* WARNING: Could not recover jumptable at 0x00402c20. Too many branches */\n                    /* WARNING: Treating indirect jump
as call */\n  DVar1 = GetCurrentThreadId();\n  return DVar1;\n}\n\n\n----------------------------------------\nFunction: GetCurrentProcessId\n\nDWORD __stdcall GetCurrentProcessId(void
)\n\n{\n  DWORD DVar1;\n  \n                    /* WARNING: Could not recover jumptable at 0x00402c28. Too many branches */\n                    /* WARNING: Treating indirect jump as c
all */\n  DVar1 = GetCurrentProcessId();\n  return DVar1;\n}\n\n\n----------------------------------------\nFunction: GetCurrentProcess\n\nHANDLE __stdcall GetCurrentProcess(void)\n\n{
\n  HANDLE pvVar1;\n  \n                    /* WARNING: Could not recover jumptable at 0x00402c30. Too many branches */\n                    /* WARNING: Treating indirect jump as call
*/\n  pvVar1 = GetCurrentProcess();\n  return pvVar1;\n}\n\n\n----------------------------------------\nFunction: EnterCriticalSection\n\nvoid __stdcall EnterCriticalSection(LPCRITICAL
_SECTION lpCriticalSection)\n\n{\n                    /* WARNING: Could not recover jumptable at 0x00402c38. Too many branches */\n                    /* WARNING: Treating indirect jum
p as call */\n  EnterCriticalSection(lpCriticalSection);\n  return;\n}\n\n\n----------------------------------------\nFunction: DeleteCriticalSection\n\nvoid __stdcall DeleteCriticalSe
ction(LPCRITICAL_SECTION lpCriticalSection)\n\n{\n                    /* WARNING: Could not recover jumptable at 0x00402c40. Too many branches */\n                    /* WARNING: Treat
ing indirect jump as call */\n  DeleteCriticalSection(lpCriticalSection);\n  return;\n}\n\n\n----------------------------------------\nFunction: .text.unlikely\n\nvoid _text_unlikely(c
har *param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)\n\n{\n  FILE *pFVar1;\n  undefined8 local_res10;\n  undefined8 local_res18;\n  undefined8 local_res20;\n  \n  loc
al_res10 = param_2;\n  local_res18 = param_3;\n  local_res20 = param_4;\n  pFVar1 = __acrt_iob_func(2);\n  fwrite(\"Mingw-w64 runtime failure:\\n\",1,0x1b,pFVar1);\n  pFVar1 = __acrt_i
ob_func(2);\n  vfprintf(pFVar1,param_1,(va_list)&local_res10);\n                    /* WARNING: Subroutine does not return */\n  abort();\n}\n\n\n----------------------------------------\n"}

'''

message1 = '''
返回返回返回啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊
啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊
啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊
啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊
啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊
啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊
啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊。。。
'''

# ② 接收上传文件 → 返回两个字符串
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # 假设我们直接返回两个字符串作为测试
    return JSONResponse(content={
        # "message1": "文件已接收",
        "message1": message1,
        "message2": "前后端连接成功"
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
