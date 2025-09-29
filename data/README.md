# Green Drive ETL Data

This folder contains datasets used for the **Green Drive ETL** project, which focuses on vehicle fuel efficiency, alternative fuel usage, and emissions data.  

**Data Sources:**  
- Vehicle Data (CSV, zipped): [Download link](https://www.fueleconomy.gov/feg/epadata/vehicles.csv.zip)  
- Emissions Data (CSV, zipped): [Download link](https://www.fueleconomy.gov/feg/epadata/emissions.csv.zip)  
- Source: [fueleconomy.gov - EPA Data Downloads](https://www.fueleconomy.gov/feg/download.shtml)  
- Data updated: **26 August 2025**

---

## **Vehicle Dataset Columns**

| Column | Description |
|--------|-------------|
| `atvtype` | Type of alternative fuel or advanced technology vehicle |
| `barrels08` | Annual petroleum consumption in barrels for fuelType1 |
| `barrelsA08` | Annual petroleum consumption in barrels for fuelType2 |
| `charge120` | EV charge time (hours) at 120V |
| `charge240` | EV charge time (hours) at 240V |
| `city08` | City MPG for fuelType1 |
| `city08U` | Unrounded city MPG for fuelType1 |
| `cityA08` | City MPG for fuelType2 |
| `cityA08U` | Unrounded city MPG for fuelType2 |
| `cityCD` | City gasoline consumption (gallons/100 miles) in charge-depleting mode |
| `cityE` | City electricity consumption in kWh/100 miles |
| `cityMpk` | City miles per kilogram for hydrogen |
| `cityUmpk` | Unrounded city miles per kilogram for hydrogen |
| `cityUF` | EPA city utility factor (share of electricity) for PHEV |
| `co2` | Tailpipe CO2 in grams/mile for fuelType1 |
| `co2A` | Tailpipe CO2 in grams/mile for fuelType2 |
| `co2TailpipeAGpm` | Tailpipe CO2 in grams/mile for fuelType2 |
| `co2TailpipeGpm` | Tailpipe CO2 in grams/mile for fuelType1 |
| `comb08` | Combined MPG for fuelType1 |
| `comb08U` | Unrounded combined MPG for fuelType1 |
| `combA08` | Combined MPG for fuelType2 |
| `combA08U` | Unrounded combined MPG for fuelType2 |
| `combE` | Combined electricity consumption in kWh/100 miles |
| `combMpk` | Combined miles per kilogram for hydrogen |
| `combUmpk` | Unrounded combined miles per kilogram for hydrogen |
| `combinedCD` | Combined gasoline consumption (gallons/100 miles) in charge-depleting mode |
| `combinedUF` | EPA combined utility factor (share of electricity) for PHEV |
| `cylinders` | Engine cylinders |
| `displ` | Engine displacement (liters) |
| `drive` | Drive axle type |
| `engId` | EPA model type index |
| `eng_dscr` | Engine descriptor |
| `evMotor` | Electric motor power (kW) |
| `feScore` | EPA Fuel Economy Score (-1 = Not available) |
| `fuelCost08` | Annual fuel cost for fuelType1 ($) |
| `fuelCostA08` | Annual fuel cost for fuelType2 ($) |
| `fuelType` | Fuel type (general) |
| `fuelType1` | Primary fuel type |
| `fuelType2` | Secondary fuel type (for dual-fuel vehicles) |
| `ghgScore` | EPA GHG score (-1 = Not available) |
| `ghgScoreA` | EPA GHG score for alternative fuel |
| `guzzler` | Subject to gas guzzler tax (G or T) |
| `highway08` | Highway MPG for fuelType1 |
| `highway08U` | Unrounded highway MPG for fuelType1 |
| `highwayA08` | Highway MPG for fuelType2 |
| `highwayA08U` | Unrounded highway MPG for fuelType2 |
| `highwayCD` | Highway gasoline consumption (gallons/100 miles) in charge-depleting mode |
| `highwayE` | Highway electricity consumption in kWh/100 miles |
| `highwayMpk` | Highway miles per kilogram for hydrogen |
| `highwayUmpk` | Unrounded highway miles per kilogram for hydrogen |
| `highwayUF` | EPA highway utility factor for PHEV |
| `hlv` | Hatchback luggage volume (cubic feet) |
| `hpv` | Hatchback passenger volume (cubic feet) |
| `id` | Vehicle record ID |
| `lv2` | 2-door luggage volume (cubic feet) |
| `lv4` | 4-door luggage volume (cubic feet) |
| `make` | Manufacturer |
| `mfrCode` | Manufacturer 3-character code |
| `model` | Vehicle model name |
| `mpgData` | Has My MPG data |
| `phevBlended` | True if vehicle operates on blended gasoline/electric mode |
| `pv2` | 2-door passenger volume (cubic feet) |
| `pv4` | 4-door passenger volume (cubic feet) |
| `rangeA` | EPA range for fuelType2 |
| `rangeCityA` | EPA city range for fuelType2 |
| `rangeHwyA` | EPA highway range for fuelType2 |
| `trany` | Transmission type |
| `trans_dscr` | Transmission description |
| `UCity` | Unadjusted city MPG for fuelType1 |
| `UCityA` | Unadjusted city MPG for fuelType2 |
| `UHighway` | Unadjusted highway MPG for fuelType1 |
| `UHighwayA` | Unadjusted highway MPG for fuelType2 |
| `VClass` | EPA vehicle size class |
| `year` | Model year |
| `youSaveSpend` | 5-year savings compared to average car ($) |
| `sCharger` | Supercharged (S) |
| `tCharger` | Turbocharged (T) |
| `c240Dscr` | EV charger description |
| `charge240b` | EV alternate charger time (hours) |
| `c240bDscr` | EV alternate charger description |
| `createdOn` | Vehicle record creation date |
| `modifiedOn` | Vehicle record modification date |
| `startStop` | Stop-start technology (Y/N) |
| `phevCity` | PHEV composite city MPGe |
| `phevHwy` | PHEV composite highway MPGe |
| `phevComb` | PHEV composite combined MPGe |
| `basemodel` | Base model name |

---

## **Emissions Dataset Columns**

| Column | Description |
|--------|-------------|
| `efid` | Engine family ID |
| `id` | Vehicle record ID (links to vehicle table) |
| `salesArea` | EPA sales area code |
| `score` | EPA smog rating for fuelType1 (1–10) |
| `scoreAlt` | EPA smog rating for fuelType2 (1–10) |
| `smartwayScore` | SmartWay efficiency score |
| `standard` | Vehicle emission standard code |
| `stdText` | Vehicle emission standard description |

---

**Notes:**  
- All data are from **26 August 2025**.  
- These datasets are publicly available and can be used for ETL, analytics, or demonstration projects.  
- Vehicle and emissions tables can be joined using the `id` column.
