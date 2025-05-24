package main

import (
    "fmt"
    "time"
    "common_msgs"
)

type Example_go struct{}

func (n *Example_go) Run() {
    for {
        // TODO: Implement node logic
        fmt.Println("Running example_go")
        time.Sleep(1 * time.Second)
    }
}

func main() {
    node := &Example_go{}
    node.Run()
}
