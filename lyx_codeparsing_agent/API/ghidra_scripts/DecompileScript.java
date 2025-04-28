import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import ghidra.program.model.address.*;
import ghidra.app.decompiler.*;
import java.io.*;
import java.util.HashSet;
import java.util.Set;
import java.util.Arrays;

public class DecompileScript extends GhidraScript {
    // 绝大多数外部库函数都跳过……
//    private static final Set<String> SKIP_LIBRARIES = new HashSet<>(Arrays.asList(
//        "kernel32", "user32", "gdi32", "advapi32", "ntdll", "ws2_32", "ole32", "shell32"    
//    ));

    // 但对这些"可能含漏洞"的函数，强制保留
    private static final Set<String> EXTERNAL_WHITELIST = new HashSet<>(Arrays.asList(
        "strcpy", "strncpy", "strcat", "memcmp", "memcpy", "memmove",
        "strlen", "strcmp", "strncmp", "sprintf", "vsprintf" 
        // 根据需要继续添加……
    ));

    private boolean isSkipFunction(Function func) {
        String name = func.getName();
        // 1. 编译器／运行时自动生成的函数
        if (name.startsWith("_") || name.startsWith("__")
            || name.contains("$") || name.contains("?") || name.contains("@")) {
            return true;
        }
        // 2. 外部导入函数
        if (func.isExternal()) {
            // 白名单放行
            if (EXTERNAL_WHITELIST.contains(name)) {
                return false;
            }
            // 其余一律跳过
            return true;
        }
        // 3. 剩下的都是应用程序自己实现的函数，保留
        return false;
    }

    @Override
    public void run() throws Exception {
        println("开始反编译（仅保留用户代码 + 白名单外部函数）…");

        PrintWriter writer = new PrintWriter(new FileWriter("decompiled_output.txt"));
        DecompInterface decomp = new DecompInterface();
        decomp.openProgram(currentProgram);

        for (Function func : currentProgram.getFunctionManager().getFunctions(true)) {
            if (isSkipFunction(func)) {
                println("跳过: " + func.getName());
                continue;
            }
            println("反编译: " + func.getName());
            DecompileResults res = decomp.decompileFunction(func, 60, monitor);
            if (res.decompileCompleted()) {
                writer.println("Function: " + func.getName());
                writer.println(res.getDecompiledFunction().getC());
                writer.println("----------------------------------------");
            } else {
                println("反编译失败: " + func.getName());
            }
        }

        writer.close();
        decomp.dispose();
        println("完成，输出保存在 decompiled_output.txt");
    }
}
