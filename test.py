from daytona import Daytona, CreateSandboxParams
import time
import argparse
import os


def main():
    parser = argparse.ArgumentParser(description='Daytona Sandbox Management Script')
    parser.add_argument('--image', help='Docker image to use for sandbox')
    parser.add_argument('--time', action='store_true', help='Enable timing of operations')
    parser.add_argument('--destroy', action='store_true', help='Destroy sandbox after execution')
    parser.add_argument('--fs', action='store_true', help='Run file-system tests')
    parser.add_argument('-n', type=int, default=1, help='Number of sandboxes to create')
    
    args = parser.parse_args()

    daytona = Daytona()
    creation_times = []
    destroy_times = []

    for _ in range(args.n):

        # sandbox = daytona.get_current_sandbox("749ed747-2d84-4461-a92c-00c0cde3e902")

        # Prepare sandbox creation parameters if image is specified
        params = None
        if args.image:
            params = CreateSandboxParams(image=args.image)

        # Time operations if requested
        if args.time:
            total_start_time = time.time()
            
            # Time sandbox creation
            start_time = time.time()

            sandbox = daytona.create(params) if params else daytona.create()
            sandbox.process.code_run("print('Hello, World!')")

            end_time = time.time()
            creation_time = end_time - start_time
            creation_times.append(creation_time)
            print(f"[{sandbox.id}]: {creation_time:.2f} seconds")

            # Time sandbox destruction if requested
            if args.destroy:
                start_time = time.time()
                daytona.remove(sandbox)
                end_time = time.time()
                destroy_time = end_time - start_time
                destroy_times.append(destroy_time)
                print(f"[DESTROY: {sandbox.id}]: {destroy_time:.2f} seconds")
        else:
            # Execute without timing
            sandbox = daytona.create(params) if params else daytona.create()
            sandbox.process.code_run("print('Hello, World!')")
            
            # Destroy sandbox if requested
            if args.destroy:
                daytona.remove(sandbox)
                print("Sandbox destroyed")

        if args.fs:
            # Get sandbox root directory
            root_dir = sandbox.get_user_root_dir()

            print(root_dir)

            # List files in the sandbox
            files = sandbox.fs.list_files(root_dir)
            print("Files:", files)

            # Create a new directory in the sandbox
            new_dir = os.path.join(root_dir, "new-dir")
            sandbox.fs.create_folder(new_dir, "755")

            file_path = os.path.join(new_dir, "data.txt")

            # Add a new file to the sandbox
            file_content = b"Hello, World!"
            sandbox.fs.upload_file(file_content, file_path)

            # Search for the file we just added
            matches = sandbox.fs.find_files(root_dir, "World!")
            print("Matches:", matches)

            # Replace the contents of the file
            sandbox.fs.replace_in_files([file_path], "Hello, World!", "Goodbye, World!")

            # Read the file
            downloaded_file = sandbox.fs.download_file(file_path)
            print("File content:", downloaded_file.decode("utf-8"))

            # Change the file permissions
            sandbox.fs.set_file_permissions(file_path, mode="777")

            # Get file info
            file_info = sandbox.fs.get_file_info(file_path)
            print("File info:", file_info)  # Should show the new permissions

            # Move the file to the new location
            new_file_path = os.path.join(root_dir, "moved-data.txt")
            sandbox.fs.move_files(file_path, new_file_path)

            # Find the file in the new location
            search_results = sandbox.fs.search_files(root_dir, "moved-data.txt")
            print("Search results:", search_results)

            # Delete the file
            sandbox.fs.delete_file(new_file_path)

            # Execute an os command in the sandbox
            new_dir = os.path.join(root_dir, "new-dir")
            sandbox.fs.create_folder(new_dir, "755")
            response = sandbox.process.exec('pwd', cwd=new_dir, timeout=10)
            if response.exit_code != 0:
                print(f"Error: {response.exit_code} {response.result}")
            else:
                print(response.result)

            response = sandbox.process.exec(f'ls -la', cwd=new_dir, timeout=10)
            if response.exit_code != 0:
                print(f"Error: {response.exit_code} {response.result}")
            else:
                print(response.result)

    # Print average times if timing is enabled and multiple sandboxes were created
    if args.time and args.n > 1:
        avg_creation_time = sum(creation_times) / len(creation_times)
        print(f"\nAverage creation time for {args.n} sandboxes: {avg_creation_time:.2f} seconds")
        
        if args.destroy:
            avg_destroy_time = sum(destroy_times) / len(destroy_times)
            print(f"Average destruction time for {args.n} sandboxes: {avg_destroy_time:.2f} seconds")


if __name__ == "__main__":
    main()