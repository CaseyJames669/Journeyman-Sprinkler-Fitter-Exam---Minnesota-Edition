import json
import re

titles = [
    "Copyright", "Minnesota Department of Public Safety State Fire Marshal Division", "Important Disclaimer", 
    "Selected Minnesota Fire Prevention Statutes", "Effective Dates of Minnesota Building and Fire Codes", 
    "Occupancy Classifications Mn State Fire Code – 2020", "Preface", "Effective Use of the International Fire Code", 
    "Part I — Administrative", "Chapter 1 Scope and Administration", "Chapter 2 Definitions", 
    "Part II — General Safety Provisions", "Chapter 3 General Requirements", "Chapter 4 Emergency Planning and Preparedness", 
    "Part III — Building and Equipment Design Features", "Chapter 5 Fire Service Features", 
    "Chapter 6 Building Services and Systems", "Chapter 7 Fire and Smoke Protection Features", 
    "Chapter 8 Interior Finish, Decorative Materials and Furnishings", "Chapter 9 Fire Protection and Life Safety Systems", 
    "Chapter 10 Means of Egress", "ICC 300 Standard for Bleachers, Folding and Telescopic Seating, and Grandstands", 
    "Chapter 11 Construction Requirements for Existing Buildings", "Chapter 12 Energy Systems", 
    "Chapters 13 Through 19 Reserved", "Part IV — Special Occupancies and Operations", 
    "Chapter 20 Aviation Facilities", "Chapter 21 Dry Cleaning", "Chapter 22 Combustible Dust-Producing Operations", 
    "Chapter 23 Motor Fuel-Dispensing Facilities and Repair Garages", "Chapter 24 Flammable Finishes", 
    "Chapter 25 Fruit and Crop Ripening", "Chapter 26 Fumigation and Insecticidal Fogging", 
    "Chapter 27 Semiconductor Fabrication Facilities", 
    "Chapter 28 Lumber Yards and Agro-Industrial, Solid Biomass and Woodworking Facilities", 
    "Chapter 29 Manufacture of Organic Coatings", "Chapter 30 Industrial Ovens", 
    "Chapter 31 Tents, Temporary Special Event Structures and Other Membrane Structures", 
    "Chapter 32 High-Piled Combustible Storage", "Chapter 33 Fire Safety During Construction and Demolition", 
    "Chapter 34 Tire Rebuilding and Tire Storage", "Chapter 35 Welding and Other Hot Work", "Chapter 36 Marinas", 
    "Chapter 37 Combustible Fibers", "Chapter 38 Higher Education Laboratories", 
    "Chapter 39 Processing and Extraction Facilities", "Chapters 40 Through 49 Reserved", 
    "Part V — Hazardous Materials", "Chapter 50 Hazardous Materials—General Provisions", "Chapter 51 Aerosols", 
    "Chapter 52 Reserved", "Chapter 53 Compressed Gases", "Chapter 54 Corrosive Materials", 
    "Chapter 55 Cryogenic Fluids", "Chapter 56 Explosives and Fireworks", "Chapter 57 Flammable and Combustible Liquids", 
    "Chapter 58 Flammable Gases and Flammable Cryogenic Fluids", "Chapter 59 Flammable Solids", 
    "Chapter 60 Highly Toxic and Toxic Materials", "Chapter 61 Liquefied Petroleum Gases", "Chapter 62 Organic Peroxides", 
    "Chapter 63 Oxidizers, Oxidizing Gases and Oxidizing Cryogenic Fluids", "Chapter 64 Pyrophoric Materials", 
    "Chapter 65 Pyroxylin (Cellulose Nitrate) Plastics", "Chapter 66 Unstable (Reactive) Materials", 
    "Chapter 67 Water-Reactive Solids and Liquids", "Chapters 68 Through 79 Reserved", 
    "Part VI—Referenced Standards", "Chapter 80 Referenced Standards", 
    "Chapter 81 Adult Day Services Centers, Residential Hospice Facilities and Supervised Living Facilities", 
    "Chapter 84 Symbols for Vehicles Fueled by Cng, Lpg, and Lng", "Part VII—Appendices", 
    "Appendix A Board of Appeals", "Appendix B Fire-Flow Requirements for Buildings", 
    "Appendix C Fire Hydrant Locations and Distribution", "Appendix D Fire Apparatus Access Roads", 
    "Appendix E Hazard Categories", "Appendix F Hazard Ranking", 
    "Appendix G Cryogenic Fluids—Weight and Volume Equivalents", 
    "Appendix H Hazardous Materials Management Plan (Hmmp)And Hazardous Materials Inventory Statement (Hmis)Instructions", 
    "Appendix I Fire Protection Systems—Noncompliant Conditions", "Appendix J Building Information Sign", 
    "Appendix K Construction Requirements Forexisting Ambulatory Care Facilities", 
    "Appendix L Requirements for Fire Fighterair Replenishment Systems", 
    "Appendix M High-Rise Buildings—Retroactiveautomatic Sprinkler Requirement", 
    "Appendix N Indoor Trade Shows and Exhibitions", "Appendix O Fires or Barbecues on Balconies or Patios", 
    "Appendix P Emergency Responder Radio Coverage", "Index"
]

base_url = "https://codes.iccsafe.org/content/MNFC2020P1/"

chapters = []
for title in titles:
    # Basic slugification
    slug = title.lower()
    slug = slug.replace("—", "-") # Replace em dash
    slug = slug.replace("–", "-") # Replace en dash
    slug = slug.replace("(", "")
    slug = slug.replace(")", "")
    slug = slug.replace(",", "")
    slug = slug.replace(".", "")
    slug = slug.replace(" ", "-")
    slug = re.sub(r'-+', '-', slug) # Remove duplicate hyphens
    
    url = base_url + slug
    chapters.append({"title": title, "url": url, "slug": slug})

with open("scraper/chapters.json", "w") as f:
    json.dump(chapters, f, indent=2)

print(f"Generated {len(chapters)} chapters in scraper/chapters.json")
