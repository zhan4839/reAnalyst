COMMON_SYMBOLS = [
  "mov", "push", "pop", "lea", "xchg", "sub", "inc", "dec", "mul", "div", "imul", "idiv", "neg", "adc", "sbb",
    "xor", "not", "shl", "sal", "shr", "ror", "rol", "jmp", "je", "jz", "jne", "jnz", "jg", "jnle", "jl",
    "jnge", "jge", "jnl", "jle", "jng", "jb", "jnae", "jc", "ja", "jnbe", "jo", "jno", "js", "jns", "call", "ret", "cmp",
    "test", "movs", "cmps", "scas", "lods", "stos", "nop", "int", "iret", "iretd", "clc", "cld", "cli", "stc", "std", "sti",
    "hlt", "rdmsr", "wrmsr", "cpuid", "rdtsc", "fadd", "fsub", "fmul", "fdiv", "fcom", "fst", "fld",

    # ARM
    "ldr", "str", "bl", "bx", "stm", "ldm", "push", "pop", "sub", "rsb", "mul", "mla", "umull", "smull", "orr",
    "eor", "bic", "lsl", "lsr", "asr", "ror", "rrx", "tst", "teq", "cmp", "cmn", "mov", "mvn", "sbc", "adc", "rsc", 
    "bne", "beq", "bge", "blt", "bgt", "ble", "bpl", "bmi", "bvs", "bvc", "bcs", "bcc", "bal", "swi", "mcr", "mrc", "ldr",
    "strb", "ldrb", "strh", "ldrh", "ldm", "stm", "swp",

    # MIPS
    "addu", "sub", "subu", "mult", "multu", "div", "divu", "mfhi", "mflo", "lis", "li", "lw", "sw", "slt", "slti",
    "beq", "bne", "jal", "jr", "syscall", "nop", "move", "sll", "srl", "sra", "andi", "ori", "xor",
    "xori", "nor", "lui", "lbu", "lh", "lhu",

    # Other common instructions across various architectures
    "ret", "mov", "cmp", "bne", "beq", "blt", "bgt", "ble", "bge", "jmp", "call", "push", "pop", "nop",
    "halt", "andi", "ori", "xori", "sll", "srl", "sra", "addi", "subi", "neg", "not", "mul", "div", "mod", "abs", "lsl",
    "lsr", "asr", "rol", "ror", "rlc", "rrc", "jz", "jnz", "jgz", "jlz", "jgez", "jlez", "ja", "jae", "jb", "jbe",
    "jna", "jnae", "jnb", "jnbe", "jc", "jnc", "jo", "jno", "js", "jns", "jp", "jnp", "jpe", "jpo", "jcxz", "jecxz",
    "jrcxz", "loop", "loope", "loopne", "loopnz", "loopz", "rep", "repe", "repne", "repnz", "repz", "enter", "leave"
]

# Define the segments
SEGMENTS = [
   '.load', 'bss', 'rodata', 'data', 'idata', 'rdata', 'pdata', 'textbss', 'eh_frame', 'got', 'plt',
                    '.debug', 'debug_info', 'comment', 'stab', 'stabstr', 'init', 'fini', 'data.rel', 'text.rel',"middle_state","check_status","up",'abs'
]
