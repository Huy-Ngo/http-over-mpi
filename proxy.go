package main

import (
    "fmt"
    "net/http"
    "io/ioutil"
    "strings"
)

var Host = "en.wikipedia.org/"

func root(w http.ResponseWriter, req *http.Request) {
    path := strings.TrimPrefix(req.URL.Path, "/")
    url := Host + path
    resp, err := http.Get("https://" + url)
    fmt.Print(resp.Status)
    defer resp.Body.Close()
    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        panic(err)
    }
    fmt.Fprintf(w, string(body))
}

func main() {
    http.HandleFunc("/", root)

    http.ListenAndServe(":8090", nil)
}
