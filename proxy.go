package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
)

var Host = "usth.edu.vn/"

func root(w http.ResponseWriter, req *http.Request) {
	path := strings.TrimPrefix(req.URL.Path, "/")
	url := Host + path
	resp, err := http.Get("https://" + url)
	mimeType := resp.Header.Get("Content-Type")
	fmt.Println(resp.Status)
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		panic(err)
	}
	w.Header().Set("Content-Type", mimeType)
	fmt.Fprintf(w, string(body))
}

func main() {
	http.HandleFunc("/", root)

	http.ListenAndServe(":8090", nil)
}
