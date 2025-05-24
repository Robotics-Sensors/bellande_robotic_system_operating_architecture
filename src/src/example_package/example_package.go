package main

import (
    "fmt"
    "time"
    "common_msgs"
)

type Example_package struct{}

func (n *Example_package) Run() {
    for {
        // TODO: Implement node logic
        fmt.Println("Running example_package")
        time.Sleep(1 * time.Second)
    }
}

func main() {
    node := &Example_package{}
    node.Run()
}
