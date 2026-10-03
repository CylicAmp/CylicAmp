#include "kev_integrator/fetcher.hpp"
#include <curl/curl.h>
#include <nlohmann/json.hpp>

namespace kev {

static size_t write_callback(void* contents, size_t size, size_t nmemb, std::string* userp) {
    userp->append((char*)contents, size * nmemb);
    return size * nmemb;
}

std::optional<nlohmann::json> fetch_json(const std::string& url, CircuitBreaker& cb, const std::string& source) {
    if (cb.is_open(source)) return std::nullopt;

    CURL* curl = curl_easy_init();
    if (!curl) return std::nullopt;

    std::string read_buffer;
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &read_buffer);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 15L);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

    CURLcode res = curl_easy_perform(curl);
    long http_code = 0;
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &http_code);
    curl_easy_cleanup(curl);

    if (res != CURLE_OK || http_code != 200) {
        cb.record_failure(source);
        return std::nullopt;
    }

    cb.record_success(source);
    try {
        return nlohmann::json::parse(read_buffer);
    } catch (...) {
        return std::nullopt;
    }
}

std::pair<std::vector<KEVEntry>, nlohmann::json> fetch_catalog() {
    CircuitBreaker cb;

    // Try CISA JSON
    auto data = fetch_json(
        "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
        cb, "cisa_json");
    if (data) {
        std::vector<KEVEntry> entries;
        for (const auto& raw : (*data)["vulnerabilities"]) {
            entries.push_back(KEVEntry::from_raw(raw));
        }
        nlohmann::json meta = {
            {"source", "cisa_json"},
            {"fetched_at", std::chrono::system_clock::now().time_since_epoch().count()},
        };
        return {entries, meta};
    }

    // Try GitHub mirror
    data = fetch_json(
        "https://raw.githubusercontent.com/cisagov/kev-data/main/known_exploited_vulnerabilities.json",
        cb, "github_mirror");
    if (data) {
        std::vector<KEVEntry> entries;
        for (const auto& raw : (*data)["vulnerabilities"]) {
            entries.push_back(KEVEntry::from_raw(raw));
        }
        nlohmann::json meta = {
            {"source", "github_mirror"},
            {"fetched_at", std::chrono::system_clock::now().time_since_epoch().count()},
        };
        return {entries, meta};
    }

    // Try CISA CSV as last resort
    data = fetch_json(
        "https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv",
        cb, "cisa_csv");
    if (data) {
        std::vector<KEVEntry> entries;
        for (const auto& raw : (*data)["vulnerabilities"]) {
            entries.push_back(KEVEntry::from_raw(raw));
        }
        nlohmann::json meta = {{"source", "cisa_csv"}};
        return {entries, meta};
    }

    throw std::runtime_error("All KEV sources unavailable");
}

} // namespace kev
