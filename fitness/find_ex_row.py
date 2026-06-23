with open(r"c:\Users\Dev\Desktop\FITNESS\env\fitness\account\templates\account\admin_dashboard.html", 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('muscle_group')
if idx != -1:
    snippet = content[max(0,idx-400):idx+400]
    with open('ex_row_dump.txt', 'w', encoding='utf-8') as out:
        out.write(snippet)
    print("Dumped to ex_row_dump.txt")
else:
    print("Not found")
