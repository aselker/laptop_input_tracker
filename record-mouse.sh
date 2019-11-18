#!/usr/bin/env bash

adddate() {
	while IFS= read -r line; do
		printf '%s %s\n' "$(date +%s%N)" "$line";
	done
}

xinput test $1 | adddate
