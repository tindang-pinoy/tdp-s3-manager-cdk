# tdp-s3-manager-cdk

AWS CDK project that provisions an S3 bucket for storing Terraform state files for Tindang Pinoy infrastructure.

## Deployed Resources

| Resource | Value |
|---|---|
| Terraform State Bucket Name | `tdp-terraform-states` |
| Terraform State Bucket ARN | `arn:aws:s3:::tdp-terraform-states` |

---

## Project Structure

```
tdp-s3-manager-cdk/
├── app.py                              # CDK entry point — loads env vars and synthesizes the app
├── cdk.json                            # CDK configuration and feature flags
├── requirements.txt                    # CDK-specific dependencies
├── setup.py                            # Creates .venv, installs dependencies, and creates .env
├── .env                                # Project-specific environment variables (not committed)
├── .env.template                       # Template for required environment variables
├── config/
│   ├── env_config.py                   # Defines StackEnvConfig and stack_config registry
│   ├── setup_stack.py                  # Resolves and instantiates the correct stack + environment
│   └── validators.py                   # Validates required env vars are set before stack init
└── tdpBucketManagerCDK/
    ├── __init__.py
    └── stack_handler.py                # CDK stack — creates the versioned S3 bucket
```

---

## What It Deploys

A single CloudFormation stack (`tdp-bucket-manager`) containing:

- **S3 bucket** named `tdp-terraform-states` — versioned, used to store Terraform state files
- CloudFormation outputs for the bucket name and ARN

---

## How It Works

```
cdk synth / cdk deploy
        │
        ├── 1. app.py loads ~/.config/.env     (global env vars)
        ├── 2. app.py loads .env               (project-specific env vars)
        │
        └── setup_stack() resolves config
                  │
                  ├── 3. Looks up stack by PROJECT_NAME in stack_config
                  ├── 4. Resolves environment (e.g. prod) from ENVIRONMENT
                  ├── 5. Validates required env vars via validators.py
                  └── 6. Instantiates the CDK stack with a StackEnvConfig object
```

---

## Prerequisites

| Requirement | Purpose |
|---|---|
| Python 3.12+ | Runtime |
| [`uv`](https://github.com/astral-sh/uv) | Fast Python package and venv manager |
| AWS CDK CLI | `npm install -g aws-cdk` |
| AWS credentials | Configured via environment or `~/.aws` |

---

## Setup

### 1. Configure your global environment file

Create `~/.config/.env` with shared variables used across projects:

```bash
PROJECT_OWNER=your-name
AWS_TINDANG_PINOY_ACCOUNT_ID=123456789012
AWS_REGION=us-east-1
```

### 2. Configure the project environment file

Copy `.env.template` to `.env` and populate it:

```bash
cp .env.template .env
```

Required variables:

```bash
PROJECT_OWNER=                      # Owner tag applied to the stack
AWS_TINDANG_PINOY_ACCOUNT_ID=       # AWS account ID to deploy into
AWS_REGION=                         # Target AWS region
AWS_CDK_APPLICATION_ID=             # Tag value for the application ID
PROJECT_NAME=tdp-bucket-manager     # Must match a key in stack_config in env_config.py
ENVIRONMENT=prod                    # Environment to deploy
```

### 3. Install the virtual environment

```bash
python3 setup.py
```

This uses `uv` to create `.venv` and installs all dependencies from `requirements.txt` plus defaults (`requests`, `python-dotenv`, `watchdog`).

### 4. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 5. Synthesize the stack

```bash
cdk synth
```

---

## Environment Variable Reference

### `~/.config/.env` — Global (shared across projects)

| Variable | Description |
|---|---|
| `PROJECT_OWNER` | Owner tag applied to deployed resources |
| `AWS_TINDANG_PINOY_ACCOUNT_ID` | AWS account ID for Tindang Pinoy |
| `AWS_REGION` | Target AWS region |

### `.env` — Project-specific

| Variable | Description |
|---|---|
| `PROJECT_OWNER` | Overrides global if set |
| `AWS_TINDANG_PINOY_ACCOUNT_ID` | Overrides global if set |
| `AWS_REGION` | Overrides global if set |
| `AWS_CDK_APPLICATION_ID` | Application ID tag applied to the stack |
| `PROJECT_NAME` | Must be `tdp-bucket-manager` |
| `ENVIRONMENT` | Must be `prod` |

> Project `.env` values take precedence over `~/.config/.env` values.

---

## Module Reference

### `config/env_config.py`
Defines `StackEnvConfig` (holds all resolved config for a single environment) and `stackConfig` (groups environments per project). The module-level `stack_config` dict is the registry that `setup_stack` uses to look up stacks by `PROJECT_NAME`.

### `config/setup_stack.py`
Resolves the correct `StackEnvConfig` for the current `PROJECT_NAME` and `ENVIRONMENT`, then instantiates the CDK stack class with it.

### `config/validators.py`
`validate_env_vars(*names)` — checks that all named environment variables are set and non-empty. Collects all failures and raises a single `ValueError` listing every missing variable.

### `tdpBucketManagerCDK/stack_handler.py`
The CDK stack class. Creates the `tdp-terraform-states` S3 bucket with versioning enabled. Receives a `StackEnvConfig` instance as `config` — use `config.region`, `config.aws_account`, `config.application_id_tag`, etc. directly inside the stack.

---

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `Environment variables are missing or empty` | One or more required vars not set in `.env` | Populate all required variables in `.env` |
| `Stack name X not found in stack_config` | `PROJECT_NAME` doesn't match a key in `env_config.py` | Ensure `PROJECT_NAME=tdp-bucket-manager` |
| `Environment X not found in the config file` | `ENVIRONMENT` value has no matching attribute on `stackConfig` | Ensure `ENVIRONMENT=prod` |
| `ModuleNotFoundError: No module named 'dotenv'` | Running CDK outside the activated venv | Run `source .venv/bin/activate` first |
