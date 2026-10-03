#pragma once
#include <string>
#include <chrono>

namespace kev {

struct KEVEntry {
    std::string cve_id;
    std::string vendor;
    std::string product;
    std::string name;
    std::chrono::system_clock::time_point date_added;
    std::chrono::system_clock::time_point due_date;
    std::string required_action;
    bool known_ransomware;
    std::string notes;

    static KEVEntry from_raw(const nlohmann::json& raw);
    nlohmann::json to_json() const;
};

} // namespace kev
