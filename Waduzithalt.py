import sys
# Because Waduzitdo is Turing incomplete, we can make a program in a Turing complete language that determines
# whether or not a Waduzitdo program halts. This type of analysis cannot be performed on Turing complete
# languages.

def calculate(line, source, flag, accepted, match):
    # Fell off
    if line >= len(source):
        return True

    s_line = source[line]

    # Ignore the asterisk
    if s_line.startswith("*"):
        s_line = s_line[1:]

    # Remove the flag from the line, allowing it to run OR blocking it from running
    if s_line.startswith(flag):
        s_line = s_line[1:]
    
    # Loop happens, this branch at least doesn't halt
    if s_line.startswith("J:0"):
        return False

    # Program stops
    if s_line.startswith("S"):
        return True
    
    # Make sure we know an A happened
    if s_line.startswith("A"):
        accepted = True
        match = None

    # Jump to the provided line
    if s_line.startswith("J:"):
        jmp_amount = int(s_line[2:])
        next_line = line
        while jmp_amount > 0:
            next_line += 1
            if source[next_line].startswith("*"):
                jmp_amount -= 1
        return calculate(next_line, source, flag, accepted, match)
    
    # Match happens: create two branches to calculate both Y and N.
    if s_line.startswith("M:"):
        if accepted:
            if match == s_line[2:]:
                return calculate(line + 1, source, flag, accepted, s_line[2:])
            elif match is not None:
                return calculate(line + 1, source, "N" if flag == "Y" else "Y", accepted, s_line[2:])
            else:
                return calculate(line + 1, source, "Y", accepted, s_line[2:]) or calculate(line + 1, source, "N", accepted, s_line[2:])
        else:
            calculate(line + 1, source, "N", accepted, match, None)

    # If we make it here, we probably skipped this line or it's a T line.
    return calculate(line + 1, source, flag, accepted, match)
    
def main():
    if len(sys.argv)>1:
        try:
            f=open(sys.argv[1])
            source = f.read()
            if calculate(0, source.split("\n"), "N", False, None):
                print("This halts!")
            else:
                print("This doesn't halt!")
        except Exception as e:
            print(e)
            print("Error reading file. File is not presend and/or corrupt.")

if __name__ == "__main__":
    main()