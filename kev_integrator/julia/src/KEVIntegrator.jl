module KEVIntegrator

using Dates
using HTTP
using JSON3
using SQLite

export KEVEntry, get_kev_catalog, get_kev_cve_ids, get_new_entries

const CISA_JSON_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
const CISA_CSV_URL = "https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv"
const GITHUB_MIRROR = "https://raw.githubusercontent.com/cisagov/kev-data/main/known_exploited_vulnerabilities.json"

struct KEVEntry
    cve_id::String
    vendor::String
    product::String
    name::String
    date_added::DateTime
    due_date::DateTime
    required_action::String
    known_ransomware::Bool
    notes::String
end

function parse_cisa_date(s::String)::DateTime
    formats = ["yyyy-mm-dd", "mm/dd/yyyy", "dd-u-yyyy"]
    for fmt in formats
        try
            return DateTime(s, fmt)
        catch
            continue
        end
    end
    error("Unable to parse CISA date: $s")
end

function KEVEntry(raw::Dict)
    KEVEntry(
        uppercase(strip(raw["cveID"])),
        get(raw, "vendorProject", ""),
        get(raw, "product", ""),
        get(raw, "vulnerabilityName", ""),
        parse_cisa_date(raw["dateAdded"]),
        parse_cisa_date(raw["dueDate"]),
        get(raw, "requiredAction", ""),
        lowercase(get(raw, "knownRansomwareCampaignUse", "")) == "known",
        get(raw, "notes", ""),
    )
end

# Circuit breaker
mutable struct CircuitBreaker
    failures::Dict{String, Int}
    last_failure::Dict{String, DateTime}
    threshold::Int
    cooldown::Minute
end

CircuitBreaker() = CircuitBreaker(Dict(), Dict(), 3, Minute(60))

function is_open(cb::CircuitBreaker, source::String)::Bool
    get(cb.failures, source, 0) < cb.threshold && return false
    last = get(cb.last_failure, source, now() - Day(1))
    return now() - last < cb.cooldown
end

const CB = CircuitBreaker()

function fetch_catalog()::Tuple{Vector{KEVEntry}, Dict}
    # Try CISA JSON
    if !is_open(CB, "cisa_json")
        try
            resp = HTTP.get(CISA_JSON_URL; timeout=15)
            data = JSON3.read(resp.body)
            CB.failures["cisa_json"] = 0
            entries = [KEVEntry(d) for d in data.vulnerabilities]
            meta = Dict("source" => "cisa_json", "fetched_at" => string(now()))
            return (entries, meta)
        catch e
            CB.failures["cisa_json"] = get(CB.failures, "cisa_json", 0) + 1
            CB.last_failure["cisa_json"] = now()
        end
    end

    # Try GitHub mirror
    if !is_open(CB, "github")
        try
            resp = HTTP.get(GITHUB_MIRROR; timeout=15)
            data = JSON3.read(resp.body)
            CB.failures["github"] = 0
            entries = [KEVEntry(d) for d in data.vulnerabilities]
            meta = Dict("source" => "github_mirror", "fetched_at" => string(now()))
            return (entries, meta)
        catch e
            CB.failures["github"] = get(CB.failures, "github", 0) + 1
            CB.last_failure["github"] = now()
        end
    end

    error("All KEV sources unavailable")
end

function get_kev_catalog(; force_refresh=false)
    fetch_catalog()
end

function get_kev_cve_ids(; force_refresh=false)::Set{String}
    entries, _ = get_kev_catalog(force_refresh=force_refresh)
    Set(e.cve_id for e in entries)
end

function get_new_entries(entries::Vector{KEVEntry}, db_path::String)
    # SQLite diff tracking
    isfile(db_path) || return entries
    db = SQLite.DB(db_path)
    result = DBInterface.execute(db, "SELECT value FROM kev_state WHERE key='last_seen_cve'")
    row = first(result, nothing)
    last_seen = isnothing(row) ? nothing : row.value

    isnothing(last_seen) && return entries

    sorted_entries = sort(entries, by=e -> e.date_added)
    new = filter(e -> e.cve_id > last_seen, sorted_entries)
    if !isempty(new)
        last = new[end].cve_id
        SQLite.execute(db, "INSERT OR REPLACE INTO kev_state (key,value) VALUES (?,?)",
                      ["last_seen_cve", last])
    end
    return new
end

end # module
