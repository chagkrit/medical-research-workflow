# Data Preparation And Cleaning

## Intake Checklist

- Confirm study design, analytic cohort, time window, inclusion/exclusion criteria, data source, extraction date, and unit of analysis.
- Preserve raw files as immutable inputs. Create derived datasets through scripts or documented transformations.
- Obtain codebook/data dictionary. If absent, infer cautiously and label inferred metadata.
- Identify protected health information and apply the minimum necessary principle.
- Record software versions, package versions, random seeds, and file hashes when feasible.

## Provenance Table

Track each source:

- Dataset name and owner.
- Extraction date and query/version.
- Population covered.
- Key variables.
- Identifier/linkage fields.
- Known limitations.
- Transformations applied.

## Cleaning Rules

Create explicit rules for:

- Duplicate patients, encounters, samples, or observations.
- Date order conflicts: birth, enrollment, diagnosis, index, exposure, outcome, death, follow-up.
- Range checks with clinical plausibility, units, and assay-specific limits.
- Coding systems: ICD, CPT, SNOMED, LOINC, RxNorm, ATC, MedDRA, or local codes.
- Outcome adjudication and phenotype definitions.
- Outliers: distinguish data errors from clinically meaningful extremes.

## Audit Output

For each cleaning decision, report:

- Rule name.
- Rationale.
- Variables affected.
- Number and percentage of records affected.
- Whether records were corrected, recoded, excluded, winsorized, flagged, or left unchanged.
- Sensitivity analysis needed.

## Reviewer Questions

- Could cleaning decisions change the exposure-outcome association?
- Were exclusions made before seeing outcomes?
- Are units, reference ranges, and coding systems consistent across sites/time?
- Are derived variables reproducible from raw data?
- Is there a participant flow diagram with counts at each step?
