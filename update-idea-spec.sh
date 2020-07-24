#!/bin/sh

echo "Checking intellij-idea-community"

version="$(cat intellij-idea-community.spec | grep Version: | awk '{print $2}')"
build="$(cat intellij-idea-community.spec | grep '%global build_vers' | awk '{print $3}')"
PKG="$version ($build)"

echo "Package version: $PKG"

LATEST="$(
	curl -s 'https://data.services.jetbrains.com/products/releases?code=IIC&latest=true&type=release'
	)"

version="$(printf "%s" "${LATEST}" | jq -r '.IIC[0].version')"
build="$(printf "%s" "${LATEST}" | jq -r '.IIC[0].build')"
LATEST="$version ($build)"

echo "Latest version:  $LATEST"

if [ "$LATEST" != "$PKG" ]; then
	printf '%-32s %s -> %s\n' 'intellij-idea-community' "$PKG" "$LATEST" >> update.log
fi

if [ "$LATEST" != "$PKG" ]; then
	DATE="$(date "+%a %b %d %Y")"
	USER="Lars Kiesow <lkiesow@uos.de>"
	sed -i "s/^Version: .*/Version:       ${version}/" intellij-idea-community.spec
	sed -i "s/^%global *build_vers .*/%global build_vers ${build}/" intellij-idea-community.spec
	sed -i "s/^%changelog/%changelog\n\* ${DATE} ${USER} - ${version}\n- Update to ${LATEST}\n/" intellij-idea-community.spec

	git commit intellij-idea-community.spec -m "Update to ${version}"
fi
