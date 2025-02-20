def brainfuck_interpreter(code):
    code = list(filter(lambda x: x in ('<', '>', '+', '-', '.', ',', '[', ']'), code))
    tape = [0] * 30000
    pointer = 0
    code_pointer = 0
    loop_stack = []

    while code_pointer < len(code):
        command = code[code_pointer]

        if command == '>':
            pointer += 1
        elif command == '<':
            pointer -= 1
        elif command == '+':
            tape[pointer] = (tape[pointer] + 1) % 256
        elif command == '-':
            tape[pointer] = (tape[pointer] - 1) % 256
        elif command == '.':
            print(chr(tape[pointer]), end='')
        elif command == ',':
            # For simplicity, we skip input handling
            pass
        elif command == '[':
            if tape[pointer] == 0:
                open_brackets = 1
                while open_brackets > 0:
                    code_pointer += 1
                    if code[code_pointer] == '[':
                        open_brackets += 1
                    elif code[code_pointer] == ']':
                        open_brackets -= 1
            else:
                loop_stack.append(code_pointer)
        elif command == ']':
            if tape[pointer] != 0:
                code_pointer = loop_stack[-1]
            else:
                loop_stack.pop()

        code_pointer += 1

# 你的 Brainfuck 代码
bf_code ="""
,>>++ +++++ +++[< +++++ +++++ >-]<+ +[<-> -]<[+ -],>> +++++ +++++
[<+++ +++++ ++>-] <++++ ++++[ <->-] <[+-] ,>>++ +++++ ++[<+ +++++
++++> -]<++ +++++ [<->- ]<[+- ],>>+ +++++ ++++[ <++++ +++++ +>-]<
+++[< ->-]< [+-], >>+++ +++++ ++++[ <++++ +++++ +>-]< +++[< ->-]<
[+-], >>+++ ++[<+ +++++ ++++> -]<++ ++++[ <->-] <[+-] ,>>++ +++++
++[<+ +++++ ++++> -]<++ +++++ ++[<- >-]<[ +-],> >++++ [<+++ +++++
++>-] <++++ +++++ [<->- ]<[+- ],>>+ ++++[ <++++ +++++ +>-]< [<->-
]<[+- ],>>+ +++++ +++[< +++++ +++++ >-]<+ +++++ ++[<- >-]<[ +-],>
>++++ +++++ [<+++ +++++ ++>-] <++++ ++++[ <->-] <[+-] ,>>++ +++[<
+++++ +++++ >-]<+ +++++ +[<-> -]<[+ -],>> +++++ [<+++ +++++ ++>-]
<++++ +[<-> -]<[+ -],>> ++++[ <++++ +++++ +>-]< +++++ [<->- ]<[+-
],>>+ ++++[ <++++ +++++ +>-]< +++[< ->-]< [+-], >>+++ +[<++ +++++
+++>- ]<+++ +++++ [<->- ]<[+- ],>>+ ++++[ <++++ +++++ +>-]< +++++
[<->- ]<[+- ],>>+ ++++[ <++++ +++++ +>-]< +++++ [<->- ]<[+- ],>>+
+++[< +++++ +++++ >-]<+ ++++[ <->-] <[+-] ,>>++ +++[< +++++ +++++
>-]<+ +[<-> -]<[+ -],>> +++++ [<+++ +++++ ++>-] <++[< ->-]< [+-],
>>+++ +++++ +[<++ +++++ +++>- ]<+++ ++++[ <->-] <[+-] ,>>++ +++[<
+++++ +++++ >-]<+ +[<-> -]<[+ -],>> ++++[ <++++ +++++ +>-]< +++++
[<->- ]<[+- ],>>+ +++++ +++[< +++++ +++++ >-]<+ +++++ +[<-> -]<[+
-],>> +++++ ++++[ <++++ +++++ +>-]< +++++ ++[<- >-]<[ +-],> >++++
+++++ +[<++ +++++ +++>- ]<++[ <->-] <[+-] ,>>++ +++++ ++[<+ +++++
++++> -]<++ +++++ ++[<- >-]<[ +-],> >++++ [<+++ +++++ ++>-] <++++
+[<-> -]<[+ -],>> +++++ [<+++ +++++ ++>-] <++++ [<->- ]<[+- ],>>+
+++++ ++++[ <++++ +++++ +>-]< +[<-> -]<[+ -],>> +++++ [<+++ +++++
++>-] <+[<- >-]<[ +-],> >++++ +[<++ +++++ +++>- ]<+++ ++++[ <->-]
<[+-] ,>>++ ++[<+ +++++ ++++> -]<++ +++++ ++[<- >-]<[ +-],> >++++
+++++ +[<++ +++++ +++>- ]<++[ <->-] <[+-] ,>>++ +++[< +++++ +++++
>-]<[ <->-] <[+-] ,>>++ ++[<+ +++++ ++++> -]<++ +++++ ++[<- >-]<[
+-],> >++++ +[<++ +++++ +++>- ]<+[< ->-]< [+-], >>+++ +[<++ +++++
+++>- ]<+++ +++++ [<->- ]<[+- ],>>+ ++++[ <++++ +++++ +>-]< ++[<-
>-]<[ +-],> >++++ [<+++ +++++ ++>-] <++++ +++++ [<->- ]<[+- ],>>+
+++++ +++++ +[<++ +++++ +++>- ]<+++ ++[<- >-]<[ +-]>> >>>++ +++++
++++[ <++++ +++++ +>-]< +.>>> >>+++ +++++ ++[<+ +++++ ++++> -]<++
+++++ .
"""

brainfuck_interpreter(bf_code)