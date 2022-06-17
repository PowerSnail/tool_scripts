#!/usr/bin/fish

function download_until_success
    while not zypper dup -y -l --no-recommends --download-only
        echo "Try again in 10 seconds..."
        sleep 10 & wait $last_pid
    end
end

download_until_success

echo "Successfully downloaded updates" | mail -s "Successfully downloaded updates" henry