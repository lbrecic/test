from daytona import CreateSandboxParams, Daytona, Image

daytona = Daytona()

# Define the dynamic image
dynamic_image = (
    Image.debian_slim("3.13")
    .pip_install(["pytest", "pytest-cov", "mypy", "ruff", "black", "gunicorn"])
    .run_commands(["apt-get update && apt-get install -y git curl", "mkdir -p /home/daytona/project"])
    .workdir("/home/daytona/project")
    .env({"ENV_VAR": "Test 2"})
)
# Create a new Sandbox with the dynamic image and stream the build logs
sandbox = daytona.create(
    CreateSandboxParams(
        image=dynamic_image,
    ),
    timeout=0,
    on_image_build_logs=lambda log_line: print(log_line, end=''),
)
