# Sources and provenance

- Original research: Antonio, N., de Almeida, A., & Nunes, L. (2019). *Hotel booking demand datasets*. Data in Brief 22, 41–49. https://doi.org/10.1016/j.dib.2018.11.126
- Open full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC6297060/ — methods and Table 1 establish the extraction reference time and field meaning. Accessed 2026-09-29. Paper is CC BY 4.0; retain authors and source attribution.
- Source mirror and transformation: https://github.com/rfordatascience/tidytuesday/tree/main/data/2020/2020-02-11 — combines H1 and H2 and adds hotel name. Its dictionary was downloaded unchanged to `source_dictionary.md`.
- CSV: https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2020/2020-02-11/hotels.csv — raw bytes and SHA256 in data/raw. download_data.py refuses a different checksum. Schema/count/date validation against paper completed; a publisher-ZIP row-by-row comparison was not performed.
- Course source: [IS507 syllabus](IS507-syllabus.md), supplied from Downloads by the student and reviewed 2026-09-30; unchanged copy preserved. The syllabus supports whole-project understanding and allows AI assistance with verification. Exact assignment deadline/format remain unavailable.

The article describes source values near arrival, not original reservation-entry snapshots. Lead-time arithmetic is a project assumption for the split, not proof that every row preserves an original immutable creation timestamp. Retrospective labels also encode no-show outcomes; the development label/status cross-tab confirms this.

No hotel/customer names are present. Public anonymization still prevents proving independence; source redistribution does not create new provenance guarantees.
