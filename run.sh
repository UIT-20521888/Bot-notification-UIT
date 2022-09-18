

#!/usr/bin/env bash

. env/bin/activate

# echo "send messenger"
python3 src/send_messenger.py

# echo 'get common news'
python3 src/detect_new_post_cs.py

# echo 'get cs news'
python3 src/detect_new_post_daa.py
# echo 'get hb new'
python3 src/detect_new_post_hbforum.py

# echo 'get special news'
python3 src/detect_new_post_ctsv.py
