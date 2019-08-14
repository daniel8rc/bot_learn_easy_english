#!/bin/bash

locale-gen "es_ES.UTF-8"
cd /opt/bot_telegram/learn_bot/ && python3 manage.py makemigrations && python3 manage.py migrate

# Read file conf
conf_file="/opt/bot_telegram/learn_bot/learn_bot/config/settings.py"
{
    while IFS= read -r line; do
    line=${line%%#*}
    case $line in
        *=*)
        var=${line%%=*}
        case $var in
            *[!A-Z_a-z]*)
            echo "Warning: invalid variable name $var ignored" >&2
            continue;;
        esac
        if eval '[ -n "${'$var'+1}" ]'; then
            echo "Warning: variable $var already set, redefinition ignored" >&2
            continue
        fi
        line=${line#*=}
        eval $var='"$line"'
    esac
    done <"$conf_file"

} || { # catch
    echo "Error read config file."
}

echo "Read config ok!"

cat <<EOF | python3 manage.py shell
from django.contrib.auth import get_user_model

User = get_user_model()  # get the currently active user model,

User.objects.filter(username=$root_username).exists() or \
    User.objects.create_superuser($root_username, $root_email, $root_password)
EOF
exit 0
