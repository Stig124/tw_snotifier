#!/bin/sh

#TW-S(napshot)notifier
#    Copyright (C) 2021  Nicolas <stig124> FORMICHELLA

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; only using version 2 of the License

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

script_name1="./main.py"
script_path1="$(dirname "$(readlink -f "$0")")"
script_path_with_name="$script_path1/$script_name1"

cd "$script_path1" || exit

pipenv run $script_name1