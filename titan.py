import re
import random
import os
import sys

class IIOIOOIIO:
    def __init__(self):
        self.alphabet = ['l', 'I', 'i', '1', '_', 'O', '0']
        self.junk_templates = self.IOIOIIO()
        
    def IOIOIIO(self):
        return [
            "private static double {id}(double a) {{ return (Math.sin(a) * Math.PI) / {rand}; }}",
            "private static long {id}(long b) {{ return b ^ {rand}L; }}",
            "static class {id} {{ public String data = \"{rand_str}\"; }}",
            "private static int[] {id}() {{ return new int[]{{ {nums} }}; }}",
            "private static void {id}(Object o) {{ if(o == null) return; synchronized(o) {{ o.notify(); }} }}"
        ]

    def OIOIOO(self, length=18):
        return 'l' + ''.join(random.choice(self.alphabet) for _ in range(length))

class OOIIOIO:
    def __init__(self, decoder_name, pool_name):
        self.decoder_name = decoder_name
        self.pool_name = pool_name
        self.string_pool = []

    def IOIO(self, text):
        key = random.randint(128, 1024)
        offset = random.randint(40, 200)
        encoded = [(((ord(c) ^ key) + offset) << 3) ^ 0xAF for c in text]
        idx = len(self.string_pool)
        self.string_pool.append({'data': encoded, 'key': key, 'off': offset})
        return f"{self.decoder_name}({idx}, {random.randint(1000, 9999)})"

    def IIOIO(self):
        pool_init = "{\n"
        for entry in self.string_pool:
            pool_init += f"        new int[]{{{','.join(map(str, entry['data']))}}},\n"
        
        return f"""
    private static final int[][] {self.pool_name}_d = {pool_init} }};
    private static String {self.decoder_name}(int idx, int salt) {{
        try {{
            int[] d = {self.pool_name}_d[idx];
            int k = 0, o = 0;
            switch(idx) {{
                {self.OIOI()}
            }}
            char[] r = new char[d.length];
            for(int i=0; i<d.length; i++) {{
                int v = (d[i] ^ 0xAF) >> 3;
                r[i] = (char)((v - o) ^ k);
            }}
            return new String(r);
        }} catch (Exception e) {{ return ""; }}
    }}"""

    def OIOI(self):
        return "\n".join([f"case {i}: k={e['key']}; o={e['off']}; break;" for i, e in enumerate(self.string_pool)])

class IOIOIOIOI:
    def __init__(self, source_code):
        self.source = source_code
        self.engine = IIOIOOIIO()
        self.main_class = self.engine.OIOIOO(14)
        self.poly = OOIIOIO(self.engine.OIOIOO(20), self.engine.OIOIOO(10))
        self.methods_map = {}

    def OIOOII(self, code):
        found_methods = re.findall(r'static\s+\w+\s+(\w+)\s*\(', code)
        for m_name in found_methods:
            if m_name not in ['main', self.poly.decoder_name]:
                if m_name not in self.methods_map:
                    self.methods_map[m_name] = self.engine.OIOIOO(20)
                code = re.sub(r'\b' + m_name + r'\b', self.methods_map[m_name], code)
        return code

    def IIIIOOO(self, code):
        def wrap(match):
            val = match.group(1)
            s_sys, s_out, s_prn = self.poly.IOIO("java.lang.System"), self.poly.IOIO("out"), self.poly.IOIO("println")
            return (f"((java.util.function.Consumer<Object>)(x) -> {{ "
                    f"try {{ java.lang.reflect.Method m = java.lang.Class.forName({s_sys}).getField({s_out}).get(null).getClass().getMethod({s_prn}, String.class); "
                    f"m.invoke(java.lang.Class.forName({s_sys}).getField({s_out}).get(null), String.valueOf(x)); "
                    f"}} catch(Exception e) {{}} }}).accept({val});")
        return re.sub(r'System\.out\.println\((.*?)\);', wrap, code)

    def OOOOII(self, code):
        def repl(m):
            n = int(m.group(1))
            k = random.randint(100, 999)
            return f"(({n ^ k} ^ {k}) + {k} - {k} + (0 & {random.randint(1,50)}))"
        return re.sub(r'\b(\d+)\b', repl, code)

    def IIOII(self, count=400):
        lines = []
        for _ in range(count):
            lines.append("    " + random.choice(self.engine.junk_templates).format(
                id=self.engine.OIOIOO(), rand=random.randint(10, 999),
                rand_str=self.engine.OIOIOO(5), nums="1,2,3"))
        return "\n".join(lines)

    def build(self):
        class_match = re.search(r'public\s+class\s+(\w+)', self.source)
        if not class_match: return None
        
        working_code = self.source.replace(class_match.group(1), self.main_class)
        working_code = self.OIOOII(working_code)
        working_code = self.IIIIOOO(working_code)
        working_code = re.sub(r'(?<!\.getMethod\()(?<!\.getField\()"(.*?)"', 
                              lambda m: self.poly.IOIO(m.group(1)), working_code)
        working_code = self.OOOOII(working_code)
        
        last_idx = working_code.rfind('}')
        final = (
            working_code[:last_idx] +
            self.poly.IIOIO() +
            self.IIOII() +
            "\n}"
        )
        return final

def main():
    print("TITAN OBFUSCATOR v 0.0.1 Release")
    if len(sys.argv) < 2: 
        print("Usage: python titan.py <file.java>")
        return
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        src = f.read()
    obf = IOIOIOIOI(src)
    res = obf.build()
    if res:
        output_file = f"{obf.main_class}.java"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(res)
        print(f"[*] Obfuscated: {output_file}")

if __name__ == "__main__":
    main()
