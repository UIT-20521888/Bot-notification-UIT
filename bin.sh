

#!/usr/bin/env bash

. ../../Bot-notification-UIT/bin/activate

python3 src/send_messebger.py

# echo 'get common news'
python3 src/detect_new_post_cs.py

# echo 'get cs news'
python3 src/detect_new_post_daa.py

# echo 'get special news'
python3 src/detect_new_pots_ctsv.py