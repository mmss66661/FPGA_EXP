import re,sys,subprocess
top=sys.argv[1]
s=open("exp5.qsf",encoding="utf-8").read()
s=re.sub(r'set_global_assignment -name TOP_LEVEL_ENTITY \S+', 'set_global_assignment -name TOP_LEVEL_ENTITY %s'%top, s)
open("exp5.qsf","w",encoding="utf-8",newline="\r\n").write(s)
r=subprocess.run([r"D:\quartus\quartus\bin64\quartus_map.exe","--read_settings_files=on","--write_settings_files=off","exp5","-c","exp5"],capture_output=True,text=True)
for l in r.stdout.splitlines():
    if re.search(r"Error|was successful|unsuccessful", l): print(l.strip()[:160])
