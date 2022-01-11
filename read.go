package main

import ( "os"
        
         "io/ioutil"
	)

func main() {
    b:= ioutil.ReadFile("ok.go")
    str := string(b)

    file:= os.Create("file.txt")

    file.WriteString(str)
}