with open(r'c:\Users\Dev\Desktop\PROJECT\env\fitness\core\static\core\css\index.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(len(lines)):
    line = lines[i].strip()
    if line.startswith('}'):
        continue
    if ':' in line and not line.endswith('{') and not line.startswith('.') and not line.startswith('#') and not line.startswith('@'):
        # Possible property line
        # Check if previous lines have a selector
        found_selector = False
        for k in range(i-1, i-5, -1):
            if k < 0: break
            prev_line = lines[k].strip()
            if prev_line.endswith('{'):
                found_selector = True
                break
            if prev_line.endswith('}'):
                break
        if not found_selector:
            print(f"Line {i+1}: Potential missing selector: {line}")
