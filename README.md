# Licence Verify AI

Licence Verify AI is an AI-assisted verification system for evaluating Ontario driver's licence documents and verifying the identity and liveness of the person presenting a licence.

The project combines document analysis, PDF417 barcode extraction, cross-source consistency checks, document validation, facial comparison, and active liveness detection into a single verification pipeline.

> **Important**
>
> A successful local verification does not mean that the Ontario Ministry of Transportation (MTO) has confirmed that a driver's licence is valid. Official licence status is maintained as a separate verification step.

---

## Overview

Licence Verify AI is designed to answer several different verification questions:

1. Can information be extracted from the licence?
2. Does information extracted from the front agree with information encoded on the back?
3. Are important document fields structurally and chronologically valid?
4. Is a live person present during identity verification?
5. Does the live face match the reference face?
6. Did all available local verification checks pass?
7. Has the licence status been independently confirmed through an official source?

Keeping these questions separate prevents one successful check from being treated as proof of another.

For example, an unexpired document is not necessarily an officially valid licence, and passing liveness detection does not establish identity without a successful face comparison.

---

## Repository data and privacy

This public repository contains the source code and documentation for Licence Verify AI, but it does **not** include the driver's licence images, facial-reference images, webcam captures, document crops, or other images used during development and testing.

These images are intentionally excluded from the repository because they may contain personal, identity, or biometric information.

The project's `.gitignore` is configured to prevent development images and the contents of the local `data/` directory from being committed to the repository.

As a result, examples in this README describe the verification process and its outputs without publishing the original test images.

Anyone running the project must provide their own appropriately authorized test data locally.

## Verification pipeline

The current system is organized as a multi-stage pipeline.

```text
Driver's licence
       │
       ├──────── Front ────────┐
       │                       │
       │                 ID Analyzer
       │                       │
       │                       ▼
       │                Structured fields
       │                       │
       └──────── Back ─────────┤
                               │
                         PDF417 barcode
                               │
                               ▼
                     Structured barcode data
                               │
                               ▼
                 Cross-source consistency
                               │
                               ▼
                     Document validation
                               │
                               ▼
                  Identity verification
                    ├─ Active liveness
                    └─ Face comparison
                               │
                               ▼
                    Local assessment
                               │
                               ▼
                  Official-status boundary
                               │
                               ▼
                       Final result
```

### Stage 1 — Document input

The system receives images of the front and back of a driver's licence.

The input images are used by different components of the pipeline rather than relying on a single extraction method.

### Stage 2 — Document detection and preprocessing

Document-processing utilities prepare licence images for downstream analysis.

The project includes components for:

- document detection
- cropping
- image preprocessing
- region-of-interest extraction
- OCR
- portrait extraction

These components support later field extraction and verification operations.

### Stage 3 — Front-side field extraction

The front of the licence is processed using ID Analyzer as the primary structured field-extraction provider.

Important normalized fields include:

- licence number
- date of birth
- issue date
- expiry date
- document type
- document name
- country
- province
- vehicle class

Provider-specific responses are normalized before they are passed to later verification stages.

### Stage 4 — Back-side PDF417 extraction

The PDF417 barcode on the back of the licence provides an independent source of document information.

Barcode data is parsed into normalized fields that can be compared with information obtained from the front of the document.

This creates two independent extraction paths:

```text
Front image → ID Analyzer ─────┐
                              ├─ comparison
Back image  → PDF417 parser ───┘
```

### Stage 5 — Cross-source consistency

Fields independently obtained from the front and back of the licence are compared.

The system currently compares information such as:

- licence number
- expiry date
- issue date
- date of birth

A field can be classified differently depending on whether it matches, conflicts with another source, or cannot be read reliably.

The overall consistency result can include:

- `CONSISTENT`
- `INCONSISTENT`
- `PARTIAL`

An unreadable field is not automatically treated as a confirmed mismatch.

### Stage 6 — Document validation

Extracted document data is evaluated using local validation rules.

Current checks include:

- required fields
- Ontario licence-number format
- expiry status
- issue-date chronology
- date-of-birth validation
- jurisdiction checks

For example, the validator can determine whether an extracted expiry date has passed or whether an issue date occurs after an expiry date.

These checks validate information available to the application. They do not query MTO records.

### Stage 7 — Identity and active liveness verification

Identity verification contains two separate checks:

```text
                 Identity verification
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       Active liveness         Face comparison
              │                     │
       head movement           reference face
       challenges                    +
              │                 live face
              └──────────┬──────────┘
                         ▼
                  Identity result
```

#### Active liveness

MediaPipe Face Landmarker is used to analyze facial landmarks and head pose from the webcam.

The system first calibrates a neutral head position. It then presents movement challenges such as:

- look left
- look right
- look up
- look down

Challenge sequences can vary so that the person being verified must respond to live instructions rather than simply provide a static image.

After the challenge succeeds, the system asks the person to return to a centered position before capturing the image used for facial comparison.

This prevents the final liveness movement from unnecessarily reducing face-comparison quality.

#### Face comparison

The face-verification pipeline uses MTCNN and FaceNet through `facenet-pytorch`.

A face is extracted from:

1. a reference image, and
2. the live webcam capture.

FaceNet converts the faces into numerical embeddings. The embeddings are compared to produce a similarity score.

The current development threshold is:

```text
0.60
```

The threshold is part of the current development configuration and should be evaluated with representative validation data before production use.

#### Development mode

The current project supports a `DEVELOPMENT` identity-verification mode.

During development, the person whose licence was used for document testing was not available for the live identity test. A separate development reference image was therefore used so the developer could test the liveness and facial-comparison pipeline with their own face.

This means a development result such as:

```text
Liveness: PASSED
Face match: MATCH
Mode: DEVELOPMENT
```

demonstrates that the identity-verification pipeline is functioning. It does **not** establish that the developer is the person represented by the driver's licence.

A production workflow must use the appropriate licence-holder reference for identity comparison.

### Stage 8 — Local verification assessment

Results from the local verification components are combined into a local assessment.

The assessment currently considers:

- cross-source consistency
- document validation
- identity verification

Possible local outcomes include:

- `PASS`
- `PARTIAL`
- `FAIL`
- `UNKNOWN`

For example:

```text
cross_source_consistency: PASS
document_validation: PASS
identity_verification: PASS

Local status: PASS
```

A local `PASS` means that the configured local verification checks passed.

It does **not** mean that MTO has confirmed the licence's official status.

### Stage 9 — Official licence-status boundary

Ontario provides an official Driver's Licence Check service for checking Ontario driver's licence status.

The current application does **not** have an authorized programmatic MTO integration configured.

Stage 9 therefore creates an explicit boundary between local verification and official licence-status information.

The current development result is:

```text
Source: MTO
Status: NOT_CHECKED
Checked: False
Official: False
```

The application deliberately does not infer an official status from OCR, barcode data, expiration checks, facial comparison, or any other local result.

An authorized official-status provider can be connected to this boundary in the future without redesigning the rest of the verification pipeline.

### Stage 10 — Final result

The final-result layer combines the local assessment with the official-status result while preserving the distinction between them.

For the current development configuration, a successful pipeline can produce:

```text
Local verification: PASS
Official licence status: NOT_CHECKED
Overall: LOCAL_PASS_OFFICIAL_NOT_CHECKED
```

The system reserves:

```text
VERIFIED
```

for a workflow in which the required local checks pass and an integrated official-status provider returns an appropriate valid result.

---

## Current end-to-end result

A successful development run has produced:

```text
CROSS-SOURCE CONSISTENCY
Status: CONSISTENT

DOCUMENT VALIDATION
Status: VALID

IDENTITY VERIFICATION
Status: VERIFIED
Liveness: PASSED
Face match: MATCH
Mode: DEVELOPMENT

LOCAL VERIFICATION ASSESSMENT
cross_source_consistency: PASS
document_validation: PASS
identity_verification: PASS

FINAL LOCAL STATUS: PASS

OFFICIAL MTO STATUS
Status: NOT_CHECKED
Checked: False
Official: False

FINAL RESULT
Local verification: PASS
Official licence status: NOT_CHECKED
Overall: LOCAL_PASS_OFFICIAL_NOT_CHECKED
```

Similarity scores are intentionally not presented as fixed project performance because individual development runs are not sufficient to establish biometric accuracy.

---

## Project structure

```text
licence-verify-ai/
├── app/
│   ├── document/
│   │   ├── ocr/
│   │   └── templates/
│   ├── face/
│   ├── liveness/
│   ├── providers/
│   ├── verification/
│   └── main.py
│
├── data/                        # Local only; not published       
│   ├── debug/
│   ├── input/
│   ├── output/
│   └── test/
│
├── models/
│   └── face_landmarker.task
│
├── scripts/
│   └── test_*.py
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```
> **Privacy note:** The `data/` directory shown above represents the local development structure. Its contents are excluded from the public repository. Development and test images are not published because they may contain personal or biometric information.

### `app/document`

Contains document-processing functionality, including barcode extraction, barcode parsing, cropping, OCR, normalization, field extraction, portrait extraction, preprocessing, templates, and validation helpers.

### `app/face`

Contains webcam capture, face detection, and face-matching functionality.

### `app/liveness`

Contains active-liveness components, including head-pose detection and challenge handling.

### `app/providers`

Contains integrations with external document-analysis providers.

### `app/verification`

Contains the higher-level verification logic used to combine document, identity, local-assessment, official-status, and final-result operations.

### `scripts`

Contains development and integration tests for individual components and the complete local pipeline.

---

## Technologies

The project uses technologies including:

- Python
- OpenCV
- MediaPipe Tasks
- MediaPipe Face Landmarker
- PyTorch
- Torchvision
- `facenet-pytorch`
- MTCNN
- FaceNet
- PDF417 processing
- OCR utilities
- ID Analyzer

Important versions from the current working development environment include:

```text
facenet-pytorch==2.6.0
mediapipe==1.0.1
numpy==1.26.4
opencv-contrib-python==4.10.0.84
torch==2.2.0+cpu
torchvision==0.17.0+cpu
```

The project currently uses NumPy 1.26.4 because the tested PyTorch/FaceNet environment is based on NumPy 1.x compatibility.

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd licence-verify-ai
```

### 2. Create a virtual environment

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file for credentials required by external providers.

Do not commit `.env` or provider credentials to source control.

### 5. Install the Face Landmarker model

The liveness pipeline expects the MediaPipe Face Landmarker model at:

```text
models/face_landmarker.task
```

The model must be available before running head-pose or active-liveness verification.

---

## Running the verification tests

### Document field extraction

```powershell
python -m scripts.test_field_extractor
```

### Cross-source consistency

```powershell
python -m scripts.test_cross_source_consistency
```

### Document validation

```powershell
python -m scripts.test_document_validation
```

### Face verification

```powershell
python -m scripts.test_identity_verification
```

### Head-pose detection

```powershell
python -m scripts.test_head_pose
```

### Active liveness

```powershell
python -m scripts.test_liveness
```

### Identity pipeline

```powershell
python -m scripts.test_identity_pipeline
```

### Local assessment

```powershell
python -m scripts.test_local_assessment
```

### Official-status boundary

```powershell
python -m scripts.test_licence_status
```

### Final-result logic

```powershell
python -m scripts.test_final_result
```

### Full local verification pipeline

```powershell
python -m scripts.test_full_local_pipeline
```

This is the primary end-to-end development test.

It combines identity verification with document consistency, document validation, local assessment, the official-status boundary, and the final result.

---

## Understanding the results

Several terms in the project intentionally have different meanings.

| Result | Meaning |
|---|---|
| `CONSISTENT` | Compared front-side and back-side fields did not contain a confirmed mismatch. |
| `VALID` (document validation) | Configured local document-validation rules passed. |
| `PASSED` (liveness) | The active-liveness challenge was completed successfully. |
| `MATCH` | Face similarity met the configured comparison threshold. |
| `VERIFIED` (identity) | Required liveness and facial-comparison checks passed. |
| `PASS` (local assessment) | Required local verification checks passed. |
| `NOT_CHECKED` | Official licence status was not queried. |
| `LOCAL_PASS_OFFICIAL_NOT_CHECKED` | Local checks passed, but no official MTO status was obtained. |

These labels should not be treated as interchangeable.

---

## Privacy and security

Licence Verify AI processes information that can be sensitive, including driver's licence data and facial images. Privacy is therefore treated as part of the project's design rather than only as a deployment consideration.

### Images are not published

The images used to develop and test this project are **not included in the public GitHub repository**.

This includes:

- driver's licence front images
- driver's licence back images
- facial-reference images
- webcam captures
- cropped licence images
- extracted portrait images
- debug images
- other generated images that may contain personal information

These files remain local and are excluded from version control for privacy reasons.

The absence of these images from the repository is intentional. They are not required to understand the system architecture or review the source code.

### Development data

Anyone testing the project should use data they are authorized to process. Test images should be stored locally and should not be committed to a public repository.

The repository should not contain:

- real driver's licence images
- facial or biometric test images
- extracted personal information
- API credentials
- `.env` files containing secrets
- generated debug artifacts containing personal information

### Data handling

Development and deployment environments should:

- collect only information needed for the verification task
- restrict access to licence and facial data
- avoid unnecessary storage of webcam captures
- minimize retention of document and biometric information
- avoid logging unnecessary personal information
- protect credentials outside source control
- use appropriate encryption for stored or transmitted sensitive information
- remove temporary data when it is no longer needed

Generated crops, debug images, and intermediate outputs should receive the same privacy protections as the original document because they may still contain identifiable information.
---

## Limitations

The current project is a development prototype.

Known limitations include:

- no authorized programmatic MTO integration is currently configured
- development-mode identity testing can use a development reference identity rather than the licence holder
- biometric thresholds have not yet been established through a production-scale validation study
- active liveness based on head-pose challenges is not equivalent to a fully evaluated commercial presentation-attack-detection system
- OCR and barcode extraction can be affected by image quality, glare, cropping, document damage, and camera conditions
- a locally consistent document can still have an official status that cannot be determined without an authoritative source
- the current system is focused on the Ontario driver's licence workflow

The system should therefore be treated as an AI-assisted verification prototype rather than an authoritative government licence-status service.

---

## Design principles

The project follows several principles:

**Independent evidence sources.**  
Front-side extraction and PDF417 barcode extraction are compared instead of relying on one source.

**Uncertainty is preserved.**  
Unreadable or unavailable information is distinguished from a confirmed failure.

**Liveness and identity are separate.**  
A person can pass a liveness challenge without necessarily matching the reference identity.

**Local and official verification are separate.**  
Local document checks never manufacture an official MTO result.

**Development and production modes are distinguishable.**  
Development substitutions are explicitly labelled so that test results are not presented as production identity verification.

---

## Future work

Planned improvements include:

- authorized official-status integration if an appropriate programmatic mechanism becomes available
- production identity-reference handling
- broader biometric threshold evaluation
- stronger presentation-attack detection
- automated test coverage
- structured application logging with privacy safeguards
- API integration
- user interface development
- deployment configuration
- improved error handling and recovery
- additional document-quality checks

---

## Responsible use

Licence Verify AI should support verification workflows rather than replace authoritative records or appropriate human review.

Results should be presented with enough context for a user to understand:

- which checks were performed
- which checks passed or failed
- which information was unavailable
- whether identity verification was performed in development or production mode
- whether official licence status was actually checked

The system should not infer characteristics about a person that are unrelated to the verification task.

---

## Status

**Current development milestone:** Complete local verification pipeline through Stage 10.

```text
Document extraction          ✓
PDF417 extraction            ✓
Cross-source consistency     ✓
Document validation          ✓
Active liveness              ✓
Face comparison              ✓
Identity assessment          ✓
Local verification           ✓
Official-status boundary     ✓
Final-result aggregation     ✓
Authorized MTO integration   Not configured
```

The next development phase is application integration and user-facing API/UI development.