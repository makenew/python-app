#!/usr/bin/env bash

set -e
set -u

pkg_name=$(grep '^name = ".*"$' pyproject.toml | head -n 1 | cut -f2 -d'"')
pkg_version=$(grep '^version = ".*"$' pyproject.toml | head -n 1 | cut -f2 -d'"')

if [[ "$(git log -1 --pretty='%s')" == "${pkg_version}" ]]; then
  deploy_target="${pkg_name}:${pkg_version}"
  echo "TODO: deploy $deploy_target"
fi
