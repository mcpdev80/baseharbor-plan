package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/mcpdev80/baseharbor/internal/application"
	"github.com/mcpdev80/baseharbor/internal/openbao"
)

// renderBrokerHealthcheck renders the broker compose and prints its healthcheck
// block. Run as: go run ./evidence/board-2026-11-02/broker-ready3/scripts/...
func main() {
	dir, err := os.MkdirTemp("", "broker-hc")
	if err != nil {
		panic(err)
	}
	defer os.RemoveAll(dir)
	write := func(name string) string {
		p := filepath.Join(dir, name)
		if err := os.WriteFile(p, []byte("test"), 0o644); err != nil {
			panic(err)
		}
		return p
	}
	m := application.New("demo", "dev", false, false, true)
	mtls := openbao.RuntimeMTLSFiles{
		CA:         write("ca.pem"),
		BrokerCert: write("broker-cert.pem"),
		BrokerKey:  write("broker-key.pem"),
		ClientCert: write("client-cert.pem"),
		ClientKey:  write("client-key.pem"),
	}
	got, err := composeYAML(
		m,
		mtls,
		write("runtime-token"),
		write("openbao.env"),
		write("openbao-ca.pem"),
		write("permissions.json"),
		write("service-tokens.json"),
		"baseharbor-runtime:test",
		"",
		nil,
	)
	if err != nil {
		panic(err)
	}
	idx := strings.Index(got, "healthcheck:")
	end := strings.Index(got[idx:], "\n    ")
	block := strings.TrimSpace(got[idx : idx+end])
	fmt.Println("=== rendered broker healthcheck block ===")
	fmt.Println(block)
}
