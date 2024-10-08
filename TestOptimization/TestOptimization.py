import os
import shutil
import nuke

def clear_temp_files():
    # Get the path to the %tmp% directory
    temp_dir = os.environ['TMP']  # This will resolve to the path of the temp directory

    # List to keep track of files that couldn't be deleted
    skipped_files = []

    # Check if the temp directory exists
    if os.path.exists(temp_dir):
        # Confirm with the user before proceeding
        if nuke.ask("Are you sure you want to clear all temporary files?"):
            try:
                # Remove all files and subdirectories in the temp directory
                for filename in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, filename)
                    try:
                        if os.path.isdir(file_path):
                            shutil.rmtree(file_path)  # Remove the directory and its contents
                        else:
                            os.remove(file_path)  # Remove the file
                    except PermissionError:
                        # Collect files that couldn't be deleted due to being in use
                        skipped_files.append(file_path)
                    except Exception as e:
                        # Collect files that had other exceptions
                        skipped_files.append(f"{file_path}: {str(e)}")
                
                # Final message
                if skipped_files:
                    # Display a single message with all skipped files
                    skipped_files_str = "\n".join(skipped_files)
                    nuke.message(f"Temporary files cleared, but the following files couldn't be deleted:\n{skipped_files_str}")
                else:
                    nuke.message("Temporary files cleared successfully from the Temp directory.")
            except Exception as e:
                nuke.message(f"Error during cleanup: {str(e)}")
        else:
            nuke.message("Operation canceled.")
    else:
        nuke.message("Temporary directory does not exist.")