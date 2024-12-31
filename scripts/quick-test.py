"""
Just a file to experiment with code as needed
"""

import os
import sys
from pathlib import Path

import django

PWD = os.getenv("PWD")
BASE_DIR = Path(PWD).resolve()
if BASE_DIR not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

# import pandas as pd

# PWD = os.getenv("PWD")

# latin_name,english_name,french_name,url,light_from,light_to,bloom_start,bloom_end,soil_humidity_min,soil_humidity_max,min_height,max_height,size,stratification_detail,stratification_duration,sowing_depth,sowing_period,sharing_priority,harvesting_start,harvesting_end,harvesting_indicator,harvesting_mean,seed_head,remove_non_seed_material,viability_test,seed_storage,one_cultivar,packaging_measure,dormancy,seed_preparation,hyperlink,envelope_label_link,harvesting_video_link,seed_picture_link,pods_seed_head_picture_link,seed_storage_label_info\
# n\nExpected header:\n

# latin_name,english_name,french_name,url,light_from,light_to,bloom_start,bloom_end,soil_humidity_min,soil_humidity_max,min_height,max_height,size,stratification_detail,stratification_duration,sowing_depth,sowing_period,sharing_priority,harvesting_start,harvesting_end,harvesting_indicator,harvesting_mean,seed_head,remove_non_seed_material,viability_test,seed_storage,one_cultivar,packaging_measure,dormancy,seed_preparation,hyperlink,envelope_label_link,harvesting_video_link,seed_picture_link,pods_seed_head_picture_link
