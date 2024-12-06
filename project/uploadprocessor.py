from abc import ABC, abstractmethod
import pandas as pd
import logging
from django.contrib import messages
from django.db import models, IntegrityError
from django.core.exceptions import ValidationError
import os
from pathlib import Path
from project import models

logger = logging.getLogger("uploadcsv")


class UploadProcessor(ABC):
    class Meta:
        abstract = True

    def __init__(self, filepath) -> None:
        if Path.is_file(filepath):
            self.filepath = filepath
        else:
            raise FileNotFoundError(f"File {filepath} not found")
        self.header = None

    def _find_duplicate(self, df: pd.DataFrame) -> pd.DataFrame:
        df[self.unique] = df[self.unique].str.lower()
        duplicates = df[df.duplicated(subset=[self.unique], keep=False) == True]
        if duplicates.empty:
            return pd.DataFrame
        else:
            return duplicates

    def _check_header(self, file_header) -> bool:
        fh_list = file_header.split(",")
        exp_list = self.header.split(",")

        delta = len(fh_list) - len(exp_list)
        if self.header + "\n" == file_header:
            return True
        if delta == 0:
            no_matching = []
            for i, fh_item in enumerate(fh_list):
                if fh_item != exp_list[i]:
                    no_matching.append(f"{fh_item} <=> {exp_list[i]}")
            if len(no_matching) > 0:
                print(no_matching)
                return False
            else:
                print("File header seem OK")
        if delta < 0:
            print(f"File header missing {-delta} item(s)")
            return False
        elif delta > 0:
            print(f"File header has {delta} items in surplus")
            return False

    def header_good(self) -> bool:
        with open(self.filepath, "r") as f:
            header = f.readline()
        if not self._check_header(header):
            raise ValidationError(
                f"\n*** Column header not matching***\nFile Header:\n{header}\nExpected header:\n{self.header}"
            )
        return True

    def dataframe(self):
        return pd.read_csv(self.filepath, delimiter=",").fillna("")

    def as_dict(self, df: pd.DataFrame) -> dict:
        return df.to_dict("records")

    @abstractmethod
    def main(self):
        pass


class SeedLibraryProcessor(UploadProcessor):
    def __init__(self, filepath) -> None:
        UploadProcessor.__init__(self, filepath)
        self.header = "latin_name,english_name,french_name,url,light_from,light_to,bloom_start,bloom_end,soil_humidity_min,soil_humidity_max,min_height,max_height,size,stratification_detail,stratification_duration,sowing_depth,sowing_period,sharing_priority,harvesting_start,harvesting_end,harvesting_indicator,harvesting_mean,seed_head,remove_non_seed_material,viability_test,seed_storage,one_cultivar,packaging_measure,dormancy,seed_preparation,hyperlink,envelope_label_link,harvesting_video_link,seed_picture_link,pods_seed_head_picture_link,seed_storage_label_info,notes,germinate_easy,rock_garden,rain_garden,pond_edge,shoreline_rehab,container_suitable,ground_cover,garden_edge,woodland_garden,wind_break_hedge,erosion_control"
        self.unique = "latin_name"

    def set_item(self, item):
        item["english_name"] = item["english_name"].strip()
        if item["bloom_start"] == "":
            item["bloom_start"] = 0
        if item["bloom_end"] == "":
            item["bloom_end"] = 0

        if item["min_height"] == "":
            item["min_height"] = 0

        if item["max_height"] == "":
            item["max_height"] = 0

        if item["harvesting_start"] == "":
            item["harvesting_start"] = 0

        if item["harvesting_end"] == "":
            item["harvesting_end"] = 0

        if item["stratification_duration"] == "":
            item["stratification_duration"] = 0

        yes_no = {"yes": True, "no": False, "": False}
        item["remove_non_seed_material"] = yes_no.get(item["remove_non_seed_material"].lower())

        # sharing priority
        try:
            item["sharing_priority"] = models.SharingPriority.objects.get(
                sharing_priority=item["sharing_priority"]
            )
        except models.SharingPriority.DoesNotExist:
            print(f"No record found for {item['sharing_priority']} in SharingPriority")
            exit(0)

        # Harvesting indicator
        try:
            item["harvesting_indicator"] = models.HarvestingIndicator.objects.get(
                harvesting_indicator=item["harvesting_indicator"]
            )
        except models.HarvestingIndicator.DoesNotExist:
            print(
                f"No record found for <<{item['harvesting_indicator']}>> in Harvesting Indicator for <<{item['latin_name']}>>"
            )
            exit(0)

        # Seed Head
        try:
            item["seed_head"] = models.SeedHead.objects.get(seed_head=item["seed_head"])
        except models.SeedHead.DoesNotExist:
            print(f"No record found for <<{item['seed_head']}>> in Seed Head for <<{item['latin_name']}>>")
            exit(0)

        # Harvesting Mean
        try:
            item["harvesting_mean"] = models.HarvestingMean.objects.get(
                harvesting_mean=item["harvesting_mean"]
            )
        except models.HarvestingMean.DoesNotExist:
            print(
                f"No record found for <<{item['harvesting_mean']}>> in Harvesting Mean for <<{item['latin_name']}>>"
            )
            exit(0)

        # Viablity Test
        try:
            item["viability_test"] = models.ViablityTest.objects.get(viability_test=item["viability_test"])
        except models.ViablityTest.DoesNotExist:
            print(
                f"No record found for <<{item['viability_test']}>> in Viability Test for <<{item['latin_name']}>>"
            )
            exit(0)

        # Seed Storage
        try:
            item["seed_storage"] = models.SeedStorage.objects.get(seed_storage=item["seed_storage"])
        except models.SeedStorage.DoesNotExist:
            print(
                f"No record found for <<{item['seed_storage']}>> in Seed Storage for <<{item['latin_name']}>>"
            )
            exit(0)

        # Packaging Measure
        try:
            item["packaging_measure"] = models.PackagingMeasure.objects.get(
                packaging_measure=item["packaging_measure"]
            )
        except models.PackagingMeasure.DoesNotExist:
            print(
                f"No record found for <<{item['packaging_measure']}>> in PAckaging Measure for <<{item['latin_name']}>>"
            )
            exit(0)

        # One cultivar
        try:
            item["one_cultivar"] = models.OneCultivar.objects.get(one_cultivar=item["one_cultivar"])
        except models.OneCultivar.DoesNotExist:
            print(
                f"No record found for <<{item['one_cultivar']}>> in One Cultivar for <<{item['latin_name']}>>"
            )
            exit(0)

        # Dormancy
        try:
            item["dormancy"] = models.Dormancy.objects.get(dormancy=item["dormancy"])
        except models.Dormancy.DoesNotExist:
            print(f"No record found for <<{item['dormancy']}>> in Dormancy for <<{item['latin_name']}>>")
            exit(0)

        # Seed Preparation
        try:
            item["seed_preparation"] = models.SeedPreparation.objects.get(
                seed_preparation=item["seed_preparation"]
            )
        except models.SeedPreparation.DoesNotExist:
            print(
                f"No record found for <<{item['seed_preparation']}>> in Seed Preparation for <<{item['latin_name']}>>"
            )
            exit(0)

        # seed_storage_label_infoseed_storage_label_info
        try:
            item["seed_storage_label_info"] = models.SeedStorageLabelInfo.objects.get(
                seed_storage_label_info=item["seed_storage_label_info"]
            )
        except models.SeedStorageLabelInfo.DoesNotExist:
            print(
                f"No record found for <<{item['seed_storage_label_info']}>> in Seed Storage Label Info for <<{item['latin_name']}>>"
            )
            exit(0)

        # Light From
        try:
            item["light_from"] = models.Lighting.objects.get(lighting=item["light_from"])
        except models.Lighting.DoesNotExist:
            print(
                f"No record found for <<{item['light_from']}>> in Light condition Info for <<{item['latin_name']}>>"
            )
            exit(0)

        # Light To
        try:
            item["light_to"] = models.Lighting.objects.get(lighting=item["light_to"])
        except models.Lighting.DoesNotExist:
            print(
                f"No record found for <<{item['light_to']}>> in Light condition Info for <<{item['latin_name']}>>"
            )
            exit(0)

        # Humidity min
        try:
            item["soil_humidity_min"] = models.SoilHumidity.objects.get(
                soil_humidity=item["soil_humidity_min"]
            )
        except models.SoilHumidity.DoesNotExist:
            print(
                f"No record found for <<{item['soil_humidity_min']}>> in Soil Humidity Infofor <<{item['latin_name']}>>"
            )
            exit(0)

        # Humidity max
        try:
            item["soil_humidity_max"] = models.SoilHumidity.objects.get(
                soil_humidity=item["soil_humidity_max"]
            )
        except models.SoilHumidity.DoesNotExist:
            print(
                f"No record found for <<{item['soil_humidity_max']}>> in Light condition Info for <<{item['latin_name']}>>"
            )
            exit(0)

        return item

    def main(self, request=None):
        if not self.header_good():
            msg = f"{__class__.__name__} Invalid columns header"
            logger.error(msg)
            if request:
                messages.error(request, msg)
                return
        df = self.dataframe()
        duplicates = self._find_duplicate(df)
        if not duplicates.empty and request:
            messages.error(request, f"Duplicates have been detected: {duplicates.to_html()}")
            return

        _dict_list = self.as_dict(df)
        counter = 0
        for item in _dict_list:
            item = self.set_item(item)
            data_model = models.SeedLibrary(**item)
            try:
                data_model.save()
                counter += 1
                logger.info(f"Uploaded System Info {data_model}.")
            except IntegrityError as err:
                msg = f"Saving {__class__.__name__} {item} generates {err}."
                logger.warning(msg)
                if request:
                    messages.error(request, msg)
        if counter:
            msg = f"{counter} {__class__.__name__} have been uploaded."
            if request:
                messages.info(request, msg)
            else:
                print(msg)
