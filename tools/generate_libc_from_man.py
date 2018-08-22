from urllib.request import urlopen
import html2text

resp= urlopen("https://www.gnu.org/software/libc/manual/html_mono/libc.html")
with open("libc.json","w") as wf:
    result="{"
    for line in resp:
        content = line.decode("utf8")
        if "Function: " in content:
            data=html2text.html2text(content).replace("\r\n"," ").replace("\n"," ").replace("\r"," ")
            function=data[data.find("_ **")+4:data.find("** _(")]
            args=data[data.find(" _(")+3:data.find(")_")].split(", ")
            arguments=""
            for arg in args:
                if len(arg)==1:
                    continue
                if arg=="void":
                    continue
                arguments+="\""+arg+"\", "
            arguments=arguments[:-2]
            
            if (len(arguments)!=0):
                result+=(f"\"{function}\" : [{arguments}],")
    result=result[:-1]+"}"
    wf.write(result)
    print("Done !")
resp.close()

