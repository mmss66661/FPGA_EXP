import re,subprocess,sys
tops=["exp5_t1_7474","exp5_t2_74112","exp5_t4_jk2d","exp5_t4_jk2t","keyin","exp5_top"]
base=open("exp5.qsf",encoding="utf-8").read()
for t in tops:
    s=re.sub(r"set_global_assignment -name TOP_LEVEL_ENTITY \S+","set_global_assignment -name TOP_LEVEL_ENTITY %s"%t,base)
    open("exp5.qsf","w",encoding="utf-8",newline="\r\n").write(s)
    r=subprocess.run([r"D:\quartus\quartus\bin64\quartus_map.exe","--read_settings_files=on","--write_settings_files=off","exp5","-c","exp5"],capture_output=True,text=True)
    msgs=[l.strip()[:100] for l in r.stdout.splitlines() if "was successful" in l or "Error (" in l]
    print(t,"->"," | ".join(msgs))
open("exp5.qsf","w",encoding="utf-8",newline="\r\n").write(base)
