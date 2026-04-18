#!/usr/bin/env python3
import os
from pathlib import Path
from dotenv import load_dotenv

# Shared env (global across projects file)
load_dotenv(dotenv_path=Path.home() / ".config" / ".env", override=False)
# Project specific env file
load_dotenv(dotenv_path=Path(__file__).resolve().parents[0] / ".env", override=True)

import aws_cdk as cdk
from config.setup_stack import setup_stack
from tdpBucketManagerCDK.stack_handler import tdpBucketManagerCDK

env = os.getenv("ENVIRONMENT")

app = cdk.App()
setup_stack(env, app, "PROJECT_NAME", tdpBucketManagerCDK)

app.synth()
