package main

import (
	"context"
	"io"
	"net"
	"net/http"
	"os"
	"path/filepath"
	"strings"

	"github.com/google/go-github/v45/github"
	"github.com/oschwald/geoip2-golang"
	"github.com/oschwald/maxminddb-golang"
	"github.com/sagernet/sing-box/common/srs"
	C "github.com/sagernet/sing-box/constant"
	"github.com/sagernet/sing-box/log"
	"github.com/sagernet/sing-box/option"
	"github.com/sagernet/sing/common"
	E "github.com/sagernet/sing/common/exceptions"
)

var githubClient *github.Client

func init() {
	accessToken, loaded := os.LookupEnv("ACCESS_TOKEN")
	if !loaded {
		githubClient = github.NewClient(nil)
		return
	}
	transport := &github.BasicAuthTransport{
		Username: accessToken,
	}
	githubClient = github.NewClient(transport.Client())
}

func fetch(from string) (*github.RepositoryRelease, error) {
	fixedRelease := os.Getenv("FIXED_RELEASE")
	names := strings.SplitN(from, "/", 2)
	if fixedRelease != "" {
		latestRelease, _, err := githubClient.Repositories.GetReleaseByTag(context.Background(), names[0], names[1], fixedRelease)
		if err != nil {
			return nil, err
		}
		return latestRelease, err
	} else {
		latestRelease, _, err := githubClient.Repositories.GetLatestRelease(context.Background(), names[0], names[1])
		if err != nil {
			return nil, err
		}
		return latestRelease, err
	}
}

func get(downloadURL *string) ([]byte, error) {
	log.Info("download ", *downloadURL)
	response, err := http.Get(*downloadURL)
	if err != nil {
		return nil, err
	}
	defer response.Body.Close()
	return io.ReadAll(response.Body)
}

func download(release *github.RepositoryRelease) ([]byte, error) {
	geoipAsset := common.Find(release.Assets, func(it *github.ReleaseAsset) bool {
		return *it.Name == "Country.mmdb"
	})
	if geoipAsset == nil {
		return nil, E.New("Country.mmdb not found in upstream release ", release.Name)
	}
	return get(geoipAsset.BrowserDownloadURL)
}

func parse(binary []byte) (metadata maxminddb.Metadata, countryMap map[string][]*net.IPNet, err error) {
	database, err := maxminddb.FromBytes(binary)
	if err != nil {
		return
	}
	metadata = database.Metadata
	networks := database.Networks(maxminddb.SkipAliasedNetworks)
	countryMap = make(map[string][]*net.IPNet)
	var country geoip2.Enterprise
	var ipNet *net.IPNet
	for networks.Next() {
		ipNet, err = networks.Network(&country)
		if err != nil {
			return
		}
		// idk why
		code := strings.ToLower(country.RegisteredCountry.IsoCode)
		countryMap[code] = append(countryMap[code], ipNet)
	}
	err = networks.Err()
	return
}

func generateRuleSets(source string, ruleSetOutput string) error {
	sourceRelease, err := fetch(source)
	if err != nil {
		return err
	}
	
	// 检查是否已经是最新版本
	destinationRelease, err := fetch("proother/rule_singbox_mihomo")
	if err != nil {
		log.Warn("missing destination latest release")
	} else {
		if os.Getenv("NO_SKIP") != "true" && strings.Contains(*destinationRelease.Name, *sourceRelease.Name) {
			log.Info("already latest")
			setActionOutput("skip", "true")
			return nil
		}
	}
	
	binary, err := download(sourceRelease)
	if err != nil {
		return err
	}
	
	_, countryMap, err := parse(binary)
	if err != nil {
		return err
	}
	
	// 创建输出目录
	os.RemoveAll(ruleSetOutput)
	err = os.MkdirAll(ruleSetOutput, 0o755)
	if err != nil {
		return err
	}
	
	// 生成每个国家的规则集文件
	for countryCode, ipNets := range countryMap {
		var headlessRule option.DefaultHeadlessRule
		headlessRule.IPCIDR = make([]string, 0, len(ipNets))
		for _, cidr := range ipNets {
			headlessRule.IPCIDR = append(headlessRule.IPCIDR, cidr.String())
		}
		var plainRuleSet option.PlainRuleSet
		plainRuleSet.Rules = []option.HeadlessRule{
			{
				Type:           C.RuleTypeDefault,
				DefaultOptions: headlessRule,
			},
		}
		srsPath, _ := filepath.Abs(filepath.Join(ruleSetOutput, "geoip-"+countryCode+".srs"))
		os.Stderr.WriteString("write " + srsPath + "\n")
		outputRuleSet, err := os.Create(srsPath)
		if err != nil {
			return err
		}
		err = srs.Write(outputRuleSet, plainRuleSet)
		if err != nil {
			outputRuleSet.Close()
			return err
		}
		outputRuleSet.Close()
	}
	
	setActionOutput("tag", *sourceRelease.Name)
	return nil
}

func setActionOutput(name string, content string) {
	os.Stdout.WriteString("::set-output name=" + name + "::" + content + "\n")
}

func main() {
	err := generateRuleSets("Dreamacro/maxmind-geoip", "release/sing-geoip")
	if err != nil {
		log.Fatal(err)
	}
} 