import apache_beam as beam
import pandas as pd
from dataclasses import dataclass

from pangeo_forge_recipes.config import RecipeConfig
from pangeo_forge_recipes.patterns import ConcatDim, FilePattern
from pangeo_forge_recipes.transforms import OpenURLWithFSSpec, OpenWithXarray, StoreToZarr


recipe_config = RecipeConfig()

dates = [
    d.to_pydatetime().strftime('%Y%m%d')
    for d in pd.date_range("1996-10-01", "1999-02-01", freq="D")
]

def make_url(time):
    url_base = "https://storage.googleapis.com/pforge-test-data"
    return f"{url_base}/gpcp/v01r03_daily_d{time}.nc"


concat_dim = ConcatDim("time", dates, nitems_per_file=1)
pattern = FilePattern(make_url, concat_dim)


@dataclass
class MyCustomTransform(beam.PTransform):
     target_root: None
     cache: None

     def expand(self, pcoll: beam.PCollection):
         import logging
         logger = logging.getLogger("pangeo_forge_runner")
         logger.error(f"[ CONFIG TARGET ]: {self.target_root}")
         logger.error(f"[ CONFIG CACHE ]: {self.cache}")
         return pcoll
   

recipe = (
    beam.Create(pattern.items())
    | OpenURLWithFSSpec()
    | OpenWithXarray(file_type=pattern.file_type, xarray_open_kwargs={"decode_coords": "all"})
    | MyCustomTransform(target_root=recipe_config.target_root, cache=recipe_config.cache)
    | StoreToZarr(
        store_name="gpcp",
        combine_dims=pattern.combine_dim_keys,
    )
)
