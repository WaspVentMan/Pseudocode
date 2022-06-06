import json
import time
import os

m = json.load(open("messages.json"))

code = open(input("Enter the name of a .ps file to run.\n>>> ")+".ps", "r").read().split("\n")
variables = {}; ln = 0; i = 0; ifDepth = 0; endIgnore = 0; elseHelper = False

def error(m, ew, id, ln, e1="", e2="", e3="", e4="", e5=""): print("[ERROR {}] Error on line {}, ".format(ew.upper()+str(id), str(ln)) + m[ew][id].format(e1, e2, e3, e4, e5))

while True:
    ln += 1

    if ln > len(code): break
    else: line = code[ln-1]

    for x in range(len(line)):
        if line[x] == " ": pass
        else: i = x; break

    if line[i:].startswith("end"):
        if endIgnore > 0: endIgnore -= 1; continue
        try: line = line[i:].split(" ", 1)[1]
        except: error(m, "e", 3, ln); break
        if ifDepth == 0: error(m, "w", 1, ln); continue
        if line in ["if", "elif"]: ifDepth -= 1; elseHelper = False
        else: error(m, "e", 4, ln, line); break

    elif line[i:].startswith("if"):
        line = line[i:].split(" ", 1)[1].replace("less than or equal to", "<=").replace("greater than or equal to", ">=").replace("less than", "<").replace("greater than", ">").replace("not equal to", "!=").replace("equal to", "==").replace(" is", "").split(" ")
        if line[0].startswith("\"") and line[0].endswith("\""): line[0] = line[0][1:-1]
        else:
            try: line[0] = int(line[0])
            except: line[0] = variables[line[0]]
        if line[2].startswith("\"") and line[2].endswith("\""): line[2] = line[2][1:-1]
        else:
            try: line[2] = int(line[2])
            except: line[2] = variables[line[2]]
        if type(line[0]) == type("WYSI") or type(line[2]) == type("WYSI"): # WYSI -When You See It-
            if line[1] in ["<=", ">=", "<", ">"]: error(m, "e", 5, ln); break
        if   line[1] == "<=" and line[0] <= line[2]: ifDepth += 1; elseHelper = True
        elif line[1] == ">=" and line[0] >= line[2]: ifDepth += 1; elseHelper = True
        elif line[1] == "<"  and line[0] <  line[2]: ifDepth += 1; elseHelper = True
        elif line[1] == ">"  and line[0] >  line[2]: ifDepth += 1; elseHelper = True
        elif line[1] == "!=" and line[0] != line[2]: ifDepth += 1; elseHelper = True
        elif line[1] == "==" and line[0] == line[2]: ifDepth += 1; elseHelper = True
        else: endIgnore += 1

    elif line[i:].startswith("elif"):
        if elseHelper: ifDepth -= 1; continue
        line = line[i:].split(" ", 1)[1].replace("less than or equal to", "<=").replace("greater than or equal to", ">=").replace("less than", "<").replace("greater than", ">").replace("not equal to", "!=").replace("equal to", "==").replace(" is", "").split(" ")
        if line[0].startswith("\"") and line[0].endswith("\""): line[0] = line[0][1:-1]
        else:
            try: line[0] = int(line[0])
            except: line[0] = variables[line[0]]
        if line[2].startswith("\"") and line[2].endswith("\""): line[2] = line[2][1:-1]
        else:
            try: line[2] = int(line[2])
            except: line[2] = variables[line[2]]
        if type(line[0]) == type("WYSI") or type(line[2]) == type("WYSI"): # WYSI -When You See It-
            if line[1] in ["<=", ">=", "<", ">"]: error(m, "e", 5, ln); break
        if   line[1] == "<=" and line[0] <= line[2]: ifDepth += 1; endIgnore -= 1; elseHelper = True
        elif line[1] == ">=" and line[0] >= line[2]: ifDepth += 1; endIgnore -= 1; elseHelper = True
        elif line[1] == "<"  and line[0] <  line[2]: ifDepth += 1; endIgnore -= 1; elseHelper = True
        elif line[1] == ">"  and line[0] >  line[2]: ifDepth += 1; endIgnore -= 1; elseHelper = True
        elif line[1] == "!=" and line[0] != line[2]: ifDepth += 1; endIgnore -= 1; elseHelper = True
        elif line[1] == "==" and line[0] == line[2]: ifDepth += 1; endIgnore -= 1; elseHelper = True
        else: endIgnore += 1

    elif line[i:].startswith("else"):
        if elseHelper: ifDepth -= 1; endIgnore += 1; continue
        else: ifDepth += 1; endIgnore -= 1; elseHelper = True

    elif endIgnore > 0: continue

    elif line[i:].startswith("print"):
        line = line[i:].split(" ", 1)[1].split(" and ")
        text = ""
        for item in line:
            if item.startswith("\"") and item.endswith("\""): text += str(item[1:-1])
            else:
                try: text += str(variables[item])
                except: error(m, "e", 1, ln, item); break
        print(text)

    elif line[i:].startswith("set"):
        line = line[i:].split(" ", 1)[1].split(" to ")
        if line[1].startswith("input"): variables[line[0]] = input(">>> ")
        elif line[1].startswith("\"") and line[1].endswith("\""): variables[line[0]] = str(line[1])
        else:
            try: variables[line[0]] = int(line[1])
            except:
                try: variables[line[0]] = variables[line[1]]
                except: error(m, "e", 2, ln, line[1]); break

    elif line[i:].startswith("change"):
        line = line[i:].split(" ", 1)[1].split(" by ")
        try: variables[line[0]] += int(line[1])
        except: error(m, "e", 2, ln, line[1]); break

    elif line[i:].startswith("wait"):
        line = line[i:].split(" ", 1)[1]
        try: time.sleep(int(line))
        except: error(m, "e", 6, ln); break