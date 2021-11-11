class changeMath():
    def __init__(self) -> None:
        self.useMath = False

useMath = changeMath()

nativeFunctions : str = '''func print_true(){ 
    fmt.Printf("%c",84);
    fmt.Printf("%c",114);
    fmt.Printf("%c",117);
    fmt.Printf("%c",101);
    //fmt.Printf("%c",10);
}\n

func print_false(){   
    fmt.Printf("%c",70);
    fmt.Printf("%c",97);
    fmt.Printf("%c",108);
    fmt.Printf("%c",115);
    fmt.Printf("%c",101);
    //fmt.Printf("%c",10);
}\n\n\n
'''